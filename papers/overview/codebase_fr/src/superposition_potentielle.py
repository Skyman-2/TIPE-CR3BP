import numpy as np


def distance(x,y,pPos):
    res = np.sqrt((x - pPos[0])**2 + (y - pPos[1])**2)
    return res

def omega(systeme):
    G = 6.674e-11  # Constante gravitationnelle en SI
    masse_corps1 = systeme["corps1"]["masse"]  # Masse de la Terre en kg
    position_corps1 = np.array([-1*systeme["barycentre"], 0.])  # Position du corps 1
    masse_corps2 = systeme["corps2"]["masse"]  # Masse de la Lune en kg
    position_corps2 = np.array([systeme["rayon"]-systeme["barycentre"], 0.])  # Position du corps 2
    omega = np.sqrt(G * (masse_corps1 + masse_corps2) / np.linalg.norm(position_corps1 - position_corps2)**3) # 3e loi de Kepler
    return omega

def potentiel(x,y,systeme):
    G = 6.674e-11  # Constante gravitationnelle en SI
    masse_corps1 = systeme["corps1"]["masse"]  # Masse de la Terre en kg
    position_corps1 = np.array([-1*systeme["barycentre"], 0.])  # Position du corps 1
    masse_corps2 = systeme["corps2"]["masse"]  # Masse de la Lune en kg
    position_corps2 = np.array([systeme["rayon"]-systeme["barycentre"], 0.])  # Position du corps 2
    rayon_orbital = systeme["rayon"]  # Distance moyenne Terre-Lune en m
    grav_potential_body1 = -1 * G*masse_corps1/(distance(x,y,position_corps1))
    grav_potential_body2 = -1 * G*masse_corps2/(distance(x,y,position_corps2))
    potentiel_centrifuge = -0.5 * omega(systeme)**2*(x**2+y**2)
    resultat = grav_potential_body1 + grav_potential_body2 + potentiel_centrifuge
    return resultat


def potentiel_total(systeme,surface,pas):
    x = np.linspace(surface[0][0], surface[0][1], pas)
    y = np.linspace(surface[1][0], surface[1][1], pas)
    X,Y = np.meshgrid(x,y)
    Z = potentiel(X,Y,systeme)
    return (X,Y,Z)



def equipotentielles(systeme,pas,pmin,pmax):
    surface = [
        [-2*systeme["rayon"], 2*systeme["rayon"]],
        [-2*systeme["rayon"], 2*systeme["rayon"]]
    ]
    X,Y,Z = potentiel_total(systeme,surface,pas)
    Z = np.nan_to_num(Z, nan=np.nan, posinf=np.nan, neginf=np.nan)
    vmin, vmax = np.nanpercentile(Z, [pmin, pmax])
    Z_plot = np.clip(Z, vmin, vmax)
    return X,Y,Z_plot