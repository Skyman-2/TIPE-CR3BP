import src.rk4 as rk4
import src.dichotomy as dich
import src.linearize as lin

import numpy as np

def monodromy_matrix(system, gamma, dt):
    A = lin.Df(gamma,system)
    Phi = np.eye(4)

    for n in range(len(A)-1):

        A1 = A[n]
        A2 = A[n]          # better: interpolate between A[n] and A[n+1]
        A3 = A[n]
        A4 = A[n+1]

        k1 = A1 @ Phi
        k2 = A2 @ (Phi + dt*k1/2)
        k3 = A3 @ (Phi + dt*k2/2)
        k4 = A4 @ (Phi + dt*k3)

        Phi = Phi + dt*(k1 + 2*k2 + 2*k3 + k4)/6

    return Phi



def latex_sci_real(x, digits=2):
    mantissa, exponent = f"{x:.{digits}e}".split("e")
    exponent = int(exponent)

    if exponent == 0:
        return mantissa

    return rf"{mantissa} \cdot 10^{{{exponent}}}"


def latex_sci(z, digits=2, tol=1e-12):
    z = complex(z)

    if abs(z.imag) < tol:
        return latex_sci_real(z.real, digits)

    if abs(z.real) < tol:
        return latex_sci_real(z.imag, digits) + r"\mathrm{i}"

    sign = "+" if z.imag >= 0 else "-"
    return (
        latex_sci_real(z.real, digits)
        + f" {sign} "
        + latex_sci_real(abs(z.imag), digits)
        + r"\mathrm{i}"
    )



def pythonMatrix_to_bmatrix(matrix):
    n = len(matrix)
    p = len(matrix[0])
    latex_code = "\\begin{bmatrix} \n"
    for i in range(n):
        for j in range(p):
            latex_code += latex_sci(matrix[i][j])
            if j != p-1:
                latex_code += " & "
        latex_code += "\\\\ \n" 
    latex_code += "\\end{bmatrix}"
    return latex_code


def latexformat_eigenstuff(M):
    eigM = np.linalg.eig(M)
    eigenvaluesM = eigM[0]
    eigenvectorsM = eigM[1]

    latex_matrix_monodromy = pythonMatrix_to_bmatrix(M)
    latex_eigen_vectors = pythonMatrix_to_bmatrix(eigenvectorsM)
    print(latex_matrix_monodromy)
    print(latex_eigen_vectors)

    latex_eigenvalues = "\{"
    for i in range(len(eigenvaluesM)):
        latex_eigenvalues += latex_sci(eigenvaluesM[i])
        if i != len(eigenvaluesM)-1:
            latex_eigenvalues += "\: , "
    latex_eigenvalues += "\}"
    print(latex_eigenvalues)

