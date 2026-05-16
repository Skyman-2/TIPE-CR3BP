def radius_through_time(traj,time_step):
    t = 0
    r = []
    for i in range(len(traj)):
        x = traj[i][0]
        y = traj[i][1]
        r.append([t,(x**2+y**2)/1e13+4.32e6])
        t += time_step
    return r
