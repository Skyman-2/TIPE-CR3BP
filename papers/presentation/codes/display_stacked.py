def affichage_trajectoires_empilees(trajs,systeme_actif,pas_temps=10,color_palette=[]):
    if color_palette == []:
        for i in range(len(trajs)//2):
            color_palette.append("plasma")
        for i in range(len(trajs)//2):
            color_palette.append("viridis")
    disposition = [
        ["traj","phase"]
    ]
    fig, axes = plt.subplot_mosaic(disposition, figsize=(12, 6),constrained_layout=True)
    for i in range(len(trajs)):
        tracer_sur_ax(axes["traj"],trajs[i],color_palette[i],isTraj=True)
        tracer_sur_ax(axes["phase"],trajectoire_vitesse(trajs[i]),color_palette[i],isTraj=True)
    tracer_sur_ax_corps(axes["traj"],systeme_actif)
    tracer_potentiel(axes["traj"],systeme_actif,pmin=98,levels=50,steps=4000,alpha=0.2)