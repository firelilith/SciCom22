from newton import nbody
import numpy as np

x = np.array([[1, 0, 0],
              [0, 1, 0],
              [0, 0, 1]])
v = np.ones(x.shape)

m = np.ones(3)

for step in nbody(x, v, m, 1, 3):
    print(step)
