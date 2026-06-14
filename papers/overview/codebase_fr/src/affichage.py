import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
import src.espace_de_phase as ps
import src.superposition_potentielle as uo
import src.energie as en
import src.difference_relative as rd



### FONCTION CHATGPT POUR FORCER LE DÉCALAGE
import matplotlib.ticker as mticker

def forcer_echelle_decalage(ax):
    fmt = mticker.ScalarFormatter(useMathText=True)

    fmt.set_useOffset(True)      # force le "+4.322e6"
    fmt.set_scientific(False)    # interdit le "*10^6"

    ax.yaxis.set_major_formatter(fmt)
### FIN DU CODE CHATGPT


def sous_graphique_autonome(axes, etiquettes_graph):
    for nom, ax in axes.items():
        ax.set_title(etiquettes_graph[nom]["nom"])
        ax.set_xlabel(etiquettes_graph[nom]["xlabel"])
        ax.set_ylabel(etiquettes_graph[nom]["ylabel"])


def tracer_sur_ax(ax,graph,color_palette,display_precision=10,isTraj=False):
    traj_arr = np.array(graph)
    x = traj_arr[::display_precision, 0]
    y = traj_arr[::display_precision, 1]

    points = np.column_stack([x, y]).reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    t_idx = np.arange(len(segments))
    norm = Normalize(t_idx.min(), t_idx.max())

    lc = LineCollection(segments, cmap=color_palette, norm=norm)
    lc.set_array(t_idx)
    lc.set_linewidth(1.5)

    if isTraj:
        ax.set_aspect("equal", adjustable="datalim")

    ax.add_collection(lc)
    ax.autoscale()
    ax.autoscale_view()



def tracer_sur_ax_corps(ax,systeme_actif):
    ax.add_patch(
        plt.Circle(
            [-systeme_actif["barycentre"],0], 
            systeme_actif["corps1"]["rayon"], 
            color="black", fill=False)
        )
    ax.add_patch(
        plt.Circle(
            [systeme_actif["rayon"]-systeme_actif["barycentre"],0], 
            systeme_actif["corps2"]["rayon"], 
            color="black", fill=False)
        )


def tracer_potentiel(ax, systeme_actif, pmin=20, steps=250, levels=25,
                   colors="k", linewidths=0.5, alpha=0.7):
    # freeze current limits
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    X, Y, Z = uo.equipotentielles(systeme_actif, steps, pmin=pmin, pmax=100)
    ax.contour(
        X, Y, Z,
        levels=levels,
        colors=colors,
        linewidths=linewidths,
        alpha=alpha,
        linestyles="solid"
    )

    # restore + lock
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_autoscale_on(False)



def affichage_trajectoire_simple(traj,systeme_actif,pas_temps=10,color_palette="plasma"):
    disposition = [
        ["traj","traj","phase","phase"],
        ["traj","traj","phase","phase"],
        ["traj","traj","phase","phase"],
        ["energie","energie","energie","energie"]
    ]
    fig, axes = plt.subplot_mosaic(disposition, figsize=(12, 6),constrained_layout=True)
    
    tracer_sur_ax(axes["traj"],traj,color_palette,isTraj=True)
    tracer_sur_ax_corps(axes["traj"],systeme_actif)
    tracer_potentiel(axes["traj"],systeme_actif,pmin=30,levels=50,alpha=0.2)

    axes["phase"].grid(True)
    tracer_sur_ax(axes["phase"],trajectoire_vitesse(traj),color_palette,isTraj=True)

    axes["energie"].grid(True)
    tracer_sur_ax(axes["energie"],en.energie(traj,systeme_actif,pas_temps),color_palette)

    labels = {
        "traj": {
            "nom": "Trajectoire",
            "xlabel": "x [m]",
            "ylabel": "y [m]",
        },
        "phase": {
            "nom": "Espace des vitesses",
            "xlabel": "v_x [m/s]",
            "ylabel": "v_y [m/s]",
        },
        "energie": {
            "nom": "Énergie",
            "xlabel": "Temps [s]",
            "ylabel": "Énergie [J]",
        }
    }
    sous_graphique_autonome(axes, labels)



def comparaison_trois_trajectoires(traj1,traj2,traj3,systeme_actif,pas_temps=10,color_palette="plasma"):
    disposition = [
        ["traj1","phase1","energie1","energie1"],
        ["traj2","phase2","energie2","energie2"],
        ["traj3","phase3","energie3","energie3"]
    ]
    fig, axes = plt.subplot_mosaic(disposition, figsize=(12, 6),constrained_layout=True)
    
    tracer_sur_ax(axes["traj1"],traj1,color_palette,isTraj=True)
    tracer_sur_ax_corps(axes["traj1"],systeme_actif)
    tracer_potentiel(axes["traj1"],systeme_actif,pmin=30,levels=50,alpha=0.2)

    tracer_sur_ax(axes["traj2"],traj2,color_palette,isTraj=True)
    tracer_sur_ax_corps(axes["traj2"],systeme_actif)
    tracer_potentiel(axes["traj2"],systeme_actif,pmin=30,levels=50,alpha=0.2)

    tracer_sur_ax(axes["traj3"],traj3,color_palette,isTraj=True)
    tracer_sur_ax_corps(axes["traj3"],systeme_actif)
    tracer_potentiel(axes["traj3"],systeme_actif,pmin=30,levels=50,alpha=0.2)

    axes["phase1"].grid(True)
    tracer_sur_ax(axes["phase1"],ps.diag_espace_de_phase(traj1),color_palette)

    axes["phase2"].grid(True)
    tracer_sur_ax(axes["phase2"],ps.diag_espace_de_phase(traj2),color_palette)

    axes["phase3"].grid(True)
    tracer_sur_ax(axes["phase3"],ps.diag_espace_de_phase(traj3),color_palette)

    axes["energie1"].grid(True)
    tracer_sur_ax(axes["energie1"],en.energie(traj1,systeme_actif,pas_temps),color_palette)
    # tracer_sur_ax(axes["energie1"],en.rayon_dans_le_temps(traj1,pas_temps),"viridis")

    axes["energie2"].grid(True)
    tracer_sur_ax(axes["energie2"],en.energie(traj2,systeme_actif,pas_temps),color_palette)
    # tracer_sur_ax(axes["energie2"],en.rayon_dans_le_temps(traj2,pas_temps),"viridis")

    axes["energie3"].grid(True)
    tracer_sur_ax(axes["energie3"],en.energie(traj3,systeme_actif,pas_temps),color_palette)
    # tracer_sur_ax(axes["energie3"],en.rayon_dans_le_temps(traj3,pas_temps),"viridis")

    for k in ["energie1", "energie2", "energie3"]:
        forcer_echelle_decalage(axes[k])


def comparaison_traj_ref(traj_ref,traj_comp,systeme_actif,pas_temps=10,color_palette="plasma"):
    disposition = [
        ["traj_ref","phase_ref","energie_ref"],
        ["traj_comp","phase_comp","energie_comp"],
        ["rayon_relatif","phase_relative","energie_relative"],
        ["rayon_relatif","phase_relative","energie_relative"]
    ]
    fig, axes = plt.subplot_mosaic(disposition, figsize=(12, 6),constrained_layout=True)

    rayon_ref = en.rayon_dans_le_temps(traj_ref,pas_temps)
    rayon_comp = en.rayon_dans_le_temps(traj_comp,pas_temps)

    phase_ref = ps.diag_espace_de_phase(traj_ref)
    phase_comp = ps.diag_espace_de_phase(traj_comp)

    energie_ref = en.energie(traj_ref,systeme_actif,pas_temps)
    energie_comp = en.energie(traj_comp,systeme_actif,pas_temps)

    tracer_sur_ax(axes["traj_ref"],traj_ref,color_palette,isTraj=True)
    tracer_sur_ax_corps(axes["traj_ref"],systeme_actif)
    tracer_potentiel(axes["traj_ref"],systeme_actif,pmin=30,levels=50,alpha=0.2)

    tracer_sur_ax(axes["traj_comp"],traj_comp,color_palette,isTraj=True)
    tracer_sur_ax_corps(axes["traj_comp"],systeme_actif)
    tracer_potentiel(axes["traj_comp"],systeme_actif,pmin=30,levels=50,alpha=0.2)

    axes["phase_ref"].grid(True)
    tracer_sur_ax(axes["phase_ref"],phase_ref,color_palette)

    axes["phase_comp"].grid(True)
    tracer_sur_ax(axes["phase_comp"],phase_comp,color_palette)

    axes["energie_ref"].grid(True)
    tracer_sur_ax(axes["energie_ref"],energie_ref,color_palette)
    # tracer_sur_ax(axes["energie_ref"],en.rayon_dans_le_temps(traj_ref,pas_temps),"viridis")

    axes["energie_comp"].grid(True)
    tracer_sur_ax(axes["energie_comp"],energie_comp,color_palette)
    # tracer_sur_ax(axes["energie_comp"],en.rayon_dans_le_temps(traj_comp,pas_temps),"viridis")

    axes["rayon_relatif"].grid(True)
    tracer_sur_ax(axes["rayon_relatif"],rd.difference_relative_1D(rayon_ref, rayon_comp, pas_temps),color_palette)

    axes["phase_relative"].grid(True)
    tracer_sur_ax(axes["phase_relative"],rd.difference_relative_2D(phase_ref, phase_comp, pas_temps),color_palette)

    axes["energie_relative"].grid(True)
    tracer_sur_ax(axes["energie_relative"],rd.difference_relative_1D(energie_ref, energie_comp, pas_temps),color_palette)

    labels = {
        "traj_ref": {
            "nom": "Trajectoire 1",
            "xlabel": "x [m]",
            "ylabel": "y [m]",
        },
        "phase_ref": {
            "nom": "Espace de phase de la trajectoire 1",
            "xlabel": "v_x [m/s]",
            "ylabel": "v_y [m/s]",
        },
        "energie_ref": {
            "nom": "Énergie de la trajectoire 1",
            "xlabel": "Temps [s]",
            "ylabel": "Énergie [J]",
        },
        "traj_comp": {
            "nom": "Trajectoire 2",
            "xlabel": "x [m]",
            "ylabel": "y [m]",
        },
        "phase_comp": {
            "nom": "Espace de phase de la trajectoire 2",
            "xlabel": "v_x [m/s]",
            "ylabel": "v_y [m/s]",
        },
        "energie_comp": {
            "nom": "Énergie de la trajectoire 2",
            "xlabel": "Temps [s]",
            "ylabel": "Énergie [J]",
        },
        "rayon_relatif": {
            "nom": "Différence relative de rayon",
            "xlabel": "Temps [s]",
            "ylabel": "Rapport relatif",
        },
        "phase_relative": {
            "nom": "Différence relative de l'état dans l'espace de phase en norme.",
            "xlabel": "Temps [s]",
            "ylabel": "Rapport relatif",
        },
        "energie_relative": {
            "nom": "Différence relative de l'énergie",
            "xlabel": "Temps [s]",
            "ylabel": "Rapport relatif",
        },
    }

    sous_graphique_autonome(axes, labels)

    for k in ["energie_ref", "energie_comp", "energie_relative"]:
        forcer_echelle_decalage(axes[k])


def espaces_de_phase(traj,systeme_actif,color_palette):
    disposition = [
        ["traj","phase1","phase2"],
        ["traj","phase1","phase2"],
        ["phase","phase1","phase2"],
        ["phase","phase1","phase2"]
    ]
    fig, axes = plt.subplot_mosaic(disposition, figsize=(12, 6),constrained_layout=True)
    tracer_sur_ax(axes["traj"],traj,color_palette,isTraj=True)
    tracer_sur_ax_corps(axes["traj"],systeme_actif)
    tracer_potentiel(axes["traj"],systeme_actif,pmin=30,levels=50,alpha=0.2)

    axes["phase"].grid(True)
    tracer_sur_ax(axes["phase"],ps.diag_espace_de_phase(traj),color_palette)

    axes["phase1"].grid(True)
    tracer_sur_ax(axes["phase1"],ps.coupe_x_espace_de_phase(traj),color_palette)

    axes["phase2"].grid(True)
    tracer_sur_ax(axes["phase2"],ps.coupe_y_espace_de_phase(traj),color_palette)



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

    # axes["phase"].grid(True)
    # tracer_sur_ax(axes["phase"],ps.diag_espace_de_phase(traj),color_palette)

    axes["energie"].grid(True)
    tracer_sur_ax(axes["energie"],en.energie(traj,systeme_actif,pas_temps),color_palette)

    traj_origine_cte = [traj[0]+[0.1,0,0,0] for i in range(len(traj))]
    origine_rayon = en.rayon_dans_le_temps(traj_origine_cte,pas_temps)
    rayon_traj = en.rayon_dans_le_temps(traj,pas_temps)
    orbite_degenerescence = rd.difference_relative_1D(rayon_traj, origine_rayon, pas_temps)

    axes["rayon_relatif"].grid(True)
    tracer_sur_ax(axes["rayon_relatif"],orbite_degenerescence,color_palette)

    labels = {
        "traj": {
            "nom": "Trajectoire",
            "xlabel": "x [m]",
            "ylabel": "y [m]",
        },
        # "phase": {
        #     "nom": "Espace de phase en norme",
        #     "xlabel": "rayon [m]",
        #     "ylabel": "vitesse [m/s]",
        # },
        "energie": {
            "nom": "Énergie",
            "xlabel": "Temps [s]",
            "ylabel": "Énergie [J]",
        },
        "rayon_relatif": {
            "nom": "Distance à l'origine spatiale",
            "xlabel": "Temps [s]",
            "ylabel": "Déplacement relatif [/]",
        },
    }
    sous_graphique_autonome(axes, labels)

    for k in ["energie", "rayon_relatif"]:
        forcer_echelle_decalage(axes[k])
    
    return orbite_degenerescence



def trajectoire_vitesse(traj):
    traj_np = np.array(traj)
    return traj_np[:,2:4]

def coordinate_projection(traj,coord,pas_temps):
    traj_np = np.array(traj)
    traj_return = []
    for i in range(len(traj)):
        traj_return.append([i*pas_temps, traj_np[i][coord]])
    return np.array(traj_return)



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

    labels = {
        "traj": {
            "nom": "Trajectoire dans le plan",
            "xlabel": "x [m]",
            "ylabel": "y [m]",
        },
        "phase": {
            "nom": "Espace des vitesse",
            "xlabel": "vx [m/s]",
            "ylabel": "vy [m/s]",
        }
    }
    sous_graphique_autonome(axes, labels)




def trajectoire_toutes_variables_dans_le_temps(traj,systeme_actif,pas_temps=10,color_palette="plasma"):
    disposition = [
        ["traj","x_proj"],
        ["traj","y_proj"],
        ["vitesse_proj","vx_proj"],
        ["vitesse_proj","vy_proj"]
    ]

    fig, axes = plt.subplot_mosaic(disposition, figsize=(12, 6),constrained_layout=True)
    tracer_sur_ax(axes["traj"],traj,color_palette,isTraj=True)
    tracer_sur_ax_corps(axes["traj"],systeme_actif)
    velocity = trajectoire_vitesse(traj)
    tracer_sur_ax(axes["vitesse_proj"],velocity,color_palette,isTraj=True)
    tracer_potentiel(axes["traj"],systeme_actif,pmin=30,levels=50,alpha=0.2)

    tracer_sur_ax(axes["x_proj"],coordinate_projection(traj,0,pas_temps),color_palette)
    tracer_sur_ax(axes["y_proj"],coordinate_projection(traj,1,pas_temps),color_palette)
    tracer_sur_ax(axes["vx_proj"],coordinate_projection(traj,2,pas_temps),color_palette)
    tracer_sur_ax(axes["vy_proj"],coordinate_projection(traj,3,pas_temps),color_palette)


    labels = {
        "traj": {
            "nom": "Trajectoire dans le plan",
            "xlabel": "x [m]",
            "ylabel": "y [m]",
        },
        "vitesse_proj": {
            "nom": "Espace des vitesse",
            "xlabel": "vx [m/s]",
            "ylabel": "vy [m/s]",
        },
        "x_proj": {
            "nom": "Projection de la trajectoire sur x",
            "xlabel": "Temps [s]",
            "ylabel": "x [m]",
        },
        "y_proj": {
            "nom": "Projection de la trajectoire sur y",
            "xlabel": "Temps [s]",
            "ylabel": "y [m]",
        },
        "vx_proj": {
            "nom": "Projection de la trajectoire sur vx",
            "xlabel": "Temps [s]",
            "ylabel": "vx [m/s]",
        },
        "vy_proj": {
            "nom": "Projection de la trajectoire sur vy",
            "xlabel": "Temps [s]",
            "ylabel": "vy [m/s]",
        }
    }
    sous_graphique_autonome(axes, labels)