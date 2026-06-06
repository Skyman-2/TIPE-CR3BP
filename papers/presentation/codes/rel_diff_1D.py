def difference_relatif_1D(ref, donnees, pas):
    relatif = []
    t = 0
    if (len(ref) != len(donnees)):
        print("Erreur : les donnees et la reference n'ont pas la meme longueur.")
        return [[0,0]]
    for i in range(len(donnees)):
        if (ref[i][1] == 0):
            print("Erreur : division par 0.")
            relatif.append([ref[i][0],0])
        else:
            relatif.append([ref[i][0],(donnees[i][1]-ref[i][1])/ref[i][1]])
        t += pas
    return relatif