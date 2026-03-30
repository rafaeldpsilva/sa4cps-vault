# WP1-B — Synthesis Agent

## Identity
| Field | Value |
|---|---|
| **ID** | WP1-B |
| **Name** | Synthesis Agent |
| **WP** | WP1 |
| **RQ Addressed** | RQ1, RQ2, RQ3, RQ4 (identifies gaps for all RQs) |
| **Type** | On-demand + Periodic |
| **Status** | Planned |

---

## Purpose
Reads the accumulated and annotated paper corpus and produces a structured synthesis: identifying research gaps at the intersection of GNNs × LLMs × Edge Computing × Intelligent Buildings. Maintains a living "gap map" that directly informs WP2 design decisions and WP4/WP5 technical choices.

---

## Inputs
| Source | Description |
|---|---|
| Annotated paper corpus | PDFs + researcher annotations (from WP1-A pipeline) |
| Gap taxonomy | Predefined dimensions: methodology gaps, application gaps, integration gaps |
| WP2 requirements doc | Current FR/NFR set — used to cross-check if known gaps are already addressed |

---

## Outputs
| Artifact | Description |
|---|---|
| Gap map | Structured knowledge graph: research topics × coverage × open questions |
| Synthesis note | Per-topic summary of state-of-the-art, consensus, and contradictions |
| Design feed | List of open questions directly relevant to WP4 (HGNN design) and WP5 (agent architecture) |
| Paper 1 draft input | Structured content for the systematic review paper (PRISMA-compatible) |

---

## Core Behaviour
1. **Cluster analysis** — groups papers by topic using embedding clustering (UMAP + HDBSCAN or similar)
2. **Coverage matrix** — builds a matrix of (technology domain) × (application domain) × (coverage level: none/partial/saturated)
3. **Contradiction detection** — flags papers with conflicting claims on the same topic
4. **Gap articulation** — for each empty/partial cell in the coverage matrix, generates a one-paragraph gap statement
5. **Living update** — re-runs when WP1-A surfaces ≥5 new papers (incremental, not full reprocessing)

---

## Technologies
- LLM/SLM (local — raspllm or similar) for synthesis text generation
- Sentence-transformers + UMAP/HDBSCAN for clustering
- Neo4j or JSON-LD for gap map storage
- Obsidian-compatible markdown output (links to paper notes)

---

## Interfaces
| Agent / System | Direction | Description |
|---|---|---|
| WP1-A Literature Scout | ← | Receives new papers to incorporate |
| WP2-A Requirements Consistency Agent | → | Feeds gap findings to validate FR/NFR coverage |
| WP4-C Relational Psychographics Agent | → | Informs psychological modeling design choices |
| WP5-A Building Unit Agent | → | Informs agent architecture design |
| Paper 1 (WP7) | → | Provides structured synthesis for systematic review manuscript |

---

## KPIs Contributed
- Supports quality of T2.1 (requirements) and T2.2 (KPIs) by grounding design in identified gaps
- Measurable: gap map completeness score, % of WP design decisions traceable to a gap finding

---

## Implementation Notes
- PRISMA compliance requires explicit inclusion/exclusion criteria — agent must track which papers were excluded and why
- Gap map format should be machine-readable (JSON-LD or RDF) to allow querying by WP2-A
- Open question: how to handle interdisciplinary papers that span multiple clusters?
- Risk: LLM synthesis may overstate or conflate findings — researcher must validate top-level gap statements before using them in Paper 1
