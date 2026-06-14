import numpy as np
import time

# Numerical calculations
def simuler_trajectoire(conditions_initiales,temps_simulation,pas,systeme):

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

    def verlet_step(P,V):
        return [equation_x(P[0],P[1],V[1]), equation_y(P[0],P[1],V[0])]


    P = [np.array([x0,y0])]
    V = [np.array([vx0,vy0])]


    # Calculateur de temps restant (ChatGPT)
    pas_total = int(t_max / dt)
    taille_bloc = 200          # mesure toutes les 200 itérations
    debut_bloc = time.perf_counter()
    pas_bloc_realises = 0
    moyenne_temps_par_pas = None
    alpha = 0.2               # lissage un peu plus fort (car mesures moins fréquentes)


    while t < t_max:
        t += dt

        # if (i % 1000) == 0:
        #     time.sleep(0.3)
        #     print([P[i],V[i]])
        P.append(P[i] + V[i]*dt + 0.5*np.array(verlet_step(P[i],V[i]))*dt**2)

        # Approximation de V[i+1] pour f(P[i+1],V[i+1])
        kx1 = V[i][0] * dt
        ky1 = V[i][1] * dt
        kvx1 = equation_x(P[i][0],P[i][1],V[i][1]) * dt
        kvy1 = equation_y(P[i][0],P[i][1],V[i][0]) * dt

        # Midpoints
        x_mid = P[i][0] + kx1/2.
        y_mid = P[i][1] + ky1/2.
        vx_mid = V[i][0] + kvx1/2.
        vy_mid = V[i][1] + kvy1/2.

        kvx2 = equation_x(x_mid,y_mid,vy_mid) * dt
        kvy2 = equation_y(x_mid,y_mid,vx_mid) * dt

        VX = V[i][0] + kvx2
        VY = V[i][1] + kvy2

        V.append(V[i] + 0.5*dt*(np.array(verlet_step(P[i],V[i])) + np.array(verlet_step(P[i+1],np.array([VX,VY])))))


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
        resultat.append([P[i][0],P[i][1],V[i][0],V[i][1]])
    return resultat
