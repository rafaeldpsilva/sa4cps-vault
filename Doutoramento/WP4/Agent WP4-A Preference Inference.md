# WP4-A — Preference Inference Agent

## Identity
| Field | Value |
|---|---|
| **ID** | WP4-A |
| **Name** | Preference Inference Agent |
| **WP** | WP4 |
| **RQ Addressed** | RQ1 |
| **Type** | Continuous + Event-driven |
| **Status** | Planned |

---

## Purpose
The core ML agent of the system. Runs the trained Heterogeneous Graph Neural Network (HGNN) against the current user-context graph to produce preference predictions with associated confidence scores for each actuator dimension. Detects preference drift and triggers incremental model updates. This agent is the primary answer to RQ1.

---

## Inputs
| Source | Description |
|---|---|
| WP3-B DT state | Current building state graph (zones, sensors, actuators, occupancy) |
| User-preference graph | Heterogeneous graph: users, preferences, contexts, devices, sensors, activities |
| Feedback events | User-accepted / user-overridden actuator actions (implicit feedback) |
| Explicit feedback | User-provided preference ratings or dialogue-confirmed updates (from WP4-D) |
| WP2-B DP budget signal | Remaining (ε, δ) budget per user; governs whether inference / update is permitted |

---

## Outputs
| Artifact | Description |
|---|---|
| Preference vector | Per-user, per-dimension predicted preference: `{thermal: 22.5°C, lux: 400lux, CO₂: <800ppm, acoustic: low}` |
| Confidence scores | Per-dimension confidence (0–1); low confidence triggers WP4-D elicitation |
| Drift flag | Boolean signal when HR@5 degrades > 5% over a sliding window |
| Updated graph | Incrementally updated user-preference graph after model update |

---

## Core Behaviour
1. **Graph assembly** — constructs the heterogeneous input graph from WP3-B DT state + persistent user graph
2. **HGNN forward pass** — runs inference through the trained HAN (Heterogeneous Attention Network):
   - Node types: Users, Preferences, Contexts, Zones, Devices, Sensors, Activities
   - Edge types: User→Preference, Preference→Context, User→Sensor interaction, Temporal, Spatial
   - Output: per-user preference embedding + predicted setpoints + confidence scores
3. **Confidence thresholding** — if confidence < threshold for any dimension, sets `elicitation_needed=true` → signals WP4-D
4. **Drift detection** — tracks HR@5 over a sliding window of N=50 feedback events; if HR@5 drops > 5%, sets `drift_flag=true`
5. **Incremental update** — on drift detection or explicit feedback: runs DP-SGD update step on affected subgraph only (not full retraining)
6. **Budget check** — before any inference or update, queries WP2-B; skips operation if budget exhausted for that user

---

## Technologies
- PyTorch Geometric (HGNN / HAN implementation)
- DP-SGD: Opacus library (PyTorch-compatible differentially private training)
- Neo4j or Apache Jena (user-preference graph store)
- FastAPI (preference query endpoint for WP5-A and WP5-E)
- MLflow or similar (model versioning and experiment tracking)

---

## Graph Schema
```
Nodes:
  User {id, personality_embedding, interaction_style, trust_level}
  Preference {dimension, value, confidence, timestamp}
  Context {time_of_day, season, activity_type, occupancy_density}
  Zone {id, current_temp, current_lux, current_co2}
  Device {id, type, current_state}
  Sensor {id, type, last_reading}
  Activity {type, typical_duration}

Edges:
  (User)-[:HAS_PREFERENCE]->(Preference)
  (Preference)-[:IN_CONTEXT]->(Context)
  (User)-[:INTERACTED_WITH]->(Sensor)
  (Zone)-[:CONTAINS]->(Sensor)
  (Zone)-[:CONTAINS]->(Device)
  (User)-[:LOCATED_IN]->(Zone)
  (Activity)-[:AFFECTS]->(Context)
```

---

## Interfaces
| Agent / System | Direction | Description |
|---|---|---|
| WP3-B DT Sync Agent | ← | Current building state for graph construction |
| WP2-B DP Budget Planner | ↔ | Budget check before inference; reports expenditure |
| WP4-B Conflict Detection Agent | → | Forwards multi-user preference vectors |
| WP4-C Relational Psychographics Agent | ← | Receives personality/interaction style embeddings for personalisation |
| WP4-D Preference Elicitation Dialogue Agent | ↔ | Signals low confidence; receives confirmed preference updates |
| WP5-A Building Unit Agent | → | Provides preference vector for actuator decision-making |
| WP5-E MCP Context Builder | → | Provides current preference state for MCP payload |
| WP6-A KPI Monitor | → | Reports M-WP4-01 (HR@5), M-WP4-03 (drift speed), M-WP4-05 (ECE) |

---

## KPIs Contributed
- **M-WP4-01:** Preference Prediction Accuracy — Implicit (HR@5 ≥ 80%) — **Primary**
- **M-WP4-02:** Preference Prediction Accuracy — Explicit (NDCG@5 ≥ 0.75) — **Primary**
- **M-WP4-03:** Preference Drift Adaptation Speed (≤ 10 interactions) — **Primary**
- **M-WP4-05:** Confidence Calibration Error (ECE ≤ 0.05)
- **M-WP4-06:** HGNN vs Baseline Improvement (≥ 15% relative gain) — **Primary**

---

## Implementation Notes
- HGNN inference target: < 1 second per user query (NFR1) — validate on caravel cluster under full graph scale (≥500 users, 1M edges)
- DP-SGD with Opacus requires per-sample gradient clipping — this is memory-intensive; test memory footprint on edge hardware (Raspberry Pi, 4 GB RAM) early
- Model versioning is critical: every incremental update must be tagged with the (ε, δ) expenditure so budget tracking remains consistent
- Graph scale test: ≥500 users, 10,000 sensor nodes, 1,000,000 edges — performance benchmarking is a WP6 deliverable
- Baseline models to train and compare against: rule-based controller, standard homogeneous GNN, collaborative filtering, LSTM encoder-decoder, Informer Transformer
