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



### 3D ATTEMPTS 

def distance(x,y,pPos):
    res = np.sqrt((x - pPos[0])**2 + (y - pPos[1])**2)
    return res

def potential(x,y,system):
    G = 6.674e-11  # Constante gravitationnelle en SI
    body1_mass = system["body1"]["mass"]  # Masse de la Terre en kg
    body1_pos = np.array([-1*system["barycenter"], 0.])  # Position du corps 1
    body2_mass = system["body2"]["mass"]  # Masse de la Lune en kg
    body2_pos = np.array([system["radius"]-system["barycenter"], 0.])  # Position du corps 2
    omega = np.sqrt(G * (body1_mass + body2_mass) / np.linalg.norm(body1_pos - body2_pos)**3) # 3e loi de Kepler
    orbital_radius = system["radius"]  # Distance moyenne Terre-Lune en m

    grav_potential_body1 = -1 * G*body1_mass/(distance(x,y,body1_pos))
    grav_potential_body2 = -1 * G*body2_mass/(distance(x,y,body2_pos))

    centrifugal_potential = -0.5 * omega**2*(x**2+y**2)

    result = grav_potential_body1 + grav_potential_body2 + centrifugal_potential

    return result


def total_potential(system,surface,step):
    x = np.linspace(surface[0][0], surface[0][1], step)
    y = np.linspace(surface[1][0], surface[1][1], step)

    X,Y = np.meshgrid(x,y)

    Z = potential(X,Y,system)

    return (X,Y,Z)


def plot_potential_3d_limited(system, step, pmin=2, pmax=100):

    surface = [
        [-1.8*system["radius"], 1.8*system["radius"]],
        [-1.8*system["radius"], 1.8*system["radius"]]
    ]

    # Compute grid and potential
    X, Y, Z = total_potential(system, surface, step)

    # Clean infinities if any
    Z = np.nan_to_num(Z, nan=np.nan, posinf=np.nan, neginf=np.nan)

    # Choose a "reasonable" Z window based on percentiles
    vmin, vmax = np.nanpercentile(Z, [pmin, pmax])

    # Clip Z for plotting (this avoids huge spikes near singularities)
    Z_plot = np.clip(Z, vmin, vmax)

    # 3D figure
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")

    # Surface (you can adjust rstride/cstride to trade detail vs speed)
    surf = ax.plot_surface(
        X, Y, Z_plot,
        rstride=2,
        cstride=2,
        linewidth=0,
        antialiased=True,
    )

    # Colorbar
    fig.colorbar(surf, shrink=0.6, aspect=12, label="Φ(x, y) (clipped)")

    # Axes labels
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("Φ(x, y)")

    # Limit z-axis to the same clipped range
    ax.set_zlim(vmin, vmax)

    plt.tight_layout()
    plt.show()




def plot_potential_3d_opaque(system, step, pmin=20, pmax=100):
    surface = [
        [-1.8*system["radius"], 1.8*system["radius"]],
        [-1.8*system["radius"], 1.8*system["radius"]]
    ]

    X, Y, Z = total_potential(system, surface, step)

    # Remove inf values
    Z = np.nan_to_num(Z, nan=np.nan, posinf=np.nan, neginf=np.nan)

    # Clip the potential to a reasonable window
    vmin, vmax = np.nanpercentile(Z, [pmin, pmax])
    Z_plot = np.clip(Z, vmin, vmax)

    # Center colormap on middle of clipped region (visually clearer)
    mid = 0.5 * (vmin + vmax)
    norm = Normalize(vmin=vmin, vmax=vmax, clip=True)

    # --- 3D FIGURE ---
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(
        X, Y, Z_plot,
        cmap='terrain',        # or 'inferno' for strong contrast
        norm=norm,
        rstride=1, cstride=1,
        linewidth=0,
        antialiased=False,
        shade=True,            # <--- IMPORTANT: shading ON
        alpha=1.0,             # <--- FULL OPACITY, no see-through
        edgecolor='none'       # <--- No transparent grid
    )

    # Colorbar
    fig.colorbar(surf, shrink=0.55, aspect=12, label="Φ (clipped)")

    # Axis labels
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("Φ")

    # Ensure z-limits match clipping
    ax.set_zlim(vmin, vmax)

    plt.tight_layout()
    plt.show()




def plot_potential_3d_shaded(system, step,
                             pmin=2, pmax=100, base_color=(0.75, 0.80, 0.90)):

    surface = [
        [-1.8*system["radius"], 1.8*system["radius"]],
        [-1.8*system["radius"], 1.8*system["radius"]]
    ]

    # Compute grid and potential
    X, Y, Z = total_potential(system, surface, step)

    # Clean invalid numbers
    Z = np.nan_to_num(Z, nan=np.nan, posinf=np.nan, neginf=np.nan)

    # Clip extremes in Z to avoid singularities dominating the plot
    vmin, vmax = np.nanpercentile(Z, [pmin, pmax])
    Z_plot = np.clip(Z, vmin, vmax)

    # Build a uniform RGB base color array of shape (Ny, Nx, 3)
    ny, nx = Z_plot.shape
    base = np.zeros((ny, nx, 3), dtype=float)
    base[..., 0] = base_color[0]
    base[..., 1] = base_color[1]
    base[..., 2] = base_color[2]

    # Light source
    ls = LightSource(azdeg=120, altdeg=10)

    # Apply shading to the uniform base color using the height map Z_plot
    rgb = ls.shade_rgb(base, Z_plot)  # shape (Ny, Nx, 3)

    # --- Plot ---
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(
        X, Y, Z_plot,
        facecolors=rgb,
        rstride=1, cstride=1,
        linewidth=0,
        antialiased=False
    )

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("Φ")
    ax.set_zlim(vmin, vmax)

    plt.tight_layout()
    plt.show()