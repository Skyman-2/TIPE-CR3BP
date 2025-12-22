import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize


# Display utilities
def flow_space_diag(traj,ax,title="First"):
    abs_pos = []
    abs_vel = []
    for i in range(len(traj)):
        x = traj[i][0]
        y = traj[i][1]
        vx = traj[i][2]
        vy = traj[i][3]
        abs_pos.append(np.sqrt(x**2 + y**2))
        abs_vel.append(np.sqrt(vx**2 + vy**2))
        # Build segments for LineCollection

    points = np.array([abs_pos, abs_vel]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Colors mapped to time index (0 -> start, 1 -> end)
    t_idx = np.arange(len(abs_pos))
    norm = Normalize(t_idx.min(), t_idx.max())
    lc = LineCollection(segments, cmap="plasma", norm=norm)
    lc.set_array(t_idx)      # color by index
    lc.set_linewidth(1.5)

    ax.set_aspect("equal", "box")
    ax.add_collection(lc)

    ax.set_xlim(-max(abs_pos), max(abs_pos))
    ax.set_ylim(-max(abs_vel), max(abs_vel))
    plt.xlabel("Position absolue (m)")
    plt.ylabel("Vitesse absolue (m/s)")
    plt.title(title)
    plt.grid()
    plt.show()

