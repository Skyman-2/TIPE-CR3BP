import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize


# Utilitaires d'affichage
def diag_espace_de_phase(traj):
    """
    Retourne un diagramme de l'espace de flux associé à une trajectoire
    sous la forme de deux tableaux r et v où r est la position absolue
    et v est la vitesse absolue
    """
    diag = []
    for i in range(len(traj)):
        x = traj[i][0]
        y = traj[i][1]
        vx = traj[i][2]
        vy = traj[i][3]
        pos_abs = np.sqrt(x**2 + y**2)
        vit_abs = np.sqrt(vx**2 + vy**2)
        diag.append([pos_abs,vit_abs])
    return diag

def coupe_x_espace_de_phase(traj):
    diag = []
    for i in range(len(traj)):
        x = traj[i][0]
        vx = traj[i][2]
        diag.append([x,vx])
    return diag

def coupe_y_espace_de_phase(traj):
    diag = []
    for i in range(len(traj)):
        x = traj[i][1]
        vx = traj[i][3]
        diag.append([x,vx])
    return diag