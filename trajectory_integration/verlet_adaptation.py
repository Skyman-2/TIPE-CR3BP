import numpy as np
import time

# Numerical calculations
def simulate_trajectory(initial_conditions,simulation_time,step,system):

    # Tableau des instants où on souhaite résoudre le système
    dt = step
    t_max = simulation_time  # Durée totale de la simulation en secondes
    t = 0
    i = 0

    # Constantes
    G = 6.674e-11  # Constante gravitationnelle en SI
    body1_mass = system["body1"]["mass"]  # Masse de la Terre en kg
    body2_mass = system["body2"]["mass"]  # Masse de la Lune en kg
    orbital_radius = system["radius"]  # Distance moyenne Terre-Lune en m

    system_barycenter = system["barycenter"]
    body1_pos = np.array([-1*system_barycenter, 0.])  # Position du corps 1
    body1_radius = system["body1"]["radius"]  # Rayon du corps 1
    body2_pos = np.array([orbital_radius-system_barycenter, 0.])  # Position du corps 2
    body2_radius = system["body2"]["radius"]  # Rayon du corps 2
    omega = np.sqrt(G * (body1_mass + body2_mass) / np.linalg.norm(body1_pos - body2_pos)**3) # 3e loi de Kepler
    x0,y0,vx0,vy0 = initial_conditions

    print(system_barycenter)
    print(body1_pos)
    print(body2_pos)

    # Equations du système
    def distance(x,y,pPos):
        res = np.sqrt((x - pPos[0])**2 + (y - pPos[1])**2)
        return res

    def body_pull_x(x,y,body_pos,mass):
        return (G*mass*(body_pos[0] - x)) / distance(x,y,body_pos)**3

    def body_pull_y(x,y,body_pos,mass):
        return (G*mass*(body_pos[1] - y)) / distance(x,y,body_pos)**3

    def eqx(x,y,vy):
        coriolis = 2 * omega * vy
        centrifugal = omega**2 * x
        pull1 = body_pull_x(x,y,body1_pos,body1_mass)
        pull2 = body_pull_x(x,y,body2_pos,body2_mass)
        return pull1 + pull2 + coriolis + centrifugal

    def eqy(x,y,vx):
        coriolis = -2 * omega * vx
        centrifugal = omega**2 * y
        pull1 = body_pull_y(x,y,body1_pos,body1_mass)
        pull2 = body_pull_y(x,y,body2_pos,body2_mass)
        return pull1 + pull2 + coriolis + centrifugal

    def verlet_step(P,V):
        return [eqx(P[0],P[1],V[1]), eqy(P[0],P[1],V[0])]


    P = [np.array([x0,y0])]
    V = [np.array([vx0,vy0])]


    # Calculateur de temps restant (ChatGPT)
    steps_total = int(t_max / dt)
    block_size = 200          # mesure toutes les 200 itérations
    block_start = time.perf_counter()
    block_steps_done = 0
    avg_wall_per_step = None
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
        kvx1 = eqx(P[i][0],P[i][1],V[i][1]) * dt
        kvy1 = eqy(P[i][0],P[i][1],V[i][0]) * dt

        # Midpoints
        x_mid = P[i][0] + kx1/2.
        y_mid = P[i][1] + ky1/2.
        vx_mid = V[i][0] + kvx1/2.
        vy_mid = V[i][1] + kvy1/2.

        kvx2 = eqx(x_mid,y_mid,vy_mid) * dt
        kvy2 = eqy(x_mid,y_mid,vx_mid) * dt

        VX = V[i][0] + kvx2
        VY = V[i][1] + kvy2

        V.append(V[i] + 0.5*dt*(np.array(verlet_step(P[i],V[i])) + np.array(verlet_step(P[i+1],np.array([VX,VY])))))


        # Calculateur de temps restant (ChatGPT)
        block_steps_done += 1
        if block_steps_done == block_size:
            now = time.perf_counter()
            block_wall = now - block_start
            wall_per_step = block_wall / block_size
            if avg_wall_per_step is None:
                avg_wall_per_step = wall_per_step
            else:
                avg_wall_per_step = (1 - alpha) * avg_wall_per_step + alpha * wall_per_step
            block_start = now
            block_steps_done = 0
            steps_done = int(t / dt)
            steps_left = max(steps_total - steps_done, 0)
            remaining_calc_time = steps_left * avg_wall_per_step  # secondes
            if remaining_calc_time < 60:
                print(f"{100*steps_done/steps_total:6.2f}% | restant ≈ {remaining_calc_time:5.1f} s  ", end="\r")
            else:
                print(f"{100*steps_done/steps_total:6.2f}% | restant ≈ {remaining_calc_time/60:5.2f} min", end="\r")

        i += 1

    print("Simulation complete. Number of steps:", len(P))
    return P
