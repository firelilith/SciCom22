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
    v_vec = vals[..., 3:]
    v_prod = np.tensordot(vals[..., 3:], vals[..., 3:].T, axes=1)

    n_acc = (constants.G * m[:, None, None] * dist_vec /
             (dist_sca ** 3)[:, :, None])
    n_acc[~np.isfinite(n_acc)] = 0

    n_acc_sum = np.sum(n_acc, axis=1)

    n_acc = n_acc.value

    acc = n_acc_sum.copy()

    #  https://en.wikipedia.org/wiki/Einstein%E2%80%93Infeld%E2%80%93Hoffmann_equations
    for i in range(iterations):
        new_acc = np.zeros(n_acc_sum.shape)

        first_term = np.ones(1)[:, None, None]
        first_term[~np.isfinite(first_term)] = 0
        new_acc += np.sum(n_acc * first_term, axis=1)

        second_term = (m[:, None, None] / dist_sca[:, :, None]**2
                       * ((np.sum(unit_vec * (4 * v_vec[None, :, :] - 3 * v_vec[:, None, :]), axis=2))[:, :, None]
                       * (v_vec[None, :, :] - v_vec[:, None, :])))
        second_term[~np.isfinite(second_term)] = 0
        new_acc += -constants.G.value / constants.c.value**2 * np.sum(second_term, axis=1)

        third_term = m[:, None, None] * acc[:, None, :].value / dist_sca[:, :, None]
        third_term[~np.isfinite(third_term)] = 0
        new_acc += constants.G.value * 7 / (2 * constants.c.value**2) * np.sum(third_term, axis=1)

        print(new_acc - acc)
        acc = new_acc

    out[..., 3:] = acc
    return out


def _iteration():
    pass
