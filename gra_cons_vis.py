import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os
import random

random.seed(2026)


min_site = 0
max_site = 5
min_height = 0
min_time = 0
max_time = 5


events = []
for _ in range(max_site * max_time):
    site = random.randint(0, max_site - 1)
    time = random.uniform(0, max_time)
    events.append((site, time))

# dynamics
NONE = None
h = [NONE] * max_site  # h[u] = top of column u, None = never reached
h[0] = 1  # seed at cell (0,0)

# track parents to reconstruct paths
last_event = [None] * max_site
last_event[0] = (0, 0)
parent = {}

blocks = []
live = []  # epochs working
dead = []  # epochs wasted

# dynamics
for u, t in sorted(
    events, key=lambda e: e[1]
):  # lambda function to sort by time (instead of site)
    left = h[u - 1] if u > 0 else NONE
    tops = [x for x in (left, h[u]) if x is not NONE]
    if tops:  # clock working

        # best previous node for the path (dynamic programming)
        if left is not NONE and h[u] is not NONE:
            best_prev = last_event[u - 1] if left > h[u] else last_event[u]
        elif left is not NONE:
            best_prev = last_event[u - 1]
        else:
            best_prev = last_event[u]

        parent[(u, t)] = best_prev
        last_event[u] = (u, t)

        h[u] = max(tops) + 1
        blocks.append((u, h[u] - 1))
        live.append((u, t))
    else:  # clock wasted
        dead.append((u, t))

tops = {(u, h[u] - 1) for u in range(max_site) if h[u] is not NONE}
if blocks != None:
    max_height = max(j for _, j in blocks) + 2

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(5, 5))

# drawing blue edges
edges_to_draw = set()
for U in range(max_site):
    if last_event[U] is not None:
        # Connect the top red star to the last valid event in this column
        edges_to_draw.add((last_event[U], (U, max_time)))
        curr = last_event[U]
        while curr in parent:
            prev = parent[curr]
            edges_to_draw.add((prev, curr))
            curr = prev

# Draw edges in blue, placing them under the dots [alpha for transparency, zorder for layering]
for (u1, t1), (u2, t2) in edges_to_draw:
    ax0.plot(
        [u1 + 0.5, u2 + 0.5],
        [t1, t2],
        color="blue",
        linewidth=1.5,
        alpha=0.5,
        zorder=2,
        linestyle="--",
    )

for u, t in live:
    ax0.plot(
        u + 0.5, t, marker="o", linestyle="None", color="black", markersize=2, zorder=3
    )
for u, t in dead:
    ax0.plot(
        u + 0.5, t, marker="x", linestyle="None", color="grey", markersize=2, zorder=3
    )

ax0.plot(
    0.5,
    0,
    marker="*",
    linestyle="None",
    color="red",
    markersize=5,
    zorder=5,
    clip_on=False,
)
for u in range(max_site):
    ax0.plot(
        u + 0.5,
        max_time,
        marker="*",
        linestyle="None",
        color="red",
        markersize=5,
        zorder=5,
        clip_on=False,
    )

ax0.axline(
    xy1=(0, max_time), xy2=(8, max_time), color="black", linewidth=1, linestyle="--"
)
for i in range(max_site + 1):
    ax0.axvline(x=i + 0.5, color="black", linewidth=0.5, linestyle="--")

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
# ax1.set_yticks([j + 0.5 for j in range(min_height - 1, max_height)])
# ax1.set_yticklabels([str(j) for j in range(min_height - 1, max_height)])

for ax in (ax0, ax1):
    # ax.set_xticks([i + 0.5 for i in range(min_site, max_site)])
    # ax.set_xticklabels([str(i) for i in range(min_site, max_site)])
    ax.tick_params(axis="both", which="both", length=0)
    ax.plot(1.0, 0.0, ">k", transform=ax.transAxes, clip_on=False)
    ax.plot(0.0, 1.0, "^k", transform=ax.transAxes, clip_on=False)

fig.tight_layout()
file_path = os.path.join(os.getcwd(), "bd_panel_G5.pdf")
plt.savefig(file_path, bbox_inches="tight")
plt.show()
