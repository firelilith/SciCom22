import matplotlib
import matplotlib.pyplot as plt
from matplotlib import pyplot

from library.file_io import load_yaml_preset
from newton import adaptive_nbody as newt_nbody
from post_newton_eih import adaptive_nbody as post_nbody
from render.plotting import topdown_cmp, topdown
from library.file_io import save_series, load_series

preset = load_yaml_preset("examples/isco.yml")

tolerance = 100000

t = 1

newt = newt_nbody(*preset, tolerance=tolerance, time=t, dt=0.001)
post = post_nbody(*preset, tolerance=tolerance, time=t, dt=0.001)

topdown_cmp(series1=newt, series1_name="newt",
            series2=post, series2_name="post",
            show=True,
            radius=None)
