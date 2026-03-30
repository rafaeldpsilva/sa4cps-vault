# WP4-C — Relational Psychographics Agent

## Identity
| Field | Value |
|---|---|
| **ID** | WP4-C |
| **Name** | Relational Psychographics Agent |
| **WP** | WP4 |
| **RQ Addressed** | RQ1, RQ2 |
| **Type** | Continuous + Periodic update |
| **Status** | Planned |

---

## Purpose
Maintains the psychological and behavioural layer of each user's graph representation, moving beyond environmental setpoints into personality traits, interaction styles, and expectations. This is the agent that implements **relational psychographics** — the core theoretical novelty that distinguishes this thesis from prior smart building work. Its outputs personalise both WP4-A (preference inference) and WP4-D (dialogue style).

---

## Inputs
| Source | Description |
|---|---|
| Interaction logs (WP4-D) | Dialogue turn history: preferred modality, response latency, verbosity, clarification requests |
| Feedback signal (WP4-A) | Override patterns, frequency and magnitude of corrections to agent decisions |
| Explicit survey / onboarding | Optional: Big Five personality questionnaire at onboarding (1-time) |
| Temporal behaviour patterns | Time-of-day interaction patterns, seasonal variation in engagement |
| WP3-B occupancy context | Social context (alone vs. in group) at time of interaction |

---

## Outputs
| Artifact | Description |
|---|---|
| Personality embedding | Continuous vector representation of Big Five traits (O, C, E, A, N) inferred from behaviour |
| Interaction style profile | Categorical + continuous: `{modality: voice/app/passive, proactivity: 0–1, verbosity: 0–1, trust_in_automation: 0–1}` |
| Expectation model | Predicted user expectation of system response time, explanation depth, and confirmation frequency |
| Archetype assignment | Soft assignment to interaction archetypes (e.g., "delegator", "micromanager", "passive acceptor") |
| Updated user graph nodes | Personality, interaction style, and expectation nodes written into the HGNN user graph |

---

## Core Behaviour
1. **Behavioural signal extraction** — monitors all user interaction events and extracts psychographic signals:
   - Override frequency → low trust in automation (Neuroticism / Agreeableness signal)
   - Dialogue verbosity → Openness / Extraversion signal
   - Response latency to escalations → engagement level
   - Proactive vs. reactive initiation → Conscientiousness signal
2. **Incremental personality update** — updates Big Five embedding using Bayesian update or gradient-based method; changes slowly (personality is stable)
3. **Interaction style update** — updates interaction style profile more frequently (behaviour adapts faster than personality)
4. **Archetype detection** — applies soft clustering across interaction style space to assign archetype; used to initialise new users by nearest-archetype warm start
5. **Graph node update** — writes updated personality/style/expectation embeddings to user graph nodes in WP4-A's graph store
6. **Cross-user structural comparison** — uses graph isomorphism / alignment to compare user graphs for archetype clustering (the "relational" in relational psychographics)

---

## Technologies
- PyTorch / NumPy (personality embedding update)
- UMAP + HDBSCAN (archetype soft-clustering across user embedding space)
- Bayesian update or online learning (incremental personality inference)
- Neo4j (user graph node updates)
- Graph isomorphism tools (e.g., NetworkX `is_isomorphic`, GED algorithms)

---

## Graph Nodes Managed
```
User {
  id,
  big_five: {O, C, E, A, N},          # continuous 0–1 each
  interaction_style: {
    modality,                           # categorical: voice/app/passive
    proactivity,                        # 0–1
    verbosity,                          # 0–1
    trust_in_automation                 # 0–1
  },
  expectation: {
    response_time_tolerance,            # ms
    explanation_depth,                  # low/medium/high
    confirmation_frequency              # 0–1
  },
  archetype                             # soft assignment, e.g., "delegator"
}
```

---

## Interfaces
| Agent / System | Direction | Description |
|---|---|---|
| WP4-D Preference Elicitation Dialogue Agent | ← | Provides interaction logs; receives personality-informed dialogue style |
| WP4-A Preference Inference Agent | → | Provides personality and style embeddings for HGNN node features |
| WP5-B Escalation Agent | → | Provides trust and proactivity scores to calibrate escalation threshold per user |
| WP1-B Synthesis Agent | ← | Informs theoretical grounding of psychographic model from literature |

---

## KPIs Contributed
- Directly enables M-WP4-01 and M-WP4-02 improvement (richer user graph → better preference inference)
- Enables M-WP5-04 (user satisfaction) via personalised dialogue style
- Supports M-USR-04 (perceived explainability) — explanation depth matched to user expectation model
- This agent is the **primary vehicle** for the "relational psychographics" claim in Paper 3

---

## Implementation Notes
- This is the most theoretically novel agent — it needs a dedicated literature review section (WP1) establishing that personality-as-graph-structure is a gap in existing work
- Big Five inference from behaviour alone is noisy; the optional onboarding survey gives a strong prior — design onboarding to be low-friction (≤ 5 minutes, 10 items, validated BFI-10 instrument)
- Personality is largely stable (trait theory); update cadence should be slow (weekly smoothing) to avoid overfitting to transient behaviour
- Archetype warm-start for new users is critical for cold-start problem — document this mechanism explicitly in Paper 3
- Privacy note: personality embeddings are sensitive personal data under GDPR — document data minimisation and access control in T2.1 NFR5
