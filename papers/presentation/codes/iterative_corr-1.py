def estimation_orbite_lineaire_0(amplitude,estimation_init_coef):
    return np.array([amplitude, 0, 0, estimation_init_coef*amplitude])


def trouver_intervalle(systeme,gamma_0):
    trouve = False
    i = 1
    while not trouve:
        perturbation = np.array([0, 0, 0, 0.01*i*gamma_0[3]])
        traj_a = rk4.simuler_trajectoire(gamma_0+perturbation, 2*T/3, 100, systeme)
        traj_b = rk4.simuler_trajectoire(gamma_0-perturbation, 2*T/3, 100, systeme)
        x_point_a = etat_retour(traj_a,systeme)[2]
        x_point_b = etat_retour(traj_b,systeme)[2]
        print(x_point_a, x_point_b)
        if x_point_a * x_point_b < 0:
            trouve = True
        else:
            i += 1
    return [gamma_0[3] - 0.01*i*gamma_0[3], gamma_0[3] + 0.01*i*gamma_0[3]]