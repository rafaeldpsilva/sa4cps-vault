# WP5-B — Escalation & Mediation Agent

## Identity
| Field | Value |
|---|---|
| **ID** | WP5-B |
| **Name** | Escalation & Mediation Agent |
| **WP** | WP5 |
| **RQ Addressed** | RQ3, RQ2 |
| **Type** | Event-driven |
| **Status** | Planned |

---

## Purpose
Receives escalation events from WP5-A when a decision exceeds the configured autonomy envelope. Decides whether to route to autonomous resolution (WP5-C negotiation), user dialogue (WP4-D), or direct user notification. The critical safety gatekeeper: responsible for ensuring that missed escalation rate stays ≤ 5% while false escalation rate stays ≤ 15%.

---

## Inputs
| Source | Description |
|---|---|
| WP5-A escalation event | Decision context: proposed action, reason for escalation, urgency level, affected users |
| WP4-C interaction style profile | Per-user trust level, proactivity preference, notification tolerance |
| WP4-B conflict graph | If escalation is due to multi-occupant conflict |
| User response (from WP4-D) | User's decision after being presented with the escalation |
| Escalation history | Previous escalations for the same scenario (to learn patterns and reduce false escalations) |

---

## Outputs
| Artifact | Description |
|---|---|
| Routing decision | `{route: negotiate | dialogue | notify | override}` with justification |
| User notification | Formatted escalation message sent to user via WP4-D (if dialogue) or push notification |
| Resolution instruction | Decision returned to WP5-A for action |
| Escalation log entry | Record of every escalation: trigger, route taken, user response, resolution |
| False escalation feedback | After user response, records whether escalation was warranted (input for M-WP5-08/09) |

---

## Core Behaviour
1. **Escalation classification** — categorises incoming escalation by type:
   - `SAFETY`: immediate user override required (never route to autonomous resolution)
   - `CONFLICT`: multi-occupant preference conflict → route to WP5-C first
   - `CONFIDENCE`: low preference confidence → route to WP4-D elicitation
   - `DEADLOCK`: negotiation timeout → route to user
   - `FAIRNESS`: systematic bias detected → route to user with explanation
2. **User calibration** — applies WP4-C profile to decide notification format:
   - High trust in automation → minimal notification ("I had to escalate X, here's what I chose")
   - Low trust → full dialogue via WP4-D
   - Passive user → push notification with one-tap approve/reject
3. **Timeout handling** — if user does not respond within configurable window: falls back to safe default action (last committed preference or safe midpoint)
4. **Pattern learning** — tracks escalation outcomes; if the same scenario escalates repeatedly with user always approving the same choice → adjusts autonomy envelope to handle autonomously in future
5. **False escalation audit** — after each escalation, prompts user: "Was this notification necessary?" — feeds M-WP5-08

---

## Technologies
- Python asyncio (event-driven routing)
- Push notification service (FCM / APNs for mobile)
- Redis (escalation state tracking, timeout management)
- SQLite / InfluxDB (escalation history log)
- Kafka (event bus with WP5-A and WP4-D)

---

## Interfaces
| Agent / System | Direction | Description |
|---|---|---|
| WP5-A Building Unit Agent | ← | Receives escalation events; → returns resolution |
| WP4-D Preference Elicitation Dialogue | ↔ | Triggers user dialogue for CONFIDENCE/DEADLOCK escalations |
| WP5-C Negotiation Agent | → | Routes CONFLICT escalations for autonomous resolution attempt |
| WP4-C Relational Psychographics | ← | Per-user trust and notification preference |
| WP6-A KPI Monitor | → | Reports M-WP5-08 (FER), M-WP5-09 (MER), M-WP5-05 (escalation precision) |

---

## KPIs Contributed
- **M-WP5-05:** Proactive Escalation Precision (≥ 80%) — **Primary**
- **M-WP5-08:** False Escalation Rate (≤ 15%) — Secondary
- **M-WP5-09:** Missed Escalation Rate (≤ 5%) — **Primary** (safety-critical)

---

## Implementation Notes
- Missed escalation rate (M-WP5-09) is the **safety-critical metric** — asymmetric cost: a missed escalation (agent does something it shouldn't) is much worse than a false one
- Ground truth for M-WP5-09 is hard to obtain automatically — embed the comfort violation reporting button (red flag) in the UI from day one to capture passive ground truth
- The pattern learning component (autonomy envelope adjustment) must be gated: requires explicit user consent and a minimum of N confirmed instances before adjusting — document policy in T2.1 FR6
- Timeout fallback behaviour must be formally defined and documented: "safe default" is not obvious in all scenarios (e.g., a medical unit during an alert)
- This agent's logic is the primary mechanism for KPI M-WP5-09 — it must be instrumented with full decision tracing from the start
