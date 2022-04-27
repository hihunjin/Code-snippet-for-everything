import os
import numpy as np
from PIL import Image

out_loc = './random_image'
os.makedirs(out_loc, exist_ok=True)
for i in range(20):
    e = (np.random.rand(512, 512, 3) * 255).astype('uint8')
    out = Image.fromarray(e)
    out.save(os.path.join(
        out_loc, f'rand_{i}.png'
    ))
print(f"Location: {out_loc}")
# Location: ./random_image
