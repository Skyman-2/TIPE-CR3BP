def rayon_dans_le_temps(traj,pas_temps):
    t = 0
    r = []
    for i in range(len(traj)):
        x = traj[i][0]
        y = traj[i][1]
        r.append([t,(x**2+y**2)/1e13+4.32e6])
        t += pas_temps
    return r