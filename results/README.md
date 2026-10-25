# Results

Everything in this folder is **generated** by `python code/export_results.py`. Do not edit these files by hand. If a number looks wrong, fix the code and run it again.

| Path | Contents |
| --- | --- |
| `metrics/ml_metrics.json` | Held-out accuracy, macro F1, per-class results, confusion matrix, blocked cells missed |
| `metrics/route_metrics.json` | Length and cost of every route |
| `routes/<SCENARIO>_distance_only.csv`, `routes/<SCENARIO>_traffic_aware.csv` | Every route as `step,row,col`, start cell first. Judges score these files |
| `figures/<SCENARIO>.png` | Route maps. Add your own figures here too |
| `results_summary.md` | A ready-made table to paste into the README and the technical report |
