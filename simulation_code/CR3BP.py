import json
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path

import src.verlet as vt
import src.rk as rk
import src.rk4 as rk4
import src.VFVDP as ei
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


# traj1 = vt.simulate_trajectory(
#     [7e6,0.,0.,8e3],
#     1e6,
#     20,
#     working_system
# )
# traj2 = rk.simulate_trajectory(
#     [7e6,0.,0.,8e3],
#     2.5e6,
#     10,
#     working_system
# )
# traj3 = ei.simulate_trajectory(
#     [7e6,0.,0.,8e3],
#     1e6,
#     20,
#     working_system
# )
# Conjecture : dt/n => delta_spike/n^2 (in RK) (cf petit papier bureau)
# display.ref_traj_comp(traj1,traj3,working_system,time_step=20,color_palette="inferno")

Rm = working_system["radius"]
vm = 1023.15

# traj = vt.simulate_trajectory(
#     [(0.8369151258-1.0081e-3)*Rm, 0., 0., 0.008372273267*vm],
#     2e6,
#     10,
#     working_system
# )

traj = vt.simulate_trajectory(
    [7e6, 0., 0., 8e3],
    2.5e6,
    10,
    working_system
)

trajNew = rk.simulate_trajectory(
    [7e6, 0., 0., 8e3],
    2.5e6,
    10,
    working_system
)

# display.phase_spaces(traj,working_system,"plasma")
display.ref_traj_comp(traj,trajNew,working_system,time_step=10,color_palette="plasma")


plt.show()
