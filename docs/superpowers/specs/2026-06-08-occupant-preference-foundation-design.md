 # Occupant-Preference Foundation (Design)

**Date:** 2026-06-08
**Author:** Rafael Silva
**Status:** Approved direction → ready for implementation plan
**Thesis link:** RQ1 (profile generation/evolution), RQ2 (inference across context/time),
RQ3 (proactive engagement / latent intent) · WP4 (preference + context modeling),
WP5 (agent interaction)

## Why this is the first sub-project

Thesis end goal = model the **occupant as an evolving persona** (preferences,
interaction style, latent intent) via **heterogeneous GNN + LLM/SLM**, moving
*from* environmental modeling *to* cognitive/behavioral modeling
(`Full Review Doc.md`, line 1).

A pure sensing rig records the **room**, not the **occupant** — that is EC1
(environment-only), the exclusion criterion the review uses to reject papers as
off-topic. The first build must instead produce an **identity-attributed,
evolving preference** the GNN can reason over. Context (sensing) is a necessary
*input channel*, not the foundation itself.

## The foundation — 5 parts

### 1. Occupant identity (the anchor)
Persistent per-person ID. Every signal, context, and preference attributes to a
person. Minimal start: single known user (self), identified via voice-ID
(`local-voice-ai` already hears them) + Home Assistant presence (phone/BLE).
Without identity there is no per-user profile, no persona evolution (RQ1/RQ2),
no multi-occupant conflict (RQ4/WP5).

### 2. Three preference-signal channels
Matches the adaptation triggers in the review (`Full Review Doc.md`, 384-388):

| Channel              | Source                                                              | Example                                                                            |
| -------------------- | ------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **Explicit**         | voice agent                                                         | user says "make it warmer"; answers an elicitation prompt                          |
| **Implicit / drift** | Home Assistant device events, attributed to the identified occupant | turned on lamp; nudged thermostat                                                  |
| **Context envelope** | the **context-channel spec** (sensing foundation)                   | world-state stamped onto each signal: time, presence, light, sound, later tidiness |

Channels 1+2 are the **preference signal**. Channel 3 is the **context around
it** — the job of the subordinate sensing spec
(`2026-06-08-instrumented-room-sensing-design.md`).

### 3. Heterogeneous preference graph (WP4 T4.1 — the novelty)
Neo4j, typed nodes — the GNN substrate:

```
(:User)-[:PREFERS {strength, ts, source}]->(:Setpoint)-[:IN]->(:Context)
(:User)-[:DID {ts}]->(:Action)-[:UNDER]->(:Context)
(:Context)-[:AT]->(:TimeOfDay)
(:Context)-[:HAS]->(:Presence|:LightLevel|:SoundClass|:Activity)
(:Setpoint)-[:ON]->(:Device)
```

This is what makes the work research rather than a logger: a heterogeneous graph
of User / Preference / Device / Context / Time, ready for relational learning.

### 4. Inference + evolution (RQ2)
Given current context + history → predict the user's preferred setpoint/action.
- **Start with a relational baseline** (e.g. context-conditioned frequency /
  simple link-prediction), *not* a full GNN. Establish a measurable accuracy
  baseline before adding model complexity.
- **Evolution:** profile updates on each new signal — time-decay / drift so
  recent behavior outweighs old (Guo & Yuan, Virvou — review lines 378, 387).
- **KPI:** preference-prediction accuracy over a held-out window. This is the
  WP6-style metric that gives the build a research question to answer.

### 5. Interaction loop (RQ3)
`local-voice-ai` (STT + llama.cpp LLM + TTS, LiveKit Agents) = the elicitation +
proactive surface. Loop:

```
inference uncertain ──► agent asks/confirms ──► user feedback ──► profile updates
        ▲                                                              │
        └──────────────────── proactive prompt ◄───────────────────────┘
```

This is already largely built — it is reused, not re-implemented.

## How the pieces relate

```
[context channel: sense+store]  ──context-stamp──┐
[Home Assistant device events]  ──implicit signal─├─► preference graph ─► inference/evolution
[voice agent]  ──explicit signal + loop──────────┘                              │
                          ▲──────────────── proactive prompt ───────────────────┘
```

## First slice — minimal preference loop (MVP)

Thinnest end-to-end that yields an evolving, identity-attributed preference and
tests an RQ. **Skip the camera at first** — cheapest identity-attributable
signal wins.

1. **Identity:** single known user (self).
2. **Signal:** Home Assistant device events + explicit voice statements.
3. **Context:** timestamp + a few cheap HA features (time-of-day, presence,
   light level). Not the vision rig yet.
4. **Graph:** minimal `User–PREFERS–Setpoint–IN–Context` in Neo4j.
5. **Inference:** relational baseline → predict next setpoint given context;
   measure accuracy = RQ2 KPI.
6. **Loop:** voice agent confirms / asks on low-confidence predictions.

## Sensing rig becomes an experiment, not premature infra

Once the loop works on HA-only context, the sensing foundation plugs in as a
**context-richness ablation arm**:

> Does camera / sound / tidiness context improve preference prediction over
> HA-only context?

That ablation is a publishable result (RQ1 — what context enriches the profile),
and it gives every sensing component a research justification instead of being
collected for its own sake.

## Storage

- **Neo4j** (Docker, mac-mini) — primary: the heterogeneous preference graph +
  context nodes. The substrate for relational learning.
- **Timescale** (Docker, mac-mini) — raw signal/event stream (HA events,
  explicit statements, context stamps) before they are materialized into the
  graph. Source of truth / replayable log.
- Raw AV buffer: owned by the subordinate sensing spec, only once that channel
  is activated.

## Testing & validation

- **Signal-ingest contract** — HA event / voice statement → normalized
  `preference-signal` record; identity attached; malformed rejected.
- **Graph materialization** — a sequence of signals → expected nodes/edges in
  Neo4j (golden-graph test).
- **Inference baseline** — held-out context windows → accuracy reported; guards
  against regressions when the model changes.
- **Evolution** — synthetic drift sequence → recent preference outweighs stale
  (decay behaves).
- **Loop** — low-confidence prediction triggers an elicitation prompt; user
  reply updates the profile (integration test against a mocked agent).

## RQ / KPI traceability

| Component | RQ | KPI |
|-----------|----|----|
| Identity + signal channels | RQ1 | profile populated per user from ≥3 signal types |
| Preference graph | RQ1 | graph schema captures User/Pref/Context/Device |
| Inference + evolution | RQ2 | prediction accuracy; drift responsiveness |
| Interaction loop | RQ3 | % uncertain cases resolved via elicitation; user-confirmed accuracy lift |
| Sensing ablation (later) | RQ1 | accuracy delta: rich-context vs HA-only |

## Privacy & ethics

- Identity-attributed behavioral/persona data → consent + GDPR obligations
  beyond "I consent to myself" the moment a second person is observed or persona
  inference begins. Design the consent/anonymization boundary **now**, before
  the camera channel activates.
- Preference graph holds inferences about a person — treat as sensitive; keep
  local (mac-mini), no cloud.

## Open items for the implementation plan

- Relational baseline choice (frequency-conditioned vs simple link-prediction)
  before committing to a GNN.
- Identity mechanism: voice-ID confidence vs HA presence vs assumed-single-user
  for the MVP.
- Home Assistant: stand up home instance now (required for the implicit channel).
- Exact `Context` granularity in the MVP (which HA features become nodes).
- Drift/decay function + update cadence.
- Where elicitation policy lives (agent prompt vs separate decision module — ties
  to WP5 bounded autonomy, future).
