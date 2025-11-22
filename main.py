import numpy as np
import matplotlib.pyplot as plt

# Tableau des instants où on souhaite résoudre le système
dt = 5
t_max = 720000  # Durée totale de la simulation en secondes
t = 0
i = 0

# Constantes
MT=5.972e24 # kg
RT=6.371e6   # m
G=6.674e-11 # SI
x0,y0 = 5e7+6.8e6,0. # Coordonnées initiales du satellite
vx0,vy0 = 0.,9.8e3 # Vitesse initiale du satellite
xT,yT = 5e7,0 # Coordonnées de la Terre
# omega = 0 # Vitesse angulaire du réf

# Equations du système
def distance(x,y,pPos):
    res = np.sqrt((x - pPos[0])**2 + (y - pPos[1])**2)
    return res

def eqx(x,y,pPos):
    return (G*MT*(pPos[0] - x)) / distance(x,y,pPos)**3

def eqy(x,y,pPos):
    return (G*MT*(pPos[1] - y)) / distance(x,y,pPos)**3

sols = [[x0, y0, vx0, vy0]] # Conditions initiales [x0, y0, vx0, vy0]

while t <= t_max:
    t+=dt
    i+=1

    print(t/t_max*100, "%" , end="\r")
    
    x_n = sols[i-1][0] + dt * sols[i-1][2]
    y_n = sols[i-1][1] + dt * sols[i-1][3]
    ax = eqx(sols[i-1][0], sols[i-1][1],[xT,yT]) + eqx(sols[i-1][0], sols[i-1][1],[-1*xT,-1*yT]) # + eqx(sols[i-1][0], sols[i-1][1],[0,0])
    ay = eqy(sols[i-1][0], sols[i-1][1],[xT,yT]) + eqy(sols[i-1][0], sols[i-1][1],[-1*xT,-1*yT]) #à + eqy(sols[i-1][0], sols[i-1][1],[0,0])
    vx_n = sols[i-1][2] + dt * ax
    vy_n = sols[i-1][3] + dt * ay
    # print("")
    # print("Pos: ", x_n, y_n)
    # print("Speed: ", vx_n, vy_n)
    # print("Acc: ", ax, ay)
    # print("")

    # time.sleep(1)

    if distance(x_n, y_n,[-1*xT,-1*yT]) <= RT/100 or distance(x_n, y_n,[xT,yT]) <= RT/100: 
        sols = sols[:i]  # Truncate the array to the current size
        break
    
    sols.append([x_n, y_n, vx_n, vy_n])

print("Simulation complete. Number of steps:", len(sols))

# Extraction des coordonnées pour le tracé
x_coords = [sol[0] for sol in sols]
y_coords = [sol[1] for sol in sols]

# Tracé de la trajectoire
plt.figure(figsize=(8,8))
plt.axis('equal')
#plt.xlim([-100,100.])  # Limites de l'axe x
#plt.ylim([-100,100.])  # Limites de l'axe y
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.plot(x_coords, y_coords, color='blue')
ax = plt.gca()
radius = RT  # Rayon de la Terre en m
circle = plt.Circle((xT, yT), radius, color='black', fill=False)
circle2 = plt.Circle((-xT, -yT), radius, color='black', fill=False)
# circle3 = plt.Circle((0, 0), radius, color='black', fill=False)
ax.add_patch(circle)
ax.add_patch(circle2)
# ax.add_patch(circle3)
plt.show()