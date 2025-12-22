import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
import src.phase_space as ps
import src.potential_overlay as uo

def plot_on_ax(ax,graph,color_palette,display_precision=10,isTraj=False):
    traj_arr = np.array(graph)
    x = traj_arr[::display_precision, 0]
    y = traj_arr[::display_precision, 1]

    points = np.column_stack([x, y]).reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    t_idx = np.arange(len(segments))
    norm = Normalize(t_idx.min(), t_idx.max())

    lc = LineCollection(segments, cmap=color_palette, norm=norm)
    lc.set_array(t_idx)
    lc.set_linewidth(1.5)

    if isTraj:
        ax.set_aspect("equal", adjustable="datalim")

    ax.add_collection(lc)
    ax.autoscale()
    ax.autoscale_view()



def plot_on_ax_bodies(ax,working_system):
    ax.add_patch(
        plt.Circle(
            [-working_system["barycenter"],0], 
            working_system["body1"]["radius"], 
            color="black", fill=False)
        )
    ax.add_patch(
        plt.Circle(
            [working_system["radius"]-working_system["barycenter"],0], 
            working_system["body2"]["radius"], 
            color="black", fill=False)
        )


def plot_potential(ax, working_system, pmin=20, steps=250, levels=25,
                   colors="k", linewidths=0.5, alpha=0.7):
    # freeze current limits
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    X, Y, Z = uo.equipotentials(working_system, steps, pmin=pmin, pmax=100)
    ax.contour(
        X, Y, Z,
        levels=levels,
        colors=colors,
        linewidths=linewidths,
        alpha=alpha,
        linestyles="solid"
    )

    # restore + lock
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_autoscale_on(False)




def one_traj_display(traj,working_system,color_palette="plasma"):
    layout = [
        ["traj","traj","phase","phase"],
        ["traj","traj","phase","phase"],
        ["traj","traj","phase","phase"],
        ["energy","energy","energy","energy"]
    ]
    fig, axes = plt.subplot_mosaic(layout, figsize=(12, 6),constrained_layout=True)
    
    plot_on_ax(axes["traj"],traj,color_palette,isTraj=True)
    plot_on_ax_bodies(axes["traj"],working_system)
    plot_potential(axes["traj"],working_system,pmin=30,levels=50,alpha=0.2)

    axes["phase"].grid(True)
    plot_on_ax(axes["phase"],ps.phase_space_diag(traj),color_palette)

def phase_spaces(traj,working_system,color_palette):
    layout = [
        ["traj","phase1","phase2"],
        ["traj","phase1","phase2"],
        ["phase","phase1","phase2"],
        ["phase","phase1","phase2"]
    ]
    fig, axes = plt.subplot_mosaic(layout, figsize=(12, 6),constrained_layout=True)
    plot_on_ax(axes["traj"],traj,color_palette,isTraj=True)
    plot_on_ax_bodies(axes["traj"],working_system)
    plot_potential(axes["traj"],working_system,pmin=30,levels=50,alpha=0.2)

    axes["phase"].grid(True)
    plot_on_ax(axes["phase"],ps.phase_space_diag(traj),color_palette)

    axes["phase1"].grid(True)
    plot_on_ax(axes["phase1"],ps.phase_space_xslice(traj),color_palette)

    axes["phase2"].grid(True)
    plot_on_ax(axes["phase2"],ps.phase_space_yslice(traj),color_palette)