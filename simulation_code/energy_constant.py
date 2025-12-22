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


def energy(x,y,vx,vy,system):
    kinetic_energy = 0.5 * (vx**2 + vy**2)
    potential_energy = potential(x, y, system)
    return kinetic_energy + potential_energy


