# WP3-A — Sensor Ingestion Agent

## Identity
| Field | Value |
|---|---|
| **ID** | WP3-A |
| **Name** | Sensor Ingestion Agent |
| **WP** | WP3 |
| **RQ Addressed** | RQ0 |
| **Type** | Continuous (stream processing) |
| **Status** | Planned |

---

## Purpose
Consumes raw sensor events from the building IoT layer (via MQTT broker or direct Kafka producer), validates schema, applies Local Differential Privacy (LDP) perturbation at the edge before forwarding to the Digital Twin, and monitors consumer lag to enforce the 500 ms end-to-end ingestion SLA.

---

## Inputs
| Source | Description |
|---|---|
| MQTT broker / Kafka producer | Raw sensor events: temperature (°C), humidity (%), CO₂ (ppm), occupancy (binary), lux (lux), door events |
| LDP configuration | Perturbation mechanism per sensor type (Laplace for continuous, randomised response for categorical), ε_sensor budget |
| Schema registry | Expected message schema per sensor type and topic |

---

## Outputs
| Artifact | Description |
|---|---|
| LDP-perturbed events | Sensor readings with privacy noise applied, published to downstream Kafka topic |
| Schema validation errors | Malformed events flagged to monitoring layer |
| Lag metrics | Per-topic consumer lag in ms, exported to Prometheus |
| Ingestion latency trace | P95 end-to-end timestamp delta (sensor emit → Kafka ack) |

---

## Core Behaviour
1. **Topic subscription** — subscribes to all sensor Kafka topics per building zone
2. **Schema validation** — validates each message against registered Avro/JSON schema; dead-letter queue for malformed messages
3. **LDP perturbation** — applies appropriate mechanism before data leaves the edge:
   - Continuous values (temp, humidity, CO₂, lux): Laplace mechanism with calibrated scale = Δf/ε_sensor
   - Categorical values (occupancy, door state): Randomised Response
4. **Lag monitoring** — continuously tracks consumer lag per partition; fires alert if lag > 100 ms
5. **Forwarding** — publishes perturbed events to the DT ingestion topic with original timestamp preserved
6. **One instance per zone** — horizontally scaled; one agent process per building zone or sensor cluster

---

## Technologies
- Apache Kafka (consumer + producer)
- MQTT bridge (Kafka Connect MQTT Source Connector or custom)
- Node-RED (optional edge preprocessing before Kafka)
- Google DP / IBM Diffprivlib (LDP mechanisms)
- Prometheus exporter (lag and latency metrics)
- Avro / JSON Schema registry

---

## Interfaces
| Agent / System | Direction | Description |
|---|---|---|
| Physical sensors / MQTT broker | ← | Raw sensor events |
| WP3-B DT Sync Agent | → | LDP-perturbed events on DT ingestion topic |
| WP2-B DP Budget Planner | ← | Receives LDP ε_sensor configuration; reports per-zone expenditure |
| WP6-A KPI Monitor Agent | → | Exports M-WP3-01 (ingestion latency) and M-WP3-02 (Kafka throughput) |

---

## KPIs Contributed
- **M-WP3-01:** Data Ingestion End-to-End Latency (target: P95 ≤ 500 ms)
- **M-WP3-02:** Kafka Throughput (target: ≥ 10,000 msgs/sec)
- **M-PRI-03:** LDP perturbation overhead (utility cost of noise)

---

## Implementation Notes
- LDP must be applied **at the edge** (before data leaves the building zone), not at the central broker — the agent must run co-located with or close to the sensor gateway
- Laplace scale parameter Δf/ε must be tuned per sensor type to balance privacy and utility — document calibration in T2.1 NFR3
- Dead-letter queue messages must be reviewed periodically; malformed sensor data can silently degrade DT accuracy
- For the Raspberry Pi edge target (≥4 GB RAM, ≥4-core ARM), Kafka consumer + LDP perturbation is feasible in Python; consider confluent-kafka-python for performance
- Performance target: process ≥10,000 msgs/sec aggregate across all zone agents on the K8s cluster
