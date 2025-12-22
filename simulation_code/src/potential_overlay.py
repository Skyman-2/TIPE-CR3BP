import numpy as np


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



def equipotentials(system,step,pmin,pmax):
    surface = [
        [-2*system["radius"], 2*system["radius"]],
        [-2*system["radius"], 2*system["radius"]]
    ]
    X,Y,Z = total_potential(system,surface,step)
    Z = np.nan_to_num(Z, nan=np.nan, posinf=np.nan, neginf=np.nan)
    vmin, vmax = np.nanpercentile(Z, [pmin, pmax])
    Z_plot = np.clip(Z, vmin, vmax)
    return X,Y,Z_plot