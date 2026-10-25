# Project RUSH HOUR: Start here

**Read this first.** It explains the whole contest, what is in this repository, how to read the data, and what your team has to build. **You submit your own repository:** these starter files are a template. Your team creates its own new Git repository, copies these files in, works there, and submits the link to *your* repository. The organizers' starter is read-only. Start with [`SETUP_YOUR_OWN_REPOSITORY.md`](SETUP_YOUR_OWN_REPOSITORY.md). The challenge brief is the official statement of the problem; if anything here seems to differ from the brief, the brief wins.

---

## 1. The contest in one minute

**The setting.** Metro City is large, dense, and always busy. In its high-traffic zones, ambulances, fire engines, and police vehicles lose precious minutes to congestion, incidents, and closed roads. The city wants to improve its emergency response with AI.

**The service the city has in mind.**

1. A citizen dials the emergency number.
2. An AI system predicts traffic conditions across the city and recommends the **fastest and safest route** for the vehicle.
3. The nearest available vehicle is dispatched along that route.

The city pays for the service. The vehicles are run by third-party operators, who are paid by the government for their services.

**Your team's job.** You are a combined engineering and consulting team advising the city. You must build a *complete solution*, which has three parts:

| Part | What you deliver |
| --- | --- |
| **1. The AI engine** | A model that predicts how drivable each road cell is, and a route planner that uses those predictions to find the fastest, safest route |
| **2. The operating plan** | How the city should set up, fund, and run the service: operating model, funding and operator contracts, risks, rollout |
| **3. The recommendation** | A one-page executive summary for the city and a short deck (about 5 slides), presented in a 5-minute pitch |

**What this repository is.** A template for your team's own repository: your working folder and your submission, in one. It holds the datasets, a working baseline, code to export your results, a self-check, and a template for every document you must write. It does **not** contain the answer. The key pieces of the engine are left for you.

> **Everything here is simulated.** The city, the roads, and all numbers are fictional. The data was generated from illustrative rules with added noise. It is not real traffic data, and results do not show how a real city's traffic behaves.

---

## 2. What is in this repository

```
rush_hour_team_repo/
├── README.md                          <- YOUR team README (fill it in; this is the front page of your submission)
├── SUBMISSION_CHECKLIST.md            <- tick-list before you submit
├── requirements.txt                   <- Python libraries to install
├── .gitignore
├── .github/workflows/                 <- runs the self-check automatically on GitHub
│
├── code/
│   ├── starter_student.py             <- baseline code + the parts you must finish
│   ├── export_results.py              <- runs everything and writes results/
│   └── check_submission.py            <- checks your submission is complete
│
├── data/                              <- the contest data (do not edit)
│   ├── README.md                      <-   short data dictionary
│   ├── labelled/                      <-   data WITH answers, for the model
│   │   ├── train_cells.csv            <-     train on this (6 maps)
│   │   └── test_cells.csv            <-     measure on this (2 other maps)
│   ├── scenarios/                     <-   the maps you route on (NO answers)
│   │   ├── scenario_RUSH_1.csv
│   │   ├── scenario_RUSH_2.csv
│   │   ├── scenario_RUSH_3.csv        <-     same map as RUSH-1
│   │   └── scenarios.json             <-     start and destination of each scenario
│   └── baseline_predictions/          <-   the baseline model's predictions
│
├── notebooks/                         <- your exploration and experiments
├── results/                           <- generated: metrics, route files, figures
│
├── docs/                              <- your written deliverables
│   ├── 00_START_HERE.md               <-   this guide
│   ├── SETUP_YOUR_OWN_REPOSITORY.md   <-   how to create YOUR repository (do this first)
│   ├── 01_technical_report.md         <-   model, blocking policy, cost function, planner, results
│   ├── 02_executive_summary.md        <-   one page for the city
│   ├── 03_service_model_and_rollout.md
│   ├── 04_funding_and_cost_model.md
│   ├── 05_stakeholder_map.md
│   ├── 06_risk_register.md
│   └── 07_assumptions_log.md
│
└── presentation/                      <- your short deck (about 5 slides) goes here
```

**Where to start:** this guide, then `code/starter_student.py`, then the `data/` folder. If the many CSV files look confusing, remember there are only three kinds: `labelled/` (data with answers), `scenarios/` (maps to route on), and `baseline_predictions/` (the baseline model's guesses for those maps).

---

## 3. Quick start (10 minutes)

You need Python 3.10 or later. Open a terminal in the repository's main folder and run every command from there.

```bash
python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
python code/starter_student.py --scenario RUSH-1
```

What you should see:

1. The baseline model trains and prints **held-out metrics**: accuracy, macro F1, a confusion matrix, and a count of blocked cells the model missed.
2. The script prints the **distance-only route** for the scenario, with its length and a cost.
3. It prints `Traffic-aware planner not implemented yet`. That message is expected. Finishing it is your job.

Useful options:

| Command | What it does |
| --- | --- |
| `--scenario RUSH-2` or `RUSH-3` | Run another scenario |
| `--save-plot` | Save a picture to `output/` instead of opening a window |
| `--use-precomputed` | Skip training and use the files in `data/baseline_predictions/` instead (faster, but no held-out report) |

No internet connection, GIS software, or real-time traffic service is needed.

---

## 4. Understanding the data

### 4.1 The big idea: a city as a grid

Every map is a **60 × 60 grid** of road cells, 3,600 cells per map. Think of each cell as a small stretch of road, described by a few traffic measurements.

* A cell is identified by `(row, col)`.
* `(0, 0)` is the **top-left** cell. **Row increases downward**, and column increases to the right.
* A vehicle moves from a cell to any of its 8 neighbors (up, down, left, right, and the four diagonals).

### 4.2 Three kinds of files

| Kind | Files | Has the answer (`congestion_label`)? | Use it to |
| --- | --- | --- | --- |
| **Training** | `data/labelled/train_cells.csv` | Yes | Teach your model. 21,600 cells from 6 different maps (`map_id` 0 to 5) |
| **Held-out test** | `data/labelled/test_cells.csv` | Yes | Measure how well your model works on maps it has never seen. 7,200 cells from 2 other maps. **Never train on it.** |
| **Scenario maps** | `data/scenarios/scenario_RUSH_1/2/3.csv` | **No** | The maps you route on. 3,600 cells each. The true labels are hidden and used only for judging |

Scenario RUSH-3 uses the **same map** as RUSH-1; only the start and destination differ.

### 4.3 What each column means

| Column | In which files | Meaning | Typical range |
| --- | --- | --- | --- |
| `row`, `col` | all | Position on the grid | 0 to 59 |
| `map_id` | train, test | Which map the cell came from | train 0 to 5, test 0 to 1 |
| `avg_speed_kmh` | all | Simulated average vehicle speed on the cell | about 3 to 77 |
| `signal_delay_sec` | all | Simulated delay from traffic signals, in seconds | about 0 to 30 |
| `traffic_density_0_1` | all | How crowded the cell is. 0 = empty, 1 = packed | 0 to 1 |
| `intersection_density_0_1` | all | How many junctions the cell has nearby | 0 to 1 |
| `incident_probability_0_1` | all | Simulated likelihood of an accident or road closure | 0 to 1 (mostly low) |
| `road_type` | all | `highway`, `arterial`, `collector`, or `residential` | highway is the rarest, residential the most common |
| `congestion_label` | train, test | **The target.** `free_flow`, `congested`, or `blocked` | see below |
| `simulated_travel_cost` | train, test | A synthetic numeric cost of crossing the cell | about 0.5 to 14 |

**The three labels, in plain words**

| Label | Meaning | Typical cost (train data) |
| --- | --- | --- |
| `free_flow` | Traffic moves normally | about 1 |
| `congested` | Slow, but passable | about 3.5 |
| `blocked` | Must not be entered | about 13 |

Rough class balance in the training data: about 62% free flow, 30% congested, 8% blocked. **Blocked is rare**, and it is the label that matters most for safety. The balance differs from map to map, so check it before you choose your metrics.

### 4.4 A first look in Python

```python
import pandas as pd, numpy as np
import matplotlib.pyplot as plt

train = pd.read_csv("data/labelled/train_cells.csv")
print(train.head())
print(train["congestion_label"].value_counts(normalize=True))

# class balance map by map
print(train.groupby("map_id")["congestion_label"].value_counts(normalize=True).unstack())

# how do the numbers differ by label?
print(train.groupby("congestion_label")[["avg_speed_kmh", "traffic_density_0_1",
                                         "incident_probability_0_1"]].mean())
```

**Turn a column into a 60 × 60 picture** (works for any file):

```python
scen = pd.read_csv("data/scenarios/scenario_RUSH_1.csv")
density = scen.pivot(index="row", columns="col", values="traffic_density_0_1").to_numpy()
plt.imshow(density, cmap="viridis"); plt.colorbar(); plt.title("Traffic density"); plt.show()
```

**See a labelled training map:**

```python
code = {"free_flow": 0, "congested": 1, "blocked": 2}
m = train[train.map_id == 0].sort_values(["row", "col"])
grid = m["congestion_label"].map(code).to_numpy().reshape(60, 60)
plt.imshow(grid, cmap="RdYlGn_r"); plt.title("Map 0: 0 free, 1 congested, 2 blocked"); plt.show()
```

**Read the baseline's predictions** (the files in `data/baseline_predictions/` have one row per scenario cell):

```python
pred = pd.read_csv("data/baseline_predictions/predictions_RUSH_1.csv")
print(pred.head())       # row, col, predicted_label, p_free_flow, p_congested, p_blocked
p_blocked = pred.pivot(index="row", columns="col", values="p_blocked").to_numpy()
```

`p_free_flow`, `p_congested`, and `p_blocked` are the model's probabilities for each class. They add up to 1 for every cell. Cells where the model is unsure are exactly where your policy matters.

### 4.5 Things to notice

* **Labels are a rule plus noise**, not an exact formula. A perfect score is not possible, and you should not expect one.
* **Neighboring cells look alike.** Traffic is smooth across a map, so congestion appears in patches, not as scattered dots.
* **The scenario files have no labels.** Your route is judged against the hidden truth, so a route that "looks safe" on your predictions may still pass through a blocked cell the model missed.
* **Do not mix maps carelessly.** If you split the training file yourself for tuning, split by `map_id`, not by random rows. Cells from the same map are neighbors and look alike, so a random split gives results that are too good.

---

## 5. What you have to do

### Task A: predict traffic conditions (machine learning)

**Goal:** predict `congestion_label` for each cell from these features: `avg_speed_kmh`, `signal_delay_sec`, `traffic_density_0_1`, `intersection_density_0_1`, `incident_probability_0_1`, and `road_type`.

* Train on `data/labelled/train_cells.csv`. Evaluate on `data/labelled/test_cells.csv`.
* The starter script already trains a Random Forest and prints its metrics. You may keep it, improve it, or replace it. A fancier model is not automatically better.
* **Required:** at least one **error analysis**. Look at the confusion matrix, especially blocked cells predicted as *not* blocked. A missed blocked road is the costliest mistake, so ask why it happens and what your routing policy should do about it.
* *Optional:* predict `simulated_travel_cost` as a regression target.

### Task B: plan the route (optimization)

**Goal:** find a route `P` from the **start** to the **destination** that minimizes the total predicted cost:

```
J(P) = sum over each step (u -> v) of  d(u, v) * ( c(u) + c(v) ) / 2
```

* `u` and `v` are adjacent cells on the route.
* `d(u, v)` is **1** for a horizontal or vertical step and **√2 (about 1.414)** for a diagonal step.
* `c(u)` and `c(v)` are the predicted travel costs of those two cells.

*Worked example.* Stepping sideways from a free-flow cell (cost 1) into a congested cell (cost 3.5) costs `1 × (1 + 3.5) / 2 = 2.25`. A diagonal step between two free-flow cells costs `1.414 × (1 + 1) / 2 = 1.41`.

**Rules for your route**

* **Blocked cells.** Your team chooses a **blocking policy**: which cells the route may never enter. The simplest policy blocks cells predicted `blocked`. A more cautious one blocks any cell whose `p_blocked` is above a threshold you can justify.
* **No corner-cutting.** A diagonal move may not squeeze past the corner of a blocked cell. The provided code already enforces this.
* **Fair comparison.** Compare your traffic-aware route with the distance-only route using the **same blocking policy** for both.
* **Report two numbers for every route:** the geometric **length** and the cumulative **cost** under your stated objective.
* Any justified planner is fine. A* and Dijkstra are both acceptable. The goal is the quality of the whole system, not a fashionable algorithm.

### How the pieces fit together

```
 features ──> ML model ──> predicted label + probabilities
                                   │
              ┌────────────────────┴────────────────────┐
              ▼                                         ▼
      blocking_policy()                            cell_cost()
   (which cells are off limits)             (how costly is each cell)
              │                                         │
              └──────────────────┬──────────────────────┘
                                 ▼
                      plan_traffic_aware()
                (shortest route on your costs)
                                 │
                                 ▼
            compare with the distance-only baseline
        (length, cost, missed blocked cells, trade-offs)
```

### What the starter code gives you, and what it leaves for you

Open `code/starter_student.py`. Everything you must write is marked `TODO`.

| Function | Status | What it does |
| --- | --- | --- |
| `train_baseline()`, `evaluate()`, `predict_scenario()` | Provided | Trains the Random Forest, prints held-out metrics, predicts a scenario |
| `shortest_path(blocked, start, goal, edge_weight)` | Provided | Dijkstra search. Handles the 8 neighbor moves and the corner-cutting check. **You supply the edge weight** |
| `default_blocked_mask()`, `plan_distance_only()` | Provided | The distance-only baseline route |
| `route_length()`, `route_cost()` | Provided | Report a route's length and cost using the formula above |
| `plot_routes()` | Provided | Side-by-side map plots of the routes |
| **`cell_cost()`** | **TODO** | Turn predictions into a cost for every cell |
| **`blocking_policy()`** | **TODO** | Decide which cells are blocked |
| **`plan_traffic_aware()`** | **TODO** | Plan the route using your costs and your policy |

Design questions to think about while you fill these in:

* Should a cell's cost come from its predicted *label*, or from the *probabilities*, so that uncertain cells cost more?
* Should incident probability add cost, even for cells the model calls free flow?
* How cautious should the blocking policy be? Every extra blocked cell makes routes longer. Every missed one risks a hazard.
* How much extra distance is a safer, cheaper route worth?

---

## 6. The scenarios

Each scenario gives a start and a destination as `[row, column]` (see `data/scenarios/scenarios.json`). Think of the start as where the vehicle begins, and the destination as the incident.

| Scenario | Name | Start | Destination | Map file | Status |
| --- | --- | --- | --- | --- | --- |
| RUSH-1 | The Morning Commute | [3, 3] | [56, 55] | `scenario_RUSH_1.csv` | **Required** |
| RUSH-2 | The Ring Road | [55, 4] | [4, 55] | `scenario_RUSH_2.csv` | **Required** |
| RUSH-3 | The Emergency Run | [30, 3] | [30, 56] | `scenario_RUSH_3.csv` | Optional stress test |

* **RUSH-1:** compare the shortest-distance route with your traffic-aware route, and report length and cost. *How much extra distance is worth taking to reduce predicted cost?*
* **RUSH-2:** a different city layout. Does your model and policy still work? Explain which traffic features most influence the route.
* **RUSH-3:** same map as RUSH-1, new start and destination. Try a more conservative blocking policy and explain how and why the route changes. *How should a vehicle balance caution against a much longer route?*

Treat each scenario as a **client question**: answer it in terms the city cares about, such as response time and risk, not only route numbers.

---

## 7. The consulting half

This contest is judged on engineering **and** consulting. The city does not want a model; it wants a service it can run.

**You deliver:**

* A **one-page executive summary** for the city.
* A **short deck (about 5 slides)** that includes your implementation plan, presented in a **5-minute pitch**.

**Cover these four core themes** in your plan (four more are optional):

| Core theme | Questions to answer |
| --- | --- |
| Service model | How does a citizen's call become a dispatched vehicle with a recommended route? Where do dispatchers stay in the loop? |
| Funding and contracts | How does the city fund the AI service, and how should it pay the third-party operators? What should contracts require? Include a rough pilot cost. |
| Risks and mitigations | What if the model misses a blocked road, a data feed fails, or dispatchers over-rely on the tool? Link to your error analysis. |
| Rollout and success measures | Where would you pilot first? What are the go/no-go criteria and the KPIs? |

The `docs/` folder has a template for each deliverable: executive summary, service model and rollout, funding and cost model, stakeholder map, risk register, and assumptions log. The `presentation/` folder has the pitch outline. Fill in every `[[FILL IN]]` marker.

**Important:** every cost and business-impact figure you write, such as minutes saved or pilot cost, is an **assumption**. State where it comes from and label it illustrative. Judges reward clear, honest assumptions, and they penalize unsupported claims.

---

## 8. How you are judged

Suggested weights (the organizers may adjust them):

| Category | Weight | What judges look for |
| --- | --- | --- |
| Route quality | 15% | A feasible route that costs less than the baseline under a stated objective, a fair comparison, correct movement rules |
| ML quality and error analysis | 10% | Held-out metrics, a confusion matrix, thoughtful error analysis, especially missed blocked roads |
| Robustness and experimentation | 10% | Multiple scenarios, threshold experiments, failure analysis |
| Visualization, explanation and reproducibility | 15% | Clear maps and routes, a clear cost function, repeatable results |
| Client recommendation | 15% | Clear framing of the city's problem, options compared, a well-supported recommendation |
| Implementation plan | 15% | Service model, funding and operator contracts, rollout and KPIs |
| Risk analysis | 10% | Risks identified and mitigated, limitations stated |
| Business insight and pitch | 10% | Trade-offs translated into value for the city, clear storytelling, confident answers |

**How routes are scored:** the judges compare your route against the **hidden true labels and costs** of the scenario maps. They look at the route's length, its true cost, and how many truly blocked cells it enters. A longer route can still win if it clearly lowers cost.

---

## 9. Minimum submission checklist

- [ ] Reproducible source code and run instructions
- [ ] A trained or justified ML model, held-out results, and at least one error analysis, including missed blocked roads
- [ ] A working traffic-aware route planner, compared with the distance-only baseline using stated metrics
- [ ] A visualization of at least one scenario
- [ ] A short explanation of the cost function, blocking policy, trade-offs, and limitations
- [ ] A one-page executive summary for the city
- [ ] A short deck (about 5 slides) with your implementation plan, ready for a 5-minute pitch

RUSH-1 and RUSH-2 are required; RUSH-3 and the other extensions are optional.

**How to submit.** Your submission is **your team's own repository**, not the organizers' starter. The starter is read-only: you cannot push to it. Follow [`SETUP_YOUR_OWN_REPOSITORY.md`](SETUP_YOUR_OWN_REPOSITORY.md) to create your repository and copy these files into it. Before you submit:

1. Run `python code/export_results.py` to generate `results/`.
2. Run `python code/check_submission.py` and fix every `FAIL`.
3. Tick `SUBMISSION_CHECKLIST.md`.
4. Make sure the organizers can open your repository (add them with Read access if it is private).
5. Push your final commit and send the organizers **your repository link and the commit hash or tag**.

---

## 10. A suggested 48-hour plan

| Hours | Focus |
| --- | --- |
| 0 to 4 | Explore the data and the maps. Run the starter script. Split roles |
| 4 to 10 | Baselines: run the ML baseline and the distance-only route. Frame the client problem |
| 10 to 20 | Analyze errors. Design your cost function and blocking policy |
| 20 to 30 | Build the traffic-aware planner |
| 30 to 38 | Experiment: all scenarios, thresholds, edge cases |
| 38 to 44 | Write the executive summary and deck. Prepare the pitch |
| 44 to 48 | Final testing and demo |

Work in parallel. Some of you can improve the model while others build the planner, and the consulting work should start early. **A working, measurable baseline beats an unfinished sophisticated model.**

**Not a coder?** You can still own the blocking policy, the trade-off analysis, and the business case, working from the precomputed predictions and the templates in `docs/`.

---

## 11. Common pitfalls

1. **Training on the test set.** Never. It is only for the final measurement.
2. **Random row splits for tuning.** Cells on the same map are neighbors. Split by `map_id`.
3. **Judging the model by accuracy alone.** Blocked cells are rare. Look at recall for `blocked` and at the confusion matrix.
4. **Unfair route comparisons.** Use the same blocking policy for both routes, and report both length and cost.
5. **Mixing up row and column.** Cells are `(row, col)`. In plots, row is the vertical axis. The starter code already follows this.
6. **Claims without a baseline.** Say what you improved on, and by how much.
7. **Treating assumptions as facts.** Every cost, saving, or figure in your plan should say where it came from.

---

## 12. Glossary

| Term | Meaning |
| --- | --- |
| **Cell** | One square of the 60 × 60 grid, with its traffic features |
| **Traversability / congestion class** | Whether a cell is `free_flow`, `congested`, or `blocked` |
| **Blocked mask** | A yes/no grid showing which cells a route may not enter |
| **Blocking policy** | Your rule for building the blocked mask |
| **Cost** | A number saying how expensive it is to cross a cell. Lower is better |
| **Distance-only route** | The shortest route by geometry that only avoids blocked cells |
| **Traffic-aware route** | A route that minimizes `J(P)` using your cell costs |
| **Held-out data** | Data the model never trained on, used for honest evaluation |
| **Macro F1** | An F1 score averaged equally over all classes, so rare classes count |
| **Confusion matrix** | A table of true class versus predicted class |
| **Error analysis** | Studying where and why the model is wrong |
| **Missed hazard** | A truly blocked cell that the model predicted as not blocked |
| **Baseline** | A simple reference result you must beat |
| **KPI** | A measure the city would track to see if the service works |

---

## 13. Questions?

Ask an organizer or mentor. For the full problem statement, scoring, and deliverables, see the Project RUSH HOUR challenge brief.

*Good luck, drivers.*
