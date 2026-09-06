import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

height = []

fig, ax = plt.subplots()


ax.add_patch(Rectangle((0, 0), 1, 1, facecolor="red"))
ax.hlines(
    y=-0.5,
    xmin=1,
    xmax=5,
    color="red",
    linewidth=4,
    linestyle="--",
)

ax.set_xlim(0, 5)
ax.set_ylim(-0.5, 5)
ax.set_aspect("equal")
for i in range(6):
    ax.axvline(x=i, color="black", linewidth=0.2, linestyle="--")
for i in range(-1, 6):
    ax.axhline(y=i, color="black", linewidth=0.2, linestyle="--")

ax.set_xlabel("sites")
ax.set_ylabel("height")
ax.plot(1.0, 0.0, ">k", transform=ax.transAxes, clip_on=False)
ax.plot(0.0, 1.0, "^k", transform=ax.transAxes, clip_on=False)
ax.set_title("Seed at site 0", fontsize=10)

file_path = os.path.join(os.getcwd(), "bd_seed.pdf")
plt.savefig(file_path, bbox_inches="tight")
plt.show()
