# install
!pip install connected-components-3d --no-binary :all:




# generate 3d numpy array
import numpy as np
import torch

a = torch.randint(0,6,(50,512,512))
print(a.min(),a.max())
with open('5.npy', 'wb') as f:
            np.save(f, a)


# connected component 3d
import os
import cc3d
from tqdm import tqdm

input_loc = '.'
output_loc = 'postpros'

def main():
    
    if not os.path.exists(output_loc):
        os.mkdir(output_loc)
    
    predictions = os.listdir(input_loc)
    for pred in tqdm(predictions):
        if pred[-4:]!='.npy':
            continue
        vol = np.load(open(os.path.join(input_loc,pred), 'rb'))
        vol = post_processing(vol)

        with open(os.path.join(output_loc,pred), 'wb') as f:
            np.save(f, vol)



def post_processing(vol):
    vol_ = vol.copy()
    vol_[vol_ > 0] = 1
    vol_cc = cc3d.connected_components(vol_)
    cc_sum = [(i, vol_cc[vol_cc == i].shape[0]) for i in range(vol_cc.max() + 1)]
    cc_sum.sort(key=lambda x: x[1], reverse=True)
    cc_sum.pop(0)  # remove background
    reduce_cc = [cc_sum[i][0] for i in range(1, len(cc_sum)) if cc_sum[i][1] < cc_sum[0][1] * 0.1]
    for i in reduce_cc:
        vol[vol_cc == i] = 0
    
    return vol

main()
