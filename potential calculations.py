import matplotlib.pyplot as plt
import numpy as np
import math

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

def normeSubPolarVectors(r,theta,s,phi):
    return np.sqrt( (r*np.cos(theta) - s*np.cos(phi))**2 + (r*np.sin(theta) - s*np.sin(phi))**2 )

# Create the mesh in polar coordinates and compute corresponding Z.

G = 6.67*10**(-11)
S = 1.989*10**30
T = 5.97*10**24
m = 1
STDist = 150.92*10**9   # Distance Terre-Soleil
W = math.sqrt(G*(S+T)/STDist**3)
r2 = 150*10**9
r1 = 0.92*10**9


r = np.linspace(0, 3000000000, 50)
p = np.linspace(0, 2*np.pi, 50)
R, P = np.meshgrid(r, p)
# Z = (0.5*m*(W**2)*(R**2))
Z = ((-1)*G*m*(S/normeSubPolarVectors(R,P,r1,3.14)) - 0.5*m*(R**2)*(W**2))

# Express the mesh in the cartesian system.
X, Y = R*np.cos(P), R*np.sin(P)

# Plot the surface.
ax.plot_surface(X, Y, Z, cmap=plt.cm.viridis)

# Tweak the limits and add latex math labels.
# ax.set_zlim(0, 1)
ax.set_xlabel("X axis")
ax.set_ylabel("Y axis")
ax.set_zlabel("Potential")

plt.show()