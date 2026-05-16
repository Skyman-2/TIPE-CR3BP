def return_state(traj):
    for i in range(2, len(traj)):
        if traj[i-1][1] < 0 and traj[i][1] > 0:
            alpha = -traj[i-1][1] / (traj[i][1] - traj[i-1][1])
            return traj[i-1] + alpha * (traj[i] - traj[i-1])
    return None

def nearest_in_index(liste, reference, index_considered):
    if len(liste) == 0:
        return -1
    best_i = 0
    best_diff = abs(liste[0][index_considered] - reference)
    for i in range(len(liste)):
        diff = abs(liste[i][index_considered] - reference)
        if diff < best_diff:
            best_i = i
            best_diff = diff
    return best_i

