import numpy as np
import matplotlib.pyplot as plt
import vector
from matplotlib.colors import PowerNorm, LightSource

# Constantes factices
G = 1         # Constante gravitationnelle (unités arbitraires)
masse_terre = 1         # Masse de la Terre
masse_soleil = 10        # Masse du Soleil
d = 1.0       # Distance Soleil-Terre (unités arbitraires)
W = np.sqrt(G * (masse_soleil + masse_terre) / d**3)     # Vitesse de rotation

# Grille autour du système Soleil-Terre
x = np.linspace(-1.5, 2.5, 200)
y = np.linspace(-1.5, 1.5, 200)
X, Y = np.meshgrid(x, y)

sun_dist = d*masse_terre/(masse_soleil+masse_terre)

earth_pos = vector.obj(x=d-sun_dist, y=0.0)
sun_pos = vector.obj(x=-sun_dist, y=0.0)

# Champ de potentiel
potentiel = np.zeros_like(X)

potentiel_gravitationnel = np.zeros_like(X)
potentiel_centrifuge = np.zeros_like(X)

for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        r_vec = vector.obj(x=X[i, j], y=Y[i, j])
        r_earth = (r_vec - earth_pos).rho + 1e-6
        r_sun = (r_vec - sun_pos).rho + 1e-6
        potentiel_gravitationnel[i, j] = -G * (masse_soleil / r_sun + masse_terre / r_earth)
        potentiel_centrifuge[i, j] = 0.5 * W**2 * r_vec.rho**2

potentiel = potentiel_gravitationnel - potentiel_centrifuge



# norm = TwoSlopeNorm(vmin=potentiel.min(), vcenter=0, vmax=potentiel.max())

vmin = np.percentile(potentiel, 1)
vmax = np.percentile(potentiel, 99)

# Traçage
fig, ax = plt.subplots(figsize=(10, 8))
cont = ax.contour(X, Y, potentiel, levels=10000, cmap='plasma', vmin=vmin, vmax=vmax, norm=PowerNorm(gamma=0.8))
plt.colorbar(cont, label='Energie Potentielle Apparente (grandeurs arbitraires)')

# Marquer le Soleil et la Terre
ax.plot(-sun_dist, 0, 'yo', label='Soleil')
ax.plot(d-sun_dist, 0, 'bo', label='Terre')

ax.legend()
ax.set_title("Visualisation du potentiel apparent")
ax.set_xlabel("x (non-dimensionnalisé)")
ax.set_ylabel("y (non-dimensionnalisé)")
ax.set_aspect('equal')
plt.grid(True)
plt.tight_layout()
plt.show()



### ESSAIS 3D ###

def distance(x,y,pPos):
    res = np.sqrt((x - pPos[0])**2 + (y - pPos[1])**2)
    return res

def potentiel(x,y,systeme):
    G = 6.674e-11  # Constante gravitationnelle en SI
    masse_corps1 = systeme["corps1"]["masse"]  # Masse de la Terre en kg
    position_corps1 = np.array([-1*systeme["barycentre"], 0.])  # Position du corps 1
    masse_corps2 = systeme["corps2"]["masse"]  # Masse de la Lune en kg
    position_corps2 = np.array([systeme["rayon"]-systeme["barycentre"], 0.])  # Position du corps 2
    omega = np.sqrt(G * (masse_corps1 + masse_corps2) / np.linalg.norm(position_corps1 - position_corps2)**3) # 3e loi de Kepler
    rayon_orbital = systeme["rayon"]  # Distance moyenne Terre-Lune en m

    grav_potential_body1 = -1 * G*masse_corps1/(distance(x,y,position_corps1))
    grav_potential_body2 = -1 * G*masse_corps2/(distance(x,y,position_corps2))

    potentiel_centrifuge = -0.5 * omega**2*(x**2+y**2)

    resultat = grav_potential_body1 + grav_potential_body2 + potentiel_centrifuge

    return resultat


def potentiel_total(systeme,surface,pas):
    x = np.linspace(surface[0][0], surface[0][1], pas)
    y = np.linspace(surface[1][0], surface[1][1], pas)

    X,Y = np.meshgrid(x,y)

    Z = potentiel(X,Y,systeme)

    return (X,Y,Z)


def tracer_potentiel_3d_limite(systeme, pas, pmin=2, pmax=100):

    surface = [
        [-1.8*systeme["rayon"], 1.8*systeme["rayon"]],
        [-1.8*systeme["rayon"], 1.8*systeme["rayon"]]
    ]

    # Calculer la grille et le potentiel
    X, Y, Z = potentiel_total(systeme, surface, pas)

    # Nettoyer les infinis le cas échéant
    Z = np.nan_to_num(Z, nan=np.nan, posinf=np.nan, neginf=np.nan)

    # Choisir une fenêtre Z "raisonnable" basée sur des percentiles
    vmin, vmax = np.nanpercentile(Z, [pmin, pmax])

    # Limiter Z pour le tracé (évite les pics énormes près des singularités)
    Z_plot = np.clip(Z, vmin, vmax)

    # Figure 3D
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")

    # Surface (vous pouvez ajuster rstride/cstride pour échanger détail et vitesse)
    surf = ax.plot_surface(
        X, Y, Z_plot,
        rstride=2,
        cstride=2,
        linewidth=0,
        antialiased=True,
    )

    # Barre de couleurs
    fig.colorbar(surf, shrink=0.6, aspect=12, label="Φ(x, y) (tronqué)")

    # Étiquettes des axes
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("Φ(x, y)")

    # Limiter l'axe z à la même plage tronquée
    ax.set_zlim(vmin, vmax)

    plt.tight_layout()
    plt.show()




def tracer_potentiel_3d_opaque(systeme, pas, pmin=20, pmax=100):
    surface = [
        [-1.8*systeme["rayon"], 1.8*systeme["rayon"]],
        [-1.8*systeme["rayon"], 1.8*systeme["rayon"]]
    ]

    X, Y, Z = potentiel_total(systeme, surface, pas)

    # Supprimer les valeurs inf
    Z = np.nan_to_num(Z, nan=np.nan, posinf=np.nan, neginf=np.nan)

    # Limiter le potentiel à une fenêtre raisonnable
    vmin, vmax = np.nanpercentile(Z, [pmin, pmax])
    Z_plot = np.clip(Z, vmin, vmax)

    # Centrer la palette de couleurs sur le milieu de la région tronquée (plus clair visuellement)
    mid = 0.5 * (vmin + vmax)
    norm = Normalize(vmin=vmin, vmax=vmax, clip=True)

    # --- FIGURE 3D ---
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
        edgecolor='none'       # <--- No transparent grille
    )

    # Barre de couleurs
    fig.colorbar(surf, shrink=0.55, aspect=12, label="Φ (tronqué)")

    # Étiquettes des axes
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("Φ")

    # S'assurer que les limites z correspondent au découpage
    ax.set_zlim(vmin, vmax)

    plt.tight_layout()
    plt.show()




def tracer_potentiel_3d_ombrage(systeme, pas,
                             pmin=2, pmax=100, base_color=(0.75, 0.80, 0.90)):

    surface = [
        [-1.8*systeme["rayon"], 1.8*systeme["rayon"]],
        [-1.8*systeme["rayon"], 1.8*systeme["rayon"]]
    ]

    # Calculer la grille et le potentiel
    X, Y, Z = potentiel_total(systeme, surface, pas)

    # Nettoyer les nombres invalides
    Z = np.nan_to_num(Z, nan=np.nan, posinf=np.nan, neginf=np.nan)

    # Limiter les extrêmes de Z pour éviter que les singularités n'écrasent le tracé
    vmin, vmax = np.nanpercentile(Z, [pmin, pmax])
    Z_plot = np.clip(Z, vmin, vmax)

    # Construire un tableau de couleurs RGB uniforme de forme (Ny, Nx, 3)
    ny, nx = Z_plot.shape
    base = np.zeros((ny, nx, 3), dtype=float)
    base[..., 0] = base_color[0]
    base[..., 1] = base_color[1]
    base[..., 2] = base_color[2]

    # Source de lumière
    ls = LightSource(azdeg=120, altdeg=10)

    # Appliquer un ombrage à la couleur de base uniforme en utilisant la carte d'altitude Z_plot
    rgb = ls.shade_rgb(base, Z_plot)  # forme (Ny, Nx, 3)

    # --- Tracé ---
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