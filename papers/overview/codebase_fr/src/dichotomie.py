import src.rk4 as rk4
import numpy as np


def dichotomie(extrema1, extrema2, precision, systeme, pas=10):
    if extrema1 > extrema2:
        extrema1, extrema2 = extrema2, extrema1
    while abs(extrema2 - extrema1) > precision:
        print("Précision actuelle : ", abs(extrema2 - extrema1))
        mid = (extrema1 + extrema2) / 2
        x0, y0, vx0, vy0 = mid, 0, 0, 0
        traj = rk4.simuler_trajectoire([x0, y0, vx0, vy0], 100, pas, systeme)
        distance_init = abs(traj[0][0] - extrema1)
        distance_end = abs(traj[-1][0] - extrema1)
        if distance_init < distance_end:
            extrema2 = mid
        else:
            extrema1 = mid
    return (extrema1 + extrema2) / 2


