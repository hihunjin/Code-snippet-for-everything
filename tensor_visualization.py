import torch
from matplotlib.pyplot import imshow, show    

def tensor_vis4d(tensor):
    imshow(tensor.squeeze(0).permute(1,2,0).numpy())
    show()
def tensor_vis3d(tensor):
    imshow(tensor.permute(1,2,0).numpy())
    show()
def tensor_vis4d_channel(tensor, channel=0):
    imshow(tensor.squeeze(0)[channel].numpy())
    show()


for i in range(10,20):
    feat = torch.rand(1, 100, 256, 64)
    tensor_vis4d_channel(feat, i)
