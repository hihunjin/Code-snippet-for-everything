import cv2
from matplotlib import pyplot as plt

image = cv2.imread('image.png')
plt.imshow(image)
plt.title('my picture')
# plt.axis('off')
plt.show()
