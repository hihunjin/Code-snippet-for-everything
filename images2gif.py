import imageio
import numpy as np

# collect images
images = []
for _ in range(10):
    images.append(np.uint8(np.random.randint(0,255,(512,512))))

# to gif
imageio.mimsave('movie.gif', images, format='GIF', duration=0.2) # duration unit = second | format='GIF' 는 없어도 됨.
