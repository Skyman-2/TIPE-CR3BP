def systeme_linearise(state,systeme_actif):
    x,y,vx,vy = state
    return np.array([
        [0,0,1,0],
        [0,0,0,1],
        [(-1)*Ubar_xx_sans_m(x,y,systeme_actif),(-1)*Ubar_xy_sans_m(x,y,systeme_actif),0,2*po.omega(systeme_actif)],
        [(-1)*Ubar_xy_sans_m(x,y,systeme_actif),(-1)*Ubar_yy_sans_m(x,y,systeme_actif),-2*po.omega(systeme_actif),0]
    ])


def derivee(orbit,systeme):
    linearized_map = []
    for i in range(len(orbit)):
        linearized_map.append(systeme_linearise(orbit[i],systeme))
    return linearized_map