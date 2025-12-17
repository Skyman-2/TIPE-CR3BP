traj.display_pretty_trajectory(
    traj.simulate_trajectory(
        [3.15e8,0.,0.,1e1], # initial conditions
        1e6, # simulation time
        10, # time step
        earth_moon_system
    ),
    earth_moon_system,
    ax,fig,
    display_precision = 10
)