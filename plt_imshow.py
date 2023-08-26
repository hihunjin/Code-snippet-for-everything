# !wget https://thispersondoesnotexist.com -O 'image.png'

import matplotlib.pyplot as plt
import cv2

# load
image = cv2.imread("image.png")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# show
plt.imshow(image)

# show without edge blur
plt.imshow(image, interpolation='nearest')
