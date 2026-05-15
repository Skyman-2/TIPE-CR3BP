### Faire le code pour la meta-dichotomie pour minimiser la vitesse en x lors du retour en y=0.
# Idée : Utiliser la position relative de la branche du retour dans l'espace de phase
# (témoigne du signe de la vitesse en x pour une raison ou une autre... weird)


import numpy as np
import src.rk4 as rk4
import matplotlib.pyplot as plt
import src.dichotomy as dich
import src.display as display


T = 1010880


def linear_orbit_guess_0(amplitude):
    return np.array([amplitude, 0, 0, -2.37e-5*amplitude])


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


# Hypothèse : il n'y a qu'une seule branche qui repasse par y = 0 après T/4 et l'impulsion initiale est en v_y < 0
def return_state(traj):
    for i in range(2, len(traj)):
        if traj[i-1][1] < 0 and traj[i][1] > 0:
            alpha = -traj[i-1][1] / (traj[i][1] - traj[i-1][1])
            return traj[i-1] + alpha * (traj[i] - traj[i-1])
    return None
        

def find_bracket(system,gamma_0):
    found = False
    i = 1
    while not found:
        print("Recherche n°", i)
        perturbation = np.array([0, 0, 0, 0.1*i*gamma_0[3]])
        traj_a = rk4.simulate_trajectory(gamma_0+perturbation, 2*T/3, 10, system)
        traj_b = rk4.simulate_trajectory(gamma_0-perturbation, 2*T/3, 10, system)
        x_dot_a = return_state(traj_a)[2]
        x_dot_b = return_state(traj_b)[2]
        print(x_dot_a, x_dot_b)
        display.ref_traj_comp(traj_a,traj_b,system)
        plt.show()
        if x_dot_a * x_dot_b < 0:
            found = True
        else:
            i += 1
    return [gamma_0[3] - 0.1*i*gamma_0[3], gamma_0[3] + 0.1*i*gamma_0[3]]

def dichotomy_vy(amplitude,system,precision):
    x_L1 = dich.dichotomy(0, system["radius"], precision=1, system=system, step=10)
    gamma_0 = linear_orbit_guess_0(amplitude) + np.array([x_L1, 0, 0, 0])
    bracket = find_bracket(system,gamma_0)
    c = (bracket[0]+bracket[1])/2
    gamma_a = gamma_0.copy()
    gamma_b = gamma_0.copy()
    gamma_c = gamma_0.copy()
    gamma_a[3] = bracket[0]
    gamma_b[3] = bracket[1]
    gamma_c[3] = c
    traj_a = rk4.simulate_trajectory(gamma_a, 2*T/3, 10, system)
    traj_b = rk4.simulate_trajectory(gamma_b, 2*T/3, 10, system)
    traj_c = rk4.simulate_trajectory(gamma_c, 2*T/3, 10, system)
    x_dot_a = return_state(traj_a)[2]
    x_dot_b = return_state(traj_b)[2]
    x_dot_c = return_state(traj_c)[2]
    print("Précision actuelle : ", abs(x_dot_c))
    while abs(x_dot_c) > precision:
        print()
        print()
        if x_dot_c * x_dot_a < 0:
            bracket[1] = c
            x_dot_b = x_dot_c
        else:
            bracket[0] = c
            x_dot_a = x_dot_c
        
        c = (bracket[0]+bracket[1])/2
        gamma_c[3] = c
        traj_c = rk4.simulate_trajectory(gamma_c, 2*T/3, 10, system)
        x_dot_c = return_state(traj_c)[2]
        print("Précision actuelle : ", abs(x_dot_c))
    return c














"""
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