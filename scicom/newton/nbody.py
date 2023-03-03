import numpy as np

from functools import partial

from astropy import constants

from scicom.library import rk4_integration, distance_vec, distance_sca


def nbody(pos, vel, mas, dt, time):
    ode = partial(_diff_eq, m=mas)
    vals = np.concatenate((pos, vel), axis=-1)

    return rk4_integration(ode=ode, start_vals=vals, dt=dt, stop_time=time)


def _diff_eq(vals, m):
    """Newtonian acceleration: a = Gm/r^2 """
    out = np.zeros(vals.shape)
    out[..., :3] = vals[..., 3:]

    # numpy black magic, sorry not sorry
    dist = distance_vec(vals[..., :3])

    with np.errstate(divide="ignore", invalid="ignore"):
        acc = (constants.G * m[:, None, None] * dist /
               (distance_sca(vals[..., :3]) ** 3)[:, :, None])
    acc[~np.isfinite(acc)] = 0
    out[..., 3:] = np.sum(acc, axis=1)
    return out
