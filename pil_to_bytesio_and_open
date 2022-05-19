from io import BytesIO
from PIL import Image
import numpy as np

np_image = (np.random.rand(100, 100, 3) * 255).astype("uint8")
np_image[3:20, 20:80] = 0
img_crop_pil = Image.fromarray(np_image)

# to bytes io
byte_io_image = BytesIO()
img_crop_pil.save(byte_io_image, format="PNG")

# browse
jpg_buffer = byte_io_image.getvalue()
print(jpg_buffer)
# b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x02\x00\x00\x00\x02\x00\x08\x02\x00\x00\x00{\x1aC\xad\x00\x01\x00\x00IDATx\x9c\x00\xff\x7f\x00\x80\x01\x8e\x9cr\xea4\xb1b\xfb\x04B\xeb\n\x10\x1f-\x01W\xef\xb54I\xb9\xa97&\x8ff\xb3sJ\xb2\x98^\xee\xbbR\x1e\xdcc\xde\x1a\x
print(byte_io_image)
# <_io.BytesIO object at 0x7fe8b9821890>

# Image open from BytesIO
d = Image.open(byte_io_image)
display(img_crop_pil)
display(d)
