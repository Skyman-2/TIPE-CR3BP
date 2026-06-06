    while abs(x_point_c) > precision:
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
    return c
