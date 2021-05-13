'''
jupyter notebook or colab is desired
'''

#@markdown Quiet parts without notes detected (dB)
transparency = 0.95 #@param {type:"slider", min: 0, max:1, step:0.05}

import cv2
from matplotlib import pyplot as plt

##### read two images #####
background = cv2.imread('image1.png')
overlay = cv2.imread('image2.jpg')
print(background.shape)
print(overlay.shape)


##### resize          #####
background = cv2.resize(background, dsize=(700,700), interpolation=cv2.INTER_CUBIC)
overlay = cv2.resize(overlay, dsize=(700,700), interpolation=cv2.INTER_CUBIC)

##### overlay         #####
added_image = cv2.addWeighted(background,transparency,overlay,1-transparency,0)


##### save and show on notebook #####
cv2.imwrite('combined.png', added_image)
plt.imshow(added_image)
plt.title('my picture')
plt.show()
