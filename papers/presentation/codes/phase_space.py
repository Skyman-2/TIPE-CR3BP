def phase_space_diag(traj):
    diag = []
    for i in range(len(traj)):
        x = traj[i][0]
        y = traj[i][1]
        vx = traj[i][2]
        vy = traj[i][3]
        abs_pos = np.sqrt(x**2 + y**2)
        abs_vel = np.sqrt(vx**2 + vy**2)
        diag.append([abs_pos,abs_vel])
        # print(diag[i])
    return diag