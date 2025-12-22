import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import PowerNorm
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (needed for 3D plotting)
import vector

# Your constants and setup unchanged
G = 1
M = 1
S = 10
d = 1.0
W = np.sqrt(G * (S + M) / d**3)

x = np.linspace(-1.5, 2.5, 200)
y = np.linspace(-1.5, 1.5, 200)
X, Y = np.meshgrid(x, y)

sun_dist = d * M / (S + M)

earth_pos = vector.obj(x=d - sun_dist, y=0.0)
sun_pos = vector.obj(x=-sun_dist, y=0.0)

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

vmin = np.percentile(potential, 1)
vmax = np.percentile(potential, 99)

# Plotting 3D surface
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Normalize the colors using PowerNorm like your contour
norm = PowerNorm(gamma=0.8, vmin=vmin, vmax=vmax)
colors = plt.cm.plasma(norm(potential))

surf = ax.plot_surface(X, Y, potential, facecolors=colors, rstride=1, cstride=1, linewidth=0, antialiased=False, shade=False)

# Add color bar (works by creating a mappable scalar)
mappable = plt.cm.ScalarMappable(norm=norm, cmap='plasma')
mappable.set_array(potential)
fig.colorbar(mappable, ax=ax, shrink=0.5, aspect=10, label='Fake Gravitational Potential')

# Mark Sun and Earth as points elevated a bit above the surface for visibility
ax.scatter(-sun_dist, 0, potential.min() - 0.1, color='yellow', s=100, label='Sun', edgecolors='k')
ax.scatter(d - sun_dist, 0, potential.min() - 0.1, color='blue', s=100, label='Earth', edgecolors='k')

ax.set_title("3D Simplified Lagrange Point Potential Surface")
ax.set_xlabel("x (normalized units)")
ax.set_ylabel("y (normalized units)")
ax.set_zlabel("Potential")

plt.legend()
plt.tight_layout()
plt.show()
