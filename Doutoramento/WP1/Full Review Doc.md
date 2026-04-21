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
