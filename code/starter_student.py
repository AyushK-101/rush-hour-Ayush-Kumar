# -*- coding: utf-8 -*-
"""
Project RUSH HOUR - Starter Code & Core Algorithms
Includes:
- Feature extraction and model training (Soft-Voting Ensemble: RF + HistGradientBoosting)
- Safety-first blocking policy (cost-sensitive thresholding tau=0.18)
- Probabilistic cell cost function balancing congestion & incident risk
- Traffic-aware Dijkstra path planner enforcing 8-connectivity and corner-cutting avoidance
- Route metrics evaluation (geometric length and objective cost)
"""

import argparse
import heapq
import json
import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier, VotingClassifier
from sklearn.metrics import accuracy_score, f1_score, recall_score, confusion_matrix

CLASS_ORDER = ['free_flow', 'congested', 'blocked']
BASE_FEATURES = [
    'avg_speed_kmh',
    'signal_delay_sec',
    'traffic_density_0_1',
    'intersection_density_0_1',
    'incident_probability_0_1'
]
ROAD_TYPES = ['highway', 'arterial', 'collector', 'residential']

def preprocess_features(df):
    """Extract numerical features and one-hot encode road_type deterministically."""
    X_num = df[BASE_FEATURES].copy()
    for rt in ROAD_TYPES:
        X_num[f'road_type_{rt}'] = (df['road_type'] == rt).astype(float)
    return X_num

def train_model(train_df):
    """Train the Soft-Voting Ensemble (RandomForest + HistGradientBoosting)."""
    X = preprocess_features(train_df)
    y = train_df['congestion_label']
    
    rf = RandomForestClassifier(n_estimators=100, max_depth=12, class_weight='balanced', random_state=42)
    hgb = HistGradientBoostingClassifier(max_iter=100, max_depth=6, class_weight='balanced', random_state=42)
    
    ensemble = VotingClassifier(
        estimators=[('rf', rf), ('hgb', hgb)],
        voting='soft'
    )
    ensemble.fit(X, y)
    return ensemble

def evaluate_model(model, val_df):
    """Compute held-out metrics on validation data."""
    X_val = preprocess_features(val_df)
    y_true = val_df['congestion_label'].values
    
    y_pred = model.predict(X_val)
    probs = model.predict_proba(X_val)
    
    blocked_col = list(model.classes_).index('blocked')
    p_blocked = probs[:, blocked_col]
    
    acc = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average='macro')
    rec_blocked_argmax = recall_score(y_true == 'blocked', y_pred == 'blocked')
    
    is_blocked = (y_true == 'blocked')
    missed_argmax = int(np.sum(is_blocked & (y_pred != 'blocked')))
    
    # Cost-sensitive tau = 0.18
    tau = 0.18
    rec_blocked_tau = float(np.sum(is_blocked & (p_blocked >= tau)) / np.sum(is_blocked))
    missed_tau = int(np.sum(is_blocked & (p_blocked < tau)))
    
    cm = confusion_matrix(y_true, y_pred, labels=CLASS_ORDER)
    
    metrics = {
        'accuracy': float(acc),
        'macro_f1': float(macro_f1),
        'recall_blocked_argmax': float(rec_blocked_argmax),
        'missed_blocked_argmax': missed_argmax,
        'recall_blocked_tau018': rec_blocked_tau,
        'missed_blocked_tau018': missed_tau,
        'confusion_matrix': cm.tolist(),
        'classes': CLASS_ORDER
    }
    return metrics

def predict_scenario(model, scenario_df):
    """Predict class probabilities and labels for a scenario grid."""
    X_scen = preprocess_features(scenario_df)
    probs = model.predict_proba(X_scen)
    
    cls_list = list(model.classes_)
    idx_free = cls_list.index('free_flow')
    idx_cong = cls_list.index('congested')
    idx_block = cls_list.index('blocked')
    
    out = scenario_df[['row', 'col']].copy()
    out['p_free_flow'] = probs[:, idx_free]
    out['p_congested'] = probs[:, idx_cong]
    out['p_blocked'] = probs[:, idx_block]
    
    preds_idx = np.argmax(probs, axis=1)
    out['predicted_label'] = [cls_list[i] for i in preds_idx]
    
    # Merge incident_probability_0_1 and avg_speed for cost calculation
    out['incident_probability_0_1'] = scenario_df['incident_probability_0_1'].values
    out['avg_speed_kmh'] = scenario_df['avg_speed_kmh'].values
    return out

def blocking_policy(pred_df, tau=0.18):
    """
    Determine 60x60 boolean mask of blocked cells.
    A cell is marked blocked if:
    - p_blocked >= tau (safety-first threshold based on Bayesian decision theory), OR
    - predicted_label == 'blocked'
    """
    grid = np.zeros((60, 60), dtype=bool)
    is_blocked_cell = (pred_df['p_blocked'] >= tau) | (pred_df['predicted_label'] == 'blocked')
    for (r, c, b) in zip(pred_df['row'], pred_df['col'], is_blocked_cell):
        grid[int(r), int(c)] = bool(b)
    return grid

def cell_cost(pred_df):
    """
    Compute a 60x60 grid of traversal costs.
    Formulation:
    c(u) = p_free * c_free + p_cong * c_cong + p_block * c_block + alpha * incident_prob
    where baseline empirical costs from training data are:
    c_free = 1.0, c_cong = 3.5, c_block = 13.0, alpha = 2.0
    """
    cost_grid = np.zeros((60, 60), dtype=float)
    
    c_free = 1.0
    c_cong = 3.5
    c_block = 13.0
    alpha = 2.0
    
    exp_cost = (
        pred_df['p_free_flow'] * c_free +
        pred_df['p_congested'] * c_cong +
        pred_df['p_blocked'] * c_block +
        alpha * pred_df['incident_probability_0_1']
    )
    
    for (r, c, val) in zip(pred_df['row'], pred_df['col'], exp_cost):
        cost_grid[int(r), int(c)] = float(val)
    return cost_grid

def shortest_path(blocked_mask, start, goal, cost_grid=None):
    """
    Dijkstra shortest path on 60x60 grid.
    If cost_grid is None, computes distance-only shortest path (c(u) = 1.0 everywhere).
    Respects 8-connectivity and prevents diagonal corner-cutting past blocked cells.
    Edge cost formula: d(u, v) * (c(u) + c(v)) / 2
    """
    start = tuple(start)
    goal = tuple(goal)
    
    if blocked_mask[start[0], start[1]] or blocked_mask[goal[0], goal[1]]:
        return None, float('inf')
        
    R, C = blocked_mask.shape
    dist = {start: 0.0}
    parent = {start: None}
    pq = [(0.0, start)]
    visited = set()
    
    # 8 directional neighbors: (dr, dc)
    dirs = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]
    
    while pq:
        curr_d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        
        if u == goal:
            # Reconstruct path
            path = []
            curr = goal
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
            return path, curr_d
            
        ur, uc = u
        for dr, dc in dirs:
            vr, vc = ur + dr, uc + dc
            if 0 <= vr < R and 0 <= vc < C:
                if blocked_mask[vr, vc]:
                    continue
                
                # Diagonal corner-cutting check:
                # If moving diagonally, both orthogonal cells (ur+dr, uc) and (ur, uc+dc) must NOT be blocked.
                if dr != 0 and dc != 0:
                    if blocked_mask[ur + dr, uc] or blocked_mask[ur, uc + dc]:
                        continue
                    step_d = math.sqrt(2.0)
                else:
                    step_d = 1.0
                    
                v = (vr, vc)
                if cost_grid is not None:
                    cu = cost_grid[ur, uc]
                    cv = cost_grid[vr, vc]
                    step_cost = step_d * (cu + cv) / 2.0
                else:
                    step_cost = step_d * 1.0 # distance-only
                    
                new_d = curr_d + step_cost
                if v not in dist or new_d < dist[v]:
                    dist[v] = new_d
                    parent[v] = u
                    heapq.heappush(pq, (new_d, v))
                    
    return None, float('inf')

def route_metrics(path, cost_grid):
    """Calculate geometric length and objective cost J(P)."""
    if not path or len(path) < 2:
        return 0.0, 0.0
    length = 0.0
    cost = 0.0
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        dr = abs(u[0] - v[0])
        dc = abs(u[1] - v[1])
        d = math.sqrt(2.0) if (dr == 1 and dc == 1) else 1.0
        length += d
        cu = cost_grid[u[0], u[1]]
        cv = cost_grid[v[0], v[1]]
        cost += d * (cu + cv) / 2.0
    return round(length, 2), round(cost, 2)

def plan_distance_only(blocked_mask, start, goal, cost_grid):
    """Plan distance-only route and evaluate under objective cost_grid."""
    path, _ = shortest_path(blocked_mask, start, goal, cost_grid=None)
    length, cost = route_metrics(path, cost_grid)
    return path, length, cost

def plan_traffic_aware(blocked_mask, start, goal, cost_grid):
    """Plan traffic-aware route minimizing J(P)."""
    path, _ = shortest_path(blocked_mask, start, goal, cost_grid=cost_grid)
    length, cost = route_metrics(path, cost_grid)
    return path, length, cost

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run Project RUSH HOUR engine")
    parser.add_argument('--scenario', type=str, default='RUSH-1', choices=['RUSH-1', 'RUSH-2', 'RUSH-3'])
    parser.add_argument('--tau', type=float, default=0.18, help="Safety blocking threshold")
    args = parser.parse_args()
    
    print(f"Loading training data...")
    train_df = pd.read_csv('train_cells_capped.csv')
    
    # Split: Train on maps 0-4, validate on map 5
    tr = train_df[train_df['map_id'] < 5]
    te = train_df[train_df['map_id'] == 5]
    
    print(f"Training Soft-Voting Ensemble (RandomForest + HistGradientBoosting)...")
    model = train_model(tr)
    metrics = evaluate_model(model, te)
    print(f"Held-out Validation on Map 5:")
    print(f"  Accuracy: {metrics['accuracy']:.4f}")
    print(f"  Macro F1: {metrics['macro_f1']:.4f}")
    print(f"  Recall for Blocked (Argmax): {metrics['recall_blocked_argmax']:.4f}")
    print(f"  Recall for Blocked (Tau=0.18): {metrics['recall_blocked_tau018']:.4f}")
    print(f"  Missed Blocked Cells (Argmax): {metrics['missed_blocked_argmax']}")
    print(f"  Missed Blocked Cells (Tau=0.18): {metrics['missed_blocked_tau018']}")
    
    with open('data/scenarios/scenarios.json') as f:
        scenarios = json.load(f)
    scen_info = scenarios[args.scenario]
    scen_csv = f"data/scenarios/{scen_info['map']}"
    scen_df = pd.read_csv(scen_csv)
    
    print(f"Predicting scenario {args.scenario}...")
    preds = predict_scenario(model, scen_df)
    blocked = blocking_policy(preds, tau=args.tau)
    costs = cell_cost(preds)
    
    start, goal = scen_info['start'], scen_info['goal']
    p_dist, len_dist, cost_dist = plan_distance_only(blocked, start, goal, costs)
    p_traf, len_traf, cost_traf = plan_traffic_aware(blocked, start, goal, costs)
    
    print(f"\n--- Scenario {args.scenario} Results ---")
    print(f"Distance-Only:  Length = {len_dist:.2f}, Cost = {cost_dist:.2f}")
    print(f"Traffic-Aware:  Length = {len_traf:.2f}, Cost = {cost_traf:.2f}")
    cost_diff = ((cost_traf - cost_dist) / cost_dist) * 100
    len_diff = ((len_traf - len_dist) / len_dist) * 100
    print(f"Objective Cost Reduction: {abs(cost_diff):.1f}% (Extra Distance: {len_diff:+.1f}%)")


