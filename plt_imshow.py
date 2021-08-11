# !wget https://thispersondoesnotexist.com/image -O 'image.png'

import matplotlib.pyplot as plt

# load
image = cv2.imread("image.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# show
plt.imshow(image)
