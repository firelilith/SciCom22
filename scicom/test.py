import datetime

import newton
from post_newton_eih.nbody import _naive
import render.plotting
from library import solar_system_reference
from library import coords, file_io
from render.renderlib import animate
from render.plotting import *


from astropy import constants
import numpy as np
import rustlib

from library import file_io

pos_vel = np.array(([0, 0, 0, 0, 0, 0], [1, 0, 0, 1E20, 0, 0]))
m = np.array([1, 1]) * 1E20

print(constants.G.value)
print(constants.c.value)

print(_naive(pos_vel, m))
print(np.array(rustlib.post_newt_diff_eq(pos_vel, constants.G.value, constants.c.value, m, 5)))
