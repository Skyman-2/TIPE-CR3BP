# coding: utf8
# JCG
# 09 Avril 2020
import numpy as np
import matplotlib.pyplot as plt

#Constantes
MT=5.972e24 # kg
RT=6.371e6   # m
G=6.674e-11 # SI
V0=7.9e3#m/s
C=RT*V0
h=0.5e6   # m
print,MT,RT,G,V0,C,h

# equation differentielle selon ux
def eqx(x,y):
    r=np.sqrt(x**2+y**2)
    dvxdt=-G*MT*x/(r**3)
    return dvxdt
    
# equation differentielle selon uy
def eqy(x,y):
    r=np.sqrt(x**2+y**2)
    dvydt=-G*MT*y/(r**3)
    return dvydt
    
#condition initiales
X0=0
Y0=RT+h
VX0=V0
VY0=0.
time=[0]
X=[X0]
Y=[Y0]
VX=[VX0]
VY=[VY0]
# tableau de temps
t,dt,tmax=0, 1,100000
#t = np.linspace(0, 100000., 10000001)
#dt
xkm=[X0/1000.]
ykm=[Y0/1000.]

print,X,Y,VX,VY

#implementation RK
i=0
while t < tmax:
    time.append(round(t,2))
    kx1=VX[i]*dt
    ky1=dt*VY[i]
    kvx1=dt*eqx(X[i],Y[i])
    kvy1=dt*eqy(X[i],Y[i])
    
    kx2=dt*(VX[i]+kvx1/2.)
    ky2=dt*(VY[i]+kvy1/2.)
    kvx2=dt*eqx(X[i]+kx1/2.,Y[i]+ky1/2.)
    kvy2=dt*eqy(X[i]+kx1/2.,Y[i]+ky1/2.)

    kx3=dt*(VX[i]+kvx2/2.)
    ky3=dt*(VY[i]+kvy2/2.)
    kvx3=dt*eqx(X[i]+kx2/2.,Y[i]+ky2/2.)
    kvy3=dt*eqy(X[i]+kx2/2.,Y[i]+ky2/2.)

    kx4=dt*(VX[i]+kvx3/2.)
    ky4=dt*(VY[i]+kvy3/2.)
    kvx4=dt*eqx(X[i]+kx3/2.,Y[i]+ky3/2.)
    kvy4=dt*eqy(X[i]+kx3/2.,Y[i]+ky3/2.)

    
#    print,(ky1+2.*ky2+2.*ky3+ky4)/6.   
    X.append(X[i]+(kx1+2.*kx2+2.*kx3+kx4)/6.)
    Y.append(Y[i]+(ky1+2.*ky2+2.*ky3+ky4)/6.)
    VX.append(VX[i]+(kvx1+2.*kvx2+2.*kvx3+kvx4)/6.)
    VY.append(VY[i]+(kvy1+2.*kvy2+2.*kvy3+kvy4)/6.)
    i=i+1
    theta=np.arctan(Y[i]/X[i])
    xkm.append(X[i]/1000.)
    ykm.append(Y[i]/1000.)
    r=np.sqrt(X[i-1]**2+Y[i-1]**2)
    if(abs(r-RT)<=h/4.5):
        cas='1'
        break
    theta=np.arctan(-Y[i]/X[i])
    t=t+dt
    if((i-1)>=1000 and abs(theta+np.pi/2)<0.1 and Y[i]>0):
        cas='2'
        break

#verif
print,theta,t,X[-1],VX[-1],Y[-1],VY[-1],r,RT,cas


plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.xlabel('$X$ (km)')
plt.ylabel('$Y$ (km)')
#plt.xlim([-100,100.])
#plt.ylim([Y0/1000.-30.,Y0/1000.+30.])

tt=np.arange(0,100,0.1)
plt.axis([-10000, 10000, -10000, 10000])
plt.grid()
plt.plot(RT/1000.*np.cos(tt),RT/1000.*np.sin(tt),color='red')
plt.plot(xkm,ykm,color='blue')

plt.show()
