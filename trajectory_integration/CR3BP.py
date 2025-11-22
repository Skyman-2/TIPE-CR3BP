import numpy as np
import matplotlib.pyplot as plt

# Tableau des instants où on souhaite résoudre le système
dt = 5
t_max = 720000  # Durée totale de la simulation en secondes
t = 0
i = 0

# Constantes
G = 6.674e-11  # Constante gravitationnelle en SI
body1_mass = 5.972e24  # Masse de la Terre en kg
body2_mass = 7.348e22  # Masse de la Lune en kg
orbital_radius = 384.4e6  # Distance moyenne Terre-Lune en m

def barycentre(m1,m2,r):
    return (m2*r)/(m1+m2)

system_barycenter = barycentre(body1_mass,body2_mass,orbital_radius)
body1_pos = np.array([-1*system_barycenter, 0.])  # Position de la Terre
body1_radius = 6.371e6  # Rayon de la Terre m
body2_pos = np.array([orbital_radius-system_barycenter, 0.])  # Position de la Lune
body2_radius = 1.737e6  # Rayon de la Lune m
x0, y0 = 7e6,0.  # Coordonnées initiales du satellite
vx0, vy0 = 0.,8e3  # Vitesse initiale du satellite
omega = np.sqrt(G * (body1_mass + body2_mass) / np.linalg.norm(body1_pos - body2_pos)**3) # Vitesse angulaire du réf avec 3e loi de Kepler

print(system_barycenter)
print(body1_pos)
print(body2_pos)


# Equations du système
def distance(x,y,pPos):
    res = np.sqrt((x - pPos[0])**2 + (y - pPos[1])**2)
    return res

def body_pull_x(x,y,body_pos,mass):
    return (G*mass*(body_pos[0] - x)) / distance(x,y,body_pos)**3

def body_pull_y(x,y,body_pos,mass):
    return (G*mass*(body_pos[1] - y)) / distance(x,y,body_pos)**3

def eqx(x,y,vy):
    coriolis = 2 * omega * vy
    centrifugal = omega**2 * x
    pull1 = body_pull_x(x,y,body1_pos,body1_mass)
    pull2 = body_pull_x(x,y,body2_pos,body2_mass)
    return pull1 + pull2 #+ coriolis + centrifugal

def eqy(x,y,vx):
    coriolis = -2 * omega * vx
    centrifugal = omega**2 * y
    pull1 = body_pull_y(x,y,body1_pos,body1_mass)
    pull2 = body_pull_y(x,y,body2_pos,body2_mass)
    return pull1 + pull2 #+ coriolis + centrifugal


traj = []
traj.append([x0,y0,vx0,vy0])


while t < t_max:
    t += dt

    print(t/t_max*100, "%" , end="\r")

    kx1 = traj[i][0] + traj[i][2] * dt
    ky1 = traj[i][1] + traj[i][3] * dt
    kvx1 = eqx(traj[i][0],traj[i][1],traj[i][3]) * dt
    kvy1 = eqy(traj[i][0],traj[i][1],traj[i][2]) * dt

    # kx2 = traj[i][0] + kvx1 * dt
    # ky2 = traj[i][1] + kvy1 * dt
    # kvx2 = eqx(traj[i][0]+kx1/2.,traj[i][0]+ky1/2.,traj[i][3]) * dt
    # kvy2 = eqy(traj[i][0]+kx1/2.,traj[i][0]+ky1/2.,traj[i][2]) * dt

    # X = traj[i][0] + (kx1 + kx2) / 2.
    # Y = traj[i][1] + (ky1 + ky2) / 2.
    # VX = traj[i][2] + (kvx1 + kvx2) / 2
    # VY = traj[i][3] + (kvx1 + kvx2) / 2.

    X = kx1
    Y = ky1
    VX = traj[i][2] + kvx1
    VY = traj[i][3] + kvy1

    traj.append([X, Y, VX, VY])
    i += 1

print("Simulation complete. Number of steps:", len(traj))



from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize

traj_arr = np.array(traj)   # shape (nsteps, 4)
x = traj_arr[:, 0]
y = traj_arr[:, 1]

# Build segments for LineCollection
points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# Colors mapped to time index (0 -> start, 1 -> end)
t_idx = np.arange(len(x))
norm = Normalize(t_idx.min(), t_idx.max())
lc = LineCollection(segments, cmap="plasma", norm=norm)
lc.set_array(t_idx)      # color by index
lc.set_linewidth(1.5)

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect("equal", "box")
ax.add_collection(lc)

# Bodies
ax.add_patch(plt.Circle(body1_pos, body1_radius, color="black", fill=False))
ax.add_patch(plt.Circle(body2_pos, body2_radius, color="black", fill=False))

# Limits
pad = 0.2 * orbital_radius
ax.set_xlim(body1_pos[0]-pad, body2_pos[0]+pad)
ax.set_ylim(-pad, pad)

ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")

# Colorbar = time
cbar = fig.colorbar(lc, ax=ax)
cbar.set_label("simulation step (color = time)")

plt.show()
