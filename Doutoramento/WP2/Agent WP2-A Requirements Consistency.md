# WP2-A — Requirements Consistency Agent

## Identity
| Field | Value |
|---|---|
| **ID** | WP2-A |
| **Name** | Requirements Consistency Agent |
| **WP** | WP2 |
| **RQ Addressed** | RQ0 (system integrity across all RQs) |
| **Type** | On-demand (triggered by design changes) |
| **Status** | Planned |

---

## Purpose
Given the large and interdependent set of functional (FR1–FR9) and non-functional (NFR1–NFR7) requirements, this agent validates that new design decisions, architecture changes, or feature additions do not introduce contradictions with existing requirements. Acts as a live consistency checker throughout WP2–WP6.

---

## Inputs
| Source | Description |
|---|---|
| Requirements document (T2.1) | Full FR/NFR specification |
| Change proposal | New design decision, architecture modification, or feature description |
| Gap map (from WP1-B) | Research gaps that requirements are intended to address |
| KPI definitions (T2.2) | To check that new changes don't break measurability |

---

## Outputs
| Artifact | Description |
|---|---|
| Conflict report | List of FR/NFR pairs in conflict with the proposed change, with explanation |
| Impact map | Which downstream components / agents are affected by the change |
| Recommendation | Suggested modifications to the proposal that resolve the conflict |
| Approval signal | Green/amber/red flag for the proposed change |

---

## Core Behaviour
1. **Requirement graph construction** — models FR/NFR as nodes with dependency and conflict edges
2. **Change injection** — parses the proposed change and maps it to affected FR/NFR nodes
3. **Conflict traversal** — propagates impact through the dependency graph, identifying contradictions
4. **Privacy check** — special pass: ensures any new data flow respects NFR3 (DP/LDP), NFR5 (GDPR), data minimization
5. **Performance check** — validates that proposed changes don't violate NFR1 (latency), NFR2 (scalability), NFR4 (reliability) thresholds
6. **Report generation** — produces structured conflict report with traceability to specific FR/NFR IDs

---

## Technologies
- LLM/SLM with requirements document as context (MCP-primed)
- Graph-based requirement model (Neo4j or NetworkX)
- Structured diff parser for change proposals

---

## Interfaces
| Agent / System | Direction | Description |
|---|---|---|
| WP1-B Synthesis Agent | ← | Receives gap map to validate requirement coverage |
| WP2-B DP Budget Planner | ↔ | Co-validates privacy-related requirements |
| WP4-A Preference Inference Agent | → | Notifies of FR3/NFR3 constraints relevant to HGNN design |
| WP5-A Building Unit Agent | → | Notifies of FR6/NFR1 constraints relevant to autonomy design |
| T2.1 document | ↔ | Reads and (with researcher approval) updates requirement spec |

---

## KPIs Contributed
- Directly supports requirement traceability (T2.1 deliverable quality)
- Measurable: % of change proposals reviewed, conflict detection precision (validated by researcher)

---

## Implementation Notes
- Requirements need to be stored in a machine-readable format (JSON or RDF), not just prose markdown — conversion step required
- Agent should maintain a change log so requirement evolution is traceable (important for thesis documentation)
- Risk: over-flagging — agent may raise false conflicts on benign changes; needs confidence threshold calibration
- Open question: who has authority to override a conflict flag? Needs a formal escalation path documented in T2.1
