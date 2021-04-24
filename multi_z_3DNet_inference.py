import math
import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parallel.data_parallel import DataParallel
from torch.nn.parallel.parallel_apply import parallel_apply
from torch.nn.parallel.scatter_gather import scatter

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
    def __init__(self, args, module, nclass, device_ids=None, flip=True):
        super(MultiEvalModule, self).__init__(module, device_ids)
        self.args = args
        self.nclass = nclass
        self.z_len = args.z_len
        self.flip = flip
        print('MultiEvalModule: z_len {}'. \
            format(self.z_len))

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
        batch, _, z, h, w = image.size()
        assert(batch == 1)
        stride_rate = 2.0/3.0
        stride = int(self.z_len * stride_rate)
        with torch.cuda.device_of(image):
            scores = image.new().resize_(batch,self.nclass,z,h,w).zero_().cuda()

        if z <= self.z_len:
            pad_img = pad_z(image, self.args.mean,
                      self.args.std, self.z_len)

            outputs = module_inference(self.module, pad_img, self.flip)
            outputs = crop_image(outputs, 0, z)
        else:
            # grid forward and normalize
            z_grids=[]
            for i in range(z//self.z_len+1):
                z_grids.append(i*stride)
                if i == z//self.z_len:
                  z_grids.append(z-self.z_len)
            with torch.cuda.device_of(image):
                outputs = image.new().resize_(batch,self.nclass,z,h,w).zero_().cuda()
                count_norm = image.new().resize_(batch,1,z,h,w).zero_().cuda()
            # grid evaluation
            for z0 in z_grids:
                  z1 = z0 + self.z_len
                  crop_img = crop_image(image, z0,z1)
                  output = module_inference(self.module, crop_img, self.flip)
                  count_norm[:,:,z0:z1,:,:] += 1
            assert((count_norm==0).sum()==0)
            outputs = outputs / count_norm

        return outputs


def module_inference(module, image, flip=True):
    output = evaluate(module, image)
    if flip:
        fimg = flip_image(image)
        foutput = evaluate(module, fimg)
        output += flip_image(foutput)
    return output.exp()

def pad_z(img, mean, std, crop_size):
    b,c,z,h,w = img.size()
    assert(c==1)
    padz = crop_size - z if z < crop_size else 0
    pad_values = -np.array(mean) / np.array(std)
    img_pad = img.new().resize_(b,c,z+padz,h,w)
    for i in range(c):
        # note that pytorch pad params is in reversed orders
        img_pad[:,i,:,:,:] = F.pad(img[:,i,:,:,:], (0, 0, 0, 0, 0, padz), value=pad_values[i])
    assert(img_pad.size(2)>=crop_size)
    return img_pad

def crop_image(img,z0,z1):
    return img[:,:,z0:z1,:,:]

def flip_image(img):
    assert(img.dim()==5)
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
        self.encoder = nn.Conv3d(in_channels=args.in_channels, out_channels=c, kernel_size=1)
        self.bn = nn.BatchNorm3d(c)
        self.decoder = nn.Conv3d(in_channels=3, out_channels=args.nclass, kernel_size=1)
    def forward(self, x):
        if args.aux:
            return tuple([self.decoder(x),self.bn (self.encoder(x))])
        else:
            return tuple([self.decoder(self.bn(self.encoder(x)))])[0]

class args:
    not_bin=False
    aux=False
    z_len=40
    mean = [.485]*z_len
    std = [.229]*z_len
    nclass=2
    in_channels = 1

######### prepare multi z evaluation models a.k.a evaluator #########

model = small(args)
evaluator = MultiEvalModule(args, model, args.nclass, flip=False).cuda()
evaluator.eval()

######### inference #########

ex = torch.rand(1, args.in_channels,126,100,100).cuda()
out = evaluator.parallel_forward(ex)
# print(out)
print(out[0].size())
