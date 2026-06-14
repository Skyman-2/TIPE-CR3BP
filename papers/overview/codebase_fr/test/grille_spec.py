import numpy as np
import matplotlib.pyplot as plt

fig, axs = plt.subplots(ncols=4, nrows=3)
gs = axs[1,2].get_gridspec()

# Supprimer les axes sous-jacents
for ax in axs[1:,-1]:
    ax.remove()

axbig = fig.add_subplot(gs[1:,-1])
axbig.annotate('Grand axes \nGridSpec[1:,-1]', xy=(0.1, 0.5), xycoords='axes fraction', va='center')

fig.tight_layout()
plt.show()
