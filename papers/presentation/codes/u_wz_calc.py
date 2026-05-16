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