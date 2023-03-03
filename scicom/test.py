from newton import nbody
import numpy as np

import astropy.units as u

x = np.array([[1, 0, 0],
              [-1, 0, 0]])
v = np.array([[0, .5, 0],
              [0, -.5, 0]])

m = np.ones(2) * 10**11
