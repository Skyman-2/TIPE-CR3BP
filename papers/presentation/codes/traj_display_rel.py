def one_traj_relative_origin_display(traj,working_system,time_step=10,color_palette="plasma"):
    layout = [ // ]
    fig, axes = plt.subplot_mosaic(layout, figsize=(12, 6),constrained_layout=True)
    plot_on_ax(axes["traj"],traj,color_palette,isTraj=True)
    plot_on_ax_bodies(axes["traj"],working_system)
    plot_potential(axes["traj"],working_system,pmin=30,levels=50,alpha=0.2)
    plot_on_ax(axes["phase"],ps.phase_space_diag(traj),color_palette)
    plot_on_ax(axes["energy"],en.energy(traj,working_system,time_step),color_palette)
    origin_constant_traj = [traj[0]+[0.1,0,0,0] for i in range(len(traj))]
    origin_radius = en.radius_through_time(origin_constant_traj,time_step)
    traj_radius = en.radius_through_time(traj,time_step)
    orbit_degenerescence = rd.relative_diff_1D(traj_radius, origin_radius, time_step)
    plot_on_ax(axes["relative_radius"],orbit_degenerescence,color_palette)    
    return orbit_degenerescence