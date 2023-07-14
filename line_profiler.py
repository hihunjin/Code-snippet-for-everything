import torch


class MyClass2:
    def __init__(self, x=1000):
        self.x = x

    @torch.inference_mode()
    def divide(self, x):
        return x / self.x


class MyClass:
    def __init__(self):
        self.x = 1
        self.div: MyClass2 = MyClass2(1000)

    def inc(self):
        self.x += 1

    def dec(self):
        self.x -= 1

    @torch.no_grad()
    def get(self):
        return self.x

    def sec_to_ms(self, x):
        return self.div.divide(x)


instance = MyClass()

# 라인 프로파일러
from line_profiler import LineProfiler
profiler = LineProfiler()
profiler.add_function(instance.inc)
profiler.add_function(instance.dec)
profiler.add_function(instance.get.__wrapped__)
profiler.add_function(instance.sec_to_ms)
profiler.add_function(instance.div.divide.__wrapped__)

num_iter = 200
for i in range(num_iter):
    profiler.run('instance.inc()')
    profiler.run('instance.dec()')
    profiler.run('instance.get()')
    profiler.run('instance.sec_to_ms(10.5)')


profiler.print_stats(output_unit=1e-3)  # ms 단위로 출력


# $ python test_profiler.py
# Timer unit: 0.001 s

# Total time: 6.2251e-05 s
# File: test_profiler.py
# Function: divide at line 8

# Line #      Hits         Time  Per Hit   % Time  Line Contents
# ==============================================================
#      8                                               @torch.inference_mode()
#      9                                               def divide(self, x):
#     10       200          0.1      0.0    100.0          return x / self.x

# Total time: 6.169e-05 s
# File: test_profiler.py
# Function: inc at line 18

# Line #      Hits         Time  Per Hit   % Time  Line Contents
# ==============================================================
#     18                                               def inc(self):
#     19       200          0.1      0.0    100.0          self.x += 1

# Total time: 6.3482e-05 s
# File: test_profiler.py
# Function: dec at line 21

# Line #      Hits         Time  Per Hit   % Time  Line Contents
# ==============================================================
#     21                                               def dec(self):
#     22       200          0.1      0.0    100.0          self.x -= 1

# Total time: 3.7258e-05 s
# File: test_profiler.py
# Function: get at line 24

# Line #      Hits         Time  Per Hit   % Time  Line Contents
# ==============================================================
#     24                                               @torch.no_grad()
#     25                                               def get(self):
#     26       200          0.0      0.0    100.0          return self.x

# Total time: 0.00111729 s
# File: test_profiler.py
# Function: sec_to_ms at line 28

# Line #      Hits         Time  Per Hit   % Time  Line Contents
# ==============================================================
#     28                                               def sec_to_ms(self, x):
#     29       200          1.1      0.0    100.0          return self.div.divide(x)
