from PIL import Image
import numpy as np

arr = np.random.uniform(size=(3,256,256))*255
arr = np.ascontiguousarray(arr.transpose(1,2,0))
img = Image.fromarray(arr, 'RGB')
img.save('out.png')
