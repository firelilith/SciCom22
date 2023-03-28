import numpy as np


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
        out = rk4_step(ode, start_vals, dt)
        yield out.copy()
