# WP5-C — Multi-Agent Negotiation Agent

## Identity
| Field | Value |
|---|---|
| **ID** | WP5-C |
| **Name** | Multi-Agent Negotiation Agent |
| **WP** | WP5 |
| **RQ Addressed** | RQ0, RQ4 |
| **Type** | On-demand (P2P session-based) |
| **Status** | Planned |

---

## Purpose
Handles peer-to-peer resource negotiation between building unit agents for shared commodities (energy capacity, cooling/heating capacity, computational resources). Operates without a central broker, implements a distributed negotiation protocol with convergence guarantees, applies LDP perturbation before transmitting data to peer agents, and escalates to WP5-B on deadlock or timeout.

---

## Inputs
| Source | Description |
|---|---|
| WP5-A negotiation request | Resource demand: `{resource_type, quantity_needed, priority, deadline}` |
| WP5-B conflict routing | Conflict escalation from multi-occupant dispute needing inter-agent resolution |
| Peer WP5-C agents | Offer/counter-offer messages from other building unit agents |
| WP2-B LDP configuration | LDP mechanism and ε_sensor budget for data shared in P2P exchanges |
| WP3-D external signal | Grid demand response constraints (e.g., total building energy cap from OpenADR) |

---

## Outputs
| Artifact | Description |
|---|---|
| Negotiation agreement | Accepted resource allocation: `{resource_type, allocated_quantity, duration, counterparty}` |
| LDP-perturbed offer | Agent's own resource offer with privacy noise applied before transmission |
| Deadlock signal | If negotiation times out → forwarded to WP5-B for user escalation |
| Negotiation log | Full session record: offers, counter-offers, outcome (for M-WP5-10) |
| Credit update | Reputation/credit score update for participating agents |

---

## Core Behaviour
1. **Session initiation** — WP5-A sends a resource request; agent initiates a P2P negotiation session with relevant peer agents
2. **LDP perturbation** — before broadcasting resource availability to peers, applies LDP:
   - Energy availability (continuous): Laplace mechanism
   - Resource categories (categorical): Randomised response
   - Only minimum required fields are transmitted (data minimisation — M-PRI-04)
3. **Negotiation protocol** — iterative bilateral or multilateral negotiation:
   - Round 1: broadcast demand + perturbed supply offer
   - Rounds 2+: counter-offers based on priority and credit score
   - Convergence criterion: all parties agree or max rounds reached
4. **Fairness enforcement** — monitors allocation across agents; flags systematic bias (same agent always loses) → triggers WP5-B fairness escalation
5. **Deadlock detection** — if no convergence within configurable round limit (< 60s total for HVAC): signals deadlock to WP5-B
6. **Offline mode** — if central registry is unavailable: falls back to local peer-to-peer discovery via mDNS / gossip (target: ≥ 70% fulfillment in offline mode — M-SCL-03)
7. **Agreement execution** — confirmed allocation passed back to WP5-A for actuation; logs outcome

---

## Technologies
- gRPC / MQTT (P2P inter-agent message passing)
- mDNS / Zeroconf (peer discovery in offline mode)
- Google DP / IBM Diffprivlib (LDP perturbation)
- Redis (session state, credit ledger)
- Python asyncio (non-blocking negotiation sessions)
- Kafka (negotiation event log for WP6-A)

---

## Negotiation Message Schema
```json
{
  "session_id": "uuid",
  "round": 2,
  "from_agent": "unit_A3",
  "resource_type": "thermal_capacity",
  "offer_quantity": 2.1,           // LDP-perturbed
  "priority": 0.8,
  "deadline_ms": 45000,
  "credit_score": 0.92
}
```

---

## Interfaces
| Agent / System | Direction | Description |
|---|---|---|
| WP5-A Building Unit Agent | ↔ | Receives resource request; returns agreement |
| WP5-B Escalation Agent | ← | Receives conflict escalations; → sends deadlock signals |
| Peer WP5-C agents (other units) | ↔ | P2P negotiation message exchange |
| WP2-B DP Budget Planner | ← | LDP configuration; reports per-exchange ε expenditure |
| WP3-D External Integration | ← | Grid demand response constraints |
| WP6-A KPI Monitor | → | Reports M-WP5-10 (negotiation success rate), M-SCL-03 (offline availability) |

---

## KPIs Contributed
- **M-WP5-10:** Multi-agent Resource Negotiation Success Rate (≥ 90%) — **Primary**
- **M-SCL-03:** P2P Resource Availability in Offline Scenarios (≥ 70%) — **Primary**
- **M-PRI-04:** Data Minimization Compliance in P2P (100%)
- **M-PRI-03:** LDP perturbation overhead contribution

---

## Implementation Notes
- The P2P nature is essential for RQ4 (privacy-preserving resource sharing) — a centralized broker would be simpler but defeats the privacy purpose
- LDP must be applied per-message, not per-session — the agent must re-perturb even if the same value is shared in subsequent rounds (to prevent reconstruction attacks)
- Credit/reputation system prevents free-riding but introduces complexity — start with a simple exponential moving average credit score, not a sophisticated mechanism
- Offline mode (mDNS discovery) must be tested independently from the normal K8s-networked mode — WP6-B chaos agent should test network partition scenarios
- Convergence guarantee requires a formal protocol proof or empirical evidence — this is a contribution point for Paper 5
- The 60-second HVAC convergence deadline is a hard NFR; monitor round-trip times between caravel cluster nodes (10.8.91.x via VPN) early to assess feasibility
