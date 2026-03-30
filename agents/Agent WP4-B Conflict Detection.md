# WP4-B — Conflict Detection Agent

## Identity
| Field | Value |
|---|---|
| **ID** | WP4-B |
| **Name** | Conflict Detection Agent |
| **WP** | WP4 |
| **RQ Addressed** | RQ1, RQ0 |
| **Type** | Event-driven (triggered by occupancy changes or preference updates) |
| **Status** | Planned |

---

## Purpose
Monitors preference vectors across co-located users and detects conflicting preferences (e.g., two occupants requiring incompatible thermal setpoints in the same zone). Computes Pareto-optimal compromise candidates and forwards them to the WP5-C negotiation layer or WP5-B escalation agent for resolution.

---

## Inputs
| Source | Description |
|---|---|
| WP4-A preference vectors | Per-user, per-dimension preference predictions with confidence scores |
| WP3-B DT state | Current zone occupancy — which users are co-located |
| Conflict resolution history | Previous conflict outcomes for the same user pairs (to improve future compromises) |
| Safety constraints | Hard bounds per zone (e.g., temperature must stay 18–26°C) |

---

## Outputs
| Artifact | Description |
|---|---|
| Conflict graph | Graph of conflicting user pairs per zone, with conflict dimension and severity |
| Pareto candidates | Set of Pareto-optimal compromise setpoints across conflicting preference dimensions |
| Conflict event | Structured event forwarded to WP5-B/WP5-C for resolution |
| Resolution signal | After WP5-C resolves: confirmation of accepted compromise, written back to preference graph |

---

## Core Behaviour
1. **Occupancy grouping** — queries DT for current zone occupancy; groups users by shared zone
2. **Pairwise conflict detection** — for each co-located user pair, checks if preference vectors are incompatible on any dimension:
   - Thermal: overlap check between individual comfort ranges
   - Lighting: range overlap check
   - CO₂/ventilation: range overlap
   - Acoustic: categorical conflict (one wants silence, another wants background noise)
3. **Conflict severity scoring** — scores severity as distance between conflicting preferences normalised by the safety constraint range
4. **Pareto front computation** — for N conflicting users in a zone, computes Pareto front across the preference space (multi-objective optimisation)
5. **Compromise generation** — selects top-K Pareto-optimal candidates; ranks by minimum total dissatisfaction (utilitarian criterion)
6. **Routing decision** — if a clear Pareto-dominant compromise exists: forwards to WP5-C for autonomous resolution; otherwise: forwards to WP5-B for escalation
7. **History update** — writes conflict and resolution outcome to persistent store for future learning

---

## Technologies
- NumPy / SciPy (multi-objective Pareto front computation — `scipy.optimize` or DEAP)
- NetworkX (conflict graph construction)
- Redis or SQLite (conflict resolution history)
- Kafka / gRPC (event publishing to WP5-B/C)

---

## Interfaces
| Agent / System | Direction | Description |
|---|---|---|
| WP4-A Preference Inference Agent | ← | Receives per-user preference vectors |
| WP3-B DT Sync Agent | ← | Queries current zone occupancy |
| WP5-B Escalation Agent | → | Forwards unresolvable conflicts for human escalation |
| WP5-C Negotiation Agent | → | Forwards Pareto candidates for autonomous multi-agent resolution |
| WP6-A KPI Monitor Agent | → | Reports M-WP4-04 (conflict resolution accuracy) |

---

## KPIs Contributed
- **M-WP4-04:** Multi-occupant Conflict Resolution Accuracy (≥ 70% Pareto-optimal outcomes) — **Primary**
- **M-USR-02:** Conflict Resolution Success Rate (≥ 65% autonomous + acceptable) — **Primary**

---

## Implementation Notes
- Multi-occupant conflict resolution is one of the key novelty claims of the thesis — ensure the Pareto-front computation method is well-documented and compared against baselines (majority vote, priority-based)
- For zones with > 2 conflicting users, Pareto front computation becomes expensive — consider approximate methods (NSGA-II) for performance at scale
- Conflict resolution history is a valuable dataset for Paper 5 — instrument from the beginning, not retrospectively
- Open question: how to handle asymmetric authority (e.g., a manager's preference overrides subordinates)? Document policy decision in T2.1 FR4 before implementation
- The distinction between "conflict resolvable autonomously" vs. "requires escalation" is a key design decision — needs formal threshold definition (ties into M-WP5-09 missed escalation rate)
