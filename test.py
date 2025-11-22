import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def alkashi(r,s,theta):
    return np.sqrt( r**2 + s**2 - 2*r*s*np.cos(theta) )


def potential_energy(r,p):
    m = 1
    G = 6.67e-11
    S = 2e30
    T = 6e24
    print(alkashi(r,150e9,p), " | " , r)
    return (
        (-1)*G*m*(0*S/r + T/alkashi(r,150e9,p))
    )

# Create a grid of 3D coordinates (x, y, z)
x = np.linspace(-1e10, 1e10, 50)
y = np.linspace(-1e10, 1e10, 50)
z = np.linspace(1e6, 1e8, 5000)

X, Y, Z = np.meshgrid(x, y, z)

# Compute the radial distance (r) from the origin (0, 0, 0) for each point
R = np.sqrt(X**2 + Y**2 + Z**2)
P = np.arctan(Y/X)

# Compute the potential energy at each distance
U = potential_energy(R, P)

# --- 3D Surface Plot ---
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
surf = ax.plot_surface(X[:, :, 0], Y[:, :, 0], U[:, :, 0], cmap='viridis', edgecolor='none')

# Labels and title
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Potential Energy (J)')
ax.set_title('Surface Plot of Potential Energy in a 3D Two-Body System')

# Add color bar
# fig.colorbar(surf, label='Potential Energy (J)')

plt.show()