import numpy as np

from scicom.library import rk4_integration, distance_sca, distance_vec, distance_unt

from astropy import constants

from functools import partial


def nbody(pos, vel, mas, dt, time):
    pass


def _diff_eq(m, vals):
    iterations = 5

    out = np.zeros(vals.shape)

    out[..., :3] = vals[..., 3:]

    # calculate common values
    dist_vec = distance_vec(vals[..., :3])
    dist_sca = distance_sca(vals[..., :3])
    unit_vec = distance_unt(vals[..., :3])
    v_prod = np.tensordot(vals[..., 3:], vals[..., 3:].T, axes=1)

    n_acc = (constants.G * m[:, None, None] * dist_vec /
             (dist_sca ** 3)[:, :, None])
    n_acc[~np.isfinite(n_acc)] = 0

    n_acc_sum = np.sum(n_acc, axis=1)

    acc = n_acc.copy()

    #  https://en.wikipedia.org/wiki/Einstein%E2%80%93Infeld%E2%80%93Hoffmann_equations
    for i in range(iterations):
        new_acc = n_acc_sum
        new_acc += (1/(constants.c**2) *
                    n_acc * 1)

    out[..., 3:] = acc
    return out


def _iteration():
    pass
