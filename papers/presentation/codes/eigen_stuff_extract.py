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