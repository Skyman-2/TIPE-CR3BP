import json
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path
import csv
import numpy as np

import src.verlet as vt
import src.rk as rk
import src.rk4 as rk4
import src.VFVDP as ei
import src.dichotomy as dich
import src.display as display
import src.linearize as lin
import src.linear_orbit_correction as loc
import src.monodromy as mon
import src.manifold as mf
import src.potential_overlay as po

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

x_L1 = dich.dichotomy(0, working_system["radius"], precision=1, system=working_system, step=10)
x_L1_100 = dich.dichotomy(0, working_system["radius"], precision=100, system=working_system, step=10)


x_0 = 1000000
vy0 = -21.898965265005835 
loc.dichotomy_vy(x_0,working_system,0.0000001)
# print(vy0)

# traj = rk4.simulate_trajectory([x_0+x_L1, 0, 0, vy0], 1010880, 10, working_system)

# M = mon.monodromy_matrix(working_system, traj, 10)
# print(mon.latexformat_eigenstuff(M))


# period = 2*np.pi/po.omega(working_system)
# dim = [working_system["radius"], working_system["radius"], working_system["radius"]/period, working_system["radius"]/period]

# traj_periodic = rk4.simulate_trajectory([x_0+x_L1, 0, 0, vy0], 1010880, 10, working_system)
# lambda_s = np.array([-8.98e-1,-4.40e-1,7.11e-6,3.34e-6])
# lambda_u = np.array([-8.98e-1,4.40e-1,-7.11e-6,3.34e-6])

# sampling = 20

# unstable_manifold_pos = mf.unstable_manifold_sampling(
#     lambda_u,
#     dim,
#     2e6,
#     100,
#     working_system,
#     traj_periodic,
#     sampling
# )
# unstable_manifold_neg = mf.unstable_manifold_sampling(
#     (-1)*lambda_u,
#     dim,
#     1.8e6,
#     100,
#     working_system,
#     traj_periodic,
#     sampling
# )
# stable_manifold_pos = mf.stable_manifold_sampling(
#     lambda_s,
#     dim,
#     2e6,
#     100,
#     working_system,
#     traj_periodic,
#     sampling
# )
# stable_manifold_neg = mf.stable_manifold_sampling(
#     (-1)*lambda_s,
#     dim,
#     1.8e6,
#     100,
#     working_system,
#     traj_periodic,
#     sampling
# )

# manifolds = stable_manifold_pos + stable_manifold_neg + unstable_manifold_pos + unstable_manifold_neg
# display.stacked_trajectories_display(manifolds,working_system)
# plt.show()

traj_startatL1_1 = rk4.simulate_trajectory([x_L1_100, 0, 0, 0], 2e6, 10, working_system)
degenerescence = display.one_traj_relative_origin_display(
    traj_startatL1_1,
    working_system,
    1,
    "plasma"
)
plt.show()

# with open("processing_code/output.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerows(degenerescence)

# IDEE : (cf * dans MCOT) CE DERNIER POINT FAIT REF A L’IDEE DE RAJOUTER DU BRUIT SUR UNE TRAJECTOIRE POUR ETUDIER SON EVOLUTION  SIMULATION DES FORCES ATTRACTIVES D’AUTRES CORPS DU SYSTEME