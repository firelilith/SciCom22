import numpy as np
import logging

logger = logging.getLogger(__name__)


def rk4_step(ode: callable, vals: np.array, dt: float):
    """
    Time-independent RK4-integration.
    :param ode: callable, the system of ODEs to be solved
    :param vals: np.array or array-like, old system state
    :param dt: float, time step for integration
    :return: np.array or array-like, new system state
    """
    k1 = dt * ode(vals)
    k2 = dt * ode(vals + k1/2)
    k3 = dt * ode(vals + k2/2)
    k4 = dt * ode(vals + k3)

    vals += (k1 + 2*k2 + 2*k3 + k4) / 6
    return vals


def rk4_integration(ode, start_vals, dt, stop_time):
    for i in range(int(stop_time/dt)):
        yield rk4_step(ode, start_vals, dt).copy()


def rkf45_integration(ode, vals, dt, stop_time, tolerance, **kwargs):
    t = 0
    next_log = 0
    while t < stop_time:
        if next_log == 0:
            logger.info(f"{t=:.2f}, {t/stop_time:.2%} done")
            next_log = 1000
        next_log -= 1
        if (stop_time-t) < dt:
            dt = stop_time - t
        t, dt = rkf45_step(ode, vals, t, dt, tolerance, **kwargs)
        yield vals.copy(), t


# https://link.springer.com/article/10.1007/BF02234758
COEFFICIENT_TABLE = (
    (0,      0,        0,      0,     0),
    (2/9,    0,        0,      0,     0),
    (1/12,   1/4,      0,      0,     0),
    (69/128, -243/128, 135/64, 0,     0),
    (-17/12, 27/4,     -27/5,  16/15, 0),
    (65/432, -5/16,    13/16,  4/27,  5/144)
)
AVERAGE_TABLE = (47/450, 0, 12/25, 32/225, 1/30, 6/25)
ERROR_TABLE = (6/25, 0, -3/100, 16/75, 1/20, -6/25)


def rkf45_step(ode: callable, vals: np.array, current_time, dt, tolerance,
               c_tab=COEFFICIENT_TABLE,
               a_tab=AVERAGE_TABLE,
               e_tab=ERROR_TABLE) -> (np.ndarray, float):
    """https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta%E2%80%93Fehlberg_method"""

    while True:
        k1 = dt * ode(vals)
        k2 = dt * ode(vals + k1 * c_tab[1][0])
        k3 = dt * ode(vals + k1 * c_tab[2][0] + k2 * c_tab[2][1])
        k4 = dt * ode(vals + k1 * c_tab[3][0] + k2 * c_tab[3][1] + k3 * c_tab[3][2])
        k5 = dt * ode(vals + k1 * c_tab[4][0] + k2 * c_tab[4][1] + k3 * c_tab[4][2] + k4 * c_tab[4][3])
        k6 = dt * ode(vals + k1 * c_tab[5][0] + k2 * c_tab[5][1] + k3 * c_tab[5][2] + k4 * c_tab[5][3] + k5 * c_tab[5][4])

        truncation_error = np.linalg.norm(
            e_tab[0] * k1 + e_tab[1] * k2 + e_tab[2] * k3 + e_tab[3] * k4 + e_tab[4] * k5 + e_tab[5] * k6)

        new_dt = 0.9 * dt * (tolerance / truncation_error) ** 0.2

        if truncation_error < tolerance:
            vals += a_tab[0] * k1 + a_tab[1] * k2 + a_tab[2] * k3 + a_tab[3] * k4 + a_tab[4] * k5 + a_tab[5] * k6
            return current_time + dt, new_dt
        else:
            logger.warning(f"not accurate enough: {truncation_error}; retrying with {dt=}")
            dt = new_dt
