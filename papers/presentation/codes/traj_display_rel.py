def affichage_trajectoire_origine_relative(traj,systeme_actif,pas_temps=10,color_palette="plasma"):
    disposition = [
        ["traj","traj","rayon_relatif","rayon_relatif"],
        ["traj","traj","rayon_relatif","rayon_relatif"],
        ["energie", "energie", "energie", "energie"]
    ]
    fig, axes = plt.subplot_mosaic(disposition, figsize=(12, 6),constrained_layout=True)
    tracer_sur_ax(axes["traj"],traj,color_palette,isTraj=True)
    tracer_sur_ax_corps(axes["traj"],systeme_actif)
    tracer_potentiel(axes["traj"],systeme_actif,pmin=98,levels=50,steps=4000,alpha=0.2)
    axes["energie"].grid(True)
    tracer_sur_ax(axes["energie"],en.energie(traj,systeme_actif,pas_temps),color_palette)
    traj_origine_cte = [traj[0]+[0.1,0,0,0] for i in range(len(traj))]
    origine_rayon = en.rayon_dans_le_temps(traj_origine_cte,pas_temps)
    rayon_traj = en.rayon_dans_le_temps(traj,pas_temps)
    orbite_degenerescence = rd.difference_relative_1D(rayon_traj, origine_rayon, pas_temps)
    axes["rayon_relatif"].grid(True)
    tracer_sur_ax(axes["rayon_relatif"],orbite_degenerescence,color_palette)
    return orbite_degenerescence