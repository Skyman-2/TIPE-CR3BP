import numpy as np
import src.rk4 as rk4

def multiplier_coefs_par_coefs(array1,array2):
    resultat = np.array([0 for i in range(len(array1))])
    for i in range(len(array1)):
        resultat[i] = array1[i]*array2[i]
    return resultat


def ombre_variete_instable_1D(starting_state,lambda_i,dimensionalisation,temps_sim,pas,systeme,eps=1e-6):
    ci = starting_state + eps * multiplier_coefs_par_coefs(lambda_i,dimensionalisation)
    return rk4.simuler_trajectoire(ci,temps_sim,pas,systeme)

def ombre_variete_stable_1D(starting_state,lambda_s,dimensionalisation,temps_sim,pas,systeme,eps=1e-6):
    ci = starting_state + eps * multiplier_coefs_par_coefs(lambda_s,dimensionalisation)
    return rk4.simuler_trajectoire(ci,temps_sim,pas,systeme,inverse_temps=True)


def echantillonnage_variete_instable(lambda_i,dimensionalisation,temps_sim,pas,systeme,orbite_reference,echantillonage,eps=1e-6):
    variete = []
    for i in range(echantillonage):
        etat_i = orbite_reference[i*len(orbite_reference)//echantillonage]
        print(i*len(orbite_reference)//echantillonage, etat_i)
        variete.append(ombre_variete_instable_1D(etat_i,lambda_i,dimensionalisation,temps_sim,pas,systeme,eps))
    return variete

def echantillonnage_variete_stable(lambda_s,dimensionalisation,temps_sim,pas,systeme,orbite_reference,echantillonage,eps=1e-6):
    variete = []
    for i in range(echantillonage):
        etat_i = orbite_reference[i*len(orbite_reference)//echantillonage]
        print(i*len(orbite_reference)//echantillonage, etat_i)
        variete.append(ombre_variete_stable_1D(etat_i,lambda_s,dimensionalisation,temps_sim,pas,systeme,eps))
    return variete