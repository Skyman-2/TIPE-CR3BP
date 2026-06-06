def diag_espace_de_phase(traj):
    diag = []
    for i in range(len(traj)):
        x = traj[i][0]
        y = traj[i][1]
        vx = traj[i][2]
        vy = traj[i][3]
        pos_abs = np.sqrt(x**2 + y**2)
        vit_abs = np.sqrt(vx**2 + vy**2)
        diag.append([pos_abs,vit_abs])
    return diag