def etat_retour(traj, systeme_actif):
    for i in range(2, len(traj)):
        if traj[i-1][1] < 0 and traj[i][1] > 0:
            alpha = -traj[i-1][1] / (traj[i][1] - traj[i-1][1])
            return traj[i-1] + alpha * (traj[i] - traj[i-1])
    return None


def plus_proche_dans_index(liste, reference, index_considered):
    if len(liste) == 0:
        return -1
    meilleur_i = 0
    meilleur_diff = abs(liste[0][index_considered] - reference)
    for i in range(len(liste)):
        diff = abs(liste[i][index_considered] - reference)
        if diff < meilleur_diff:
            meilleur_i = i
            meilleur_diff = diff
    return meilleur_i
