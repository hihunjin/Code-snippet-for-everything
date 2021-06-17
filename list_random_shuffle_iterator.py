import random

a = list(range(5))
random.shuffle(a)
print(a)
c = iter(a)
print(next(c))
