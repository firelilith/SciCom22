import numpy as np

from scipy.constants import G, pi

from scicom.integration import integrate_ode2


def newton_3body(starting_positions, starting_velocities, masses, time_step, max_time):
    def acceleration(x, x_dot, masses: np.ndarray):
        out = np.zeros(x.shape)

        for i, r in enumerate(x):
            for q in x:
                if np.all(r == q):
                    continue
                out[i] += G * masses[i] * (q - r) / np.sum((r-q)**2)**3
        return np.array(out)

    return integrate_ode2(second_order_ode=acceleration,
                          starting_x=starting_positions,
                          starting_xdot=starting_velocities,
                          timestep=time_step,
                          time=max_time,
                          constants=masses)


def random(time_step, max_time, N=3):
    positions = np.random.random((N, 3))
    velocities = np.random.random((N, 3)) / 10
    masses = np.random.random(N) * 10**7

    speed_offset = np.sum(velocities * masses[:, np.newaxis], axis=1) / np.sum(masses)
    velocities -= speed_offset[:, np.newaxis]

    return newton_3body(starting_positions=positions,
                        starting_velocities=velocities,
                        masses=masses,
                        time_step=time_step,
                        max_time=max_time)


