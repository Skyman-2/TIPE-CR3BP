import json
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path
import csv
import numpy as np

import src.verlet as vt
import src.rk as rk
import src.rk4 as rk4
import src.VFVDP as ei
import src.dichotomie as dich
import src.affichage as affichage
import src.lineariser as lin
import src.correction_orbite_lineaire as loc
import src.monodromie as mon
import src.variete as mf
import src.superposition_potentielle as po


def __init__(systeme):
    def barycentre(m1,m2,r):
        return (m2*r)/(m1+m2)
    def update_system(systeme):
        systeme["barycentre"] = barycentre(
            systeme["corps1"]["masse"],
            systeme["corps2"]["masse"],
            systeme["rayon"]
        )
    here = Path(__file__).parent
    with open(here / "systems.json", "r") as f:
        data = json.load(f)[systeme]
    update_system(data)
    return data
systeme_actif = __init__("soleil_terre")



x_L1 = dich.dichotomie(0, systeme_actif["rayon"], precision=1, systeme=systeme_actif, pas=10)

T = 14.99625e6

x_0 = 100000000
# vy0 = loc.dichotomie_vy(x_0,systeme_actif,0.0000001,init_guess_coef)
vy0 = -128.8143495396376


traj_ref = rk4.simuler_trajectoire([x_0+x_L1, 0, 0, vy0], 5*T, 1000, systeme_actif)
affichage.trajectoire_toutes_variables_dans_le_temps(
    traj_ref,
    systeme_actif,
    100,
    "plasma"
)
plt.show()


system_period = 2*np.pi/po.omega(systeme_actif)
dim = [systeme_actif["rayon"], systeme_actif["rayon"], systeme_actif["rayon"]/system_period, systeme_actif["rayon"]/system_period]
traj_periodic = rk4.simuler_trajectoire([x_0+x_L1, 0, 0, vy0], T, 100, systeme_actif)
lambda_s = np.array([-8.34e-1,5.52e-1,-4.55e-7,2.58e-7])
lambda_i = np.array([-8.34e-1,-5.52e-1,4.55e-7,2.58e-7])
sampling = 25


varietes_instables_pos = mf.echantillonnage_variete_instable(
    lambda_i,
    dim,
    1.8*T,
    100,
    systeme_actif,
    traj_periodic,
    sampling
)
varietes_instables_neg = mf.echantillonnage_variete_instable(
    (-1)*lambda_i,
    dim,
    1.5*T,
    100,
    systeme_actif,
    traj_periodic,
    sampling
)
varietes_stables_pos = mf.echantillonnage_variete_stable(
    lambda_s,
    dim,
    1.8*T,
    100,
    systeme_actif,
    traj_periodic,
    sampling
)
varietes_stables_neg = mf.echantillonnage_variete_stable(
    (-1)*lambda_s,
    dim,
    1.5*T,
    100,
    systeme_actif,
    traj_periodic,
    sampling
)


manifolds = varietes_stables_pos + varietes_stables_neg + varietes_instables_pos + varietes_instables_neg
affichage.affichage_trajectoires_empilees(manifolds,systeme_actif)
plt.show()