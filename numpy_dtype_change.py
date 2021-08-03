import numpy as np

x = np.random.rand(3,10,10)

###### type check
print(x.dtype)
# dtype('float64')

###### change type
x = x.astype('uint8')
print(x.dtype)
# dtype('uint8')
