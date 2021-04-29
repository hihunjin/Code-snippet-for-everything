import numpy as np
import torch

ex = np.random.randint(0,2,(40,100,100))
def get_pointcloud_from_np(ex):
    pc=[]
    for i in range(ex.shape[0]):
        for j in range(ex.shape[1]):
            for k in range(ex.shape[2]):
                # print(ex[i,j,k])
                if ex[i,j,k] == 1:
                    pc.append((i,j,k))
    return pc
print(len(get_pointcloud_from_np(ex)))
