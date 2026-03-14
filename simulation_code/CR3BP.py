import json
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path
import csv

import src.verlet as vt
import src.rk as rk
import src.rk4 as rk4
import src.VFVDP as ei
import src.dichotomy as dich
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


# traj_orbite = vt.simulate_trajectory(
#     [(0.8369151258-1.0081e-3)*Rm, 0., 0., 0.008372273267*vm],
#     2e6,
#     10,
#     working_system
# )

# traj = vt.simulate_trajectory(
#     [1.47e11, 0., 0., 8e3],
#     2.5e7,
#     10,
#     working_system
# )

# trajNew = rk.simulate_trajectory(
#     [7e9, 0., 0., 8e4],
#     2.5e6,
#     10,
#     working_system
# )

x_L1 = dich.dichotomy(0, working_system["radius"], 1, working_system, 10)

traj_startatL1_1 = vt.simulate_trajectory(
    [x_L1, 0., 0., 0.],
    1e6,
    1,
    working_system
)

degenerescence = display.one_traj_relative_origin_display(
    traj_startatL1_1,
    working_system,
    100,
    "plasma"
)

plt.show()

with open("output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(degenerescence)

# IDEE : (cf * dans MCOT) CE DERNIER POINT FAIT REF A L’IDEE DE RAJOUTER DU BRUIT SUR UNE TRAJECTOIRE POUR ETUDIER SON EVOLUTION  SIMULATION DES FORCES ATTRACTIVES D’AUTRES CORPS DU SYSTEME