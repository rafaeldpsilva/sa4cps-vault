# WP3-D — External Integration Agent

## Identity
| Field | Value |
|---|---|
| **ID** | WP3-D |
| **Name** | External Integration Agent |
| **WP** | WP3 |
| **RQ Addressed** | RQ0 |
| **Type** | Continuous (event-driven) |
| **Status** | Planned |

---

## Purpose
Bridges external systems — smart grid (OpenADR), BMS (BACnet/MQTT), fire safety, and facility management — into the Digital Twin event stream. Translates protocol-specific signals into standardised DT events, enforcing strict latency requirements for safety-critical signals (≤ 50 ms for fire alarm / access control).

---

## Inputs
| Source | Description |
|---|---|
| Smart grid / OpenADR | Demand response signals, energy pricing, grid load events |
| BMS (BACnet/MQTT) | Facility-level HVAC, chiller, and electrical system data |
| Fire safety system | Fire alarm, smoke detector, emergency evacuation signals |
| Facility management system | Maintenance events, room booking, scheduled occupancy |
| Smart meter data | Real-time energy consumption per zone/unit |

---

## Outputs
| Artifact | Description |
|---|---|
| Normalised DT events | Translated signals in standard schema, published to Kafka DT topic |
| Emergency broadcast | High-priority event (fire alarm) published with guaranteed <50 ms latency to all WP5-A agents |
| Grid constraint signal | Demand response instruction forwarded to WP5-C negotiation layer |
| Maintenance event | Room unavailability or equipment fault published to DT state |

---

## Core Behaviour
1. **Protocol adapters** — maintains one adapter per external system type:
   - OpenADR: REST/XML polling or push listener
   - BACnet: BACnet/IP polling via bacpypes
   - Fire safety: dedicated MQTT topic with QoS 2 (exactly-once delivery)
   - Facility management: REST API poller
2. **Signal classification** — categorises incoming signals by urgency: Emergency / Operational / Informational
3. **Emergency path** — Emergency signals bypass normal Kafka pipeline and are published via a dedicated high-priority topic with < 50 ms SLA
4. **Schema normalisation** — translates protocol-specific payloads into the DT event schema (type, zone, value, timestamp, source, priority)
5. **Deduplication** — suppresses duplicate events within a configurable time window to prevent DT state thrashing
6. **Failure isolation** — external system failures do not propagate to DT; agent maintains last-known state per external source

---

## Technologies
- OpenADR 2.0 client library (oadr-ven)
- bacpypes (BACnet/IP adapter)
- Paho MQTT (fire safety and BMS MQTT topics)
- Apache Kafka (producer, with priority topic for emergency signals)
- Node-RED (optional orchestration of adapter pipelines)

---

## Interfaces
| Agent / System | Direction | Description |
|---|---|---|
| Smart grid / OpenADR | ← | Demand response and energy pricing signals |
| BMS, Fire Safety, Facility Mgmt | ← | Building infrastructure events |
| WP3-B DT Sync Agent | → | Normalised events for DT state update |
| WP5-C Negotiation Agent | → | Grid constraint / demand response signals for resource negotiation |
| WP5-A Building Unit Agent | → | Emergency broadcast (fire, evacuation) bypassing normal cycle |

---

## KPIs Contributed
- **M-WP3-01:** contributes to end-to-end ingestion latency (external signals component)
- **M-SCL-04:** System availability (external integration uptime)
- Safety constraint: Emergency signal latency must be ≤ 50 ms (hard requirement, not a KPI — a safety constraint)

---

## Implementation Notes
- The < 50 ms emergency path is a **hard safety requirement** — must be tested independently of the normal pipeline and validated via chaos testing in WP6
- BACnet polling interval needs calibration: too frequent causes network congestion, too infrequent misses fast-changing states; start at 1-second polling for HVAC, 100 ms for safety signals
- OpenADR integration enables the P2P energy trading use case (WP5-C) — document this dependency explicitly
- External system credentials and VPN access (gecadvpn.ovpn) must be available before integration testing begins
- Zero PII must be transmitted to external systems — agent must strip any user-identifiable fields before forwarding to BMS or grid
