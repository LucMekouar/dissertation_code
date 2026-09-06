import os
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

min_site = 0
max_site = 5
min_height = 0
min_time = 0
max_time = 5

random.seed(2026)

events = []
for _ in range(max_site * max_time):
    site = random.randint(0, max_site - 1)
    time = random.uniform(0, max_time)
    events.append((site, time))

# dynamics
NONE = None
h = [NONE] * max_site  # h[u] = top of column u, None = never reached
h[0] = 1  # seed at cell (0,0)

blocks = []
live = []  # epochs working
dead = []  # epochs wasted
first_times = {(0, 0): 0.0}  # track smallest time to reach cell (site, height)

# dynamics
for u, t in sorted(events, key=lambda e: e[1]):
    left = h[u - 1] if u > 0 else NONE
    tops = [x for x in (left, h[u]) if x is not NONE]
    if tops:  # clock working
        h[u] = max(tops) + 1
        blocks.append((u, h[u] - 1))
        live.append((u, t))
        if (u, h[u] - 1) not in first_times:
            first_times[(u, h[u] - 1)] = t
    else:  # clock wasted
        dead.append((u, t))

tops = {(u, h[u] - 1) for u in range(max_site) if h[u] is not NONE}
if blocks != None:
    max_height = max(j for _, j in blocks) + 2

fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(8.5, 5))

for u, t in live:
    ax0.hlines(y=t, xmin=u, xmax=u + 1, color="black", linewidth=1.2)
for u, t in dead:
    ax0.hlines(y=t, xmin=u, xmax=u + 1, color="lightgrey", linewidth=1.2)

ax0.axline(
    xy1=(0, max_time), xy2=(8, max_time), color="black", linewidth=1, linestyle="--"
)
for i in range(max_site + 1):
    ax0.axvline(x=i, color="black", linewidth=0.2, linestyle="--")

ax0.text(
    max_site,
    max_time + 0.15,
    "t=" + str(max_time),
    va="center",
    ha="right",
    fontsize=10,
    fontweight="bold",
)
ax0.set_xlim(min_site, max_site)
ax0.set_ylim(min_time, max_time + 0.5)
ax0.set_xlabel("sites")
ax0.set_ylabel("time")
ax0.set_title("(a) Poisson clocks", fontsize=10)

# site/height visual
ax1.add_patch(Rectangle((0, 0), 1, 1, facecolor="red"))
for i, j in blocks:
    ax1.add_patch(
        Rectangle((i, j), 1, 1, facecolor="grey" if (i, j) in tops else "lightgrey")
    )

for u in range(max_site):  # sites at -\infty
    if h[u] is NONE:
        ax1.hlines(
            y=min_height - 0.5,
            xmin=u,
            xmax=u + 1,
            color="black",
            linewidth=4,
            linestyle="--",
        )

for i in range(max_site + 1):
    ax1.axvline(x=i, color="black", linewidth=0.2, linestyle="--")
for j in range(min_height - 1, max_height + 1):
    ax1.axhline(y=j, color="black", linewidth=0.2, linestyle="--")

ax1.set_xlim(min_site, max_site)
ax1.set_ylim(min_height - 0.5, max_height)
ax1.set_aspect("equal")
ax1.set_xlabel("sites")
ax1.set_ylabel("height")
ax1.set_title("(b) interface at $t=%d$" % max_time, fontsize=10)
ax1.set_yticks([j + 0.5 for j in range(min_height - 1, max_height)])
ax1.set_yticklabels([str(j) for j in range(min_height - 1, max_height)])

# table of arrival times
for (u, j), t_val in first_times.items():
    ax2.text(u + 0.5, j + 0.5, f"{t_val:.2f}", ha="center", va="center", fontsize=8)

for i in range(max_site + 1):
    ax2.axvline(x=i, color="black", linewidth=0.2, linestyle="--")
for j in range(min_height - 1, max_height + 1):
    ax2.axhline(y=j, color="black", linewidth=0.2, linestyle="--")

ax2.set_xlim(min_site, max_site)
ax2.set_ylim(min_height - 0.5, max_height)
ax2.set_aspect("equal")
ax2.set_xlabel("sites")
ax2.set_ylabel("height")
ax2.set_title("(c) arrival times by t=5", fontsize=10)
ax2.set_yticks([j + 0.5 for j in range(min_height - 1, max_height)])
ax2.set_yticklabels([str(j) for j in range(min_height - 1, max_height)])

for ax in (ax0, ax1, ax2):
    ax.set_xticks([i + 0.5 for i in range(min_site, max_site)])
    ax.set_xticklabels([str(i) for i in range(min_site, max_site)])
    ax.tick_params(axis="both", which="both", length=0)
    ax.plot(1.0, 0.0, ">k", transform=ax.transAxes, clip_on=False)
    ax.plot(0.0, 1.0, "^k", transform=ax.transAxes, clip_on=False)

fig.tight_layout()
file_path = os.path.join(os.getcwd(), "bd_panel_R5.pdf")
plt.savefig(file_path, bbox_inches="tight")
plt.show()
