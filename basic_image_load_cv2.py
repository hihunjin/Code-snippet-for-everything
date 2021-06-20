import cv2
import numpy as np
import matplotlib.pyplot as plt

def function_of_image(path=None):
    img = cv2.imread(path, 0)
    # TODO add something here
    return img

array = function_of_image('5.png')

##### Plot
plt.figure(figsize=(10, 10), dpi=80)
plt.imshow(array)#, cmap='gray')
