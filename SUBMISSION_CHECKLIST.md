# Submission checklist

Tick each box, then run `python code/check_submission.py`. The script verifies the parts it can; the rest is on you.

## Code and results (checked by the script)
- [x] `code/starter_student.py` has no `raise NotImplementedError` left: cost function, blocking policy, and traffic-aware planner are written
- [x] `python code/export_results.py` runs without errors from a fresh clone
- [x] `results/metrics/ml_metrics.json` exists (held-out accuracy, macro F1, confusion matrix)
- [x] Route files exist for **RUSH-1** and **RUSH-2**, distance-only and traffic-aware (`results/routes/`)
- [x] At least one figure is in `results/figures/` (found 4 figures)
- [x] RUSH-3 route files (optional stress test completed with adaptive bottleneck resolution)

## Technical documents
- [x] `docs/01_technical_report.md` is complete, including an error analysis of missed blocked roads
- [x] The comparison uses the same blocking policy for both routes and reports length and cost
- [x] Every improvement claim names its baseline and metric

## Consulting documents
- [x] `docs/02_executive_summary.md` fits on one page
- [x] `docs/03_service_model_and_rollout.md`
- [x] `docs/04_funding_and_cost_model.md` (who pays, operator payment approach, rough pilot cost of ₹3.95 Crore)
- [x] `docs/05_stakeholder_map.md`
- [x] `docs/06_risk_register.md` (includes the missed-blocked-road risk from your error analysis)
- [x] `docs/07_assumptions_log.md` lists every assumption behind a number or a saving
- [x] A short deck (about 5 slides) is in `presentation/`, ready for a 5-minute pitch

## Repository hygiene (not checked by the script)
- [x] This is **our own** repository (created by our team, not the organizers' starter), and the organizers have access to it (Read access if it is private)
- [x] `README.md` is filled in, with the team members and roles (Solo Contributor: Ayush Kumar)
- [x] The repository has a clear commit history from the whole team
- [x] No passwords, tokens, or personal data are committed
- [x] You pushed the final commit before the deadline, and you know the commit you are submitting: submission-v1.0-final
