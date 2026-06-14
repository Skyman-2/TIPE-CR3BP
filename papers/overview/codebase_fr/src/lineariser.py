import src.superposition_potentielle as po
import numpy as np
import src.dichotomie as dich
G = 6.674e-11  # Constante gravitationnelle en SI

def r1(x,y,systeme):
    return np.sqrt((x+systeme["barycentre"])**2 + y**2)

def r2(x,y,systeme):
    return np.sqrt((x-(systeme["rayon"]-systeme["barycentre"]))**2 + y**2)

def Ubar_xx_sans_m(x,y,systeme):
    terme1 = -po.omega(systeme)**2
    terme2 = G*systeme["corps1"]["masse"]*((r1(x,y,systeme))**2-3*(x+systeme["barycentre"])**2)/(r1(x,y,systeme)**5)
    terme3 = G*systeme["corps2"]["masse"]*((r2(x,y,systeme))**2-3*(x-systeme["rayon"]+systeme["barycentre"])**2)/(r2(x,y,systeme)**5)
    return terme1 + terme2 + terme3

def Ubar_xy_sans_m(x,y,systeme):
    terme1 = (systeme["corps1"]["masse"]*(x+systeme["barycentre"]))*y/(r1(x,y,systeme)**5)
    terme2 = (systeme["corps2"]["masse"]*(x-systeme["rayon"]+systeme["barycentre"]))*y/(r2(x,y,systeme)**5)
    return -3*G*(terme1 + terme2)

def Ubar_yy_sans_m(x,y,systeme):
    terme1 = -po.omega(systeme)**2
    terme2 = G*systeme["corps1"]["masse"]*((r1(x,y,systeme))**2-3*y**2)/(r1(x,y,systeme)**5)
    terme3 = G*systeme["corps2"]["masse"]*((r2(x,y,systeme))**2-3*y**2)/(r2(x,y,systeme)**5)
    return terme1 + terme2 + terme3


# N.B. : orbit is a 4D vector of the form [x,y,vx,vy]
# renvoie A_state le linéarisé en la position state
def systeme_linearise(state,systeme_actif):
    x,y,vx,vy = state
    return np.array([
        [0,0,1,0],
        [0,0,0,1],
        [(-1)*Ubar_xx_sans_m(x,y,systeme_actif),(-1)*Ubar_xy_sans_m(x,y,systeme_actif),0,2*po.omega(systeme_actif)],
        [(-1)*Ubar_xy_sans_m(x,y,systeme_actif),(-1)*Ubar_yy_sans_m(x,y,systeme_actif),-2*po.omega(systeme_actif),0]
    ])

# derivee : renvoie la liste des A_i où A_i est le linéarisé en la position gamma_i
def derivee(orbit,systeme):
    linearized_map = []
    for i in range(len(orbit)):
        linearized_map.append(systeme_linearise(orbit[i],systeme))
    return linearized_map





def valeurs_propres_L1(systeme):
    x_L1 = dich.dichotomie(0, systeme["rayon"], precision=1, systeme=systeme, pas=10)
    A = systeme_linearise([x_L1, 0, 0, 0],systeme)
    return np.linalg.eigvals(A)

def tau(systeme,nu):
    x_L1 = dich.dichotomie(0, systeme["rayon"], precision=1, systeme=systeme, pas=10)
    return (-1)*(nu**2 - Ubar_xx_sans_m(x_L1,0,systeme))/(2*po.omega(systeme) * nu)

def sigma(systeme, lambdavp):
    x_L1 = dich.dichotomie(0, systeme["rayon"], precision=1, systeme=systeme, pas=10)
    return (-1)*(lambdavp**2 - Ubar_xx_sans_m(x_L1,0,systeme))/(2*po.omega(systeme) * lambdavp)