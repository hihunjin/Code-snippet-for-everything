import numpy as np
import scipy.ndimage as ndimage

seg_array = np.random.randint(0,3,(3,50,50))
print(seg_array.min(),seg_array.max())
seg_array = ndimage.rotate(seg_array, angle=3, axes=(1, 2), reshape=False, cval=0)
print(seg_array.min(),seg_array.max())

'''
The two are different!
reference : https://stackoverflow.com/questions/46048874/obtain-different-range-after-applying-rotation-in-scipy-ndimage/46050624
'''
