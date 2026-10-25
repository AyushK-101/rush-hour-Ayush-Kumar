# Notebooks

This folder holds reproducible exploratory analysis and experiments supporting the findings in `docs/`:

| Notebook | Purpose | Key Insights |
| :--- | :--- | :--- |
| `01_explore_data.ipynb` | Spatial EDA & Data Exploration | Explores class distribution (7.56% blocked base rate), feature correlations (speed vs. density), and 60x60 grid maps. |
| `02_model_comparison.ipynb` | Machine Learning Architecture Benchmarks | Evaluates Random Forest, HistGradientBoosting, and Soft-Voting Ensemble using spatial Leave-One-Map-Out cross-validation. |
| `03_threshold_experiments.ipynb` | Cost-Sensitive Thresholding & Error Analysis | Analyzes why argmax misses 89 road closures, sweeps tau from 0.05 to 0.50, and justifies the Bayesian tau=0.18 threshold. |
| `04_routing_and_scenarios.ipynb` | Dijkstra Route Optimization & Stress Testing | Tests RUSH-1, RUSH-2, and RUSH-3; demonstrates Slide 85 diagonal corner-cutting invariants and adaptive bottleneck resolution. |

All final numbers and figures reported in `docs/` and `results/` are fully reproducible via `python code/export_results.py`.
