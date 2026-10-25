"""
Dependency graph untuk simulator ILP (RAW, WAR, WAW).
Node = instruksi, panah = dependensi (dari instruksi lebih awal ke yang harus menunggu).

Pemakaian:
    from graph import draw_dependency_graph
    draw_dependency_graph(instructions, deps, "output/war_graph.png", "WAR Dependency Graph")
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

COLORS = {"RAW": "#dc2626", "WAR": "#d97706", "WAW": "#2563eb"}
GAP = 2.6          # jarak antar node
RADIUS = 0.55


def draw_dependency_graph(instructions, deps, path="dependency_graph.png",
                          title="Dependency Graph"):
    n = len(instructions)
    pos = {inst.name: i * GAP for i, inst in enumerate(instructions)}
    fig, ax = plt.subplots(figsize=(max(7, n * GAP), 5))

    for inst in instructions:
        x = pos[inst.name]
        ax.add_patch(plt.Circle((x, 0), RADIUS, fc="#dbeafe", ec="#1d4ed8", lw=2, zorder=3))
        ax.text(x, 0, inst.name, ha="center", va="center", fontsize=13, weight="bold", zorder=4)
        ax.text(x, -1.05, str(inst).split(": ", 1)[1], ha="center", va="top", fontsize=9)

    seen = {}          # pasangan (producer, consumer) -> jumlah panah, agar panah tidak menumpuk
    top = 1.2
    for d in deps:
        x1, x2 = pos[d.producer.name], pos[d.consumer.name]
        span = round((x2 - x1) / GAP)
        k = seen.get((d.producer.name, d.consumer.name), 0)
        seen[(d.producer.name, d.consumer.name)] = k + 1
        rad = -(0.28 if span == 1 else 0.45) - 0.3 * k
        color = COLORS.get(d.kind, "#444444")
        ax.annotate("", xy=(x2 - RADIUS, 0.1), xytext=(x1 + RADIUS, 0.1),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=2,
                                    connectionstyle=f"arc3,rad={rad}"), zorder=2)
        peak = 0.1 + abs(rad) * (x2 - x1 - 2 * RADIUS) / 2   # puncak lengkungan panah
        ax.text((x1 + x2) / 2, peak + 0.12, f"{d.kind} ({d.register})",
                ha="center", color=color, fontsize=10, weight="bold")
        top = max(top, peak + 0.7)

    ax.set_xlim(-1.2, (n - 1) * GAP + 1.2)
    ax.set_ylim(-2.2, top)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title + "\n(panah: dari instruksi lebih awal ke instruksi yang harus menunggu)",
                 fontsize=11)
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return path
