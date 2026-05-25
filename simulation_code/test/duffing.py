import matplotlib.pyplot as plt
import numpy as np


eps = 0.1

def F(x):
    return -x - eps*x**3

def simulate_duffing(ci,t_max,dt):
    t = np.arange(0,t_max,dt)
    t_current = 0
    traj = [ci]

    for i in range(len(t)-1):
        print(t_current/t_max,end="\r")
        t_current += dt
        x = traj[i][0]
        x_dot = traj[i][1]

        kx1 = x_dot * dt
        kv1 = F(x) * dt

        # Midpoints
        x_mid = traj[i][0] + kx1/2.
        vx_mid = traj[i][1] + kv1/2.

        # Better Guess
        kx2 = vx_mid * dt
        kv2 = F(x_mid) * dt

        # Trajectory
        X = traj[i][0] + kx2
        VX = traj[i][1] + kv2

        traj.append([X,VX])

    return traj

def flot_duffing(t,ci,dt=0.01):
    traj = simulate_duffing(ci,t,dt)
    return {"ci": ci, "flot":traj[-1], "traj": traj}


def display_trajs(flots):
    for flot in flots:
        x_vals = [point[0] for point in flot["traj"]]
        x_dot_vals = [point[1] for point in flot["traj"]]
        plt.plot(x_vals, x_dot_vals,linewidth=5,color="blue",alpha=0.5)
        plt.plot(flot["ci"][0], flot["ci"][1], marker='o', markersize=16, color="orange")  # Point de départ
        plt.plot(flot["flot"][0], flot["flot"][1], marker='o', markersize=16, color="darkgreen") # Flot à l'instant final
        plt.plot()
    plt.xlabel('x')
    plt.ylabel("x point")
    plt.title("Espace de phase de l'oscillateur de Duffing (unités arbitraires)")
    plt.show()


def draw_flot_oh(x_bounds=1, x_sampling=10, v_bounds=1, v_sampling=10):
    trajs = []
    x_0s = np.linspace(0, x_bounds, x_sampling)
    x_dot_0s = np.linspace(4, v_bounds, v_sampling)
    for x_0 in x_0s:
        for x_dot_0 in x_dot_0s:
            trajs.append(flot_duffing(4.3,[x_0, x_dot_0]))
    return trajs

display_trajs(draw_flot_oh(1,1,5,2))