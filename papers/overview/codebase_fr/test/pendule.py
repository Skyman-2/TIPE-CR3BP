import matplotlib.pyplot as plt
import numpy as np


w0 = 2
T = 2*np.pi/w0
dt = 0.01

def flot_oh(t,ci):
    A = ci[0]
    B = ci[1]/w0
    def x(t):
        return A*np.cos(w0*t) + B*np.sin(w0*t)
    def x_dot(t):
        return (-A*w0*np.sin(w0*t) + B*w0*np.cos(w0*t))
    return np.array([x(t), x_dot(t)])

def simulate_oh(ci,t_max,dt):
    t = np.arange(0,t_max,dt)
    traj = []
    for t_i in t:
        traj.append(flot_oh(t_i,ci))
    return traj

def afficher_trajectoires(trajs,flow_time=T/2):
    for traj in trajs:
        x_vals = [point[0] for point in traj]
        x_dot_vals = [point[1] for point in traj]
        plt.plot(x_vals, x_dot_vals,linewidth=5,color="blue",alpha=0.5)
        plt.plot(x_vals[0], x_dot_vals[0], marker='o', markersize=16, color="orange")  # Point de départ
        flow_display = flot_oh(flow_time, traj[0])
        plt.plot(flow_display[0], flow_display[1], marker='o', markersize=16, color="darkgreen")  # Point de l'écoulement
        plt.plot()
    plt.xlabel('x')
    plt.ylabel("x point")
    plt.title("Espace de phase de l'oscillateur harmonique (unités arbitraires)")
    plt.show()

def dessiner_flot_oh(x_bounds=1, x_sampling=10, v_bounds=1, v_sampling=10):
    trajs = []
    x_0s = np.linspace(0, x_bounds, x_sampling)
    x_dot_0s = np.linspace(1, v_bounds, v_sampling)
    for x_0 in x_0s:
        for x_dot_0 in x_dot_0s:
            trajs.append(simulate_oh([x_0, x_dot_0], T, dt))
    return trajs

afficher_trajectoires(dessiner_flot_oh(1,1,5,5),flow_time=0.41*T)