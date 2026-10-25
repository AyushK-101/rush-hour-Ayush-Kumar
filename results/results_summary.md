# Project RUSH HOUR: Results Summary

## 1. Machine Learning Performance (Held-out Map 5)
- **Model Architecture**: Soft-Voting Ensemble (RandomForest + HistGradientBoosting)
- **Overall Accuracy**: 0.7783
- **Macro F1 Score**: 0.7673
- **Recall for Blocked (Argmax Decision)**: 0.8142 (89 missed)
- **Recall for Blocked (Tau=0.18 Safety Policy)**: 0.9499 (24 missed)

## 2. Scenario Results at a Glance

| Scenario | Name | Route | Length | Cost (Objective J) | Extra Distance | Cost Change | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RUSH-1 | The Morning Commute | Distance-only | 85.08 | 215.03 | - | - | Geodesic baseline (tau=0.18) |
| RUSH-1 | The Morning Commute | Traffic-aware | 95.43 | 155.25 | +12.2% | -27.8% | Optimized routing (tau=0.18) |
| RUSH-2 | The Ring Road | Distance-only | 75.64 | 195.11 | - | - | Geodesic baseline (tau=0.18) |
| RUSH-2 | The Ring Road | Traffic-aware | 84.43 | 151.78 | +11.6% | -22.2% | Optimized routing (tau=0.18) |
| RUSH-3 | The Emergency Run | Distance-only | 68.80 | 215.72 | - | - | Geodesic baseline (tau=0.3) |
| RUSH-3 | The Emergency Run | Traffic-aware | 87.81 | 170.61 | +27.6% | -20.9% | Optimized routing (tau=0.3) |
