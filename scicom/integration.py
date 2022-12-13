import numpy as np

from typing import List, Callable


def second_order_rk4_step(ode, x_vals, y_vals, timestep, constants):
    """Runge-Kutta-4 integration steps for a second order ODE
    """

    x_k1 = timestep * y_vals
    y_k1 = timestep * ode(x_vals, y_vals, constants)

    x_k2 = timestep * (y_vals + y_k1/2)
    y_k2 = timestep * ode(x_vals + x_k1/2, y_vals + y_k1/2, constants)

    x_k3 = timestep * (y_vals + y_k2/2)
    y_k3 = timestep * ode(x_vals + x_k2/2, y_vals + y_k2/2, constants)

    x_k4 = timestep * (y_vals + y_k3)
    y_k4 = timestep * ode(x_vals + x_k3, y_vals + y_k3, constants)

    return (x_vals + (x_k1 + 2*x_k2 + 2*x_k3 + x_k4) / 6,
            y_vals + (y_k1 + 2 * y_k2 + 2 * y_k3 + y_k4) / 6)


def integrate_ode2(second_order_ode,
                   starting_x: np.ndarray,
                   starting_xdot: np.ndarray,
                   timestep: float, time: float, constants: np.ndarray):
    x, x_dot = starting_x.copy(), starting_xdot.copy()
    for i in range(int(time/timestep+1)):
        x, x_dot = second_order_rk4_step(second_order_ode, x, x_dot, timestep, constants)
        yield x, x_dot
