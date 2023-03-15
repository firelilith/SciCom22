import newton
import post_newton_eih

import numpy as np
from astropy import units, constants
from scicom.library import *

m = np.array([1., 2.])*10.**6
x = np.array([[1, 0, 0], [0, 0, 0]], dtype=float)
v = np.array([[1, 0, 0], [-1, 0, 0]], dtype=float)

vals = np.concatenate((x, v), axis=1)

for newt, post_newt in zip(newton.nbody(x, v, m, 1, 100), post_newton_eih.nbody(x, v, m, 1, 100)):
    print(np.max(newt - post_newt))
