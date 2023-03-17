import numpy as np

import newton
import post_newton_eih
import render.plotting
import library.file_io as io
from library import solar_system_reference
from library import coords
from newton.nbody import _diff_eq, _naive

preset = io.load_yaml_preset("/home/spectre/PycharmProjects/SciCom22/scicom/examples/sun_earth.yml")
# preset = solar_system_reference.solar_system()

x, v, m, names = preset

# x -= coords.barycenter(x, m)
# v -= coords.barycenter(v, m)

newt = newton.nbody(*preset, 3600, 36000)
post = post_newton_eih.nbody(*preset, 3600, 36000)

gen1 = newt[0]
gen2 = post[0]

# print([(g1 - g2) for g1, g2 in zip(gen1, gen2)])

# render.plotting.compare(newt, post)

x = np.array([[1, 0, 0], [0, 0, 0]])
v = np.array([[5, 0, 0], [0, 0, -1]])
m = np.array([1, 20]) * 1E9

vals = np.concatenate((x, v), axis=1)

print(_diff_eq(vals, m))
print(_naive(vals, m))
