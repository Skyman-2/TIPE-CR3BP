### Faire le code pour la meta-dichotomie pour minimiser la vitesse en x lors du retour en y=0.
# Idée : Utiliser la position relative de la branche du retour dans l'espace de phase
# (témoigne du signe de la vitesse en x pour une raison ou une autre... weird)


import numpy as np
import src.rk4 as rk4
import matplotlib.pyplot as plt
import src.dichotomie as dich
import src.affichage as affichage


T = 15e6


def estimation_orbite_lineaire_0(amplitude,estimation_init_coef):
    return np.array([amplitude, 0, 0, estimation_init_coef*amplitude])


def plus_proche_dans_index(liste, reference, index_considered):
    if len(liste) == 0:
        return -1
    meilleur_i = 0
    meilleur_diff = abs(liste[0][index_considered] - reference)
    for i in range(len(liste)):
        diff = abs(liste[i][index_considered] - reference)
        if diff < meilleur_diff:
            meilleur_i = i
            meilleur_diff = diff
    return meilleur_i


# Hypothèse : il n'y a qu'une seule branche qui repasse par y = 0 après T/4 et l'impulsion initiale est en v_y < 0
def etat_retour(traj, systeme_actif):
    for i in range(2, len(traj)):
        if traj[i-1][1] < 0 and traj[i][1] > 0:
            alpha = -traj[i-1][1] / (traj[i][1] - traj[i-1][1])
            return traj[i-1] + alpha * (traj[i] - traj[i-1])
    affichage.affichage_trajectoire_simple(traj, systeme_actif)
    plt.show()
    return None
        

def trouver_intervalle(systeme,gamma_0):
    trouve = False
    i = 1
    while not trouve:
        print("Recherche n°", i)
        perturbation = np.array([0, 0, 0, 0.01*i*gamma_0[3]])
        traj_a = rk4.simuler_trajectoire(gamma_0+perturbation, 2*T/3, 100, systeme)
        traj_b = rk4.simuler_trajectoire(gamma_0-perturbation, 2*T/3, 100, systeme)
        affichage.comparaison_traj_ref(traj_a,traj_b,systeme)
        plt.show()
        x_point_a = etat_retour(traj_a,systeme)[2]
        x_point_b = etat_retour(traj_b,systeme)[2]
        print(x_point_a, x_point_b)
        if x_point_a * x_point_b < 0:
            trouve = True
        else:
            i += 1
    print()
    print("------------------------------")
    print("Bracket trouvé : ", gamma_0[3] - 0.01*i*gamma_0[3], gamma_0[3] + 0.01*i*gamma_0[3])
    print("------------------------------")
    print()
    return [gamma_0[3] - 0.01*i*gamma_0[3], gamma_0[3] + 0.01*i*gamma_0[3]]

def dichotomie_vy(amplitude,systeme,precision,estimation_init_coef):
    x_L1 = dich.dichotomie(0, systeme["rayon"], precision=1, systeme=systeme, pas=10)
    gamma_0 = estimation_orbite_lineaire_0(amplitude,estimation_init_coef) + np.array([x_L1, 0, 0, 0])
    bracket = trouver_intervalle(systeme,gamma_0)
    c = (bracket[0]+bracket[1])/2
    gamma_a = gamma_0.copy()
    gamma_b = gamma_0.copy()
    gamma_c = gamma_0.copy()
    gamma_a[3] = bracket[0]
    gamma_b[3] = bracket[1]
    gamma_c[3] = c
    traj_a = rk4.simuler_trajectoire(gamma_a, 2*T/3, 100, systeme)
    traj_b = rk4.simuler_trajectoire(gamma_b, 2*T/3, 100, systeme)
    traj_c = rk4.simuler_trajectoire(gamma_c, 2*T/3, 100, systeme)
    x_point_a = etat_retour(traj_a, systeme)[2]
    print("A renvoyé état a")
    x_point_b = etat_retour(traj_b, systeme)[2]
    print("A renvoyé état b")
    x_point_c = etat_retour(traj_c, systeme)[2]
    print("A renvoyé état c")
    print("Précision actuelle : ", abs(x_point_c))
    while abs(x_point_c) > precision:
        print()
        print()
        if x_point_c * x_point_a < 0:
            bracket[1] = c
            x_point_b = x_point_c
        else:
            bracket[0] = c
            x_point_a = x_point_c
        
        c = (bracket[0]+bracket[1])/2
        gamma_c[3] = c
        traj_c = rk4.simuler_trajectoire(gamma_c, 2*T/3, 100, systeme)
        x_point_c = etat_retour(traj_c, systeme)[2]
        print("Précision actuelle : ", abs(x_point_c))
    return c

