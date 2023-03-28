import datetime

import newton
import post_newton_eih
import render.plotting
from library import solar_system_reference
from library import coords, file_io
from render.renderlib import animate
from render.plotting import *

from library import file_io

time = datetime.datetime.fromisocalendar(year=2000, week=1, day=1)

preset = file_io.load_yaml_preset("/home/spectre/PycharmProjects/SciCom22/scicom/examples/sun_comet.yml")
bodies = solar_system_reference.solar_system_bodies # .remove("moon")
# bodies = ["earth", "sun", "moon"]
# preset = solar_system_reference.solar_system(bodies=bodies, t=time, trust_v=False)

x, v, m, names = preset

step = 10
n = 300000

newt = newton.nbody(*preset, step, n*step)
post = post_newton_eih.nbody(*preset, step, n*step)
old_post = post_newton_eih.old_nbody(*preset, step, n*step)
ref  = solar_system_reference.get_series(bodies=bodies, dt=step, duration=n*step, start=time)


# file_io.save_series("series/ref36000.csv", ref, overwrite=True)


n1 = file_io.load_series("series/post36000_no_trust_v.csv")
n2 = file_io.load_series("series/test.csv")

topdown_cmp(series1=newt, series1_name="newtonian", series2=post, series2_name="relativistic", show=True, radius=None)

# file_io.save_series("series/test.csv", post, overwrite=True)

topdown_cmp(series1=post, series2=old_post, series1_name="new", series2_name="old", series3=ref, series3_name="ref", show=True)

#topdown_cmp(series1=n1, series1_name="36000",
#            series2=n2, series2_name="ref",
#            show=True)
