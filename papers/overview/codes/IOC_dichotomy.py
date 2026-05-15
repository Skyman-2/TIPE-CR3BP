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