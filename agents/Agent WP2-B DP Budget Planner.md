# WP2-B — DP Budget Planner Agent

## Identity
| Field | Value |
|---|---|
| **ID** | WP2-B |
| **Name** | Differential Privacy Budget Planner Agent |
| **WP** | WP2 (active throughout WP4, WP5, WP6) |
| **RQ Addressed** | RQ4 |
| **Type** | On-demand + Continuous monitoring |
| **Status** | Planned |

---

## Purpose
Given a system configuration (number of queries per user per day, sensitivity of each query type, and target ε_max), computes a feasible differential privacy budget allocation schedule. Monitors live budget expenditure per user and prevents budget exhaustion events. This agent bridges the privacy requirements defined in WP2 into the operational reality of WP4 and WP5.

---

## Inputs
| Source | Description |
|---|---|
| Query plan | List of query types (HGNN training, inference, P2P sharing), their sensitivities (Δf), and expected daily frequencies |
| Per-user ε_max, δ budget | Configured privacy budget ceiling per user |
| DP mechanism spec | Which mechanism per query: Gaussian, Laplace, DP-SGD, Rényi DP, zCDP |
| Live expenditure log | Running (ε, δ) consumed per user from WP4-A and WP5-C |

---

## Outputs
| Artifact | Description |
|---|---|
| Budget schedule | Per-query-type allocation of ε/δ fraction, per user, per time window |
| Exhaustion forecast | Predicted time-to-budget-exhaustion per user under current query rates |
| Throttle signal | Alert to WP4-A or WP5-C to defer/reject queries approaching budget ceiling |
| Composition report | Rényi DP / zCDP composition calculation with formal guarantees |
| Compliance certificate | Per-user DP compliance record for KPI M-PRI-01 |

---

## Core Behaviour
1. **Budget initialisation** — at session/day start, initialises per-user (ε, δ) ledger
2. **Composition calculation** — applies Rényi DP or zCDP composition rules to compute cumulative privacy loss across query sequence
3. **Schedule optimisation** — given daily query plan, allocates budget to maximise utility (model accuracy) while respecting ε_max
4. **Live monitoring** — intercepts each query event, deducts from ledger, checks against ceiling
5. **Throttling** — when remaining budget < threshold, signals WP4-A to skip model update or WP5-C to suppress P2P data sharing for that user
6. **Renewal** — resets budget at configurable window boundary (daily, weekly) per user policy

---

## Technologies
- Google DP library / OpenDP / IBM Diffprivlib (composition accounting)
- Rényi DP / zCDP accountant (PRV accountant preferred for tight bounds)
- Time-series ledger (InfluxDB or SQLite per-user log)
- Vikunja / alert webhook for budget exhaustion notifications

---

## Interfaces
| Agent / System | Direction | Description |
|---|---|---|
| WP4-A Preference Inference Agent | ↔ | Deducts budget per HGNN query; receives throttle signal |
| WP5-C Negotiation Agent | ↔ | Deducts budget per P2P data share; enforces LDP before transmission |
| WP2-A Requirements Consistency Agent | ↔ | Co-validates that budget allocation satisfies NFR3 |
| WP6-A KPI Monitor Agent | → | Reports M-PRI-01 (DP budget compliance rate) |

---

## KPIs Contributed
- **M-PRI-01:** DP Budget Compliance Rate (primary output)
- **M-PRI-03:** LDP Utility-Privacy Trade-off (informs allocation decisions)
- **CS-3:** Privacy-Utility Balance Score (PUBS)

---

## Implementation Notes
- Budget exhaustion is a **silent failure** if not monitored — this agent must exist and be operational before WP4 HGNN training begins, not retrofitted later
- Rényi DP composition is tighter than basic (ε, δ) composition — prefer PRV accountant (Gopi et al. 2021) for DP-SGD budget tracking
- Per-user granularity is important: aggregate budget tracking is insufficient for GDPR individual rights compliance
- Open question: what happens when a user exhausts their budget mid-session? Define graceful degradation behaviour (fall back to last committed preference, no new inference)
- ε_max values need to be agreed with a privacy expert and documented in T2.1 NFR3 before WP4 implementation starts
