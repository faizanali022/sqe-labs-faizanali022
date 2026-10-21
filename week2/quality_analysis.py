# ============================================================
# ISO 25010 Quality Attribute Analysis
# SQE Lab 2 - Comparative Analysis Script
# Evaluator: Faizan Ali
# Pair: A — WhatsApp vs Telegram
# ============================================================

import numpy as np
import matplotlib.pyplot as plt

# ---------- CONFIGURATION ----------
APP1_NAME = "WhatsApp"
APP2_NAME = "Telegram"
EVALUATOR = "Faizan Ali"

CHARACTERISTICS = [
    "Functional\nSuitability",
    "Performance\nEfficiency",
    "Compatibility",
    "Usability",
    "Reliability",
    "Security",
    "Maintainability",
    "Portability",
]

WEIGHTS = [0.15, 0.12, 0.10, 0.15, 0.15, 0.15, 0.08, 0.10]

# MY ACTUAL RATINGS
APP1_RATINGS = [4, 5, 5, 4, 4, 5, 4, 5]   # WhatsApp
APP2_RATINGS = [5, 4, 5, 5, 3, 3, 4, 5]   # Telegram

# ---------- VALIDATION ----------
assert len(APP1_RATINGS) == 8
assert len(APP2_RATINGS) == 8
assert all(1 <= r <= 5 for r in APP1_RATINGS)
assert all(1 <= r <= 5 for r in APP2_RATINGS)
assert abs(sum(WEIGHTS) - 1.0) < 0.001

# ---------- SCORE CALCULATION ----------
def weighted_score(ratings, weights):
    return sum(r * w for r, w in zip(ratings, weights))

app1_score = weighted_score(APP1_RATINGS, WEIGHTS)
app2_score = weighted_score(APP2_RATINGS, WEIGHTS)

# ---------- CONSOLE REPORT ----------
print("\n" + "=" * 60)
print("   ISO 25010 QUALITY ATTRIBUTE ANALYSIS REPORT")
print("=" * 60)
print(f"   Evaluator : {EVALUATOR}")
print(f"   App 1     : {APP1_NAME}")
print(f"   App 2     : {APP2_NAME}")
print("=" * 60)
print(f"   {'Characteristic':<28} {APP1_NAME:>8} {APP2_NAME:>8}  Weight")
print(f"   {'-'*55}")
for char, r1, r2, w in zip(CHARACTERISTICS, APP1_RATINGS, APP2_RATINGS, WEIGHTS):
    label = char.replace("\n", " ")
    print(f"   {label:<28} {r1:>8} {r2:>8}  ({w:.0%})")
print(f"   {'-'*55}")
print(f"   {'WEIGHTED TOTAL':<28} {app1_score:>8.2f} {app2_score:>8.2f}")
print("=" * 60)

winner = APP1_NAME if app1_score >= app2_score else APP2_NAME
margin = abs(app1_score - app2_score)
print(f"\n   Overall higher quality: {winner} (margin: {margin:.2f})")

gaps = [(abs(r1 - r2), char.replace("\n", " "), r1, r2)
        for char, r1, r2 in zip(CHARACTERISTICS, APP1_RATINGS, APP2_RATINGS)]
gaps.sort(reverse=True)
print(f"\n   Top 3 quality gaps:")
for diff, char, r1, r2 in gaps[:3]:
    better = APP1_NAME if r1 > r2 else APP2_NAME if r2 > r1 else "Tied"
    print(f"     {char}: gap={diff}  (better: {better})")

# ---------- RADAR CHART ----------
def plot_radar_chart(app1_name, app2_name, app1_ratings, app2_ratings,
                     characteristics, app1_score, app2_score):
    N = len(characteristics)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()

    app1_vals = app1_ratings + [app1_ratings[0]]
    app2_vals = app2_ratings + [app2_ratings[0]]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("#F8FAFC")
    ax.set_facecolor("#F8FAFC")

    ax.fill(angles, app1_vals, alpha=0.25, color="#2E75B6")
    ax.fill(angles, app2_vals, alpha=0.25, color="#1A6B5A")

    ax.plot(angles, app1_vals, "o-", linewidth=2.5, color="#2E75B6",
            label=f"{app1_name}  (Score: {app1_score:.2f})")
    ax.plot(angles, app2_vals, "s--", linewidth=2.5, color="#1A6B5A",
            label=f"{app2_name}  (Score: {app2_score:.2f})")

    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1", "2", "3", "4", "5"], fontsize=9, color="#666")
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(characteristics, fontsize=11, fontweight="bold", color="#1F3864")

    ax.grid(color="#CCCCCC", linestyle="--", linewidth=0.8, alpha=0.7)
    ax.spines["polar"].set_color("#CCCCCC")

    plt.title(f"ISO 25010 Quality Profile Comparison\n{app1_name} vs. {app2_name}",
              fontsize=14, fontweight="bold", color="#1F3864", pad=25)
    plt.legend(loc="upper right", bbox_to_anchor=(1.35, 1.15),
               fontsize=11, framealpha=0.9, edgecolor="#CCCCCC")

    for angle, r1, r2 in zip(angles[:-1], app1_ratings, app2_ratings):
        ax.annotate(str(r1), xy=(angle, r1), fontsize=9, color="#2E75B6",
                    fontweight="bold", ha="center", va="bottom")
        ax.annotate(str(r2), xy=(angle, r2), fontsize=9, color="#1A6B5A",
                    fontweight="bold", ha="center", va="top")

    plt.tight_layout()
    filename = f"quality_radar_{app1_name}_{app2_name}.png".replace(" ", "_")
    plt.savefig(filename, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor(), edgecolor="none")
    print(f"\n   Radar chart saved: {filename}")
    plt.show()
    return filename

plot_radar_chart(APP1_NAME, APP2_NAME, APP1_RATINGS, APP2_RATINGS,
                 CHARACTERISTICS, app1_score, app2_score)