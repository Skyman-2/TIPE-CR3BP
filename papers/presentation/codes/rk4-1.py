def simulate_trajectory(initial_conditions,simulation_time,step,system,inverse_time=False):
    if inverse_time:
        step = -step
        simulation_time = -simulation_time
    dt = step
    t_max = simulation_time
    t = 0
    i = 0
    def eqx(x,y,vy):
        coriolis = 2 * omega * vy
        centrifugal = omega**2 * x
        pull1 = body_pull_x(x,y,body1_pos,body1_mass)
        pull2 = body_pull_x(x,y,body2_pos,body2_mass)
        return pull1 + pull2 + coriolis + centrifugal
    def eqy(x,y,vx):
        coriolis = -2 * omega * vx
        centrifugal = omega**2 * y
        pull1 = body_pull_y(x,y,body1_pos,body1_mass)
        pull2 = body_pull_y(x,y,body2_pos,body2_mass)
        return pull1 + pull2 + coriolis + centrifugal
