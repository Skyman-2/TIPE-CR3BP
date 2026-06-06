def tau(systeme,nu):
    x_L1 = dich.dichotomie(0, systeme["rayon"], precision=1, systeme=systeme, pas=10)
    return (-1)*(nu**2 - Ubar_xx_sans_m(x_L1,0,systeme))/(2*po.omega(systeme) * nu)

def sigma(systeme, lambdavp):
    x_L1 = dich.dichotomie(0, systeme["rayon"], precision=1, systeme=systeme, pas=10)
    return (-1)*(lambdavp**2 - Ubar_xx_sans_m(x_L1,0,systeme))/(2*po.omega(systeme) * lambdavp)