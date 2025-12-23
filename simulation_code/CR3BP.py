import json
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path

import src.verlet as vt
import src.rk as rk
import src.display as display

# plt.style.use('dark_background')

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


traj1 = rk.simulate_trajectory(
    [7e6,0.,0.,8e3],
    1e6,
    10,
    working_system
)

traj2 = rk.simulate_trajectory(
    [7e6,0.,0.,8e3],
    1e6,
    5,
    working_system
)

traj3 = rk.simulate_trajectory(
    [7e6,0.,0.,8e3],
    1e6,
    1,
    working_system
)


# Conjecture : dt/n => delta_spike/n^2 (cf petit papier bureau)

display.three_traj_comp(traj1,traj2,traj3,working_system,time_step=20,color_palette="inferno")

plt.show()
