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
bodies = ["earth", "sun", "moon"]
preset = solar_system_reference.solar_system(bodies=bodies)

x, v, m, names = preset

step = 36000
n = 1000

newt = newton.nbody(*preset, step, n*step)
post = post_newton_eih.nbody(*preset, step, n*step)
ref  = solar_system_reference.get_series(bodies=bodies, dt=step, duration=n*step)

compare(newt, post, show=True)
# animate(topdown, ref, out="out.mp4")
# animate(compare, ref, newt, out="out2.mp4")
