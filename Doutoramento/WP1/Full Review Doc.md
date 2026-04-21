In this research, I not only want to capture "smart preferences" such as comfort ones, but what Im really after is how the user is, how does he likes to interact with systems, his personality and what he expects from the systems. Moving from Environmental Modeling, such as thermostat settings, to Cognitive and Behavioral Modeling (psychology and interaction design)

Similar concepts of the literature:
- Human-Centric Intelligent Environments
- Socially-Aware Smart Builings

This means that the system is not only modeling a "resident", but modeling a "persona".

## Research Question
*To what extent have existing approaches applied relational or generative AI methods to infer and model the psychological and interactional dimensions of occupants (personality traits, interaction styles, and expectations) within intelligent or smart buildings?*

## What is the domain of this review?
This review maps how AI has been applied to decode the human dimension within physical spaces — not what the environment does, but who the occupant is.

**The where**: The context is intelligent or smart buildings. Smart communities may serve as a broader deployment context, but the locus of user modeling is always the building level.

**The who**: The model target is the occupant's psychological and interactional profile. This includes personality traits (e.g., Big Five or MBTI-derived traits), interaction styles (e.g., preferred modality (voice/touch), agency level (proactive/reactive), feedback loops), and expectation management (e.g., trust levels in automation, anticipated system reliability, transparency, and perceived "intelligence" level).

**The how**: This review surveys the AI methods that existing work has used to infer or represent these dimensions. This encompasses **relational methods** — such as knowledge graphs, ontologies, and graph-based models — that capture structured relationships between user traits and behaviors; and **generative AI methods** — such as large language models and foundation models — that interpret qualitative or behavioral data to derive psychological attributes. The review does not prescribe a specific method; it characterises the landscape of approaches found in the literature.

## Scope Statement
This review investigates the intersection of User Profiling (UP) and User Modeling (UM) within intelligent or smart buildings, with a specific focus on the occupant's psychological and interactional dimensions. Moving beyond environmental setpoints, this research examines how existing work models the occupant as a complex entity defined by personality traits, interaction styles, and expectations.

In scope are studies that apply relational AI methods (e.g., knowledge graphs, ontologies, graph neural networks, semantic networks) or generative AI methods (e.g., large language models, foundation models, generative architectures) to infer, represent, or reason about these psychological and interactional dimensions. We are interested in the full lifecycle: from raw user data and behavioral signals, through profiling and structured modeling, to personalization or adaptation of the built environment.

We exclude papers focused solely on environmental modeling (occupancy sensing, thermal comfort, energy optimization) that do not address the user's psychological or interactional nature, user profiling for sentiment analysis or commercial ad-targeting on web platforms, and studies that apply deep learning purely as a prediction engine without producing any interpretable user model or profile representation. The goal is to map the state of the art and identify what methods and representations have been used, providing a foundation for future "expectation-aware" system design.

## Keywords

A valid paper should cover at least one keyword from Category C or D (context anchor), at least one from Category B (human dimension), and at least one from Category A or E (AI method).

Category A (Generative AI Methods):
- Large Language Models / LLM
- Generative AI
- Foundation Models
- Natural Language Processing
- Multimodal AI

Category B (Human Dimensions):
- Personality Traits
- Interaction Style / Modality
- User Expectation
- Cognitive Modeling
- Behavioral Archetypes
- Psychographic Profiling

Category C (Relational AI Methods):
- Knowledge Graph
- Graph Neural Networks / GNN
- Ontology / Semantic Web
- Heterogeneous Information Networks
- Relational Embedding
- User Modeling / User Profiling

Category D (Context):
- Smart Buildings / Smart Homes
- Intelligent Environments
- Built Environments
- Ambient Intelligence
- Smart Communities
- IoT / Cyber-Physical Systems

## Inclusion and Exclusion Criteria

All inclusion criteria must be satisfied. Any single exclusion criterion is sufficient to reject.

### ✅ Inclusion Criteria
1. **Publication type**: Peer-reviewed journal article or full conference paper (not workshop summary, poster, or extended abstract)
2. **Language**: Written in English
3. **AI Method**: Applies at least one relational AI method (knowledge graph, GNN, ontology, semantic model) OR at least one generative AI method (LLM, foundation model, generative architecture)
4. **Human Dimension**: Models or infers at least one psychological or interactional occupant trait — personality, interaction style/modality, or expectation/trust
5. **Context**: Work is situated in a built environment (smart building, smart home, intelligent environment, smart community, or equivalent)

### ❌ Exclusion Criteria
1. **EC1 – Environment-only**: Focuses exclusively on physical or environmental modeling (occupancy sensing, thermal comfort, energy, HVAC) without addressing the occupant's psychological or interactional nature
2. **EC2 – Web platform**: User profiling for web-platform purposes (ad targeting, sentiment analysis, social media recommendation) with no built-environment application
3. **EC3 – Black-box DL**: Uses deep learning purely as a black-box predictor with no interpretable user model, profile, or structured representation as output
4. **EC4 – Non-paper**: Workshop summaries, keynote abstracts, editorials, or papers with no retrievable abstract
5. **EC5 – Out of date**: Published before 2019

## Search Strings
Filters:
- Last 5 years
- Research Paper
**Total: 632**

user modeling AND user profiling 
profile AND preferences
(intelligent OR smart OR cognitive) AND (home* OR communit* OR building*)
### WOS: 
```
(ALL=("user modeling" OR "user profiling") AND (ALL=(intelligent OR smart OR cognitive) AND ALL=(home* OR communit* OR building*)))
```
Results: 54
### ACM:
```
[[**All**: "user modeling"] **OR** [**All**: "user profiling"]] **AND** [**All**: profile] **AND** [**All**: preferences] **AND** [[**All**: intelligent] **OR** [**All**: smart] **OR** [**All**: cognitive]] **AND** [[**All**: home*] **OR** [**All**: communit*] **OR** [**All**: building*]] **AND** [**E-Publication Date**: Past 5 years]
```
Results: 404


### IEEE Xplore:
```
("user modeling" OR "user profiling" AND profile AND preferences AND (intelligent OR smart OR cognitive) AND (home* OR communit* OR building*))
```
Results: 174


For each paper:
- Which problem does it address?
- What method it uses?
- What type of solution it reaches (merely computational, real life test, demonstration)?
- The innovation or the advancements of the paper

## Rule-based Selection

Script: `screen.py` — keyword heuristics applied to title + abstract only.
Output: `screening_results.csv`

### Corpus
| Source | Raw entries | After dedup |
|--------|------------|-------------|
| WOS (`savedrecs.bib`) | 55 | — |
| ACM (`acm.bib`) | 404 | — |
| IEEE (2 files) | 174 | — |
| **Total** | **633** | **625** |

### Results
| Decision | Count |
|----------|-------|
| INCLUDE | 4 |
| EXCLUDE | 104 |
| UNCERTAIN | 517 |

### Exclusion Breakdown
| Criterion | Count | % of exclusions |
|-----------|------:|----------------:|
| EC2 – web/social platform context | 90 | 86.5% |
| EC4 – non-full paper / no abstract | 11 | 10.6% |
| EC1 – environment-only modeling | 3 | 2.9% |

#### EC2 sub-contexts
| Sub-context | Count |
|-------------|------:|
| Social media | 32 |
| E-commerce | 25 |
| News recommendation | 14 |
| Sentiment analysis | 10 |
| Online platform (generic) | 9 |
| Click-through rate | 6 |
| Movie recommendation | 3 |
| Ad targeting | 1 |

### UNCERTAIN Breakdown

Individual flag frequency across the 517 uncertain papers:

| Missing criterion | Papers flagged | % of UNCERTAIN |
|-------------------|---------------:|---------------:|
| No built environment context | 496 | 95.9% |
| No relational/generative AI method | 374 | 72.3% |
| No psychological/interactional dimension | 319 | 61.7% |

Flag combinations:

| Missing signals | Count | % of UNCERTAIN |
|----------------|------:|---------------:|
| All three (method + human + context) | 223 | 43.1% |
| No built env + no relational/GenAI method | 131 | 25.3% |
| No built env + no psychological dimension | 79 | 15.3% |
| No built env only (has method + human) | 63 | 12.2% |
| No relational/GenAI + no psychological (built env present) | 16 | 3.1% |
| No relational/GenAI only | 4 | 0.8% |
| No psychological dimension only | 1 | 0.2% |

### Notes
- **EC2 is the dominant exclusion driver** (87% of all exclusions). The search pulls heavily from recommendation-systems literature (social media, e-commerce, news) that shares the right methods but not the right domain.
- **"No built environment context" is the dominant UNCERTAIN flag** (96% of uncertain papers). The UNCERTAIN pile is large but mostly not borderline — these papers lack domain relevance rather than methodological relevance.
- The 63 papers with method + human but no context signal are recommendation-system papers (POI, video, sequential) that should likely move to EC2 after manual check.
- The 223 missing all signals are almost certainly off-topic but were not safely auto-excluded; they require a fast title scan.
- The 4 automatic INCLUDEs were verified as plausible candidates.
- Rule-based pass is intentionally conservative (517 UNCERTAIN) to avoid false exclusions before manual screening.

---

## Claude Reasoning Screening

Script: `screen_claude.py` — full abstract read by Claude with IC/EC reasoning per paper.
Output: `screening_claude.csv`

### Results
| Decision  | Count | % of corpus |
| --------- | ----: | ----------: |
| INCLUDE   |     0 |          0% |
| UNCERTAIN |    56 |        9.0% |
| EXCLUDE   |   569 |       91.0% |

### Exclusion Breakdown
| Category                                                       | Count | % of exclusions |
| -------------------------------------------------------------- | ----: | --------------: |
| EC2 – Web / social / recommendation platform                   |   269 |           47.3% |
| Context mismatch – generic (wrong domain, no EC label applied) |   235 |           41.3% |
| EC4 – Non-full paper / no abstract                             |    25 |            4.4% |
| Context mismatch – Metaverse / VR / gaming                     |    17 |            3.0% |
| EC1 – Environment-only (no user psychological model)           |     6 |            1.1% |
| Context mismatch – Healthcare / clinical                       |     5 |            0.9% |
| Context mismatch – Robotics / HRI                              |     5 |            0.9% |
| EC3 – Black-box DL / no interpretable user model               |     3 |            0.5% |
| Context mismatch – Wireless / comms / hardware                 |     3 |            0.5% |
| Context mismatch – Education / e-learning                      |     2 |            0.4% |

The "generic context mismatch" category (235 papers) represents papers Claude rejected for clearly not fitting the built-environment scope, but whose reasons didn't map cleanly to EC1–EC4 (e.g., autonomous vehicles, dialog systems, urban analytics, finance). These are papers the keyword heuristic could not safely reject because they superficially matched the search terms.

### UNCERTAIN Breakdown (n=56)

These are the papers Claude could not safely decide from the abstract alone. Each paper had one or more ICs that were ambiguous.

#### IC status across uncertain papers

| IC | Missing / unclear | Borderline (partially met) |
|----|------------------:|---------------------------:|
| IC3 – Relational/generative AI method | 16 (29%) | 5 (9%) |
| IC4 – Psychological/interactional dimension | 3 (5%) | 16 (29%) |
| IC5 – Built environment context | 10 (18%) | 21 (38%) |

**IC5 is the primary bottleneck** for uncertain papers: 59% have it either missing or borderline (e.g., hospitals, museums, cultural heritage sites, autonomous vehicles, smart cities). **IC3 is the second bottleneck**: 38% have it missing or unclear, mostly papers that have the right human dimension but use classical ML or statistical methods.

#### IC combination patterns in UNCERTAIN papers

| Pattern | Count |
|---------|------:|
| IC5 borderline only (method + human present) | 9 |
| All ICs present — context ambiguity only | 9 |
| IC5 missing (clearly outside built env) | 8 |
| IC3 missing + IC4 borderline | 7 |
| IC3 missing only | 4 |
| IC3 missing + IC5 borderline | 4 |
| IC4 + IC5 both borderline | 4 |
| IC4 borderline only | 2 |
| IC4 missing + IC5 borderline | 2 |
| IC3 + IC5 both borderline | 1 |

### Comparison with Rule-Based Screening

#### Transition matrix (rule-based → Claude)

| Rule-based \ Claude | → INCLUDE | → UNCERTAIN | → EXCLUDE | Row total |
|---------------------|----------:|------------:|----------:|----------:|
| INCLUDE | 0 | 3 | 1 | 4 |
| UNCERTAIN | 0 | 48 | **469** | 517 |
| EXCLUDE | 0 | 5 | 99 | 104 |
| **Col total** | **0** | **56** | **569** | 625 |

- **Overall agreement: 23.5%** — low because the rule-based screener deferred 517 papers to UNCERTAIN, while Claude resolved 91% of them.
- **Agreement on exclusions: 95.2%** (99/104 rule-based EXCLUDEs confirmed). The 5 that Claude moved to UNCERTAIN were borderline EC4 or context-mismatch cases where the abstract hinted at some relevance.
- **469 rule-based UNCERTAINs converted to EXCLUDE** by Claude: these were papers the keyword heuristic could not safely reject, but whose abstracts made the domain mismatch clear on reading.
- **48 rule-based UNCERTAINs remained UNCERTAIN** in Claude: these are the true borderline cases for human review.
- **1 rule-based INCLUDE downgraded to UNCERTAIN** by Claude (id=1: ontology-based smart home preferences, IC4 borderline — lighting/heating state, not psychological traits).
- **0 INCLUDEs** confirmed by Claude at abstract level: the 4 rule-based INCLUDEs were either downgraded (1) or moved to UNCERTAIN (3), suggesting the full-text review is needed before confirming any inclusions.

### Notes
- The 56 UNCERTAIN papers are the actual pool for human full-text review; the rule-based 517 is now resolved to 56.
- Claude's ability to recognize context mismatch (e.g., "cognitive radio" ≠ human cognition, metaverse ≠ physical built space) was the main driver of the 91% reduction in the UNCERTAIN pool.
- EC5 (out-of-date, pre-2019) was not triggered by Claude — the search was already filtered to the last 5 years.
- IC5 ambiguity (38% of UNCERTAIN) is the most consequential design decision going forward: whether museums, hospitals, autonomous vehicles, and smart cities count as "built environments" for this review needs a clear policy decision before full-text screening.
