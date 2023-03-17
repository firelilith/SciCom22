import datetime

import newton
import post_newton_eih
import render.plotting
import library.file_io as io
from library import solar_system_reference
from library import coords
from render.renderlib import animate
from render.plotting import topdown, compare

preset = io.load_yaml_preset("/home/spectre/PycharmProjects/SciCom22/scicom/examples/sun_earth.yml")
bodies = solar_system_reference.solar_system_bodies # .remove("moon")
# bodies = ["mercury"]
preset = solar_system_reference.solar_system(bodies=bodies)

x, v, m, names = preset

# x -= coords.barycenter(x, m)
# v -= coords.barycenter(v, m)

newt = newton.nbody(*preset, 36000, 3600000)
post = post_newton_eih.nbody(*preset, 36000, 3600000)
ref  = solar_system_reference.get_series(bodies=bodies, dt=36000, duration=3600000)

gen1 = newt[0]
gen2 = post[0]

# render.plotting.topdown(ref)
animate(topdown, ref, out="out.mp4")
