# WP6-C — User Study Coordinator Agent

## Identity
| Field | Value |
|---|---|
| **ID** | WP6-C |
| **Name** | User Study Coordinator Agent |
| **WP** | WP6 |
| **RQ Addressed** | RQ1, RQ2 (validation via real users) |
| **Type** | Scheduled + Event-driven |
| **Status** | Planned |

---

## Purpose
Manages the end-to-end logistics of user study data collection during the real pilot phase: survey distribution, response rate tracking, reminder scheduling, interaction frequency logging, and data aggregation. Provides clean, structured datasets to WP6-A for user-centric KPI computation (M-USR-01 through M-USR-05, M-WP5-04).

---

## Inputs
| Source | Description |
|---|---|
| Session event stream | Every user dialogue session end, actuator override, escalation response |
| Survey templates | Validated instruments: IEQ/ASHRAE comfort questionnaire, XAI explainability scale, dialogue satisfaction scale |
| Participant registry | Enrolled pilot participants with consent records, preferred notification channel, study schedule |
| Interaction logs | WP5-A audit log, WP4-D session log — for filtering user-initiated vs. system-initiated interactions |

---

## Outputs
| Artifact | Description |
|---|---|
| Survey triggers | Contextually timed survey prompts sent to user (app notification, email) |
| Response dataset | Cleaned, anonymised survey response records |
| Interaction frequency dataset | Per-user voluntary interaction counts per week (M-USR-03) |
| Response rate report | Weekly response rate per participant; flags low responders for reminder |
| Aggregated KPI inputs | Ready-to-compute inputs for M-USR-01, M-USR-02, M-USR-03, M-USR-04, M-WP5-04 |
| Consent and ethics log | Immutable record of consent status per participant (GDPR compliance) |

---

## Core Behaviour
1. **Consent gate** — no data collected until explicit consent is confirmed; consent status stored in immutable log
2. **Survey triggering strategy**:
   - **Daily comfort micro-survey** (M-USR-01): triggered at configurable time (e.g., 17:00), 2 questions per comfort dimension
   - **Post-dialogue satisfaction** (M-WP5-04): triggered within 5 minutes of session end
   - **Post-decision explainability** (M-USR-04): triggered after 1 in 5 agent decisions (random sample)
   - **Post-conflict resolution** (M-USR-02): triggered within 10 minutes of conflict resolution event
3. **Response rate monitoring** — tracks response rate per participant per week; sends reminder if < 60% response rate; escalates to researcher if < 30% for 2 consecutive weeks
4. **Interaction logging** — subscribes to session event stream; classifies each event as user-initiated or system-initiated; computes AIF per user per week
5. **Anonymisation** — all exported datasets use anonymised participant IDs; mapping table stored separately with access-controlled
6. **Survey fatigue management** — enforces minimum intervals between surveys (e.g., max 3 prompts per day per user)

---

## Survey Instruments

| Survey | Trigger | Items | Scale |
|---|---|---|---|
| Comfort (IEQ-adapted) | Daily at 17:00 | 4 (thermal, visual, IAQ, acoustic) | 1–7 Likert |
| Dialogue satisfaction | Post-session | 5 (helpfulness, naturalness, clarity, trust, overall) | 1–5 Likert |
| Explainability (XAI-adapted) | Post-decision (1 in 5) | 4 (understanding, transparency, trust, control) | 1–5 Likert |
| Conflict resolution satisfaction | Post-conflict | 2 (outcome fairness, process transparency) | 1–5 Likert |
| Escalation necessity | Post-escalation | 1 ("Was this notification necessary?") | Yes/No |

---

## Technologies
- Push notification: FCM (Android) / APNs (iOS) or in-app web notification
- Survey engine: LimeSurvey (self-hosted) or custom React web form
- Participant registry: encrypted SQLite with consent timestamps
- Event stream consumer: Kafka (session end events)
- Data export: CSV / JSON for WP6-A integration

---

## Interfaces
| Agent / System | Direction | Description |
|---|---|---|
| WP4-D Dialogue Agent | ← | Session end events (post-dialogue survey trigger) |
| WP5-A Building Unit Agent | ← | Decision events (post-decision survey sampling), conflict resolution events |
| WP5-B Escalation Agent | ← | Escalation events (escalation necessity survey trigger) |
| WP6-A KPI Monitor | → | Aggregated survey response datasets |
| Pilot participants | ↔ | Survey prompts (push/web); receives responses |

---

## KPIs Contributed
- **M-USR-01:** User Comfort Satisfaction Score — **Primary** (real pilot required)
- **M-USR-02:** Conflict Resolution Success Rate — **Primary** (real pilot required)
- **M-USR-03:** System Adoption & Interaction Frequency — Secondary (real pilot required)
- **M-USR-04:** Perceived Explainability Score — **Primary** (real pilot required)
- **M-WP5-04:** User Satisfaction with Dialogue — **Primary** (real pilot required)
- **M-WP5-08:** False Escalation Rate (via escalation necessity survey)

---

## Implementation Notes
- Ethics committee approval must be obtained before this agent collects any real data — initiate IRB/ethics process at the start of WP6 planning (not after deployment)
- Minimum sample size for statistical significance: 30 participants × 4 weeks = target for comfort and satisfaction KPIs
- Survey fatigue is real: too many prompts will suppress response rates and bias toward disengaged users — enforce the maximum prompts-per-day limit strictly
- The distinction between user-initiated and system-initiated interactions (M-USR-03) requires careful event classification — document classification rules explicitly to ensure reproducibility
- All response data must be stored on infrastructure within GDPR jurisdiction (GECAD/ISEP servers, not external cloud)
- Anonymisation must be irreversible for exported datasets — researcher retains the participant ID mapping table separately under access control
