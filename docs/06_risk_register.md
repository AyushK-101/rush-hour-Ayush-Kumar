# Risk register: Hyderabad Deployment

| # | Risk | Likelihood | Impact | Early Warning Sign | Mitigation | Owner |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | Model misses a blocked road (e.g. flyover construction / waterlogging) | Medium | High | Vehicle speed drops to 0 km/h on suggested route | Set safety threshold $\tau = 0.18$ (95.0% recall); pilot visual override; HTP live integration | AI Engineering & 108 Ops |
| **2** | Telemetry or traffic sensor feed fails / becomes stale | Low | High | Feed latency exceeds 60 seconds | Automatic watchdog fails over to static offline GIS shortest path | GHMC IT & Cloud Vendor |
| **3** | Dispatchers over-rely on AI recommendations | Medium | Medium | Override rate drops below 3%; dispatchers ignore local flooding reports | Mandatory interactive training; random route challenge drills | Dispatch Training Lead |
| **4** | Uneven sensor coverage between IT Corridor and Old City | Medium | Medium | Prediction variance spikes in older municipal circles | Augment static map priors; deploy mobile cellular probe telemetry | Hyderabad Traffic Police & GHMC |
| **5** | Location-data privacy & patient confidentiality | Low | Medium | Concerns regarding live GPS tracking | Anonymize CAD coordinate logs; purge personal identifiers after 30 days | Telangana State Legal Directorate |
| **6** | Network partition severs cross-town corridor | Low | High | Dijkstra returns infinite cost / zero path found | Adaptive threshold relaxation ($\tau = 0.30$) combined with high cost penalty | Routing Systems Engineer |

---

## Manual fallback
When cloud services or cellular connectivity in Hyderabad experience downtime:
1. In-cab navigation tablets immediately transition to **Offline Autonomous GIS Mode**.
2. Preloaded offline OpenStreetMap topological maps compute standard shortest-distance routes using vehicle GPS.
3. The 108 dispatch center switches to verbal VHF radio dispatch protocols with zero disruption to active emergencies.

---

## Link to the technical results
On the completely held-out city benchmark (Map 5), naive argmax classification missed **89 blocked cells** (endangering emergency crews). Our cost-sensitive blocking policy ($\tau = 0.18$) captured **95.0% of all blocked hazards**, reducing missed hazards to just **24 cells** across the 3,600-cell grid (sourced directly from `results/metrics/ml_metrics.json`).
