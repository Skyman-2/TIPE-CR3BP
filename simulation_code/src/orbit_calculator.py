import numpy as np


### Objectif : déterminer numériquement une CI sur x pour un vy donné
### de manière à ce que l'orbit soit stable sur une période de temps donnée,
### stabilité qui sera définie comme la distance maximum à l'axe x=x_0 de la 
### trajectoire qui sera accepté (assez grand car les orbites ne sont pas 
### planes donc il faut laisser de la marge).