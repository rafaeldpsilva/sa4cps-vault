# WP3-B — Digital Twin Synchronization Agent

## Identity
| Field | Value |
|---|---|
| **ID** | WP3-B |
| **Name** | Digital Twin Synchronization Agent |
| **WP** | WP3 |
| **RQ Addressed** | RQ0 |
| **Type** | Continuous |
| **Status** | Planned |

---

## Purpose
Maintains the live Digital Twin (DT) state as a consistent, queryable graph representing the physical building: zones, sensors, actuators, occupancy, and their current values. Detects state divergence between the DT and the physical building, and orchestrates recovery when failures occur — targeting MTTR ≤ 30 seconds.

---

## Inputs
| Source | Description |
|---|---|
| WP3-A (LDP-perturbed events) | Validated sensor readings on DT ingestion Kafka topic |
| Actuator command log | Commands issued by WP5-A agents (to update DT actuator state) |
| Health-check signals | Liveness probes from all system components |
| Snapshot store | Last known good DT state (for recovery) |

---

## Outputs
| Artifact | Description |
|---|---|
| Live DT state | Graph-structured current state of building: nodes (zones, sensors, actuators, users), edges (relationships, readings) |
| State snapshot | Periodic serialised checkpoint of full DT state |
| Divergence alert | Notification when DT state deviates from expected physical state beyond threshold |
| Recovery confirmation | Signal when full state restoration is complete after failure |
| REST API | `/state/{zone}`, `/state/full`, `/snapshot` endpoints for agent consumption |

---

## Core Behaviour
1. **Event consumption** — subscribes to DT ingestion Kafka topic; processes events in order
2. **Graph update** — applies each sensor event as a node/edge attribute update in the DT graph
3. **Actuator state tracking** — updates actuator nodes when WP5-A issues commands (pre-emptive update before physical confirmation)
4. **Consistency check** — periodically compares DT state against incoming sensor values; flags divergence > 2% of full-scale range (M-WP3-03)
5. **Snapshot management** — writes full DT state snapshot to persistent store every N seconds (configurable); enables rapid recovery
6. **Failure recovery** — on process restart or network partition recovery: loads latest snapshot, replays Kafka events from checkpoint offset, confirms consistency → signals recovery complete
7. **State API** — serves current DT state to WP4-A, WP5-A, WP5-E, WP3-C via REST

---

## Technologies
- Neo4j or in-memory graph (NetworkX / RedisGraph) for DT state representation
- Apache Kafka (consumer)
- InfluxDB / TimescaleDB (time-series history for sensor readings)
- Redis (snapshot cache for fast recovery)
- FastAPI (REST API server)
- Kubernetes liveness/readiness probes

---

## Interfaces
| Agent / System | Direction | Description |
|---|---|---|
| WP3-A Sensor Ingestion | ← | LDP-perturbed sensor events |
| WP5-A Building Unit Agent | ↔ | Reads current state; receives actuator command confirmations |
| WP5-E MCP Context Builder | → | Provides real-time state for MCP payload assembly |
| WP3-C Scenario Simulation | → | Provides base state for hypothetical scenario runs |
| WP6-A KPI Monitor | → | Exports M-WP3-03 (sync accuracy) and M-WP3-04 (recovery time) |

---

## KPIs Contributed
- **M-WP3-03:** Digital Twin State Synchronization Accuracy (target: MAE ≤ 2% full-scale)
- **M-WP3-04:** Digital Twin Recovery Time (target: MTTR ≤ 30 s)
- **M-SCL-04:** System Availability (DT uptime component)

---

## Implementation Notes
- Graph representation choice matters for WP4: if Neo4j is used here, it can serve double duty as the HGNN input graph store — reducing data duplication
- Snapshot frequency is a trade-off: more frequent = faster recovery but higher storage I/O; start with 60-second snapshots
- During network partition: DT must continue serving last-known state to WP5-A agents (stale-but-available), not block — document this degraded mode behaviour
- Kafka offset checkpointing is critical: agent must commit offsets only after successful graph update, not before (at-least-once semantics)
- Recovery target of <30 s requires snapshot loading + Kafka replay to be fast — test on actual K8s cluster (KubernetesMaster: 192.168.2.91) early
