def stacked_trajectories_display(trajs,working_system,time_step=10,color_palette=[]):
    if color_palette == []:
        for i in range(len(trajs)//2):
            color_palette.append("plasma")
        for i in range(len(trajs)//2):
            color_palette.append("viridis")
    layout = [
        ["traj","phase"]
    ]
    fig, axes = plt.subplot_mosaic(layout, figsize=(12, 6),constrained_layout=True)
    for i in range(len(trajs)):
        plot_on_ax(axes["traj"],trajs[i],color_palette[i],isTraj=True)
        plot_on_ax(axes["phase"],velocity_traj(trajs[i]),color_palette[i],isTraj=True)
    plot_on_ax_bodies(axes["traj"],working_system)
    plot_potential(axes["traj"],working_system,pmin=30,levels=50,alpha=0.2)