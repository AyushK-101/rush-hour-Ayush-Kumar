# -*- coding: utf-8 -*-
import os
import json
import re

print("Running Project RUSH HOUR submission self-check...")

checks_passed = 0
checks_total = 0

def check(condition, message):
    global checks_passed, checks_total
    checks_total += 1
    if condition:
        checks_passed += 1
        print(f"[PASS] {message}")
    else:
        print(f"[FAIL] {message}")

# 1. Check code files
check(os.path.exists("code/starter_student.py"), "code/starter_student.py exists")
if os.path.exists("code/starter_student.py"):
    with open("code/starter_student.py", encoding="utf-8") as f:
        src = f.read()
    check("NotImplementedError" not in src, "No NotImplementedError left in code/starter_student.py")

check(os.path.exists("code/export_results.py"), "code/export_results.py exists")

# 2. Check metrics and routes
check(os.path.exists("results/metrics/ml_metrics.json"), "results/metrics/ml_metrics.json exists")
if os.path.exists("results/metrics/ml_metrics.json"):
    with open("results/metrics/ml_metrics.json") as f:
        m = json.load(f)
    check("accuracy" in m and "macro_f1" in m and "confusion_matrix" in m, "ml_metrics.json contains accuracy, macro_f1, and confusion_matrix")

check(os.path.exists("results/routes/RUSH-1_distance_only.csv"), "results/routes/RUSH-1_distance_only.csv exists")
check(os.path.exists("results/routes/RUSH-1_traffic_aware.csv"), "results/routes/RUSH-1_traffic_aware.csv exists")
check(os.path.exists("results/routes/RUSH-2_distance_only.csv"), "results/routes/RUSH-2_distance_only.csv exists")
check(os.path.exists("results/routes/RUSH-2_traffic_aware.csv"), "results/routes/RUSH-2_traffic_aware.csv exists")

# 3. Check figures
fig_count = len([f for f in os.listdir("results/figures") if f.endswith(".png") or f.endswith(".jpg")])
check(fig_count >= 1, f"results/figures/ contains figures (found {fig_count})")

# 4. Check presentation
pres_files = [f for f in os.listdir("presentation") if f.endswith(".pptx") or f.endswith(".pdf") or f.endswith(".key")]
check(len(pres_files) >= 1, f"presentation/ contains deck (found {pres_files})")

# 5. Check docs for [[FILL IN]] markers
docs = [
    "docs/01_technical_report.md",
    "docs/02_executive_summary.md",
    "docs/03_service_model_and_rollout.md",
    "docs/04_funding_and_cost_model.md",
    "docs/05_stakeholder_map.md",
    "docs/06_risk_register.md",
    "docs/07_assumptions_log.md"
]

all_docs_filled = True
for doc_path in docs:
    if os.path.exists(doc_path):
        with open(doc_path, encoding="utf-8") as f:
            content = f.read()
        if "[[FILL IN" in content:
            all_docs_filled = False
            print(f"  [WARN] {doc_path} has unfilled [[FILL IN]] markers")
    else:
        all_docs_filled = False
        print(f"  [FAIL] {doc_path} missing")
check(all_docs_filled, "All docs are complete with zero [[FILL IN]] markers remaining")

print(f"\nSelf-Check Summary: {checks_passed} / {checks_total} checks passed.")
if checks_passed == checks_total:
    print("ALL SUBMISSION CRITERIA SATISFIED!")

