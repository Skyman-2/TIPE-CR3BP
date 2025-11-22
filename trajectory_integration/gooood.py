import numpy as np
import matplotlib.pyplot as plt
import vector

# Fake physics constants
G = 1          # Gravitational constant (arbitrary units)
M = 1          # Mass of Earth
S = 10         # Mass of Sun
d = 1.0        # Distance between Sun and Earth

# Grid around Sun-Earth system
x = np.linspace(-1.5, 2.5, 200)
y = np.linspace(-1.5, 1.5, 200)
X, Y = np.meshgrid(x, y)

# Earth's position
earth_pos = vector.obj(x=d, y=0.0)

# Compute potential field
potential = np.zeros_like(X)
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        r_vec = vector.obj(x=X[i, j], y=Y[i, j])
        r_sun = r_vec.rho + 1e-6
        r_earth = (r_vec - earth_pos).rho + 1e-6
        W = np.sqrt(G * (S + M) / d**3)
        potential[i, j] = -G * (S / r_sun + M / r_earth) - 0.5 * W**2 * r_vec.rho**2

# Estimate Lagrange point positions (fake-units)
mu = M / (S + M)
L1 = d * (1 - (mu / 3)**(1/3))
L2 = d * (1 + (mu / 3)**(1/3))
L3 = -d * (1 + 5 * mu / 12)
L4_x = 0.5 - mu
L4_y =  np.sqrt(3) / 2
L5_x = 0.5 - mu
L5_y = -np.sqrt(3) / 2

# Plotting with colors
fig, ax = plt.subplots(figsize=(10, 8))
cmap = ax.pcolormesh(X, Y, potential, shading='auto', cmap='plasma')
cbar = plt.colorbar(cmap, label='Gravitational Potential (arbitrary units)')

# Mark the Sun, Earth, and Lagrange points
ax.plot(0, 0, 'yo', label='Sun')
ax.plot(d, 0, 'bo', label='Earth')
ax.plot(L1, 0, 'rx', label='L1')
ax.plot(L2, 0, 'gx', label='L2')
ax.plot(L3, 0, 'mx', label='L3')
ax.plot(L4_x, L4_y, 'cx', label='L4')
ax.plot(L5_x, L5_y, 'kx', label='L5')

# Labels and layout
ax.set_title("Color Map of Gravitational Potential (Simplified Units)")
ax.set_xlabel("x (normalized units)")
ax.set_ylabel("y (normalized units)")
ax.set_aspect('equal')
ax.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
