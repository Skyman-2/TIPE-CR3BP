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
    x_point_b = etat_retour(traj_b, systeme)[2]
    x_point_c = etat_retour(traj_c, systeme)[2]