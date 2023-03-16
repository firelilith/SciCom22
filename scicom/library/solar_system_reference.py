from datetime import datetime, timedelta
from astropy import coordinates, time, units

import numpy as np

solar_system_bodies = ["sun", "mercury", "venus", "earth", "moon", "mars", "jupiter", "saturn", "uranus", "neptune"]


def solar_system(*,
                 bodies=None,
                 t=datetime.fromisocalendar(2000, 1, 1)):

    timestamp = time.Time(t, format="datetime")

    if bodies is None:
        bodies = solar_system_bodies
    elif not set(solar_system_bodies).issuperset(bodies):
        raise ValueError("only bodies in solar_system_reference.solar_system_bodies are allowed. "
                         "custom bodies must be set up via yaml or csv file.")

    # https://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html
    # https://nssdc.gsfc.nasa.gov/planetary/factsheet/
    masses = {"sun": 1.9885E30,
              "mercury": 3.30E23,
              "venus": 4.87E24,
              "earth": 5.97E24,
              "moon": 7.3E22,
              "mars": 6.42E23,
              "jupiter": 1.898E27,
              "saturn": 5.68E26,
              "uranus": 8.68E25,
              "neptune": 1.02E26}

    pos = []
    vel = []
    mas = np.array([masses[body] for body in bodies])

    for body in bodies:
        p, v = coordinates.get_body_barycentric_posvel(body, time=timestamp)
        pos.append(p.xyz.to(units.meter))
        vel.append(v.xyz.to(units.meter/units.second))

    return (np.array(pos) * units.meter,
            np.array(vel) * units.meter/units.second,
            mas,
            bodies)


def get_series(*, bodies: list, start: datetime, stop: datetime, dt: timedelta):
    now = start
    while now < stop:
        now += dt
        timestamp = time.Time(now, format="datetime")
        pos = np.array(
            [coordinates.get_body_barycentric(body, time=timestamp).xyz.to(units.m).value for body in bodies])
        yield pos * units.meter


print(solar_system(bodies=["sun", "earth"]))
