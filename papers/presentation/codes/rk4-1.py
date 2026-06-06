def simuler_trajectoire(conditions_initiales,temps_simulation,pas,systeme,inverse_temps=False):
    if inverse_temps:
        pas = -pas
        temps_simulation = -temps_simulation
    dt = pas
    t_max = temps_simulation
    t = 0
    def equation_x(x,y,vy):
        coriolis = 2 * omega * vy
        centrifuge = omega**2 * x
        traction1 = traction_corps_x(x,y,position_corps1,masse_corps1)
        traction2 = traction_corps_x(x,y,position_corps2,masse_corps2)
        return traction1 + traction2 + coriolis + centrifuge
    def equation_y(x,y,vx):
        coriolis = -2 * omega * vx
        centrifuge = omega**2 * y
        traction1 = traction_corps_y(x,y,position_corps1,masse_corps1)
        traction2 = traction_corps_y(x,y,position_corps2,masse_corps2)
        return traction1 + traction2 + coriolis + centrifuge