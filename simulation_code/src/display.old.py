import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize





def display_pretty_trajectory(traj,system,ax,fig,display_precision=10):
    traj_arr = np.array(traj)   # shape (nsteps, 4)
    x = traj_arr[::display_precision, 0]
    y = traj_arr[::display_precision, 1]

    # Build segments for LineCollection
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Colors mapped to time index (0 -> start, 1 -> end)
    t_idx = np.arange(len(x))
    norm = Normalize(t_idx.min(), t_idx.max())
    lc = LineCollection(segments, cmap="plasma", norm=norm)
    lc.set_array(t_idx)      # color by index
    lc.set_linewidth(1.5)

    ax.set_aspect("equal", "box")
    ax.add_collection(lc)

    # Bodies
    ax.add_patch(
        plt.Circle(
            [-system["barycenter"],0], 
            system["body1"]["radius"], 
            color="black", fill=False)
        )
    ax.add_patch(
        plt.Circle(
            [system["radius"]-system["barycenter"],0], 
            system["body2"]["radius"], 
            color="black", fill=False)
        )

    # Limits
    pad = 0.5 * system["radius"]
    ax.set_xlim(-system["radius"]-pad, system["radius"]+pad)
    ax.set_ylim(-system["radius"]-pad, system["radius"]+pad)

    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")

    # Colorbar = time
    # cbar = fig.colorbar(lc, ax=ax)
    # cbar.set_label("simulation step (color = time)")