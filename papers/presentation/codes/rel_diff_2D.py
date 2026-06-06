def difference_relatif_2D(ref, donnees, pas):
    relatif = []
    t = 0
    if (len(ref) != len(donnees)):
        print("Erreur : les donnees et la reference n'ont pas la meme longueur.")
        return [[0,0]]
    for i in range(len(donnees)):
        x = donnees[i][0]-ref[i][0]
        y = donnees[i][1]-ref[i][1]
        relatif.append([t,np.sqrt(x**2+y**2)/np.sqrt(ref[i][0]**2+ref[i][1]**2)])
        t += pas
    return relatif