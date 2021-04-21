import threading
import numpy as np
import torch

__all__ = ['accuracy', 'get_pixacc_miou',
           'SegmentationMetric', 'batch_intersection_union', 'batch_pix_accuracy',
           'pixel_accuracy', 'intersection_and_union']

def accuracy(output, target, topk=(1,)):
    """Computes the accuracy over the k top predictions for the specified values of k"""
    with torch.no_grad():
        maxk = max(topk)
        batch_size = target.size(0)

        _, pred = output.topk(maxk, 1, True, True)
        pred = pred.t()
        correct = pred.eq(target.view(1, -1).expand_as(pred))

        res = []
        for k in topk:
            correct_k = correct[:k].view(-1).float().sum(0, keepdim=True)
            res.append(correct_k.mul_(100.0 / batch_size))
        return res

def get_pixacc_miou(args, total_correct, total_label, total_inter, total_union):
    pixAcc = 1.0 * total_correct / (np.spacing(1) + total_label)
    IoU = 1.0 * total_inter / (np.spacing(1) + total_union)
    if args.not_bin:
        return pixAcc, IoU.mean()   #mIoU
    else:
        return pixAcc, IoU
    

class SegmentationMetric(object):
    """Computes pixAcc and mIoU metric scroes
    """
    def __init__(self, args, nclass, criterion=None):
        self.args = args
        self.nclass = nclass
        self.criterion = criterion
        self.lock = threading.Lock()
        self.reset()

    def update(self, labels, preds):
        def evaluate_worker(self, label, pred):
            if self.criterion != None:
                loss = self.criterion(pred,label).cpu().numpy() * label.size(0)
            else:
                loss = 0
            num_images = label.size(0)
            correct, labeled = batch_pix_accuracy(
                pred, label)
            inter, union = batch_intersection_union(
                pred, label, self.nclass)
            with self.lock:
                self.total_correct += correct
                self.total_label += labeled
                self.total_inter += inter
                self.total_union += union
                self.total_loss += loss
                self.total_images += num_images
            return
        
        def evaluate_worker_bin(self, label, pred):
            if self.criterion != None:
                loss = self.criterion(pred.to(label.device),label).cpu().numpy() * label.size(0)
            else:
                loss = 0
            num_images = label.size(0)
            pred = pred.cpu().numpy()
            label = label.cpu().numpy()#.astype(dtype=bool)
            if pred.shape != label.shape:
                pred = pred.squeeze(axis=1)
            correct, labeled = batch_pix_accuracy_bin(pred, label, self.args.threshold)
            inter, union = batch_DSC(pred, label, self.args.threshold)
            with self.lock:
                self.total_correct += correct
                self.total_label += labeled
                self.total_inter += inter
                self.total_union += union
                self.total_loss += loss
                self.total_images += num_images
            return

        if isinstance(preds, torch.Tensor):
            if self.args.not_bin:
                evaluate_worker(self, labels, preds)
            else:
                evaluate_worker_bin(self, labels, preds)
        elif isinstance(preds, (list, tuple)):
            if self.args.not_bin:
                threads = [threading.Thread(target=evaluate_worker,
                                        args=(self, label, pred),
                                       )
                           for (label, pred) in zip(labels, preds)]
            else:
                threads = [threading.Thread(target=evaluate_worker_bin,
                                        args=(self, label, pred),
                                       )
                       for (label, pred) in zip(labels, preds)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
        else:
            raise NotImplemented

    def get_all(self):
        return self.total_correct, self.total_label, self.total_inter, self.total_union
    
    def get(self):
        return get_pixacc_miou(self.args, self.total_correct, self.total_label, self.total_inter, self.total_union)
    
    def get_loss(self):
        return self.total_loss / self.total_images
     
    def reset(self):
        self.total_inter = 0
        self.total_union = 0
        self.total_correct = 0
        self.total_label = 0
        self.total_loss = 0
        self.total_images = 0
        return

def batch_pix_accuracy(output, target):
    """Batch Pixel Accuracy
    Args:
        predict: input 4D tensor
        target: label 3D tensor
    """
    _, predict = torch.max(output, 1)

    predict = predict.cpu().numpy().astype('int64') + 1
    target = target.cpu().numpy().astype('int64') + 1

    pixel_labeled = np.sum(target > 0)
    pixel_correct = np.sum((predict == target)*(target > 0))
    assert pixel_correct <= pixel_labeled, \
        "Correct area should be smaller than Labeled"
    return pixel_correct, pixel_labeled


def batch_intersection_union(output, target, nclass):
    """Batch Intersection of Union
    Args:
        predict: input 4D tensor
        target: label 3D tensor
        nclass: number of categories (int)
    """
    _, predict = torch.max(output, 1)
    mini = 1
    maxi = nclass
    nbins = nclass
    predict = predict.cpu().numpy().astype('int64') + 1
    target = target.cpu().numpy().astype('int64') + 1

    predict = predict * (target > 0).astype(predict.dtype)
    intersection = predict * (predict == target)
    # areas of intersection and union
    area_inter, _ = np.histogram(intersection, bins=nbins, range=(mini, maxi))
    area_pred, _ = np.histogram(predict, bins=nbins, range=(mini, maxi))
    area_lab, _ = np.histogram(target, bins=nbins, range=(mini, maxi))
    area_union = area_pred + area_lab - area_inter
    assert (area_inter <= area_union).all(), \
        "Intersection area should be smaller than Union area"
    return area_inter, area_union


def batch_pix_accuracy_bin(output, target, threshold=0.5):
    """Batch Pixel Accuracy
    Args:
        predict: input 3D tensor
        target: label 3D tensor
    """
    output_bool = output > threshold
    pixel_correct = (output_bool * target).sum() + (np.logical_not(output_bool) * np.logical_not(target)).sum()
    shape = target.shape
    pixel_labeled = shape[-1] * shape[-2]
    if len(shape)!=2:
        pixel_labeled *= shape[-3]
    return pixel_correct, pixel_labeled

def batch_DSC(output, target, threshold=0.5):
    """ Dice score"""
    output_bool = output > threshold
    intersection = np.logical_and(output_bool, target).sum()
    union = output_bool.sum() + target.sum()

    return 2 * intersection, union


# ref https://github.com/CSAILVision/sceneparsing/blob/master/evaluationCode/utils_eval.py
def pixel_accuracy(im_pred, im_lab):
    im_pred = np.asarray(im_pred)
    im_lab = np.asarray(im_lab)

    # Remove classes from unlabeled pixels in gt image. 
    # We should not penalize detections in unlabeled portions of the image.
    pixel_labeled = np.sum(im_lab > 0)
    pixel_correct = np.sum((im_pred == im_lab) * (im_lab > 0))
    #pixel_accuracy = 1.0 * pixel_correct / pixel_labeled
    return pixel_correct, pixel_labeled


def intersection_and_union(im_pred, im_lab, num_class):
    im_pred = np.asarray(im_pred)
    im_lab = np.asarray(im_lab)
    # Remove classes from unlabeled pixels in gt image. 
    im_pred = im_pred * (im_lab > 0)
    # Compute area intersection:
    intersection = im_pred * (im_pred == im_lab)
    area_inter, _ = np.histogram(intersection, bins=num_class-1,
                                        range=(1, num_class - 1))
    # Compute area union: 
    area_pred, _ = np.histogram(im_pred, bins=num_class-1,
                                range=(1, num_class - 1))
    area_lab, _ = np.histogram(im_lab, bins=num_class-1,
                               range=(1, num_class - 1))
    area_union = area_pred + area_lab - area_inter
    return area_inter, area_union


def torch_dist_sum(gpu, *args):
    process_group = torch.distributed.group.WORLD
    tensor_args = []
    pending_res = []
    for arg in args:
        if isinstance(arg, torch.Tensor):
            tensor_arg = arg.clone().reshape(-1).detach().cuda(gpu)
        else:
            tensor_arg = torch.tensor(arg).reshape(-1).cuda(gpu)
        tensor_args.append(tensor_arg)
        pending_res.append(torch.distributed.all_reduce(tensor_arg, group=process_group, async_op=True))
    for res in pending_res:
        res.wait()
    return tensor_args

class args:
    nclass = 2
    not_bin = True

if __name__=='__main__':
    import torch
    import numpy as np
    metric = SegmentationMetric(args, nclass=args.nclass)
    
    pred = torch.rand((1,args.nclass,4,100,100))
    # y = np.random.randint(0,high=args.nclass,size=(1,4,100,100))
    y = torch.randint(0,high=args.nclass, size=(1,4,100,100))
    
    metric.reset()
    metric.update(y, pred)
    all_metircs = metric.get_all()
    # all_metircs = torch_dist_sum(args.gpu, *all_metircs)
    pixAcc, mIoU = get_pixacc_miou(args, *all_metircs)
    print(pixAcc, mIoU)
