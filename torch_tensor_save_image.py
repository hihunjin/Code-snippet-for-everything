import torch
from torchvision.utils import save_image

rand_tensor= torch.rand(64, 3,28,28) 

img0 = rand_tensor[0]
# img1 = img1.numpy() # TypeError: tensor or list of tensors expected, got <class 'numpy.ndarray'>
save_image(img0, 'img0.png')
