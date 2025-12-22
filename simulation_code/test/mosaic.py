import matplotlib.pyplot as plt

layout = [
        ["traj","traj","phase","phase"],
        ["traj","traj","phase","phase"],
        ["traj","traj","phase","phase"],
        ["energy","energy","energy","energy"]
]

fig, ax = plt.subplot_mosaic(layout, figsize=(12, 6))
plt.show()
