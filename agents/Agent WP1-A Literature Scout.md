# WP1-A — Literature Scout Agent

## Identity
| Field | Value |
|---|---|
| **ID** | WP1-A |
| **Name** | Literature Scout Agent |
| **WP** | WP1 |
| **RQ Addressed** | RQ1, RQ2 (feeds design of WP4 and WP5) |
| **Type** | Reactive + Scheduled |
| **Status** | Planned |

---

## Purpose
Continuously monitors academic publication channels for new papers at the intersection of the four keyword categories defined in the WP1 search strategy. Scores relevance and surfaces high-priority papers to the researcher, reducing manual triage time.

---

## Inputs
| Source | Description |
|---|---|
| arXiv RSS / Semantic Scholar API | New paper metadata (title, abstract, authors, date) |
| IEEE Xplore / ACM DL API | Conference and journal publications |
| Existing corpus index | Set of already-reviewed papers (for deduplication) |
| Keyword taxonomy | 4-category keyword set (Tech, Human, Graph/Relations, Context) |

---

## Outputs
| Artifact | Description |
|---|---|
| Relevance-scored paper list | Papers ranked by multi-category keyword overlap + semantic similarity |
| Gap signal | Flags when a new paper addresses a combination of categories not previously covered |
| Citation alert | Notifies when an existing key paper is cited by a new work |
| Weekly digest | Structured summary of top-N new papers for researcher review |

---

## Core Behaviour
1. **Scheduled poll** — queries publication APIs daily (or on new RSS event)
2. **Deduplication** — checks against existing corpus DOI/title index
3. **Relevance scoring** — computes match against the 4 keyword categories using:
   - Keyword overlap (exact + synonym expansion)
   - Semantic similarity (sentence-transformer embedding vs. seed paper set)
4. **Gap detection** — identifies papers at intersections not yet represented in corpus (e.g., GNNs + LLMs but missing Edge/Buildings angle)
5. **Surfacing** — pushes top-N results to researcher inbox (Vikunja task or structured note in WP1/)

---

## Technologies
- Semantic Scholar API, arXiv API, IEEE Xplore API
- Sentence-transformers (semantic similarity scoring)
- Vikunja API (task creation for review queue)
- SQLite or JSON index (local deduplication store)

---

## Interfaces
| Agent / System | Direction | Description |
|---|---|---|
| WP1-B Synthesis Agent | → | Forwards reviewed papers for gap analysis |
| Vikunja Inbox | → | Creates tasks for researcher paper review |
| WP4-A Preference Inference Agent | → | Feeds relevant HGNN papers for design grounding |

---

## KPIs Contributed
- Indirectly supports all primary KPIs by ensuring WP4/WP5 designs are grounded in state-of-the-art literature
- Measurable: corpus coverage rate, new-paper-to-review latency

---

## Implementation Notes
- Requires API keys for IEEE Xplore and Semantic Scholar
- Semantic similarity threshold needs calibration against existing reviewed corpus (start at cosine sim > 0.65)
- Consider rate-limiting to avoid API bans (batch nightly rather than continuous polling)
- Open question: how to handle preprints that later get published (deduplication across venues)?
