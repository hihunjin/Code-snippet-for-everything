from PIL import Image
import numpy as np

# 3d
e = np.random.rand(150,150,3).astype('uint8')
out = Image.fromarray(e)                      #no error

# 1d
e = np.random.rand(150,150).astype('uint8')
out = Image.fromarray(e, mode='L')            #no error
