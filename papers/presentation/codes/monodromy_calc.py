def monodromy_matrix(system, gamma, dt):
    A = lin.Df(gamma,system)
    Phi = np.eye(4)
    for n in range(len(A)-1):
        A1 = A[n]
        A2 = A[n]
        A3 = A[n]
        A4 = A[n+1]
        k1 = A1 @ Phi
        k2 = A2 @ (Phi + dt*k1/2)
        k3 = A3 @ (Phi + dt*k2/2)
        k4 = A4 @ (Phi + dt*k3)
        Phi = Phi + dt*(k1 + 2*k2 + 2*k3 + k4)/6
    return Phi