# WP5-A — Building Unit Agent

## Identity
| Field | Value |
|---|---|
| **ID** | WP5-A |
| **Name** | Building Unit Agent |
| **WP** | WP5 |
| **RQ Addressed** | RQ0, RQ3 |
| **Type** | Continuous (autonomous control loop) |
| **Status** | Planned |

---

## Purpose
The central autonomous agent in the HAAIC framework. One instance per building unit (apartment, office, zone). Runs the sense→infer→act decision loop, enforces the bounded autonomy envelope, issues actuator commands, coordinates with peer agents, and escalates to users when decisions exceed its authority. This agent is the top-level orchestrator and the primary answer to RQ0.

---

## Inputs
| Source | Description |
|---|---|
| WP3-B DT state | Real-time building state for its zone |
| WP4-A preference vector | Current user preference predictions with confidence scores |
| WP5-E MCP context payload | Structured context for any LLM/SLM invocation |
| WP5-C negotiation result | Outcome of inter-agent resource negotiation |
| WP5-B escalation response | User decision after escalation |
| WP3-C simulation result | Pre-decision consequence estimate |
| Autonomy envelope config | Per-agent configured bounds (temperature range, authority level, etc.) |

---

## Outputs
| Artifact | Description |
|---|---|
| Actuator command | Instruction to building actuator (HVAC setpoint, blind position, lighting level) |
| Negotiation request | Resource request sent to WP5-C |
| Escalation event | Decision forwarded to WP5-B when bounds exceeded |
| Audit log entry | Every decision recorded with: action, justification, context, timestamp, DP budget used |
| Service request | Capability gap forwarded to WP5-D for dynamic service discovery |

---

## Core Behaviour — Decision Loop (≤ 2 s P95)

```
LOOP every T seconds (configurable, default 30s):
  1. SENSE     — query WP3-B for current zone state
  2. INFER     — query WP4-A for current preference vector + confidence
  3. PLAN      — call WP3-C to simulate top candidate action (optional, <500ms)
  4. CHECK     — validate candidate action against autonomy envelope
     IF within bounds AND confidence ≥ threshold:
       5a. ACT — issue actuator command directly
     IF within bounds AND confidence < threshold:
       5b. ELICIT — trigger WP4-D to clarify preference
     IF outside bounds:
       5c. ESCALATE — forward to WP5-B with justification
     IF resource contention:
       5d. NEGOTIATE — request WP5-C inter-agent negotiation
     IF missing capability:
       5e. DISCOVER — request WP5-D to find/deploy needed service
  6. LOG       — write audit log entry for every branch taken
```

---

## Autonomy Envelope
| Bound Type | Example | Configurable? |
|---|---|---|
| Spatial | Temperature range: 18–26°C | Yes, per zone |
| Safety (hard) | Min temperature in medical unit: 20°C | No — immutable |
| Temporal | HVAC negotiation must converge < 60s | Yes |
| Authority | Autonomous up to ±2°C from preference; escalate beyond | Yes, per user |
| Computational | Each loop iteration ≤ 100ms on edge hardware | No |

---

## Escalation Triggers
- Safety constraint violation (hard — immediate escalation)
- Multi-agent negotiation deadlock or timeout
- Fairness threshold breach (systematic bias detected)
- User comfort threshold exceeded despite best action
- Confidence < minimum threshold on critical dimension

---

## Technologies
- Python asyncio (decision loop)
- gRPC / MQTT (actuator command issuing, inter-agent communication)
- FastAPI (admin/monitoring API)
- Kubernetes deployment (one pod per building unit, resource-limited per NFR4)
- Structured audit log (append-only, tamper-evident — critical for explainability NFR7)

---

## Interfaces
| Agent / System | Direction | Description |
|---|---|---|
| WP3-B DT Sync Agent | ← | Zone state (sense) |
| WP3-C Scenario Simulation | ↔ | Pre-decision consequence estimate |
| WP4-A Preference Inference | ← | Preference vector + confidence |
| WP5-B Escalation Agent | → | Escalation events; ← user decisions |
| WP5-C Negotiation Agent | ↔ | Resource negotiation requests and outcomes |
| WP5-D Service Discovery Agent | → | Capability gap requests |
| WP5-E MCP Context Builder | ← | Structured context for LLM calls |
| Physical actuators | → | HVAC, lighting, blind commands |
| WP6-A KPI Monitor | → | M-WP5-06 (latency), M-WP5-07 (boundary adherence) |

---

## KPIs Contributed
- **M-WP5-06:** Decision Cycle Latency (P95 ≤ 2000 ms) — **Primary**
- **M-WP5-07:** Autonomy Boundary Adherence Rate (100%) — **Primary**
- **M-SCL-01:** Latency degradation under scale (at N=50 agents)
- **M-USR-01:** User Comfort Satisfaction (downstream outcome)

---

## Implementation Notes
- This is the **load-bearing agent** of the entire architecture — its performance determines system-level KPIs
- The decision loop must be fully non-blocking: all I/O (DT query, preference query, simulation) must use async calls with timeouts; never block the loop
- Audit log is non-negotiable: every actuator command must be traceable to a preference vector, confidence score, and autonomy check — this is the foundation of NFR7 (explainability)
- One agent per building unit means horizontal scaling in K8s — test at N=50 on the caravel cluster (10.8.91.x) in WP6
- Cold-start problem: when a new unit is deployed with no preference history, agent should use WP4-C archetype warm-start and operate in high-escalation mode until confidence builds
- This agent is the central subject of Paper 5: "Bounded Autonomy in Multi-Agent Systems"
