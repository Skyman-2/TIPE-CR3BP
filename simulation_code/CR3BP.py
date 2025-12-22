import json
import matplotlib.pyplot as plt
from pathlib import Path

import src.verlet as vt
import src.potential_overlay as uo
import src.phase_space as ps
import src.rk as rk
import src.display as display


def __init__(system):
    def barycentre(m1,m2,r):
        return (m2*r)/(m1+m2)
    def update_system(system):
        system["barycenter"] = barycentre(
            system["body1"]["mass"],
            system["body2"]["mass"],
            system["radius"]
        )
    here = Path(__file__).parent
    with open(here / "systems.json", "r") as f:
        data = json.load(f)[system]
    update_system(data)
    return data
working_system = __init__("earth_moon")


traj = rk.simulate_trajectory(
    [3.15e8,0.,0.,1e1],
    1e7,
    50,
    working_system
)

display.one_traj_display(traj,working_system)

plt.show()
