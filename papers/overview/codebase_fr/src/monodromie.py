import src.rk4 as rk4
import src.dichotomie as dich
import src.lineariser as lin

import numpy as np

def matrice_monodromie(systeme, gamma, dt):
    A = lin.derivee(gamma,systeme)
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



def latex_sci_reel(x, digits=2):
    mantissa, exponent = f"{x:.{digits}e}".split("e")
    exponent = int(exponent)

    if exponent == 0:
        return mantissa

    return rf"{mantissa} \cdot 10^{{{exponent}}}"


def latex_sci(z, digits=2, tol=1e-12):
    z = complex(z)

    if abs(z.imag) < tol:
        return latex_sci_reel(z.real, digits)

    if abs(z.real) < tol:
        return latex_sci_reel(z.imag, digits) + r"\mathrm{i}"

    sign = "+" if z.imag >= 0 else "-"
    return (
        latex_sci_reel(z.real, digits)
        + f" {sign} "
        + latex_sci_reel(abs(z.imag), digits)
        + r"\mathrm{i}"
    )



def matrice_python_vers_bmatrix(matrix):
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


def latex_formater_valeurs_propres(M):
    eigM = np.linalg.eig(M)
    valpM = eigM[0]
    vecpM = eigM[1]

    latex_matrice_monodromie = matrice_python_vers_bmatrix(M)
    latex_matrice_vecp = matrice_python_vers_bmatrix(vecpM)
    print(latex_matrice_monodromie)
    print(latex_matrice_vecp)

    latex_valp = "\{"
    for i in range(len(valpM)):
        latex_valp += latex_sci(valpM[i])
        if i != len(valpM)-1:
            latex_valp += "\: , "
    latex_valp += "\}"
    print(latex_valp)

