import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # not strictly needed in recent versions, but safe
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import Normalize,LightSource


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


def add_equipotential_contours(
    system,
    step=250,
    n_levels=25,
    pmin=5,
    pmax=95,
    colors="k",
    linewidths=0.5,
    alpha=0.7,
):
    """
    Ajoute des lignes d'égale potentiel Φ(x,y) sur la figure courante.

    - La fonction utilise les limites actuelles des axes (xlim, ylim)
      pour définir la zone de calcul du potentiel.
    - Elle doit être appelée APRES display_pretty_trajectory, ou plus
      généralement après la création de la figure.

    Paramètres
    ----------
    system   : dict
        Système (Earth–Moon, etc.), même format que pour total_potential.
    step     : int
        Nombre de points par axe pour la grille (résolution).
    n_levels : int
        Nombre d’équipotentielles.
    pmin,pmax : float
        Percentiles pour ignorer les valeurs extrêmes de Φ (singularités).
    colors, linewidths, alpha : style graphique.
    """

    ax = plt.gca()  # récupère les axes de la figure courante

    # Zone de calcul = limites actuelles de l'axe
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    surface = [[xmin, xmax], [ymin, ymax]]

    # Grille + potentiel
    X, Y, Z = total_potential(system, surface, step)

    # Nettoyage / clipping pour éviter que les singularités écrasent tout
    Z = np.nan_to_num(Z, nan=np.nan, posinf=np.nan, neginf=np.nan)
    vmin, vmax = np.nanpercentile(Z, [pmin, pmax])
    levels = np.linspace(vmin, vmax, n_levels)

    cs = ax.contour(
        X, Y, Z,
        levels=levels,
        colors=colors,
        linewidths=linewidths,
        alpha=alpha,
    )

    # On garde un repère isométrique pour le CR3BP
    ax.set_aspect("equal", adjustable="box")

    return cs




def plot_potential_2d_limited(system, step):
    # Compute grid + potential

    surface = [
        [-1.2*system["radius"], 1.2*system["radius"]],
        [-1.2*system["radius"], 1.2*system["radius"]]
    ]

    X, Y, Z = total_potential(system, surface, step)

    Z = np.nan_to_num(Z, nan=np.nan, posinf=np.nan, neginf=np.nan)

    # Focus on, say, the 2nd–98th percentiles (ignore the extreme outliers)
    vmin, vmax = np.nanpercentile(Z, [10, 100])

    plt.figure(figsize=(6, 5))
    plt.imshow(
        Z,
        origin="lower",
        extent=(surface[0][0], surface[0][1], surface[1][0], surface[1][1]),
        aspect="equal",
        vmin=vmin,
        vmax=vmax,
    )
    plt.colorbar(label="Potential Φ")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.tight_layout()
    plt.show()




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