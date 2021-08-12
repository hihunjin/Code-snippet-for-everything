import torch

### generate a tensor
t = torch.Tensor([1.3, 5, 7.])
t.type(), t
# ('torch.FloatTensor', tensor([1.3000, 5.0000, 7.0000]))

### change
t = t.type(torch.uint8)



t.type(), t
# ('torch.ByteTensor', tensor([1, 5, 7], dtype=torch.uint8))
