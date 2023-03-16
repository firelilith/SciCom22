import numpy as np

from functools import partial

from astropy import constants

from scicom.library.rk4 import rk4_integration
from scicom.library.coords import distance_vec, distance_sca
from scicom.library.unit_helpers import unit_setup


def nbody(positions, velocities, masses, labels, dt, time):
    x, v, m = unit_setup(positions, velocities, masses)
    ode = partial(_diff_eq, m=m)
    vals = np.concatenate((x, v), axis=-1)

    return (rk4_integration(ode=ode, start_vals=vals, dt=dt, stop_time=time),
            np.linspace(0, time, int(time/dt)),
            masses,
            labels)


def _diff_eq(vals, m):
    """Newtonian acceleration: a = Gmr/|r|^3 """  # TODO: somthing is going wrong here, barycenter isn't preserved
    out = np.zeros(vals.shape)
    out[..., :3] = vals[..., 3:]

    # numpy black magic, sorry not sorry
    dist = distance_vec(vals[..., :3])
    dist_sca = distance_sca(vals[..., :3])

    with np.errstate(divide="ignore", invalid="ignore"):
        mG = constants.G.value * m
        mGdist = mG[:, None, None] * dist
        acc = mGdist / dist_sca[:, :, None] ** 3
        # acc = (constants.G.value * m[:, None, None] * dist /
        #        (dist_sca ** 3)[:, :, None])

    print(acc)

    acc[~np.isfinite(acc)] = 0
    out[..., 3:] = np.sum(acc, axis=1)
    return out
