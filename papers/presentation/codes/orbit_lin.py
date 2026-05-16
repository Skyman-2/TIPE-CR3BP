def linearized_system(state,working_system):
    x,y,vx,vy = state
    return np.array([
        [0,0,1,0],
        [0,0,0,1],
        [(-1)*Ubar_xx_wo_m(x,y,working_system),(-1)*Ubar_xy_wo_m(x,y,working_system),0,2*po.omega(working_system)],
        [(-1)*Ubar_xy_wo_m(x,y,working_system),(-1)*Ubar_yy_wo_m(x,y,working_system),-2*po.omega(working_system),0]
    ])

# Df : renvoie la liste des A_i, A_i etant le linearise en la position gamma_i
def Df(orbit,system):
    linearized_map = []
    for i in range(len(orbit)):
        linearized_map.append(linearized_system(orbit[i],system))
    return linearized_map