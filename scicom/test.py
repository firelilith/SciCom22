import newton
import post_newton_eih
import render.plotting
import library.file_io as io
from library import solar_system_reference
from library import coords

preset = io.load_yaml_preset("/home/spectre/PycharmProjects/SciCom22/scicom/examples/sun_earth.yml")
# preset = solar_system_reference.solar_system()

x, v, m, names = preset

# x -= coords.barycenter(x, m)
# v -= coords.barycenter(v, m)

print(coords.barycenter(x, m))

newt = newton.nbody(*preset, 3600, 36000)
post = post_newton_eih.nbody(*preset, 3600, 36000)

gen1 = newt[0]
gen2 = post[0]

for g in gen1:
    print("barycenter")
    print(coords.barycenter(g[:, :3], m))
    print("\\barycenter")

# print([(g1 - g2) for g1, g2 in zip(gen1, gen2)])

# render.plotting.compare(newt, post)
