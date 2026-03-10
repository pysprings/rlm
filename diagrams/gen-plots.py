"""Generate research data plots for the RLM presentation."""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid", font_scale=1.15, palette="deep")
plt.rcParams['font.family'] = 'sans-serif'

# ============================================================
# Plot 1: "Lost in the Middle" (Liu et al., 2023)
# Aggregate across models → one curve with uncertainty band
# Data from Appendix Table 6 (20 total documents)
# ============================================================

lost_data = []
models_lost = {
    "GPT-3.5-Turbo": [75.8, 57.2, 53.8, 55.4, 63.2],
    "Claude-1.3":     [59.9, 55.9, 56.8, 57.2, 60.1],
    "LongChat-13B":   [68.6, 57.4, 55.3, 52.5, 55.0],
    "MPT-30B":        [53.7, 51.8, 52.2, 52.7, 56.3],
}
positions = [1, 5, 10, 15, 20]

for model, accs in models_lost.items():
    for pos, acc in zip(positions, accs):
        lost_data.append({
            "Position of relevant document": pos,
            "Accuracy (%)": acc,
            "Model": model,
        })

df_lost = pd.DataFrame(lost_data)

fig1, ax1 = plt.subplots(figsize=(7, 4))
sns.lineplot(
    data=df_lost, x="Position of relevant document", y="Accuracy (%)",
    marker="o", markersize=8, linewidth=2.5, errorbar="sd", ax=ax1,
)
ax1.set_title(
    "Lost in the Middle\n"
    "Liu et al., 2023 — Multi-doc QA, 20 documents",
    fontsize=12,
)
ax1.set_xticks(positions)
ax1.set_ylim(45, 82)
fig1.tight_layout()
fig1.savefig("diagrams/lost-in-the-middle.png", dpi=200, bbox_inches="tight")
fig1.savefig("docs/assets/lost-in-the-middle.png", dpi=200, bbox_inches="tight")
print("Saved lost-in-the-middle.png")
plt.close(fig1)

# ============================================================
# Plot 2: "Same Task, More Tokens" (Levy et al., 2024)
# Aggregate across models → one curve with uncertainty band
# Approximate data from Figure 1 (averaged across tasks)
# ============================================================

deg_data = []
models_deg = {
    "GPT-4":          [0.99, 0.98, 0.95, 0.92, 0.87],
    "Mistral Medium": [0.93, 0.87, 0.82, 0.78, 0.73],
    "Gemini Pro":     [0.93, 0.85, 0.78, 0.68, 0.60],
    "Mixtral 8x7B":   [0.91, 0.87, 0.83, 0.78, 0.72],
    "GPT-3.5":        [0.84, 0.79, 0.72, 0.65, 0.58],
}
token_lengths = [250, 500, 1000, 2000, 3000]

for model, accs in models_deg.items():
    for toks, acc in zip(token_lengths, accs):
        deg_data.append({
            "Input length (tokens)": toks,
            "Reasoning accuracy": acc,
            "Model": model,
        })

df_deg = pd.DataFrame(deg_data)

fig2, ax2 = plt.subplots(figsize=(7, 4))
sns.lineplot(
    data=df_deg, x="Input length (tokens)", y="Reasoning accuracy",
    marker="o", markersize=8, linewidth=2.5, errorbar="sd", ax=ax2,
)
ax2.set_title(
    "Same Task, More Tokens\n"
    "Levy et al., 2024 — FLenQA benchmark",
    fontsize=12,
)
ax2.set_ylim(0.50, 1.05)
fig2.tight_layout()
fig2.savefig("diagrams/degradation.png", dpi=200, bbox_inches="tight")
fig2.savefig("docs/assets/degradation.png", dpi=200, bbox_inches="tight")
print("Saved degradation.png")
