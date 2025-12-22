import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize

def plot_on_ax(ax,graph,working_system,isTraj=False,display_precision=10):
    traj_arr = np.array(graph)   # shape (nsteps, 4)
    x = traj_arr[::display_precision, 0]
    y = traj_arr[::display_precision, 1]

    points = np.array([x,y]).T.reshape(-1,1,2)
    segments = np.concatenate([points[:-1],points[1:]],axis=1)
    t_idx = np.arange(len(x))
    norm = Normalize(t_idx.min(), t_idx.max())
    lc = LineCollection(segments, cmap="plasma", norm=norm)
    lc.set_array(t_idx)      # color by index
    lc.set_linewidth(1.5)

    if isTraj:
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
    
    ax.set_aspect("equal",adjustable="datalim")
    ax.add_collection(lc)
    ax.autoscale()
    ax.autoscale_view()


def one_traj_display(traj,working_system):
    layout = [
        ["traj","traj","phase","phase"],
        ["traj","traj","phase","phase"],
        ["traj","traj","phase","phase"],
        ["energy","energy","energy","energy"]
    ]
    fig, axes = plt.subplot_mosaic(layout, figsize=(12, 6),constrained_layout=True)
    plot_on_ax(axes["traj"],traj,working_system,isTraj=True)
