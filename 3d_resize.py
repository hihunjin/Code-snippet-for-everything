import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np

z_len=10
ex = np.random.rand(z_len,20,20)
seg = np.random.randint(0,2, (z_len,20,20))

###### ct and seg both ######

def resize(ct_array, seg_array, to_size):
    if ct_array.shape[-1]==to_size:
        return ct_array, seg_array
    with torch.no_grad():

        ct_array = torch.FloatTensor(ct_array).unsqueeze(dim=0).unsqueeze(dim=0)
        ct_array = nn.Upsample((z_len, to_size, to_size),mode='trilinear',align_corners=True)(ct_array).squeeze().detach().numpy()     #custom : //2
        # ct_array = F.interpolate(ct_array, (self.z_len, xy_dim//2, xy_dim//2), mode='trilinear',align_corners=True).squeeze().detach().numpy()

        seg_array = torch.FloatTensor(seg_array).unsqueeze(dim=0).unsqueeze(dim=0)
        seg_array = Variable(seg_array)
        seg_array = F.interpolate(seg_array, (z_len, to_size, to_size), mode='nearest').squeeze().detach().numpy()

    return ct_array, seg_array

ct,seg = resize(ex,seg,20)
print(ct.shape,seg.shape)
