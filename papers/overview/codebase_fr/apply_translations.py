import re
from pathlib import Path

root = Path(r'c:\Users\yanni\Desktop\Personal Docs\Classes\translation_new')

replacements = {
    # Modules and files
    'src.dichotomie': 'src.dichotomie',
    'src.affichage': 'src.affichage',
    'src.energie': 'src.energie',
    'src.lineariser': 'src.lineariser',
    'src.correction_orbite_lineaire': 'src.correction_orbite_lineaire',
    'src.variete': 'src.variete',
    'src.monodromie': 'src.monodromie',
    'src.espace_de_phase': 'src.espace_de_phase',
    'src.affichage_potentiel': 'src.affichage_potentiel',
    'src.superposition_potentielle': 'src.superposition_potentielle',
    'src.difference_relative': 'src.difference_relative',
    # Noms de fonctions et variables
    'systeme_actif': 'systeme_actif',
    'conditions_initiales': 'conditions_initiales',
    'temps_simulation': 'temps_simulation',
    'pas': 'pas',
    'pas_temps': 'pas_temps',
    'systeme': 'systeme',
    'corps1': 'corps1',
    'corps2': 'corps2',
    'masse': 'masse',
    'rayon': 'rayon',
    'nom': 'nom',
    'terre_lune': 'terre_lune',
    'soleil_terre': 'soleil_terre',
    'masse_corps1': 'masse_corps1',
    'masse_corps2': 'masse_corps2',
    'position_corps1': 'position_corps1',
    'position_corps2': 'position_corps2',
    'rayon_corps1': 'rayon_corps1',
    'rayon_corps2': 'rayon_corps2',
    'rayon_orbital': 'rayon_orbital',
    'potentiel_gravitationnel': 'potentiel_gravitationnel',
    'potentiel_centrifuge': 'potentiel_centrifuge',
    'potentiel_total': 'potentiel_total',
    'equipotentielles': 'equipotentielles',
    'tracer_potentiel': 'tracer_potentiel',
    'affichage': 'affichage',
    'superposition_potentielle': 'superposition_potentielle',
    'affichage_potentiel': 'affichage_potentiel',
    'difference_relative': 'difference_relative',
    'espace_de_phase': 'espace_de_phase',
    'lineariser': 'lineariser',
    'correction_orbite_lineaire': 'correction_orbite_lineaire',
    'variete': 'variete',
    'monodromie': 'monodromie',
    'dichotomie': 'dichotomie',
    'energie': 'energie',
    'systeme_linearise': 'systeme_linearise',
    'valeurs_propres_L1': 'valeurs_propres_L1',
    'derivee': 'derivee',
    'Ubar_xx_sans_m': 'Ubar_xx_sans_m',
    'Ubar_xy_sans_m': 'Ubar_xy_sans_m',
    'Ubar_yy_sans_m': 'Ubar_yy_sans_m',
    'terme1': 'terme1',
    'terme2': 'terme2',
    'terme3': 'terme3',
    'estimation_orbite_lineaire_0': 'estimation_orbite_lineaire_0',
    'plus_proche_dans_index': 'plus_proche_dans_index',
    'etat_retour': 'etat_retour',
    'trouver_intervalle': 'trouver_intervalle',
    'dichotomie_vy': 'dichotomie_vy',
    'multiplier_coefs_par_coefs': 'multiplier_coefs_par_coefs',
    'ombre_variete_instable_1D': 'ombre_variete_instable_1D',
    'ombre_variete_stable_1D': 'ombre_variete_stable_1D',
    'echantillonnage_variete_instable': 'echantillonnage_variete_instable',
    'echantillonnage_variete_stable': 'echantillonnage_variete_stable',
    'orbite_reference': 'orbite_reference',
    'etat_i': 'etat_i',
    'matrice_monodromie': 'matrice_monodromie',
    'latex_sci_reel': 'latex_sci_reel',
    'matrice_python_vers_bmatrix': 'matrice_python_vers_bmatrix',
    'latex_formater_valeurs_propres': 'latex_formater_valeurs_propres',
    'diag_espace_de_phase': 'diag_espace_de_phase',
    'coupe_x_espace_de_phase': 'coupe_x_espace_de_phase',
    'coupe_y_espace_de_phase': 'coupe_y_espace_de_phase',
    'forcer_echelle_decalage': 'forcer_echelle_decalage',
    'sous_graphique_autonome': 'sous_graphique_autonome',
    'tracer_sur_ax': 'tracer_sur_ax',
    'tracer_sur_ax_corps': 'tracer_sur_ax_corps',
    'affichage_trajectoire_simple': 'affichage_trajectoire_simple',
    'comparaison_trois_trajectoires': 'comparaison_trois_trajectoires',
    'comparaison_traj_ref': 'comparaison_traj_ref',
    'affichage_trajectoires_empilees': 'affichage_trajectoires_empilees',
    'trajectoire_toutes_variables_dans_le_temps': 'trajectoire_toutes_variables_dans_le_temps',
    'trajectoire_vitesse': 'trajectoire_vitesse',
    'traj_comp': 'traj_comp',
    'traj_ref': 'traj_ref',
    'rayon_relatif': 'rayon_relatif',
    'phase_relative': 'phase_relative',
    'energie_relative': 'energie_relative',
    'phase_ref': 'phase_ref',
    'phase_comp': 'phase_comp',
    'energie_ref': 'energie_ref',
    'energie_comp': 'energie_comp',
    'rayon_ref': 'rayon_ref',
    'rayon_comp': 'rayon_comp',
    'tracer_potentiel_3d_limite': 'tracer_potentiel_3d_limite',
    'tracer_potentiel_3d_opaque': 'tracer_potentiel_3d_opaque',
    'tracer_potentiel_3d_ombrage': 'tracer_potentiel_3d_ombrage',
    'potentiel_total': 'potentiel_total',
    'potentiel': 'potentiel',
    'equipotentielles': 'equipotentielles',
    'difference_relative_1D': 'difference_relative_1D',
    'difference_relative_2D': 'difference_relative_2D',
    'simuler_trajectoire': 'simuler_trajectoire',
    'inverse_temps': 'inverse_temps',
    'distance': 'distance',
    'traction_corps_x': 'traction_corps_x',
    'traction_corps_y': 'traction_corps_y',
    'equation_x': 'equation_x',
    'equation_y': 'equation_y',
    'coriolis': 'coriolis',
    'centrifuge': 'centrifuge',
    'traction1': 'traction1',
    'traction2': 'traction2',
    'pas_total': 'pas_total',
    'taille_bloc': 'taille_bloc',
    'debut_bloc': 'debut_bloc',
    'pas_bloc_realises': 'pas_bloc_realises',
    'moyenne_temps_par_pas': 'moyenne_temps_par_pas',
    'temps_par_pas': 'temps_par_pas',
    'pas_realises': 'pas_realises',
    'pas_restants': 'pas_restants',
    'temps_calc_restant': 'temps_calc_restant',
    'etats': 'etats',
    'etats_tab': 'etats_tab',
    'tracer': 'tracer',
    'afficher_trajectoires': 'afficher_trajectoires',
    'simuler_duffing': 'simuler_duffing',
    'dessiner_flot_oh': 'dessiner_flot_oh',
    'disposition': 'disposition',
    'grille': 'grille',
    'mosaique': 'mosaique',
}

# Additional special case replacements for JSON and affichage strings
json_replacements = {
    'terre_lune': 'terre_lune',
    'soleil_terre': 'soleil_terre',
    'corps1': 'corps1',
    'corps2': 'corps2',
    'masse': 'masse',
    'rayon': 'rayon',
    'nom': 'nom',
    'Earth': 'Terre',
    'Moon': 'Lune',
    'Sun': 'Soleil',
}

# Sort by length to prevent partial replacements
sorted_replacements = sorted(replacements.items(), key=lambda x: -len(x[0]))

for path in root.rglob('*.py'):
    text = path.read_text(encoding='utf-8')
    original = text
    for old, new in sorted_replacements:
        pattern = rf'\b{re.escape(old)}\b'
        text = re.sub(pattern, new, text)
    if text != original:
        path.write_text(text, encoding='utf-8')

# Update systems.json
json_path = root / 'systems.json'
json_text = json_path.read_text(encoding='utf-8')
original = json_text
for old, new in json_replacements.items():
    json_text = re.sub(rf'\b{re.escape(old)}\b', new, json_text)
if json_text != original:
    json_path.write_text(json_text, encoding='utf-8')

# Rename files and directories
file_map = {
    root / 'src' / 'dichotomie.py': root / 'src' / 'dichotomie.py',
    root / 'src' / 'affichage.py': root / 'src' / 'affichage.py',
    root / 'src' / 'energie.py': root / 'src' / 'energie.py',
    root / 'src' / 'lineariser.py': root / 'src' / 'lineariser.py',
    root / 'src' / 'correction_orbite_lineaire.py': root / 'src' / 'correction_orbite_lineaire.py',
    root / 'src' / 'variete.py': root / 'src' / 'variete.py',
    root / 'src' / 'monodromie.py': root / 'src' / 'monodromie.py',
    root / 'src' / 'espace_de_phase.py': root / 'src' / 'espace_de_phase.py',
    root / 'src' / 'affichage_potentiel.py': root / 'src' / 'affichage_potentiel.py',
    root / 'src' / 'superposition_potentielle.py': root / 'src' / 'superposition_potentielle.py',
    root / 'src' / 'difference_relative.py': root / 'src' / 'difference_relative.py',
    root / 'test' / 'gridspec.py': root / 'test' / 'grille_spec.py',
    root / 'test' / 'mosaique.py': root / 'test' / 'mosaique.py',
}

for old_path, new_path in file_map.items():
    if old_path.exists():
        if new_path.exists():
            new_path.unlink()
        old_path.rename(new_path)
