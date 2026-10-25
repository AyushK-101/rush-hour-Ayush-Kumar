# Assumptions log: Hyderabad Context

All operational, financial, and clinical impact figures are illustrative assumptions grounded in public urban emergency benchmarks for Hyderabad.

| ID | Assumption | Value | Where Used | Source / Operational Rationale | If Wrong |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **A1** | Baseline Zone 1 Response Time | 14.5 minutes | Executive Summary, Rollout | Typical peak-hour emergency response in congested Hyderabad IT corridors | If lower (e.g. 12 min), percentage improvement translates to smaller absolute time savings |
| **A2** | Target Response Time | 11.5 minutes | KPIs, Executive Summary | Telangana Health Mission benchmark for urban emergency services | If unattainable, phased milestones must be extended by 3 months |
| **A3** | Value of 1-Minute Response Reduction | 10% survival gain | Cost Model, Consulting Report | Clinical emergency medicine resuscitation standards (AHA / Indian Resuscitation Council) | If lower (e.g. 5%), clinical ROI remains positive but less pronounced |
| **A4** | Pilot Operating Fleet | 40 Ambulances | Budget, Cost Model | Standard 108 ambulance deployment for Hitec City & Gachibowli circles (~800k pop.) | Budget scales proportionally with vehicle count |
| **A5** | Pilot Duration & Budget | 6 Months, ₹3.95 Cr | Rollout, Presentation | Standard municipal technology pilot budget under GHMC Smart City Mission | Phased milestones adapt to budgetary tranches |

---

## Modelling assumptions

| Choice | Value | Operational Justification |
| :--- | :--- | :--- |
| **Base Class Travel Costs** | Free: 1.0, Congested: 3.5, Blocked: 13.0 | Calibrated from empirical mean synthetic travel costs in `train_cells_capped.csv` |
| **Safety Blocking Threshold** | $\tau = 0.18$ | Bayesian decision boundary balancing 9-minute entrapment penalty vs 2-minute detour penalty |
| **Incident Risk Multiplier $\alpha$** | 2.0 | Imposes predictive caution around hazardous intersections before full blockages emerge |
| **Slide 85 Corner-Cutting Rule** | Both side cells open | Strictly enforced in Dijkstra graph search to prevent physical clipping past blocked corners |
