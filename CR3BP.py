import numpy as np
import matplotlib.pyplot as plt



# Tableau des instants où on souhaite résoudre le système
dt = 5
t_max = 720000  # Durée totale de la simulation en secondes
t = 0
i = 0

# Constantes
G = 6.674e-11  # Constante gravitationnelle en SI
body1_mass = 5.972e24  # Masse de la Terre en kg
body2_mass = 7.348e22  # Masse de la Lune en kg
orbital_radius = 384.4e9  # Distance moyenne Terre-Lune en m

def barycentre(m1,m2,r):
    return (m2*r)/(m1+m2)

system_barycenter = barycentre(body1_mass,body2_mass,orbital_radius)
body1_pos = np.array([-1*system_barycenter, 0.])  # Position de la Terre
body2_pos = np.array([orbital_radius-system_barycenter, 0.])  # Position de la Lune
x0, y0 = 0.,0.  # Coordonnées initiales du satellite
vx0, vy0 = 0.,0.  # Vitesse initiale du satellite
omega = np.sqrt(G * (body1_mass + body2_mass) / np.linalg.norm(body1_pos - body2_pos)**3) # Vitesse angulaire du réf

# Equations du système
def distance(x,y,pPos):
    res = np.sqrt((x - pPos[0])**2 + (y - pPos[1])**2)
    return res

def body_pull_x(x,y,body_pos,mass):
    return (G*mass*(body_pos[0] - x)) / distance(x,y,body_pos)**3

def body_pull_y(x,y,body_pos,mass):
    return (G*mass*(body_pos[1] - y)) / distance(x,y,body_pos)**3

def eqx(x,y,vy,body1_pos,body2_pos):
    coriolis = 2 * omega * vy
    centrifugal = omega**2 * x
    pull1 = body_pull_x(x,y,body1_pos,body1_mass)
    pull2 = body_pull_x(x,y,body2_pos,body2_mass)
    return pull1 + pull2 + coriolis + centrifugal

def eqy(x,y,vx,body1_pos,body2_pos):
    coriolis = -2 * omega * vx
    centrifugal = omega**2 * y
    pull1 = body_pull_y(x,y,body1_pos,body1_mass)
    pull2 = body_pull_y(x,y,body2_pos,body2_mass)
    return pull1 + pull2 + coriolis + centrifugal