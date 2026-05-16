def energy(traj,working_system,time_step):
    t = 0
    e = []
    for i in range(len(traj)):
        x = traj[i][0]
        y = traj[i][1]
        vx = traj[i][2]
        vy = traj[i][3]
        potential_energy = uo.potential(x,y,working_system)
        kinetic_energy = 0.5*(vx**2 + vy**2)
        e.append([t,-2*potential_energy-2*kinetic_energy])
        t += time_step
    return e