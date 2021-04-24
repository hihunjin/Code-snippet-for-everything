import math
import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parallel.data_parallel import DataParallel
from torch.nn.parallel.parallel_apply import parallel_apply
from torch.nn.parallel.scatter_gather import scatter

up_kwargs = {'mode': 'bilinear', 'align_corners': True}


def evaluate(model, x, target=None):
    pred = model(x)
    if isinstance(pred, (tuple, list)):
        pred = pred[0]
    if target is None:
        return pred
    correct, labeled = batch_pix_accuracy(pred.data, target.data)
    inter, union = batch_intersection_union(pred.data, target.data, self.nclass)

class MultiEvalModule(DataParallel):
    """Multi-size Segmentation Eavluator"""
    def __init__(self, args, module, nclass, device_ids=None, flip=True,
                 scales=[0.5, 0.75, 1.0, 1.25, 1.5, 1.75]):
        super(MultiEvalModule, self).__init__(module, device_ids)
        self.args = args
        self.nclass = nclass
        self.base_size = args.base_size
        self.crop_size = args.crop_size
        self.scales = scales
        self.flip = flip
        print('MultiEvalModule: base_size {}, crop_size {}'. \
            format(self.base_size, self.crop_size))

    def parallel_forward(self, inputs, **kwargs):
        """Multi-GPU Mult-size Evaluation

        Args:
            inputs: list of Tensors
        """
        inputs = [(input.unsqueeze(0).cuda(device),)
                  for input, device in zip(inputs, self.device_ids)]
        replicas = self.replicate(self, self.device_ids[:len(inputs)])
        kwargs = scatter(kwargs, target_gpus, dim) if kwargs else []
        if len(inputs) < len(kwargs):
            inputs.extend([() for _ in range(len(kwargs) - len(inputs))])
        elif len(kwargs) < len(inputs):
            kwargs.extend([{} for _ in range(len(inputs) - len(kwargs))])
        outputs = self.parallel_apply(replicas, inputs, kwargs)
        #for out in outputs:
        #    print('out.size()', out.size())
        return outputs

    def forward(self, image):
        """Mult-size Evaluation"""
        # only single image is supported for evaluation
        batch, _, h, w = image.size()
        assert(batch == 1)
        stride_rate = 2.0/3.0
        crop_size = self.crop_size
        stride = int(crop_size * stride_rate)
        with torch.cuda.device_of(image):
            scores = image.new().resize_(batch,self.nclass,h,w).zero_().cuda()

        for scale in self.scales:
            long_size = int(math.ceil(self.base_size * scale))
            if h > w:
                height = long_size
                width = int(1.0 * w * long_size / h + 0.5)
                short_size = width
            else:
                width = long_size
                height = int(1.0 * h * long_size / w + 0.5)
                short_size = height
            """
            short_size = int(math.ceil(self.base_size * scale))
            if h > w:
                width = short_size
                height = int(1.0 * h * short_size / w)
                long_size = height
            else:
                height = short_size
                width = int(1.0 * w * short_size / h)
                long_size = width
            """
            # resize image to current size
            up_kwargs = {'mode': 'bilinear', 'align_corners': True}
            cur_img = resize_image(image, height, width, **up_kwargs)
            if long_size <= crop_size:
                pad_img = pad_image(cur_img, self.args.mean,
                                    self.args.std, crop_size)
                outputs = module_inference(self.module, pad_img, self.flip)
                outputs = crop_image(outputs, 0, height, 0, width)
            else:
                if short_size < crop_size:
                    # pad if needed
                    pad_img = pad_image(cur_img, self.args.mean,
                                        self.args.std, crop_size)
                else:
                    pad_img = cur_img
                _,_,ph,pw = pad_img.size()
                assert(ph >= height and pw >= width)
                # grid forward and normalize
                h_grids = int(math.ceil(1.0 * (ph-crop_size)/stride)) + 1
                w_grids = int(math.ceil(1.0 * (pw-crop_size)/stride)) + 1
                with torch.cuda.device_of(image):
                    outputs = image.new().resize_(batch,self.nclass,ph,pw).zero_().cuda()
                    count_norm = image.new().resize_(batch,1,ph,pw).zero_().cuda()
                # grid evaluation
                for idh in range(h_grids):
                    for idw in range(w_grids):
                        h0 = idh * stride
                        w0 = idw * stride
                        h1 = min(h0 + crop_size, ph)
                        w1 = min(w0 + crop_size, pw)
                        crop_img = crop_image(pad_img, h0, h1, w0, w1)
                        # pad if needed
                        pad_crop_img = pad_image(crop_img, self.args.mean,
                                                 self.args.std, crop_size)
                        output = module_inference(self.module, pad_crop_img, self.flip)
                        outputs[:,:,h0:h1,w0:w1] += crop_image(output,
                            0, h1-h0, 0, w1-w0)
                        count_norm[:,:,h0:h1,w0:w1] += 1
                assert((count_norm==0).sum()==0)
                outputs = outputs / count_norm
                outputs = outputs[:,:,:height,:width]

            score = resize_image(outputs, h, w, **up_kwargs)
            scores += score

        return scores


def module_inference(module, image, flip=True):
    output = evaluate(module, image)
    if flip:
        fimg = flip_image(image)
        foutput = evaluate(module, fimg)
        output += flip_image(foutput)
    return output.exp()

def resize_image(img, h, w, **up_kwargs):
    return F.interpolate(img, (h, w), **up_kwargs)

def pad_image(img, mean, std, crop_size):
    b,c,h,w = img.size()
    assert(c==3)
    padh = crop_size - h if h < crop_size else 0
    padw = crop_size - w if w < crop_size else 0
    pad_values = -np.array(mean) / np.array(std)
    img_pad = img.new().resize_(b,c,h+padh,w+padw)
    for i in range(c):
        # note that pytorch pad params is in reversed orders
        img_pad[:,i,:,:] = F.pad(img[:,i,:,:], (0, padw, 0, padh), value=pad_values[i])
    assert(img_pad.size(2)>=crop_size and img_pad.size(3)>=crop_size)
    return img_pad

def crop_image(img, h0, h1, w0, w1):
    return img[:,:,h0:h1,w0:w1]

def flip_image(img):
    assert(img.dim()==4)
    with torch.cuda.device_of(img):
        idx = torch.arange(img.size(3)-1, -1, -1).type_as(img).long()
    return img.index_select(3, idx)

######### prepare small model and args  #########

class small(nn.Module):
    def __init__(self, args=None):
        super(small, self).__init__()
        self.args=args
        if args.aux:
            c=1
        else:
            c=3
        self.encoder = nn.Conv2d(in_channels=3, out_channels=c, kernel_size=1)
        self.bn = nn.BatchNorm2d(c)
        self.decoder = nn.Conv2d(in_channels=3, out_channels=args.nclass, kernel_size=1)
    def forward(self, x):
        if args.aux:
            return tuple([self.decoder(x),self.bn (self.encoder(x))])
        else:
            return tuple([self.decoder(self.bn(self.encoder(x)))])

class args:
    nclass=1
    not_bin=False
    aux=False
    base_size=512
    crop_size=480
    scales = [0.75, 1.0, 1.25, 1.5]
    mean = [.485, .456, .406]
    std = [.229, .224, .225]
  
######### prepare multi scale evaluation models a.k.a evaluator #########

model = small(args)
evaluator = MultiEvalModule(args, model, args.nclass, scales=args.scales).cuda()
evaluator.eval()

######### inference #########

image = torch.rand(1,3,512,512)
pred = evaluator.parallel_forward(image)            # type : list
print(pred[0])
