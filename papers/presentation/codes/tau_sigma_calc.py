def tau(system,nu):
    x_L1 = dich.dichotomy(0, system["radius"], precision=1, system=system, step=10)
    return (-1)*(nu**2 - Ubar_xx_wo_m(x_L1,0,system))/(2*po.omega(system) * nu)

def sigma(system, lambdavp):
    x_L1 = dich.dichotomy(0, system["radius"], precision=1, system=system, step=10)
    return (-1)*(lambdavp**2 - Ubar_xx_wo_m(x_L1,0,system))/(2*po.omega(system) * lambdavp)