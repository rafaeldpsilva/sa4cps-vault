# Paper Outline — Systematic Review: AI-Driven Occupant Modeling in Intelligent Built Environments

## 1. Introduction
- Shift from environmental modeling to cognitive/behavioral modeling of occupants
- "Persona" vs "resident" framing — modeling who the occupant *is*, not just what they prefer
- Research question: what AI methods model, evolve, and reason over occupant preferences and latent intent?
- Scope: intelligent built environments (smart homes, buildings, offices, communities)
- Contributions of this review

## 2. Methodology
### 2.1 Search Strategy
- Databases: WOS, ACM, IEEE Xplore
- Search strings and filters (last 5 years, research papers)
- Corpus: 633 raw entries → 625 after deduplication

### 2.2 Screening Process
- **Stage 1 — Rule-based heuristic** (`screen.py`): keyword matching on title + abstract
  - Results: 4 INCLUDE / 104 EXCLUDE / 517 UNCERTAIN
- **Stage 2 — LLM-assisted screening** (`screen_claude.py`): full abstract reasoning with IC/EC logic
  - Results: 0 INCLUDE / 56 UNCERTAIN / 569 EXCLUDE
  - Transition matrix: Claude resolved 469/517 uncertain papers to EXCLUDE
- **Stage 3 — Human full-text review** of 56 uncertain papers → final corpus (~52 papers)

### 2.3 Inclusion and Exclusion Criteria
- IC1–IC5 (publication type, language, AI method, human dimension, built-environment context)
- EC1–EC5 (environment-only, web platform, no learned representation, non-paper, pre-2019)

### 2.4 Data Extraction Variables
- Occupant dimension modeled
- AI method category
- Preference evolution (static vs dynamic)
- Evaluation type (simulation, user study, benchmark, real deployment)
- Multi-occupant conflict/negotiation handling

### 2.5 PRISMA Flow Diagram
- 633 identified → 625 deduplicated → 569 excluded (Stage 2) → 56 full-text reviewed → N final included

## 3. Results
### 3.1 Corpus Overview
- Final paper count, source distribution, year distribution

### 3.2 AI Method Landscape
- Classical ML (dominant), deep learning, probabilistic/statistical
- Relational AI (KG, ontology, GNN) — 10 papers
- Generative AI (LLM, foundation models) — 8 papers
- Reinforcement learning (1 standalone), hybrid methods

### 3.3 Occupant Modeling Depth
- **Physical setpoints / comfort / demographics**: thermostat, lighting, demographic tags
- **Behavioral patterns / interaction styles**: navigation, activity routines, interaction modality
- **Cognitive / personality / latent intent**: Big Five, trust, unarticulated needs, hidden goals

### 3.4 Preference Dynamics
- Static profiling approaches (cold-start personas, demographic tags, fixed survey profiles)
- Dynamic/evolving models and their triggers:
  - Explicit feedback (surveys, direct input)
  - Implicit behavioral drift (time-on-task, navigation patterns, click divergence)
  - Context change (environmental shift, emotional state, autonomy level)

### 3.5 Latent Intent Inference
- Approximate Bayesian Inverse RL (Wu & Jokinen 2025)
- Dynamic Bayesian Networks (Han et al. 2025)
- Inverse foraging / parameter fitting (Freire et al. 2021)
- LLM rule mining (Danry et al. 2026)
- Representation learning (Liu et al. 2023)

### 3.6 Multi-Occupant Dynamics
- Algorithmic preference resolution: least misery, voting, dynamic priority, negotiation (Tran et al. 2021)
- Power dynamics in shared homes (Albayaydh & Flechais 2024)
- Interpersonal conflict modeling (Danry et al. 2026, Langerak et al. 2026)
- Human-robot task allocation (Umbrico et al. 2021)
- Sensor fusion for physical multi-occupancy (Naser et al. 2023)

## 4. Synthesis and Gap Analysis
### 4.1 Cross-Tabulation: AI Method x Occupant Depth
- The 6x3 matrix as centerpiece
- Where papers cluster, where cells are empty or sparse

### 4.2 Gap (a) — Relational Representations of User-Environment-Context
- Most models treat features as flat/independent
- KGs and GNNs emerging but not dominant
- Struggle to integrate real-time sensor streams with semantic relationships

### 4.3 Gap (b) — Generative AI for Preference Elicitation and Reasoning
- LLMs confined to chatbots and instruction generation
- Unexplored: LLM as inductive reasoner for hidden behavioral heuristics
- Unexplored: injecting dynamic world knowledge into environment decision-making

### 4.4 Gap (c) — Modeling the Occupant as a "Persona"
- Current systems reduce occupants to physiological comfort profiles
- Psychological traits, interaction styles, cognitive expectations largely ignored
- "Blueprint Personas" concept (Vozna et al. 2025) as rare exception

### 4.5 Evaluation Landscape
- Distribution across simulation / user study / dataset benchmark / real deployment
- Real deployment severely underrepresented

## 5. Discussion
- How gaps (a), (b), (c) connect and compound each other
- Relational + generative convergence as research direction
- Methodological reflection: two-stage screening with LLM as contribution
- Limitations of this review (boundary decisions, criteria evolution, corpus size)

## 6. Conclusion
- Summary of landscape: classical ML dominates, relational/generative underexplored
- Three gaps motivating next-generation occupant modeling
- Call for persona-centric, graph-structured, LLM-augmented systems in smart environments

## Appendix
- Full list of included papers with extraction variables (the screening table)
- PRISMA checklist
- Search string details per database
