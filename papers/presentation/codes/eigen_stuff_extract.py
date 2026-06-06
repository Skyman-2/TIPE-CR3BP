def latex_formater_valeurs_propres(M):
    propM = np.linalg.eig(M)
    valpM = propM[0]
    vecpM = propM[1]

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