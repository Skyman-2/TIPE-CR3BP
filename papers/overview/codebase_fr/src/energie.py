import src.superposition_potentielle as uo

def energie(traj,systeme_actif,pas_temps):
    t = 0
    e = []
    for i in range(len(traj)):
        x = traj[i][0]
        y = traj[i][1]
        vx = traj[i][2]
        vy = traj[i][3]
        energie_potentielle = uo.potentiel(x,y,systeme_actif)
        energie_cinetique = 0.5*(vx**2 + vy**2)
        e.append([t,-2*energie_potentielle-2*energie_cinetique])
        t += pas_temps
    return e

def rayon_dans_le_temps(traj,pas_temps):
    t = 0
    r = []
    for i in range(len(traj)):
        x = traj[i][0]
        y = traj[i][1]
        r.append([t,(x**2+y**2)/1e13+4.32e6])
        t += pas_temps
    return r
