import src.potential_overlay as po
import numpy as np
import src.dichotomy as dich
G = 6.674e-11  # Constante gravitationnelle en SI

def r1(x,y,system):
    return np.sqrt((x+system["barycenter"])**2 + y**2)

def r2(x,y,system):
    return np.sqrt((x-(system["radius"]-system["barycenter"]))**2 + y**2)

def Ubar_xx_wo_m(x,y,system):
    term1 = -po.omega(system)**2
    term2 = G*system["body1"]["mass"]*((r1(x,y,system))**2-3*(x+system["barycenter"])**2)/(r1(x,y,system)**5)
    term3 = G*system["body2"]["mass"]*((r2(x,y,system))**2-3*(x-system["radius"]+system["barycenter"])**2)/(r2(x,y,system)**5)
    return term1 + term2 + term3

def Ubar_xy_wo_m(x,y,system):
    term1 = (system["body1"]["mass"]*(x+system["barycenter"]))*y/(r1(x,y,system)**5)
    term2 = (system["body2"]["mass"]*(x-system["radius"]+system["barycenter"]))*y/(r2(x,y,system)**5)
    return -3*G*(term1 + term2)

def Ubar_yy_wo_m(x,y,system):
    term1 = -po.omega(system)**2
    term2 = G*system["body1"]["mass"]*((r1(x,y,system))**2-3*y**2)/(r1(x,y,system)**5)
    term3 = G*system["body2"]["mass"]*((r2(x,y,system))**2-3*y**2)/(r2(x,y,system)**5)
    return term1 + term2 + term3


# N.B. : orbit is a 4D vector of the form [x,y,vx,vy]
# renvoie A_state le linéarisé en la position state
def linearized_system(state,working_system):
    x,y,vx,vy = state
    return np.array([
        [0,0,1,0],
        [0,0,0,1],
        [(-1)*Ubar_xx_wo_m(x,y,working_system),(-1)*Ubar_xy_wo_m(x,y,working_system),0,2*po.omega(working_system)],
        [(-1)*Ubar_xy_wo_m(x,y,working_system),(-1)*Ubar_yy_wo_m(x,y,working_system),-2*po.omega(working_system),0]
    ])

# Df : renvoie la liste des A_i où A_i est le linéarisé en la position gamma_i
def Df(orbit,system):
    linearized_map = []
    for i in range(len(orbit)):
        linearized_map.append(linearized_system(orbit[i],system))
    return linearized_map





def eigenvaluesL1(system):
    x_L1 = dich.dichotomy(0, system["radius"], precision=1, system=system, step=10)
    A = linearized_system([x_L1, 0, 0, 0],system)
    return np.linalg.eigvals(A)

def tau(system,nu):
    x_L1 = dich.dichotomy(0, system["radius"], precision=1, system=system, step=10)
    return (-1)*(nu**2 - Ubar_xx_wo_m(x_L1,0,system))/(2*po.omega(system) * nu)

def sigma(system, lambdavp):
    x_L1 = dich.dichotomy(0, system["radius"], precision=1, system=system, step=10)
    return (-1)*(lambdavp**2 - Ubar_xx_wo_m(x_L1,0,system))/(2*po.omega(system) * lambdavp)