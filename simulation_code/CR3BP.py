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
import src.linearize as lin

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

vps = lin.eigenvaluesL1(working_system)
lambdavp = vps[1].real
nu = vps[2].imag
tau = lin.tau(working_system, nu)
sigma = lin.sigma(working_system, lambdavp)
print(lambdavp, nu)
print(tau)
print(sigma)



"""
tolerance = 1
precision = 0.0001
x_dot_return = float('inf')
gamma_0 = [x_L1+10000, 0, 0, -0.2]

def nearest_in_index(liste, reference, index_considered):
    if len(liste) == 0:
        return -1
    best_i = 0
    best_diff = abs(liste[0][index_considered] - reference)
    for i in range(len(liste)):
        diff = abs(liste[i][index_considered] - reference)
        if diff < best_diff:
            best_i = i
            best_diff = diff
    return best_i

x_dot_liste = []
# while abs(x_dot_return) > tolerance:
for i in range(220,300):
    gamma_0[3] = -0.2-precision*i
    traj_startatL1_1 = rk4.simulate_trajectory(gamma_0, 7e5, 10, working_system)
    study_segment = []
    # On récupère un segment ou y s'annule potentiellement
    for i in range(10000, len(traj_startatL1_1)):
        if abs(traj_startatL1_1[i][1]) < 100:
            study_segment.append(traj_startatL1_1[i])
    print(study_segment)
    # Dichotomie pour trouver le point le plus proche de y = 0
    if len(study_segment) != 0:
        index_nearest = nearest_in_index(study_segment, 0, 1)
        # On calcule la vitesse de retour
        x_dot_return = study_segment[index_nearest][2]
        x_dot_liste.append(x_dot_return)

    if x_dot_return < 0:
        print(i)
        break

    # display.one_traj_display(traj_startatL1_1,working_system)
    # plt.show()

print(x_dot_liste)"""


gamma_0 = [x_L1+10000, 0, 0, -0.2-(220+11)*0.0001]

# traj_startatL1_1 = rk4.simulate_trajectory(gamma_0, 1010880, 10, working_system)
# display.one_traj_display(traj_startatL1_1,working_system)
# plt.show()


# display.one_traj_display(traj_startatL1_1,working_system)
# plt.show()

# degenerescence = display.one_traj_relative_origin_display(
#     traj_startatL1_1,
#     working_system,
#     1,
#     "plasma"
# )

# with open("processing_code/output.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerows(degenerescence)

# IDEE : (cf * dans MCOT) CE DERNIER POINT FAIT REF A L’IDEE DE RAJOUTER DU BRUIT SUR UNE TRAJECTOIRE POUR ETUDIER SON EVOLUTION  SIMULATION DES FORCES ATTRACTIVES D’AUTRES CORPS DU SYSTEME