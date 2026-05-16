    while abs(x_dot_c) > precision:
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
    return c