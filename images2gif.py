import imageio
import numpy as np

# collect images
images = []
for _ in range(10):
    images.append(np.uint8(np.random.randint(0,2,(512,512))))

# to gif
imageio.mimsave('movie.gif', images)
