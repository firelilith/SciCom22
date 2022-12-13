import numpy as np

from scipy.constants import G, pi

from scicom.integration import integrate


def newton_3body(starting_positions, starting_velocities, time_step, max_time):
    def x_dot(delta_t, vals, masses):
        return vals[1]

    def y_dot(delta_t, vals, masses):
        return G * np.sum(
            masses
        )

def random(time_step, max_time):
    positions = np.random.random((3, 3))
    velocities = np.random.random((3, 3))
    masses = np.random.random(3) * 10**10

    speed_offset = np.sum(velocities * masses, axis=1) / np.sum(masses)
    velocities -= speed_offset

    return newton_3body(starting_positions=positions,
                        starting_velocities=velocities,
                        time_step=time_step,
                        max_time=max_time)
