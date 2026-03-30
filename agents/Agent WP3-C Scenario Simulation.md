# WP3-C — Scenario Simulation Agent

## Identity
| Field | Value |
|---|---|
| **ID** | WP3-C |
| **Name** | Scenario Simulation Agent |
| **WP** | WP3 |
| **RQ Addressed** | RQ0, RQ3 |
| **Type** | On-demand |
| **Status** | Planned |

---

## Purpose
Given a proposed actuator action or resource allocation decision from a WP5-A Building Unit Agent, runs a hypothetical scenario in an isolated copy of the Digital Twin — without affecting live state — and returns the predicted state delta and estimated comfort impact. Enables agents to reason about consequences before acting. Also used by WP6-D for A/B experiment replay.

---

## Inputs
| Source | Description |
|---|---|
| WP3-B DT state (snapshot) | Base state for the simulation (isolated copy) |
| Proposed action | Actuator command(s) to simulate (e.g., set zone A temperature to 21°C) |
| User preference vectors | From WP4-A, used to compute comfort impact of the simulated state |
| Simulation parameters | Duration (e.g., 30-minute horizon), occupancy forecast, weather forecast |

---

## Outputs
| Artifact | Description |
|---|---|
| Predicted state delta | Expected change in zone properties (temperature, CO₂, lux) over the simulation horizon |
| Comfort impact estimate | Per-user comfort score change under the proposed action |
| Energy estimate | Estimated energy consumption of the action |
| Conflict flag | Whether the proposed action creates preference conflicts with other occupants |
| Simulation trace | Full time-series of simulated DT state over horizon (for WP6-D replay) |

---

## Core Behaviour
1. **Snapshot fork** — creates an isolated in-memory copy of the current DT state (does not write to live graph)
2. **Action injection** — applies the proposed actuator command(s) to the forked state
3. **Physics model** — advances simulation over the specified horizon using a building physics model:
   - Thermal: simplified RC thermal model (configurable parameters per zone)
   - Air quality: CO₂ decay/accumulation model based on occupancy and ventilation rate
   - Lighting: lux calculation based on blind position and artificial light level
4. **Comfort scoring** — at each time step, evaluates per-user comfort using current preference vectors from WP4-A
5. **Energy estimation** — integrates power consumption of activated actuators over horizon
6. **Conflict detection** — checks if simulated state violates any other occupant's preference bounds
7. **Result return** — packages results and returns to requesting WP5-A agent within latency budget

---

## Technologies
- Python-based building physics simulation (custom RC thermal model, or EnergyPlus co-simulation for WP6)
- Fork of WP3-B graph state (in-memory copy via deepcopy or Redis snapshot)
- EnergyPlus for high-fidelity WP6 energy validation (offline, not real-time)
- gRPC or REST call interface for WP5-A integration

---

## Interfaces
| Agent / System | Direction | Description |
|---|---|---|
| WP3-B DT Sync Agent | ← | Receives base state snapshot |
| WP5-A Building Unit Agent | ← | Receives proposed action; returns simulation result |
| WP4-A Preference Inference Agent | ← | Receives current user preference vectors for comfort scoring |
| WP6-D Experiment Replay Agent | ← | Receives scenario replay requests; returns full simulation traces |

---

## KPIs Contributed
- Enables pre-decision quality assessment for M-WP5-06 (decision latency — simulation must complete within the 2s cycle)
- Supports M-USR-01 (comfort) and M-USR-05 (energy) by providing counterfactual estimates
- Enables WP6 A/B comparisons without a real pilot (measurability of DT-only KPIs)

---

## Implementation Notes
- Simulation must complete fast enough to be useful within the WP5-A decision cycle (P95 ≤ 2000 ms total) — the simulation itself should target ≤ 500 ms for a 30-minute horizon
- The building physics model parameters (thermal mass, HVAC capacity, etc.) need calibration against real building data or manufacturer specs — document in WP3 technical report
- For WP6 high-fidelity validation: EnergyPlus co-simulation is the right tool but runs offline (not real-time); use it for Paper 2 energy claims, not for live agent decisions
- Open question: how to model occupant behaviour (arrival/departure patterns) within the simulation horizon? Consider Poisson process model per zone
