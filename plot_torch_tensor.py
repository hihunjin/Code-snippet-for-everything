from matplotlib import pyplot as plt
import torch

tensor_image = torch.rand(3,100,100)
plt.imshow(  tensor_image.permute(1, 2, 0)  )
