import numpy as np

### Calcul la distance entre les données relativement à la taille de la donnée de réference

def difference_relatif_1D(ref, donnees, pas):
    relatif = []
    t = 0
    if (len(ref) != len(donnees)):
        print("Erreur : les données et la référence n'ont pas la même longueur.")
        return [[0,0]]
    for i in range(len(donnees)):
        if (ref[i][1] == 0):
            print("Erreur : division par 0.")
            relatif.append([ref[i][0],0])
        else:
            relatif.append([ref[i][0],(donnees[i][1]-ref[i][1])/ref[i][1]])
        t += pas
    return relatif

def difference_relatif_2D(ref, donnees, pas):
    relatif = []
    t = 0
    if (len(ref) != len(donnees)):
        print("Erreur : les données et la référence n'ont pas la même longueur.")
        return [[0,0]]
    for i in range(len(donnees)):
        x = donnees[i][0]-ref[i][0]
        y = donnees[i][1]-ref[i][1]
        relatif.append([t,np.sqrt(x**2+y**2)/np.sqrt(ref[i][0]**2+ref[i][1]**2)])
        t += pas
    return relatif