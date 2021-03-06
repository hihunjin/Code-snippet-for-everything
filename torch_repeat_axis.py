'''
tensor([[1., 2., 3.],
        [4., 5., 6.],
        [7., 8., 9.]])
to
tensor([[[1., 2., 3.],
         [1., 2., 3.],
         [1., 2., 3.]],

        [[4., 5., 6.],
         [4., 5., 6.],
         [4., 5., 6.]],

        [[7., 8., 9.],
         [7., 8., 9.],
         [7., 8., 9.]]])
(3,3) to (3,3,3)
'''
import torch

a = torch.FloatTensor([[1,2,3],
                       [4,5,6],
                       [7,8,9]])
b = a.unsqueeze(1).repeat(1,3,1)
print(b)
