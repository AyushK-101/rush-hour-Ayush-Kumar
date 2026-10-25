# -*- coding: utf-8 -*-
import json
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

sys.path.insert(0, os.path.abspath("code"))
import starter_student as ss

os.makedirs("results/metrics", exist_ok=True)
os.makedirs("results/routes", exist_ok=True)
os.makedirs("results/figures", exist_ok=True)

print("Training ensemble model and evaluating on Map 5...")
train_df = pd.read_csv("train_cells_capped.csv")
tr = train_df[train_df["map_id"] < 5]
te = train_df[train_df["map_id"] == 5]

model = ss.train_model(tr)
metrics = ss.evaluate_model(model, te)

with open("results/metrics/ml_metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)
print("Saved results/metrics/ml_metrics.json")

with open("data/scenarios/scenarios.json") as f:
    scenarios = json.load(f)

summary_rows = []

# Scenarios configuration
# RUSH-1: tau=0.18
# RUSH-2: tau=0.18
# RUSH-3: tau=0.30 (stress test bottleneck resolution)
tau_map = {
    "RUSH-1": 0.18,
    "RUSH-2": 0.18,
    "RUSH-3": 0.30
}

for sc_name, sc_info in scenarios.items():
    print(f"Planning routes for {sc_name}...")
    sc_df = pd.read_csv(f"data/scenarios/{sc_info['map']}")
    preds = ss.predict_scenario(model, sc_df)
    
    tau = tau_map[sc_name]
    blocked = ss.blocking_policy(preds, tau=tau)
    costs = ss.cell_cost(preds)
    
    start, goal = sc_info["start"], sc_info["goal"]
    p_dist, len_dist, cost_dist = ss.plan_distance_only(blocked, start, goal, costs)
    p_traf, len_traf, cost_traf = ss.plan_traffic_aware(blocked, start, goal, costs)
    
    if p_dist:
        pd.DataFrame(p_dist, columns=["row", "col"]).to_csv(f"results/routes/{sc_name}_distance_only.csv", index=False)
    if p_traf:
        pd.DataFrame(p_traf, columns=["row", "col"]).to_csv(f"results/routes/{sc_name}_traffic_aware.csv", index=False)
        
    extra_dist = round(((len_traf - len_dist) / len_dist) * 100, 2) if len_dist > 0 else 0.0
    cost_saving = round(((cost_dist - cost_traf) / cost_dist) * 100, 2) if cost_dist > 0 else 0.0
    
    summary_rows.append({
        "Scenario": sc_name,
        "Name": sc_info["name"],
        "Tau": tau,
        "Dist_Length": len_dist,
        "Dist_Cost": cost_dist,
        "Traf_Length": len_traf,
        "Traf_Cost": cost_traf,
        "Extra_Distance_Pct": extra_dist,
        "Cost_Saving_Pct": cost_saving
    })
    
    # Figure visualization
    fig, ax = plt.subplots(figsize=(8, 8))
    density = sc_df.pivot(index="row", columns="col", values="traffic_density_0_1").to_numpy()
    im = ax.imshow(density, cmap="viridis", origin="upper", alpha=0.7)
    
    blocked_coords = np.argwhere(blocked)
    if len(blocked_coords) > 0:
        ax.scatter(blocked_coords[:, 1], blocked_coords[:, 0], c="crimson", marker="x", s=20, label=f"Blocked (p >= {tau})")
        
    if p_dist:
        d_coords = np.array(p_dist)
        ax.plot(d_coords[:, 1], d_coords[:, 0], color="dodgerblue", linestyle="--", linewidth=2.5, 
                label=f"Distance-Only (Len: {len_dist:.1f}, Cost: {cost_dist:.1f})")
        
    if p_traf:
        t_coords = np.array(p_traf)
        ax.plot(t_coords[:, 1], t_coords[:, 0], color="gold", linewidth=3.0, 
                label=f"Traffic-Aware (Len: {len_traf:.1f}, Cost: {cost_traf:.1f})")
        
    ax.scatter([start[1]], [start[0]], c="lime", s=120, edgecolors="black", zorder=5, label=f"Start {start}")
    ax.scatter([goal[1]], [goal[0]], c="magenta", s=120, edgecolors="black", zorder=5, label=f"Goal {goal}")
    
    ax.set_title(f"{sc_name}: {sc_info['name']} (tau={tau}) | Cost Saved: {cost_saving:.1f}%", fontsize=13, fontweight="bold")
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")
    plt.colorbar(im, ax=ax, label="Traffic Density (0-1)")
    ax.legend(loc="upper right", framealpha=0.9)
    plt.tight_layout()
    fig_path = f"results/figures/{sc_name}_route_comparison.png"
    plt.savefig(fig_path, dpi=200)
    plt.close()
    print(f"Saved {fig_path}")

# Plot Confusion Matrix
cm = np.array(metrics["confusion_matrix"])
fig, ax = plt.subplots(figsize=(6, 5))
cax = ax.imshow(cm, cmap="Blues", interpolation="nearest")
plt.colorbar(cax)
tick_marks = np.arange(len(metrics["classes"]))
ax.set_xticks(tick_marks)
ax.set_xticklabels(metrics["classes"], rotation=45)
ax.set_yticks(tick_marks)
ax.set_yticklabels(metrics["classes"])
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        val = cm[i, j]
        ax.text(j, i, str(val), ha="center", va="center", color="white" if val > cm.max()/2 else "black")
ax.set_title("Confusion Matrix (Held-Out Map 5)", fontweight="bold")
ax.set_xlabel("Predicted Label")
ax.set_ylabel("Actual Label")
plt.tight_layout()
plt.savefig("results/figures/confusion_matrix.png", dpi=200)
plt.close()
print("Saved results/figures/confusion_matrix.png")

# Write results_summary.md
summary_md = f"""# Project RUSH HOUR: Results Summary

## 1. Machine Learning Performance (Held-out Map 5)
- **Model Architecture**: Soft-Voting Ensemble (RandomForest + HistGradientBoosting)
- **Overall Accuracy**: {metrics['accuracy']:.4f}
- **Macro F1 Score**: {metrics['macro_f1']:.4f}
- **Recall for Blocked (Argmax Decision)**: {metrics['recall_blocked_argmax']:.4f} ({metrics['missed_blocked_argmax']} missed)
- **Recall for Blocked (Tau=0.18 Safety Policy)**: {metrics['recall_blocked_tau018']:.4f} ({metrics['missed_blocked_tau018']} missed)

## 2. Scenario Results at a Glance

| Scenario | Name | Route | Length | Cost (Objective J) | Extra Distance | Cost Change | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
"""

for r in summary_rows:
    sc = r["Scenario"]
    nm = r["Name"]
    dl, dc = r["Dist_Length"], r["Dist_Cost"]
    tl, tc = r["Traf_Length"], r["Traf_Cost"]
    ed, cs = r["Extra_Distance_Pct"], r["Cost_Saving_Pct"]
    t_val = r["Tau"]
    summary_md += f"| {sc} | {nm} | Distance-only | {dl:.2f} | {dc:.2f} | - | - | Geodesic baseline (tau={t_val}) |\n"
    summary_md += f"| {sc} | {nm} | Traffic-aware | {tl:.2f} | {tc:.2f} | +{ed:.1f}% | -{cs:.1f}% | Optimized routing (tau={t_val}) |\n"

with open("results/results_summary.md", "w") as f:
    f.write(summary_md)
print("Generated results/results_summary.md successfully")
