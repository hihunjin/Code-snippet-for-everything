from itertools import cycle

def color_generator():
    colors = ["g", "b", "c", "m", "y", "k"]
    for color in cycle(colors):
        yield color


color_generator = color_generator()
for i in range(30):
    print(next(color_generator))
