### Code d'intégration de trajectoire

import numpy as np
import time


# Numerical calculations
def simuler_trajectoire(conditions_initiales,temps_simulation,pas,systeme,inverse_temps=False):

    if inverse_temps:
        pas = -pas
        temps_simulation = -temps_simulation

    # Tableau des instants où on souhaite résoudre le système
    dt = pas
    t_max = temps_simulation  # Durée totale de la simulation en secondes
    t = 0
    i = 0

    # Constantes
    G = 6.674e-11  # Constante gravitationnelle en SI
    masse_corps1 = systeme["corps1"]["masse"]  # Masse de la Terre en kg
    masse_corps2 = systeme["corps2"]["masse"]  # Masse de la Lune en kg
    rayon_orbital = systeme["rayon"]  # Distance moyenne Terre-Lune en m

    barycentre_systeme = systeme["barycentre"]
    position_corps1 = np.array([-1*barycentre_systeme, 0.])  # Position du corps 1
    rayon_corps1 = systeme["corps1"]["rayon"]  # Rayon du corps 1
    position_corps2 = np.array([rayon_orbital-barycentre_systeme, 0.])  # Position du corps 2
    rayon_corps2 = systeme["corps2"]["rayon"]  # Rayon du corps 2
    omega = np.sqrt(G * (masse_corps1 + masse_corps2) / np.linalg.norm(position_corps1 - position_corps2)**3) # 3e loi de Kepler
    x0,y0,vx0,vy0 = conditions_initiales

    print(barycentre_systeme)
    print(position_corps1)
    print(position_corps2)

    # Equations du système
    def distance(x,y,pPos):
        res = np.sqrt((x - pPos[0])**2 + (y - pPos[1])**2)
        return res

    def traction_corps_x(x,y,body_pos,masse):
        return (G*masse*(body_pos[0] - x)) / distance(x,y,body_pos)**3

    def traction_corps_y(x,y,body_pos,masse):
        return (G*masse*(body_pos[1] - y)) / distance(x,y,body_pos)**3

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


    P = [np.array([x0,y0])]
    V = [np.array([vx0,vy0])]

    def F(P,V):
        return np.array([equation_x(P[0],P[1],V[1]), equation_y(P[0],P[1],V[0])]) 

    # Calculateur de temps restant (ChatGPT)
    pas_total = int(t_max / dt)
    taille_bloc = 200          # mesure toutes les 200 itérations
    debut_bloc = time.perf_counter()
    pas_bloc_realises = 0
    moyenne_temps_par_pas = None
    alpha = 0.2               # lissage un peu plus fort (car mesures moins fréquentes)


    while abs(t) < abs(t_max):
        t += dt
        # print("--------")

        k1 = F(P[i], V[i])
        k2 = F(
            P[i] + V[i] * dt/2,
            V[i] + k1 * dt/2
        )
        k3 = F(
            P[i] + (V[i]*dt/2) + (k1*(dt/2)**2),
            V[i] + (k2*dt/2)
        )
        k4 = F(
            P[i] + (dt*V[i]) + (k2*dt**2/2),
            V[i] + k3*dt
        )

        P.append(P[i] + dt*V[i] + dt**2/6*(k1 + k2 + k3))
        V.append(V[i] + dt/6*(k1 + 2*k2 + 2*k3 + k4))


        # Calculateur de temps restant (ChatGPT)
        pas_bloc_realises += 1
        if pas_bloc_realises == taille_bloc:
            now = time.perf_counter()
            block_wall = now - debut_bloc
            temps_par_pas = block_wall / taille_bloc
            if moyenne_temps_par_pas is None:
                moyenne_temps_par_pas = temps_par_pas
            else:
                moyenne_temps_par_pas = (1 - alpha) * moyenne_temps_par_pas + alpha * temps_par_pas
            debut_bloc = now
            pas_bloc_realises = 0
            pas_realises = int(t / dt)
            pas_restants = max(pas_total - pas_realises, 0)
            temps_calc_restant = pas_restants * moyenne_temps_par_pas  # secondes
            if temps_calc_restant < 60:
                print(f"{100*pas_realises/pas_total:6.2f}% | restant ≈ {temps_calc_restant:5.1f} s  ", end="\r")
            else:
                print(f"{100*pas_realises/pas_total:6.2f}% | restant ≈ {temps_calc_restant/60:5.2f} min", end="\r")

        i += 1

    print("Simulation complete. Number of steps:", len(P))

    resultat = []
    for i in range(len(P)):
        resultat.append(np.array([P[i][0],P[i][1],V[i][0],V[i][1]]))
    return resultat
