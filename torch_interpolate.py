import torch
import torch.nn.functional as F

seg_array = torch.randint(0,5,size=(1,3,100,100)).type(torch.FloatTensor)
print(seg_array.min(),seg_array.max())
seg_array = F.interpolate(seg_array, (200,200), mode='nearest')
print(seg_array.min(),seg_array.max())
