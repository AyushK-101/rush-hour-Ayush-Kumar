# Data folder: what is where

All data is **synthetic**. It is generated from illustrative rules with added noise. Labels and costs are not
real traffic records, sensor feeds, or validated routing measurements. Strong performance here means your model
learned patterns in this simulation; it does not establish real-world routing safety.

For the full contest context, read the `README.md` in the main folder first.

## Folders and files

| Folder | File | Purpose |
| --- | --- | --- |
| `labelled/` | `train_cells.csv` | 21,600 cells from 6 training city maps (60 x 60 each). Has labels and costs. Use it to train. |
| `labelled/` | `test_cells.csv` | 7,200 cells from 2 separate held-out maps. Has labels and costs. Use it only to evaluate. Do not train on it. |
| `scenarios/` | `scenario_RUSH_1.csv`, `scenario_RUSH_2.csv`, `scenario_RUSH_3.csv` | The maps you route on. Features only, no labels. RUSH-3 uses the same map as RUSH-1. |
| `scenarios/` | `scenarios.json` | Start and destination of each scenario, as [row, column]. |
| `baseline_predictions/` | `predictions_RUSH_1.csv`, `_2`, `_3` | The baseline Random Forest's predictions for every scenario cell: `predicted_label`, `p_free_flow`, `p_congested`, `p_blocked`. |

## Data dictionary

| Field | Meaning |
| --- | --- |
| `row`, `col` | Grid coordinates. [0, 0] is the top-left cell; rows increase downward. |
| `map_id` | Which map a cell came from (labelled files only). |
| `avg_speed_kmh` | Simulated average vehicle speed on the cell |
| `signal_delay_sec` | Simulated delay from traffic signals, in seconds |
| `traffic_density_0_1` | Traffic-density score from 0 to 1 |
| `intersection_density_0_1` | Intersection-density score from 0 to 1 |
| `incident_probability_0_1` | Simulated likelihood of an accident or road closure, from 0 to 1 |
| `road_type` | highway, arterial, collector, or residential |
| `congestion_label` | Target class: free_flow, congested, or blocked (labelled files only) |
| `simulated_travel_cost` | Synthetic numerical travel cost (labelled files only). Optional regression target. |

## Notes

* The scenario maps have no labels on purpose: your route is judged against hidden ground truth.
* Class balance differs between maps. Look at it before choosing metrics.
* The baseline misses a meaningful share of blocked cells. Check the confusion matrix, then decide how your
  blocking policy should handle that risk.
