from matplotlib import animation
import matplotlib.pyplot as plt
import numpy as np


def plot(series):
    gen, times, mass, labels = series

    first = next(gen)

    color = np.log(mass / np.min(mass))

    fig = plt.figure()
    ax = plt.axes(projection="3d")

    scatter_plot = ax.scatter(first[:, 0], first[:, 1], first[:, 2], c=mass/np.max(mass))

    ani = animation.FuncAnimation(fig, update,
                                  frames=gen,
                                  fargs=(scatter_plot, ax),
                                  repeat=True,
                                  interval=0.05)

    plt.show()


def update(frame, plot, axis):
    plot._offsets3d = frame[:, :3].T

