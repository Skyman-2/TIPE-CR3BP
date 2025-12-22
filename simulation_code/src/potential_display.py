import numpy as np
import matplotlib.pyplot as plt
import vector
from matplotlib.colors import PowerNorm

# Fake constants
G = 1         # Gravitational constant (arbitrary units)
M = 1         # Mass of Earth
S = 10        # Mass of Sun
d = 1.0       # Distance from Sun to Earth (AU-like unit)
W = np.sqrt(G * (S + M) / d**3)     # Rotation speed

# Grid around the Sun-Earth system
x = np.linspace(-1.5, 2.5, 200)
y = np.linspace(-1.5, 1.5, 200)
X, Y = np.meshgrid(x, y)

sun_dist = d*M/(S+M)

earth_pos = vector.obj(x=d-sun_dist, y=0.0)
sun_pos = vector.obj(x=-sun_dist, y=0.0)

# Potential field
potential = np.zeros_like(X)

grav_potential = np.zeros_like(X)
centrifugal_potential = np.zeros_like(X)

for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        r_vec = vector.obj(x=X[i, j], y=Y[i, j])
        r_earth = (r_vec - earth_pos).rho + 1e-6
        r_sun = (r_vec - sun_pos).rho + 1e-6
        grav_potential[i, j] = -G * (S / r_sun + M / r_earth)
        centrifugal_potential[i, j] = 0.5 * W**2 * r_vec.rho**2

potential = grav_potential - centrifugal_potential



# norm = TwoSlopeNorm(vmin=potential.min(), vcenter=0, vmax=potential.max())

vmin = np.percentile(potential, 1)
vmax = np.percentile(potential, 99)

# Plotting
fig, ax = plt.subplots(figsize=(10, 8))
cont = ax.contour(X, Y, potential, levels=10000, cmap='plasma', vmin=vmin, vmax=vmax, norm=PowerNorm(gamma=0.8))
plt.colorbar(cont, label='Fake Gravitational Potential')

# Mark Sun and Earth
ax.plot(-sun_dist, 0, 'yo', label='Sun')
ax.plot(d-sun_dist, 0, 'bo', label='Earth')

ax.legend()
ax.set_title("Simplified Lagrange Point Visualization")
ax.set_xlabel("x (normalized units)")
ax.set_ylabel("y (normalized units)")
ax.set_aspect('equal')
plt.grid(True)
plt.tight_layout()
plt.show()