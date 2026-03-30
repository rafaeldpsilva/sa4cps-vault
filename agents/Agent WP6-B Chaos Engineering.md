# WP6-B — Chaos Engineering Agent

## Identity
| Field | Value |
|---|---|
| **ID** | WP6-B |
| **Name** | Chaos Engineering Agent |
| **WP** | WP6 |
| **RQ Addressed** | RQ0 |
| **Type** | Scheduled + On-demand |
| **Status** | Planned |

---

## Purpose
Injects controlled failures into the running system to measure resilience, validate recovery procedures, and produce MTTR data for M-SCL-02 and M-WP3-04. Runs predefined chaos scenarios on the K8s cluster and Digital Twin, measuring the system's ability to recover to nominal operation without human intervention. Used in WP6 DT validation phase before real pilot deployment.

---

## Inputs
| Source | Description |
|---|---|
| Chaos scenario catalogue | Predefined failure scenarios per component (see below) |
| System health baseline | Pre-fault KPI readings from WP6-A (to detect recovery) |
| K8s cluster access | API access to kill pods, inject network latency, partition namespaces |
| WP6-A KPI Monitor | Continuous health signal to detect when recovery is complete |
| Test schedule | Which scenarios run when (manual trigger or cron schedule) |

---

## Outputs
| Artifact | Description |
|---|---|
| MTTR measurement | Per-component mean time to recover (M-SCL-02) |
| Recovery trace | Full timeline: fault injection → degraded state → recovery detected |
| Offline availability result | P2P negotiation success rate during simulated central service outage (M-SCL-03) |
| Resilience report | Structured report per scenario: fault type, duration, impact, recovery time |
| Go/No-go signal | Whether system meets resilience NFRs before real pilot deployment |

---

## Chaos Scenario Catalogue

| Scenario ID | Target Component | Failure Mode | Recovery Target |
|---|---|---|---|
| CHAOS-01 | WP3-B DT Sync | Process kill | MTTR ≤ 30 s |
| CHAOS-02 | Kafka broker | Broker shutdown | MTTR ≤ 60 s |
| CHAOS-03 | WP5-A Building Unit | Pod kill (one agent) | MTTR ≤ 10 s (K8s restart) |
| CHAOS-04 | WP4-A HGNN service | OOM kill | MTTR ≤ 30 s |
| CHAOS-05 | Network | Partition central services | P2P avail ≥ 70% (M-SCL-03) |
| CHAOS-06 | Sensor stream | Kafka topic unavailable | DT graceful degradation |
| CHAOS-07 | WP5-C Negotiation | Deadlock injection | Escalation to WP5-B ≤ 60 s |
| CHAOS-08 | All | 30% node failure | System availability ≥ 99% sustained |

---

## Core Behaviour
1. **Pre-fault snapshot** — records current KPI baseline from WP6-A before injection
2. **Fault injection** — executes the fault action (K8s pod kill, tc netem network delay/loss, iptables block, Kafka topic deletion)
3. **Impact measurement** — monitors system behaviour during fault: which KPIs degrade, by how much, for how long
4. **Recovery detection** — polls WP6-A health signal until all relevant KPIs return to within 10% of baseline
5. **MTTR recording** — timestamps fault injection and recovery detection; computes MTTR
6. **State restoration** — confirms system is fully healthy before next scenario
7. **Report generation** — produces structured per-scenario resilience report

---

## Technologies
- Chaos Monkey / Litmus Chaos / custom K8s pod kill scripts
- `tc netem` (Linux network emulation: latency, packet loss, partition)
- `iptables` (network partition rules)
- Kubernetes Python client (pod deletion, namespace isolation)
- Prometheus / WP6-A (health monitoring during faults)

---

## Interfaces
| Agent / System | Direction | Description |
|---|---|---|
| Kubernetes cluster | ↔ | Fault injection and monitoring |
| WP6-A KPI Monitor | ← | Health signal for recovery detection |
| WP5-C Negotiation Agent | ← | Observes P2P behaviour during CHAOS-05 |
| WP3-B DT Sync | ← | Observes recovery behaviour during CHAOS-01 |
| Researcher | → | Resilience reports for WP6 evaluation deliverable |

---

## KPIs Contributed
- **M-WP3-04:** Digital Twin Recovery Time (CHAOS-01)
- **M-SCL-02:** Component Fault Recovery Time (all CHAOS scenarios)
- **M-SCL-03:** P2P Offline Availability (CHAOS-05)
- **M-SCL-04:** System Availability (CHAOS-08)

---

## Implementation Notes
- NEVER run chaos scenarios on a live production pilot — only on the K8s test cluster (caravel nodes: 10.8.91.x via VPN) or DT simulation environment
- Network partition scenarios (CHAOS-05) are the most important for validating the P2P offline mode claim (RQ4) — prioritise these in WP6 testing schedule
- CHAOS-07 (deadlock injection) requires injecting a synthetic negotiation partner that refuses to converge — implement a stub "adversarial agent" that always counter-offers without accepting
- Each scenario should be run ≥ 5 times to compute a mean MTTR with variance — single runs are not statistically meaningful
- The Go/No-go signal is a formal gate before real pilot deployment: if any component fails to meet its MTTR target, fix before deploying with real occupants
