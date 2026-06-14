import matplotlib.pyplot as plt
import numpy as np

#Constantes
G=6.673e-11
au=1.496e11
ms=1.989e30
mt=5.972e24
w=np.sqrt(G*(ms+mt)/au**3)
q=mt/(mt+ms)
e=(q/3)**(1/3)
xt=(1-q)*au
xs=-q*au
x1=xt+au*(-e+e**2/3+e**3/9) #Abscisse de L1
x2=xt+au*(e+e**2/3-e**3/9) #Abscisse de L2
x3=au*(-1-5*q/12-1127*q**3/20736) #Abscisse de L3
x4=xs+au/2 #Abscisse de L4
y4=au*np.sqrt(3/4) #Ordonnée de L4

#Résolution par la méthode de Runge-Kutta

#Accélération
def fx(x,y,vy): #Dérivée seconde de x
    return -G*ms*(x-xs)/((x-xs)**2+y**2)**(3/2)-G*mt*(x-xt)/((x-xt)**2+y**2)**(3/2)+x*w**2+2*vy*w

def fy(x,y,vx): #Dérivée seconde de y
    return -G*ms*y/((x-xs)**2+y**2)**(3/2)-G*mt*y/((x-xt)**2+y**2)**(3/2)+y*w**2-2*vx*w

#Tableau contenant les instants pour lesquels on veut résoudre le système
t=np.linspace(0,86164*2000,10000)
Te=t[1]-t[0]

#Conditions initiales
x0,y0,vx0,vy0=x1,0,0,-0.1
etats=[[x0],[y0],[vx0],[vy0]]

for n in range(1,len(t)):
    x_n=etats[0][n-1]+Te*etats[2][n-1]
    y_n=etats[1][n-1]+Te*etats[3][n-1]
    vx_n=etats[2][n-1]+Te*fx(etats[0][n-1],etats[1][n-1],etats[3][n-1])
    vy_n=etats[3][n-1]+Te*fy(etats[0][n-1],etats[1][n-1],etats[2][n-1])

    vx_n_RK=etats[2][n-1]+Te/2*(fx(etats[0][n-1],etats[1][n-1],etats[3][n-1])+fx(x_n,y_n,vy_n))
    vy_n_RK=etats[3][n-1]+Te/2*(fy(etats[0][n-1],etats[1][n-1],etats[2][n-1])+fy(x_n,y_n,vx_n))
    x_n_RK=etats[0][n-1]+Te/2*(etats[2][n-1]+vx_n_RK)
    y_n_RK=etats[1][n-1]+Te/2*(etats[3][n-1]+vy_n_RK)
    etats[2].append(vx_n_RK)
    etats[3].append(vy_n_RK)
    etats[0].append(x_n_RK)
    etats[1].append(y_n_RK)
etats_tab=np.array(etats)
fig,ax=plt.subplots(1,2,dpi=150)
ax[0].plot(t,etats_tab[0]-x4) #Abscisse centrée au point de Lagrange
ax[0].set_xlabel("t")
ax[0].set_ylabel("x")
ax[0].set_title("Abscisse x en fonction du temps")
ax[1].plot(etats_tab[0]-x4,etats_tab[1]-y4) #Trajectoire centrée au point de Lagrange
ax[1].axis("equal")
ax[1].set_xlabel("x")
ax[1].set_ylabel("y")
ax[1].set_title("Trajectoire")
plt.show()

##Résolution par le module scipy.integrate.odeint
import scipy.integrate as sci

cond_init=[x1,y0,0.00001,0]

def f(z,tc):
    return [z[2],z[3],fx(z[0],z[1],z[3]),fy(z[0],z[1],z[2])]

sol=sci.odeint(f,cond_init,t)

fig,ax=plt.subplots(1,2,dpi=150)
ax[0].plot(t,sol[:,0])
ax[0].set_xlabel("t")
ax[0].set_ylabel("x")
ax[0].set_title("Abscisse x en fonction du temps")
ax[1].plot(sol[:,0],sol[:,1])
ax[1].axis("equal")
ax[1].set_xlabel("x")
ax[1].set_ylabel("y")
ax[1].set_title("Trajectoire")
plt.show()