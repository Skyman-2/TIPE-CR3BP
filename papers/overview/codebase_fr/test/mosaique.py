import matplotlib.pyplot as plt

disposition = [
        ["traj","traj","phase","phase"],
        ["traj","traj","phase","phase"],
        ["traj","traj","phase","phase"],
        ["energie","energie","energie","energie"]
]

fig, ax = plt.subplot_mosaic(disposition, figsize=(12, 6))
plt.show()
