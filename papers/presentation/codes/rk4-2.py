    P = [np.array([x0,y0])]
    V = [np.array([vx0,vy0])]

    def F(P,V):
        return np.array([eqx(P[0],P[1],V[1]), eqy(P[0],P[1],V[0])]) 
    
    while abs(t) < abs(t_max):
        t += dt
        k1 = F( P[i], V[i])
        k2 = F( P[i] + V[i] * dt/2,
                V[i] + k1 * dt/2)
        k3 = F( P[i] + (V[i]*dt/2) + (k1*(dt/2)**2),
                V[i] + (k2*dt/2))
        k4 = F( P[i] + (dt*V[i]) + (k2*dt**2/2),
                V[i] + k3*dt)
        P.append(P[i] + dt*V[i] + dt**2/6*(k1 + k2 + k3))
        V.append(V[i] + dt/6*(k1 + 2*k2 + 2*k3 + k4))
        i += 1
    return P,V