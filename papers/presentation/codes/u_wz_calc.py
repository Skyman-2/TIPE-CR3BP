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