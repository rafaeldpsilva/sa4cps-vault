# WP6-D — Experiment Replay Agent

## Identity
| Field | Value |
|---|---|
| **ID** | WP6-D |
| **Name** | Experiment Replay Agent |
| **WP** | WP6 |
| **RQ Addressed** | RQ0, RQ1, RQ2, RQ3, RQ4 |
| **Type** | On-demand (batch) |
| **Status** | Planned |

---

## Purpose
Given a predefined experimental scenario (or a recorded real event from the Digital Twin), replays it with different agent configurations — enabling controlled A/B comparisons without requiring a real pilot. The primary mechanism for evaluating competing approaches (HGNN vs. baselines, DP vs. no-DP, different autonomy thresholds) in a reproducible, controlled setting. Critical for generating Paper 3, 4, and 5 evaluation data.

---

## Inputs
| Source | Description |
|---|---|
| Scenario definition | Structured scenario: initial DT state + event sequence + synthetic user preference profiles |
| Configuration matrix | Set of agent configurations to compare: `[(model_type, DP_on, autonomy_level, ...]` |
| WP3-C Scenario Simulation | Executes each scenario replay using the simulation engine |
| WP3-B DT snapshot | Base state for scenario initialisation |
| Synthetic user profiles | Parameterised preference profiles (from WP4-C archetype library) |
| WP6-A KPI Monitor | Collects KPI outputs from each replay run |

---

## Outputs
| Artifact | Description |
|---|---|
| Per-configuration KPI results | Full KPI measurements for each configuration run in the matrix |
| A/B comparison table | Statistical comparison of KPIs across configurations (means, confidence intervals) |
| Best configuration recommendation | Configuration that maximises composite scores under constraints |
| Ablation study report | Contribution of each component (HGNN, DP, autonomy bounds) to overall performance |
| Reproducibility package | Seed, scenario definition, configuration, results — archived for paper appendix |

---

## Core Behaviour
1. **Scenario library** — maintains a catalogue of standard evaluation scenarios:
   - `SCN-01`: Multi-occupant thermal conflict (2 users, opposing preferences)
   - `SCN-02`: Preference drift (seasonal transition, 4-week simulation)
   - `SCN-03`: Service discovery (agent detects capability gap, deploys microservice)
   - `SCN-04`: P2P energy sharing (inter-unit resource negotiation under grid constraint)
   - `SCN-05`: User dialogue escalation (low-confidence preference, SLM elicitation)
   - `SCN-06`: System stress (50 concurrent agents, peak load)
   - `SCN-07`: Privacy attack (MIA evaluation against trained HGNN)
2. **Configuration sweep** — for each scenario, runs all configurations in the comparison matrix
3. **Replay execution** — per run:
   a. Initialise WP3-C with scenario base state and synthetic user profiles
   b. Inject event sequence (sensor readings, occupancy changes, user actions)
   c. Run agent under test configuration
   d. Collect all KPI measurements from WP6-A
   e. Reset to baseline state
4. **Statistical analysis** — computes means, standard deviations, 95% confidence intervals across N repeated runs (N ≥ 5 per configuration)
5. **Reproducibility** — fixes random seed per scenario; logs all parameters; packages results for paper reproducibility appendix

---

## Standard Evaluation Matrix (example)

| Config ID | Model | DP | Autonomy Level | Dialogue |
|---|---|---|---|---|
| C1 | Rule-based | Off | None | Off |
| C2 | Collab. filtering | Off | Low | Off |
| C3 | Homogeneous GNN | Off | Medium | Off |
| C4 | **HGNN (proposed)** | Off | Medium | Off |
| C5 | **HGNN (proposed)** | **On (ε=1)** | Medium | Off |
| C6 | **HGNN (proposed)** | **On (ε=1)** | **High** | **On** |
| C7 | **HGNN (proposed)** | **On (ε=0.5)** | **High** | **On** |

C6 = full proposed system; C1 = simplest baseline; C4–C7 = ablation.

---

## Technologies
- WP3-C Scenario Simulation (execution engine)
- WP6-A KPI Monitor (metric collection during replays)
- Python (orchestration, statistical analysis — scipy.stats)
- DVC (Data Version Control) or MLflow (experiment tracking and reproducibility)
- Jupyter notebooks (result visualisation for paper figures)

---

## Interfaces
| Agent / System | Direction | Description |
|---|---|---|
| WP3-C Scenario Simulation | ↔ | Executes each scenario replay |
| WP3-B DT Sync Agent | ← | Provides base state snapshots for scenario initialisation |
| WP6-A KPI Monitor | ← | Collects KPI data during each replay run |
| Researcher (Papers 3, 4, 5) | → | A/B comparison tables, ablation results, figures |

---

## KPIs Contributed
Validates all primary KPIs for the DT-measurable subset:
- **M-WP4-01** through **M-WP4-06** (model quality — SCN-01, SCN-02, SCN-07)
- **M-WP5-06** through **M-WP5-11** (agent performance — SCN-03, SCN-04, SCN-05, SCN-06)
- **M-PRI-01** through **M-PRI-04** (privacy — SCN-07)
- **M-SCL-01** through **M-SCL-04** (scalability — SCN-06)

---

## Implementation Notes
- This agent is the **primary tool for thesis evaluation claims** that cannot wait for a real pilot — invest in it early
- Synthetic user profiles must be realistic: use the WP4-C archetype library + parameterised Big Five distributions; document the generation methodology in the paper
- Statistical rigor: N ≥ 5 runs per configuration is the minimum; N ≥ 10 is preferable for variance estimation — factor this into WP6 compute budget on the caravel cluster
- DVC or MLflow tracking is essential: without it, it becomes impossible to reproduce a specific result from a prior run when a reviewer asks
- SCN-07 (MIA evaluation) is the most compute-intensive: training shadow models requires significant GPU time — schedule on mac (Mac Mini via Tailscale) or caravel GPU nodes if available
- Ablation table (C1–C7) is the core of Paper 3 and Paper 5 evaluation sections — design the matrix carefully and document it in the paper methodology before running
