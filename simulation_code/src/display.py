import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
import src.phase_space as ps
import src.potential_overlay as uo
import src.energy as en
import src.relative_diff as rd



### CHATGPT FUNCTION TO FORCE OFFSET
import matplotlib.ticker as mticker

def force_offset_scale(ax):
    fmt = mticker.ScalarFormatter(useMathText=True)

    fmt.set_useOffset(True)      # ✅ force le "+4.322e6"
    fmt.set_scientific(False)    # ❌ interdit le "×10^6"

    ax.yaxis.set_major_formatter(fmt)
### CHATGPT STUFF ENDED


def autonamed_subplot(axes, graph_labels):
    for name, ax in axes.items():
        ax.set_title(graph_labels[name]["name"])
        ax.set_xlabel(graph_labels[name]["xlabel"])
        ax.set_ylabel(graph_labels[name]["ylabel"])


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



def one_traj_display(traj,working_system,time_step=10,color_palette="plasma"):
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

    axes["energy"].grid(True)
    plot_on_ax(axes["energy"],en.energy(traj,working_system,time_step),color_palette)
    plot_on_ax(axes["energy"],en.radius_through_time(traj,time_step),"viridis")



def three_traj_comp(traj1,traj2,traj3,working_system,time_step=10,color_palette="plasma"):
    layout = [
        ["traj1","phase1","energy1","energy1"],
        ["traj2","phase2","energy2","energy2"],
        ["traj3","phase3","energy3","energy3"]
    ]
    fig, axes = plt.subplot_mosaic(layout, figsize=(12, 6),constrained_layout=True)
    
    plot_on_ax(axes["traj1"],traj1,color_palette,isTraj=True)
    plot_on_ax_bodies(axes["traj1"],working_system)
    plot_potential(axes["traj1"],working_system,pmin=30,levels=50,alpha=0.2)

    plot_on_ax(axes["traj2"],traj2,color_palette,isTraj=True)
    plot_on_ax_bodies(axes["traj2"],working_system)
    plot_potential(axes["traj2"],working_system,pmin=30,levels=50,alpha=0.2)

    plot_on_ax(axes["traj3"],traj3,color_palette,isTraj=True)
    plot_on_ax_bodies(axes["traj3"],working_system)
    plot_potential(axes["traj3"],working_system,pmin=30,levels=50,alpha=0.2)

    axes["phase1"].grid(True)
    plot_on_ax(axes["phase1"],ps.phase_space_diag(traj1),color_palette)

    axes["phase2"].grid(True)
    plot_on_ax(axes["phase2"],ps.phase_space_diag(traj2),color_palette)

    axes["phase3"].grid(True)
    plot_on_ax(axes["phase3"],ps.phase_space_diag(traj3),color_palette)

    axes["energy1"].grid(True)
    plot_on_ax(axes["energy1"],en.energy(traj1,working_system,time_step),color_palette)
    # plot_on_ax(axes["energy1"],en.radius_through_time(traj1,time_step),"viridis")

    axes["energy2"].grid(True)
    plot_on_ax(axes["energy2"],en.energy(traj2,working_system,time_step),color_palette)
    # plot_on_ax(axes["energy2"],en.radius_through_time(traj2,time_step),"viridis")

    axes["energy3"].grid(True)
    plot_on_ax(axes["energy3"],en.energy(traj3,working_system,time_step),color_palette)
    # plot_on_ax(axes["energy3"],en.radius_through_time(traj3,time_step),"viridis")

    for k in ["energy1", "energy2", "energy3"]:
        force_offset_scale(axes[k])


def ref_traj_comp(ref_traj,comp_traj,working_system,time_step=10,color_palette="plasma"):
    layout = [
        ["ref_traj","ref_phase","ref_energy"],
        ["comp_traj","comp_phase","comp_energy"],
        ["relative_radius","relative_phase","relative_energy"],
        ["relative_radius","relative_phase","relative_energy"]
    ]
    fig, axes = plt.subplot_mosaic(layout, figsize=(12, 6),constrained_layout=True)

    ref_radius = en.radius_through_time(ref_traj,time_step)
    comp_radius = en.radius_through_time(comp_traj,time_step)

    ref_phase = ps.phase_space_diag(ref_traj)
    comp_phase = ps.phase_space_diag(comp_traj)

    ref_energy = en.energy(ref_traj,working_system,time_step)
    comp_energy = en.energy(comp_traj,working_system,time_step)

    plot_on_ax(axes["ref_traj"],ref_traj,color_palette,isTraj=True)
    plot_on_ax_bodies(axes["ref_traj"],working_system)
    plot_potential(axes["ref_traj"],working_system,pmin=30,levels=50,alpha=0.2)

    plot_on_ax(axes["comp_traj"],comp_traj,color_palette,isTraj=True)
    plot_on_ax_bodies(axes["comp_traj"],working_system)
    plot_potential(axes["comp_traj"],working_system,pmin=30,levels=50,alpha=0.2)

    axes["ref_phase"].grid(True)
    plot_on_ax(axes["ref_phase"],ref_phase,color_palette)

    axes["comp_phase"].grid(True)
    plot_on_ax(axes["comp_phase"],comp_phase,color_palette)

    axes["ref_energy"].grid(True)
    plot_on_ax(axes["ref_energy"],ref_energy,color_palette)
    # plot_on_ax(axes["ref_energy"],en.radius_through_time(ref_traj,time_step),"viridis")

    axes["comp_energy"].grid(True)
    plot_on_ax(axes["comp_energy"],comp_energy,color_palette)
    # plot_on_ax(axes["comp_energy"],en.radius_through_time(comp_traj,time_step),"viridis")

    axes["relative_radius"].grid(True)
    plot_on_ax(axes["relative_radius"],rd.relative_diff_1D(ref_radius, comp_radius, time_step),color_palette)

    axes["relative_phase"].grid(True)
    plot_on_ax(axes["relative_phase"],rd.relative_diff_2D(ref_phase, comp_phase, time_step),color_palette)

    axes["relative_energy"].grid(True)
    plot_on_ax(axes["relative_energy"],rd.relative_diff_1D(ref_energy, comp_energy, time_step),color_palette)

    labels = {
        "ref_traj": {
            "name": "Reference Trajectory",
            "xlabel": "x [m]",
            "ylabel": "y [m]",
        },
        "ref_phase": {
            "name": "Reference Phase Space",
            "xlabel": "x [m]",
            "ylabel": "y [m]",
        },
        "ref_energy": {
            "name": "Reference Energy",
            "xlabel": "Time [s]",
            "ylabel": "Energy [J]",
        },
        "comp_traj": {
            "name": "Trajectory compared",
            "xlabel": "x [m]",
            "ylabel": "y [m]",
        },
        "comp_phase": {
            "name": "Phase Space of compared",
            "xlabel": "x [m]",
            "ylabel": "y [m]",
        },
        "comp_energy": {
            "name": "Energy of compared",
            "xlabel": "Time [s]",
            "ylabel": "Energy [J]",
        },
        "relative_radius": {
            "name": "Relative Radius",
            "xlabel": "Time [s]",
            "ylabel": "Ratio",
        },
        "relative_phase": {
            "name": "Relative Phase Space",
            "xlabel": "Time [s]",
            "ylabel": "Ratio",
        },
        "relative_energy": {
            "name": "Relative Energy",
            "xlabel": "Time [s]",
            "ylabel": "Ratio",
        },
    }

    autonamed_subplot(axes, labels)

    for k in ["ref_energy", "comp_energy", "relative_energy"]:
        force_offset_scale(axes[k])


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