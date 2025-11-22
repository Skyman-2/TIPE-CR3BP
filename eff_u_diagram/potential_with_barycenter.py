import numpy as np
import matplotlib.pyplot as plt
import vector

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

# Earth's position
earth_pos = vector.obj(x=d, y=0.0)

# Potential field
potential = np.zeros_like(X)

# for i in range(X.shape[0]):
#     for j in range(X.shape[1]):
# Barycenter position
x_bary = M * d / (M + S)

# Vectorized distances
r_sun = np.sqrt(X**2 + Y**2) + 1e-6
r_earth = np.sqrt((X - d)**2 + Y**2) + 1e-6
r_bary = np.sqrt((X - x_bary)**2 + Y**2)


grav_potential = -G * (S / r_sun + M / r_earth)
centrifugal = 0.5 * W**2 * r_bary**2

potential = grav_potential - centrifugal  # or potential - grav_potential


# Approximate Lagrange points (in fake units)
mu = M / (S + M)
L1 = d * (1 - (mu / 3)**(1/3))
L2 = d * (1 + (mu / 3)**(1/3))
L3 = -d * (1 + 5*mu/12)
L4_x = 0.5 - mu
L4_y = np.sqrt(3) / 2
L5_x = 0.5 - mu
L5_y = -np.sqrt(3) / 2

# Plotting
fig, ax = plt.subplots(figsize=(10, 8))
cont = ax.contour(X, Y, potential, levels=2000, cmap='plasma')
plt.colorbar(cont, label='Fake Gravitational Potential')

# Mark Sun and Earth
ax.plot(0, 0, 'yo', label='Sun')
ax.plot(d, 0, 'bo', label='Earth')

# Mark Lagrange points
ax.plot(L1, 0, 'rx', label='L1')
ax.plot(L2, 0, 'gx', label='L2')
ax.plot(L3, 0, 'mx', label='L3')
ax.plot(L4_x, L4_y, 'cx', label='L4')
ax.plot(L5_x, L5_y, 'kx', label='L5')

ax.legend()
ax.set_title("Simplified Lagrange Point Visualization")
ax.set_xlabel("x (normalized units)")
ax.set_ylabel("y (normalized units)")
ax.set_aspect('equal')
plt.grid(True)
plt.tight_layout()
plt.show()


# Need to add the part for velocity dependent term