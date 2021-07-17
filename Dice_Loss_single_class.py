######################################## Single class
########################################

import torch
import torch.nn as nn

## dumy data
img = torch.rand(2,3,100,100)
tar = torch.randint(0,3,(2,100,100))


## single class
num_class = 2   # class number

img_new = img.softmax(1)
img_new = img_new[:,num_class]
tar_new = tar==num_class


## Define Dice Loss
class DiceLoss(nn.Module):
    def __init__(self, reduction='mean'):
        super(DiceLoss, self).__init__()
        self.reduction = reduction
    
    def forward(self, x, target):
        numerator   = 2*x*target+1
        denominator = x+target+1
        loss = 1-numerator/denominator
        if self.reduction == 'mean':
            return loss.mean()
        else:
            return loss.mean(dim = list(range(1, loss.ndim  )))


## Test
N = DiceLoss(reduction='none')(img_new, tar)
M = DiceLoss()(img_new, tar)
print(N,M)
