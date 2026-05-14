# Paper Outline — Systematic Review: AI-Driven Occupant Modeling in Intelligent Built Environments

## 1. Introduction

### Context
- P1: Built environments shifting from reactive environmental control to proactive occupant-aware intelligence
- P2: Gap between "resident" (what they prefer) and "persona" (who they are) — current systems flatten occupants to thermostat setpoints

### Content
- P3: Research question: what AI methods model, evolve, and reason over occupant preferences and latent intent in intelligent built environments?
- P4: Scope definition — smart homes, buildings, offices, communities; exclusion of purely environmental/energy models

### Conclusion
- P5: Contributions of this review (three gaps identified, cross-tabulation framework)

---

## 2. Methodology

### 2.1 Search Strategy

#### Context
- P1: Need for systematic coverage across CS and built-environment literature

#### Content
- P2: Databases (WOS, ACM, IEEE Xplore), search strings, filters (last 5 years, research papers)
- P3: Raw corpus: 633 entries → 625 after deduplication

#### Conclusion
- P4: Corpus size justifies multi-stage screening

### 2.2 Screening Process

#### Context
- P1: Manual screening of 625 papers impractical — motivation for structured approach

#### Content
- P2: Stage 1 — Rule-based heuristic screening: keyword matching on title + abstract
  - Results: 4 INCLUDE / 104 EXCLUDE / 517 UNCERTAIN
- P3: Stage 2 — Human full-text review of remaining uncertain papers → final corpus (~52 papers)

#### Conclusion
- P4: Two-stage process reduced workload while preserving relevant papers

### 2.3 Inclusion and Exclusion Criteria

#### Context
- P1: Criteria must balance specificity (AI + occupant modeling) with breadth (multiple built-environment types)

#### Content
- P2: IC1–IC5 (publication type, language, AI method, human dimension, built-environment context)
- P3: EC1–EC5 (environment-only, web platform, no learned representation, non-paper, pre-2019)

#### Conclusion
- P4: Criteria designed to isolate papers where AI explicitly models a human dimension, not just optimizes environment

### 2.4 Data Extraction Variables

#### Context
- P1: Extraction must capture both technical method and modeling depth

#### Content
- P2: Variables — occupant dimension modeled, AI method category, preference evolution (static/dynamic), evaluation type, multi-occupant handling

#### Conclusion
- P3: These variables feed the cross-tabulation (Section 4.1)

### 2.5 PRISMA Flow Diagram
- 633 identified → 625 deduplicated → screening stages → N final included

---

## 3. Results

### 3.1 Corpus Overview

#### Context
- P1: Landscape of included papers by source and year

#### Content
- P2: Final paper count, distribution across databases
- P3: Temporal trend — growth pattern over 2019–2025

#### Conclusion
- P4: Field is growing but fragmented across venues

### 3.2 AI Method Landscape

#### Context
- P1: AI methods vary widely in how they represent occupants

#### Content
- P2: Classical ML dominance (clustering, classification, regression)
- P3: Deep learning approaches (CNNs, LSTMs for behavioral sequences)
- P4: Relational AI — KGs, ontologies, GNNs (10 papers); what they capture that flat models miss
- P5: Generative AI — LLMs, foundation models (8 papers); current uses
- P6: RL (1 standalone) and hybrid methods

#### Conclusion
- P7: Classical ML dominates; relational and generative methods emerging but underexplored

### 3.3 Occupant Modeling Depth

#### Context
- P1: Not all "occupant models" model at same depth — need a taxonomy

#### Content
- P2: **Level 1 — Physical setpoints / comfort / demographics**: thermostat, lighting, demographic tags
- P3: **Level 2 — Behavioral patterns / interaction styles**: navigation routines, activity patterns, modality preferences
- P4: **Level 3 — Cognitive / personality / latent intent**: Big Five, trust, unarticulated needs, hidden goals

#### Conclusion
- P5: Most papers stay at Level 1; Levels 2–3 sparsely populated

### 3.4 Preference Dynamics

#### Context
- P1: Static profiles insufficient — occupants change over time and context

#### Content
- P2: Static approaches — cold-start personas, demographic tags, fixed survey profiles
- P3: Dynamic triggers via explicit feedback (surveys, direct input)
- P4: Dynamic triggers via implicit behavioral drift (time-on-task, navigation, click divergence)
- P5: Dynamic triggers via context change (environment shift, emotional state, autonomy level)

#### Conclusion
- P6: Dynamic models exist but rely heavily on explicit feedback; implicit and context-driven adaptation rare

### 3.5 Latent Intent Inference

#### Context
- P1: Hardest modeling challenge — inferring what occupant wants but hasn't stated

#### Content
- P2: Approximate Bayesian Inverse RL (Wu & Jokinen 2025)
- P3: Dynamic Bayesian Networks (Han et al. 2025)
- P4: Inverse foraging / parameter fitting (Freire et al. 2021)
- P5: LLM rule mining (Danry et al. 2026)
- P6: Representation learning (Liu et al. 2023)

#### Conclusion
- P7: Methods are diverse but isolated — no unifying framework for latent intent in built environments

### 3.6 Multi-Occupant Dynamics

#### Context
- P1: Real environments have multiple occupants with competing preferences

#### Content
- P2: Algorithmic resolution — least misery, voting, dynamic priority, negotiation (Tran et al. 2021)
- P3: Power dynamics and social structures (Albayaydh & Flechais 2024)
- P4: Interpersonal conflict modeling (Danry et al. 2026, Langerak et al. 2026)
- P5: Human-robot task allocation (Umbrico et al. 2021)
- P6: Sensor fusion for physical multi-occupancy (Naser et al. 2023)

#### Conclusion
- P7: Multi-occupant work exists but rarely integrates social/power dynamics with algorithmic resolution

---

## 4. Synthesis and Gap Analysis

### 4.1 Cross-Tabulation: AI Method × Occupant Depth

#### Context
- P1: Individual results sections reveal patterns; cross-tabulation makes them explicit

#### Content
- P2: 6×3 matrix (6 AI method categories × 3 occupant depth levels) — centerpiece visual
- P3: Dense clusters (classical ML × physical setpoints) vs. sparse/empty cells

#### Conclusion
- P4: Three structural gaps emerge from empty regions of matrix

### 4.2 Gap (a) — Relational Representations of User-Environment-Context

#### Context
- P1: Most models treat features as flat vectors — relationships between user, space, device, context lost

#### Content
- P2: KGs and GNNs emerging (10 papers) but not yet dominant
- P3: Key challenge: integrating real-time sensor streams with semantic graph structures

#### Conclusion
- P4: Relational representations needed to capture occupant-environment-context dependencies classical ML ignores

### 4.3 Gap (b) — Generative AI for Preference Elicitation and Reasoning

#### Context
- P1: LLMs show reasoning capability but current use in built environments is narrow

#### Content
- P2: Current use confined to chatbots and instruction generation
- P3: Unexplored: LLM as inductive reasoner for hidden behavioral heuristics
- P4: Unexplored: injecting dynamic world knowledge into environment decision-making

#### Conclusion
- P5: Generative AI potential far exceeds current deployment — reasoning over preferences is natural fit

### 4.4 Gap (c) — Modeling the Occupant as a "Persona"

#### Context
- P1: Current systems reduce occupants to physiological comfort profiles

#### Content
- P2: Psychological traits, interaction styles, cognitive expectations largely absent from literature
- P3: "Blueprint Personas" (Vozna et al. 2025) as rare exception

#### Conclusion
- P4: Persona-level modeling needed to move from comfort optimization to genuine occupant understanding

### 4.5 Evaluation Landscape

#### Context
- P1: Method validity depends on evaluation rigor

#### Content
- P2: Distribution across simulation / user study / dataset benchmark / real deployment
- P3: Real deployment severely underrepresented

#### Conclusion
- P4: Field needs more real-world validation to bridge lab-to-deployment gap

---

## 5. Discussion

### Context
- P1: Three gaps not independent — they compound (no relational structure → no rich persona → no generative reasoning over it)

### Content
- P2: Relational + generative convergence as research direction — GNN-structured personas with LLM reasoning
- P3: Limitations — boundary decisions in criteria, criteria evolution during screening, corpus size

### Conclusion
- P4: Convergence of gaps points toward unified research agenda for next-generation occupant modeling

---

## 6. Conclusion

### Context
- P1: Landscape summary — classical ML dominates; relational and generative methods underexplored

### Content
- P2: Three gaps as motivating framework for future work
- P3: Persona-centric, graph-structured, LLM-augmented systems as target architecture

### Conclusion
- P4: Call to action — smart environments must model *who* occupants are, not just *what* they want

---

## Appendix
- Full list of included papers with extraction variables (screening table)
- PRISMA checklist
- Search string details per database
