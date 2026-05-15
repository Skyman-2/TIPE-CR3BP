def find_bracket(system,gamma_0):
    found = False
    i = 1
    while not found:
        perturbation = np.array([0, 0, 0, 0.1*i*gamma_0[3]])
        traj_a = rk4.simulate_trajectory(gamma_0+perturbation, 2*T/3, 10, system)
        traj_b = rk4.simulate_trajectory(gamma_0-perturbation, 2*T/3, 10, system)
        x_dot_a = return_state(traj_a)[2]
        x_dot_b = return_state(traj_b)[2]
        if x_dot_a * x_dot_b < 0:
            found = True
        else:
            i += 1
    return [gamma_0[3] - 0.1*i*gamma_0[3], gamma_0[3] + 0.1*i*gamma_0[3]]