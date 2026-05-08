In this research, I not only want to capture "smart preferences" such as comfort ones, but what Im really after is how the user is, how does he likes to interact with systems, his personality and what he expects from the systems. Moving from Environmental Modeling, such as thermostat settings, to Cognitive and Behavioral Modeling (psychology and interaction design)

Similar concepts of the literature:
- Human-Centric Intelligent Environments
- Socially-Aware Smart Builings

This means that the system is not only modeling a "resident", but modeling a "persona".

## Research Question
*What AI methods have been applied to dynamically model, evolve, and reason over occupant preferences and latent intent — at individual and collective levels — within intelligent built environments, and to what extent have relational and generative AI approaches been explored?*

## What is the domain of this review?
This review maps how AI has been applied to model the human dimension within physical spaces — not what the environment does, but what the occupant wants, how those wants evolve, and how systems can anticipate them.

**The where**: The context is intelligent or smart built environments — smart buildings, smart homes, intelligent offices, and smart communities. The locus of modeling is always the occupant within a physical, instrumented space.

**The who**: The model target is the occupant as a dynamic, context-sensitive entity. This includes individual preferences (comfort, interaction style, behavioral patterns), latent intent (needs not yet explicitly expressed), temporal evolution of those preferences, and collective dynamics when multiple occupants share a space.

**The how**: This review surveys the AI methods that existing work has used to generate, evolve, and reason over occupant representations — spanning the full pipeline from raw behavioral and environmental signals, through preference profiling and structured modeling, to proactive personalization and adaptation. The synthesis specifically examines to what extent relational methods (knowledge graphs, ontologies, GNNs) and generative AI methods (LLMs, foundation models) have been applied, and where gaps exist.

## Scope Statement
This review investigates AI-driven occupant modeling within intelligent built environments, covering the full lifecycle of preference representation: generation from behavioral and contextual signals, evolution over time and across contexts, inference of latent intent, and accommodation of collective or multi-occupant dynamics.

In scope are studies that apply any AI method — including but not limited to machine learning, knowledge representation, probabilistic models, or generative architectures — to model or infer occupant preferences, behavioral patterns, contextual needs, or latent intent beyond physical setpoints. The review is interested in approaches at both the individual level (personal preference profiles, interaction patterns, intent recognition) and the collective level (shared-space negotiation, group preference modeling, community-scale personalization).

We exclude papers focused solely on environmental modeling (occupancy sensing, thermal comfort, energy optimization) with no occupant preference or intent layer; user profiling for web-platform purposes (social media, e-commerce, news recommendation) with no built-environment application; and pure rule-based or sensor-threshold systems with no learned occupant representation. The analytical focus of the synthesis is on identifying which methods dominate the existing landscape and where relational and generative AI approaches remain underexplored — directly motivating the thesis's technical contributions.

## Keywords

A valid paper must cover at least one keyword from Category D (context anchor) and at least one from Category B (human dimension). Category A, C, and E keywords are used for the analytical synthesis — they are not inclusion gates.

Category A (Generative AI Methods — analytical lens):
- Large Language Models / LLM
- Generative AI
- Foundation Models
- Natural Language Processing
- Multimodal AI

Category B (Human Dimensions — inclusion anchor):
- User Preferences / Preference Modeling
- Behavioral Profiling / Behavioral Patterns
- Latent Intent / Intent Inference
- Interaction Style / Modality
- Personality Traits
- User Expectation / Trust
- Cognitive Modeling
- Collective / Group Preferences
- Preference Evolution / Dynamic Profiling

Category C (Relational AI Methods — analytical lens):
- Knowledge Graph
- Graph Neural Networks / GNN
- Ontology / Semantic Web
- Heterogeneous Information Networks
- Relational Embedding
- User Modeling / User Profiling

Category D (Context — inclusion anchor):
- Smart Buildings / Smart Homes
- Intelligent Environments
- Built Environments
- Ambient Intelligence
- Smart Communities
- IoT / Cyber-Physical Systems

Category E (General AI Methods — analytical lens):
- Machine Learning / Deep Learning
- Reinforcement Learning
- Bayesian / Probabilistic Models
- Federated Learning
- Transformer / Attention Models

## Inclusion and Exclusion Criteria

All inclusion criteria must be satisfied. Any single exclusion criterion is sufficient to reject.

### ✅ Inclusion Criteria
1. **Publication type**: Peer-reviewed journal article or full conference paper (not workshop summary, poster, or extended abstract)
2. **Language**: Written in English
3. **AI Method**: Applies at least one AI method (machine learning, knowledge representation, probabilistic model, or generative architecture) to model or infer occupant-level information — not solely to optimize physical parameters
4. **Human Dimension**: Models or infers at least one dimension of occupant preference, behavioral pattern, contextual need, or latent intent — beyond physical setpoints — including comfort preferences, interaction preferences, temporal behavioral patterns, intent signals, or collective/group dynamics
5. **Context**: Work is situated in a built environment (smart building, smart home, intelligent environment, smart community, or equivalent physical space)

### ❌ Exclusion Criteria
1. **EC1 – Environment-only**: Focuses exclusively on physical or environmental modeling (occupancy sensing, thermal comfort, energy, HVAC) with no occupant preference or intent layer
2. **EC2 – Web platform**: User profiling for web-platform purposes (ad targeting, sentiment analysis, social media or e-commerce recommendation) with no built-environment application
3. **EC3 – No learned representation**: Pure rule-based or sensor-threshold systems that produce no learned occupant model, profile, or preference representation
4. **EC4 – Non-paper**: Workshop summaries, keynote abstracts, editorials, or papers with no retrievable abstract
5. **EC5 – Out of date**: Published before 2019

> **Note on method (IC3):** The AI method requirement is an *inclusion* gate only — it ensures a learned representation exists. The *type* of method (relational, generative, classical ML) is recorded as a data extraction variable and used in the synthesis to assess how much of the landscape relational and generative AI currently covers.

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
| Source                | Raw entries | After dedup |
| --------------------- | ----------- | ----------- |
| WOS (`savedrecs.bib`) | 55          | —           |
| ACM (`acm.bib`)       | 404         | —           |
| IEEE (2 files)        | 174         | —           |
| **Total**             | **633**     | **625**     |

### Results
| Decision  | Count |
| --------- | ----- |
| INCLUDE   | 4     |
| EXCLUDE   | 104   |
| UNCERTAIN | 517   |

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

> ⚠️ **These results reflect the old criteria** (IC3 required relational/generative AI; IC4 required psychological/interactional traits). Under the revised criteria, the "no relational/generative AI method" flag is no longer an exclusion signal, and "no psychological/interactional dimension" is replaced by the broader human-dimension criterion. The 374 papers flagged only for missing IC3 (old) are candidates for recovery in the re-screening.

Individual flag frequency across the 517 uncertain papers (old criteria):

| Missing criterion | Papers flagged | % of UNCERTAIN | Status under new criteria |
|-------------------|---------------:|---------------:|--------------------------|
| No built environment context | 496 | 95.9% | Still an exclusion signal (IC5) |
| No relational/generative AI method | 374 | 72.3% | **No longer an exclusion signal** |
| No psychological/interactional dimension | 319 | 61.7% | Replaced by broader IC4 |

Flag combinations (old criteria):

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
- **"No built environment context" is the dominant UNCERTAIN flag** (96% of uncertain papers). This signal remains valid under the revised criteria.
- The 63 papers with method + human but no context signal are recommendation-system papers (POI, video, sequential) that should likely move to EC2 after manual check.
- The 223 missing all signals are almost certainly off-topic but were not safely auto-excluded; they require a fast title scan.
- The 4 automatic INCLUDEs were verified as plausible candidates.
- **Both screenings need to be re-run under the revised IC3 and IC4.** The 4 papers flagged only for "no relational/GenAI method" (old IC3) are the clearest recovery candidates; the 16 papers with built-env context but missing both method and human dimension under old IC4 also warrant a second look.

---

## Claude Reasoning Screening

> ⚠️ **These results reflect the old criteria.** Under the revised RQ, IC3 no longer requires relational/generative AI as a *gate*, and IC4 is broadened to include any occupant preference, behavioral pattern, or intent dimension. This screening should be re-run with the updated criteria before full-text review begins.

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


## Screening

|Paper|(1) Occupant Dimension|(2) AI Method|(3) Evolution|(4) Evaluation Type|(5) Multi-Occupant Conflict/Negotiation|
|:--|:--|:--|:--|:--|:--|
|**Yang et al. (2024)**,|behavioral pattern|classical ML|evolves over time|simulation|No|
|**Albayaydh & Flechais (2024)**,|collective/group dynamics|knowledge representation/ontology|static|user study|Yes (handles privacy tensions/conflicts)|
|**Alsaadi & Alahmadi (2021)**|interaction style|classical ML|static|dataset benchmark|No|
|**Araujo & Junior (2026)**|interaction style|classical ML|evolves over time|dataset benchmark|No|
|**Asprino et al. (2024)**|collective/group dynamics|knowledge representation/ontology|static|dataset benchmark|Yes (models community cohesion)|
|**Cham & Kefalidou (2025)**|comfort preference|classical ML|evolves over time|user study|No|
|**Constantinescu & Iftene (2025)**|behavioral pattern|deep learning|evolves over time|simulation|No|
|**Danry et al. (2026)**,|behavioral pattern|LLM/generative|evolves over time|user study|Yes (predicts conflict responses)|
|**Delle Monache et al. (2022)**|comfort preference|classical ML|static|user study|No|
|**Di Napoli et al. (2023)**,|behavioral pattern|hybrid|evolves over time|real deployment|No|
|**Emami-Naeini et al. (2023)**|comfort preference|probabilistic|static|user study|No|
|**Festus et al. (2024)**|comfort preference|knowledge representation/ontology|evolves over time|simulation|No|
|**Florentino & Aquino-Junior (2025)**|interaction style|hybrid|evolves over time|simulation|No|
|**Freire et al. (2021)**,|latent intent|probabilistic|evolves over time|user study|No|
|**Guo & Yuan (2026)**,|behavioral pattern|hybrid|evolves over time|real deployment|No|
|**Han et al. (2025)**|latent intent|hybrid|evolves over time|user study|No|
|**Hashky et al. (2024)**|behavioral pattern|classical ML|static|dataset benchmark|No|
|**Huang et al. (2025)**|comfort preference|LLM/generative|evolves over time|user study|No|
|**Irfan et al. (2025)**,|interaction style|hybrid|evolves over time|simulation|Yes (multi-user interactions)|
|**Javdani Rikhtehgar et al. (2023)**|behavioral pattern|GNN/relational|evolves over time|user study|No|
|**Javdani Rikhtehgar et al. (2025)**|interaction style|LLM/generative|evolves over time|user study|No|
|**Jia et al. (2025)**|behavioral pattern|deep learning|static|user study|No|
|**Jin et al. (2026)**|behavioral pattern|hybrid|static|dataset benchmark|No|
|**Langerak et al. (2026)**,|latent intent|hybrid|evolves over time|simulation|Yes (handles partner factors)|
|**Liu et al. (2023a)**|behavioral pattern|GNN/relational|static|dataset benchmark|No|
|**Liu et al. (2023b)**|behavioral pattern|GNN/relational|static|dataset benchmark|No|
|**Liu et al. (2024)**|comfort preference|hybrid|evolves over time|dataset benchmark|No|
|**Liu et al. (2025)**|interaction style|GNN/relational|static|dataset benchmark|No|
|**Ma et al. (2022)**|comfort preference|classical ML|static|user study|No|
|**Md Zuki et al. (2025)**,|behavioral pattern|reinforcement learning|evolves over time|simulation|No|
|**Naser et al. (2023)**|behavioral pattern|deep learning|evolves over time|real deployment|No|
|**Packia et al. (2024)**|interaction style|hybrid|evolves over time|simulation|No|
|**Pastrakis et al. (2025)**|comfort preference|hybrid|evolves over time|dataset benchmark|No|
|**Klir et al. (2021) / Preference Lighting**|comfort preference|hybrid|evolves over time|user study|No|
|**Qianji et al. (2024)**|behavioral pattern|knowledge representation/ontology|static|simulation|No|
|**Riveiro & Thill (2022)**|latent intent|classical ML|static|user study|No|
|**Sankaran & Markopoulos (2021)**|interaction style|classical ML|static|user study|No|
|**Shukla et al. (2025)**|behavioral pattern|deep learning|static|dataset benchmark|No|
|**Slavkovik et al. (2021)**|behavioral pattern|classical ML|static|dataset benchmark|No|
|**Tamah Al-Shammari (2025)**|interaction style|LLM/generative|evolves over time|simulation|No|
|**Tang et al. (2024)**|behavioral pattern|hybrid|static|dataset benchmark|No|
|**Tran et al. (2021)**,|collective/group dynamics|hybrid|evolves over time|dataset benchmark|Yes (resolves group conflict)|
|**Tsihrintzis et al. (2025)**|interaction style|LLM/generative|static|user study|No|
|**Tsitseklis et al. (2023)**|behavioral pattern|hybrid|evolves over time|dataset benchmark|No|
|**Umbrico et al. (2021)**|collective/group dynamics|knowledge representation/ontology|evolves over time|simulation|Yes (team work & shared goals)|
|**Virvou & Tsihrintzis (2025)**,|behavioral pattern|classical ML|evolves over time|dataset benchmark|No|
|**Vozna et al. (2025)**,|interaction style|hybrid|evolves over time|simulation|No|
|**Wu & Jokinen (2025)**|latent intent|probabilistic|evolves over time|user study|No|
|**Yoo et al. (2024)**|behavioral pattern|deep learning|evolves over time|dataset benchmark|No|
|**Yu et al. (2024)**|comfort preference|hybrid|evolves over time|simulation|No|
|**Zhao & Silverajan (2024)**|interaction style|LLM/generative|static|user study|No|
|**Zukerman et al. (2023)**,|behavioral pattern|classical ML|evolves over time|user study|No|
Which papers use relational AI methods (knowledge graphs, ontologies, GNNs, semantic web) or generative AI methods (LLMs, foundation models, NLP-based generation)? For those that don't, what method do they use instead and what occupant modeling limitation does that create?
**Papers Using Relational AI Methods** The following papers leverage relational AI, such as knowledge graphs (KGs), ontologies, Graph Neural Networks (GNNs), and the Semantic Web to map complex relationships and contexts:

- **Asprino et al. (2024)** uses an Ontology Network (the SPICE Ontology Network) linked with the Semantic Web to interpret cultural heritage data, emotional responses, and citizen curation.
- **Festus et al. (2024)** leverages ontology-based user preferencing to build a dynamic knowledge base for smart home environments.
- **Javdani Rikhtehgar et al. (2023)** employs a Knowledge Graph to model user preferences and culturally relevant exhibits for personalized Virtual Reality museum tours.
- **Liu et al. (2023a)** and **Liu et al. (2023b)** construct an Urban Knowledge Graph (UrbanKG) to extract semantic relationships (e.g., home, workplace, spatiality) combined with GNNs and tensor decomposition for mobile user profiling.
- **Liu et al. (2024)** integrates knowledge graph technology into an AI-powered dialogue system for providing product recommendations in the home appliance industry.
- **Liu et al. (2025)** proposes Graph Neural Networks (GNNs) to model the complex, hierarchical, and nonlinear dependencies between user behaviors and interface elements for satisfaction classification.
- **Qianji et al. (2024)** builds a Knowledge Graph linked with user profiles to map entity relationships (like books, authors, and users) for library retrieval systems.
- **Tsitseklis et al. (2023)** utilizes a Knowledge Graph coupled with NLP for a museum chatbot assistant to handle semantic reasoning between exhibits.
- **Umbrico et al. (2021)** implements knowledge bases and standard semantic ontologies (OWL language) to model worker profiles and robot capabilities in cyber-physical manufacturing systems.
- **Vozna et al. (2025)** uses an ASP-based engine and a Reference Ontology of Trust (ROT) for dynamic semantic reasoning and trust calibration in personalized digital health.

**Papers Using Generative AI Methods** These papers employ Large Language Models (LLMs), foundation models, or NLP-based generation for reasoning, predicting behavior, or natural language generation:

- **Danry et al. (2026)** utilizes a multi-stage LLM pipeline (based on GPT-5) to mine conversational data and extract human-readable "if-then" behavioral patterns.
- **Han et al. (2025)** implements a hybrid framework combining a Dynamic Bayesian Network (DBN) with an LLM. The LLM acts as an "interaction design expert" to inject contextual world knowledge into the system for smart environments.
- **Huang et al. (2025)** proposes an LLM-based system to dynamically scan images of built environments and generate personalized accessibility heuristics for users with limited mobility.
- **Jin et al. (2026)** combines prompt fine-tuning of lightweight LLMs with traditional machine learning to efficiently extract hidden semantic features for dynamic privacy-portrait linkage.
- **Md Zuki et al. (2025)** discusses the unprecedented capabilities of LLMs to generate personalized persuasive content and understand user preferences through natural language.
- **Tamah Al-Shammari (2025)** relies on an AI-driven narrative engine for visual storytelling related to cultural heritage.
- **Tsihrintzis et al. (2025)** evaluates user trust dynamics explicitly by having expert and non-expert stakeholders interact directly with Generative AI (ChatGPT) in the energy urban domain.
- **Zhao & Silverajan (2024)** compares different LLMs (like ChatGPT-4, ChatGPT-4o, and Bing Chat) for modeling human behavior to evaluate cybersecurity dashboard usability.

**Methods Used by Other Papers and the Limitations They Create** Papers that do not rely on relational or generative models predominantly use **Classical Machine Learning** (e.g., K-means clustering, Random Forests, Support Vector Machines), **Deep Learning** (e.g., CNNs, RNNs), or **Probabilistic/Statistical Modeling** (e.g., Bayesian Inverse Reinforcement Learning, Dynamic Bayesian Networks).

Relying on these alternative methods creates several notable limitations in occupant modeling:

- **Overlooking Context and Semantics:** Traditional data-driven paradigms often ignore the complex semantic relationships between a user and their environment. As noted in multiple domains, standard machine learning frequently overlooks highly influential, nuanced contextual factors like a user's self-esteem, motivation, and abstract experiential needs. They struggle to capture non-Euclidean relationships that graph structures easily map out.
- **Stereotyping and Overgeneralization:** Methods reliant on traditional clustering and fixed stereotypes (e.g., classifying users strictly as 'novice' or 'expert' based on demographic or early behavioral data) lead to a "one-size-fits-all" trap. These systems generalize groups broadly but fail to individualize support. Consequently, they cannot dynamically adapt in real-time as a user's skills or preferences evolve, which can restrict users into biased profiles and outdated recommendations.
- **The Black-Box Interpretability Problem:** Neural networks and deep learning models with massive parameter spaces often lack transparency. Because they implicitly learn low-dimensional vectors without explicit relationship mapping, they are prone to overfitting and poor cross-dataset generalization. Crucially, they fail to explain _why_ a prediction or user adaptation was made, making them unreliable in trust-sensitive scenarios.
- **Computational Bottlenecks and Observability Constraints:** Highly rigorous probabilistic models (such as Approximate Bayesian Inverse Reinforcement Learning) are excellent at managing uncertainty but suffer from high computational overhead. They require extensive simulations to converge and frequently assume that all interface states and user traits are fully observable. In reality, human cognitive shifts are hidden and change dynamically during an ongoing task, making these models difficult to deploy for real-time occupant modeling without structural approximations.

**Papers Modeling Preference Change Over Time** Several papers in the sources actively model how user preferences and profiles evolve over time:

- **Yang et al. (2024)** highlights the necessity of dynamic user profiling for products with long life cycles, specifically tracking how needs, physiological states, and behaviors shift progressively over the stages of pregnancy.
- **Virvou & Tsihrintzis (2025)** proposes an anti-bias framework that transitions from cold-start stereotypes to highly individualized models that continuously evolve over time based on ongoing behavioral interactions.
- **Guo & Yuan (2026)** utilizes a dynamic tag weight iteration technique with a time-decay algorithm to downgrade historical behaviors and elevate recent interests (e.g., shifting from "daily consumption" to "maternal products").
- **Vozna et al. (2025)** introduces evolving "Blueprint Personas" for digital health, adapting interaction styles and prompt frequencies as a patient's medical condition and trust in the system fluctuate over time.
- **Klir et al. (2021)** implements a Preference Lighting Model using Contextual Multi-Armed Bandits to dynamically recommend optimal light spectra as the user's biological rhythms and preferences naturally alter throughout the day.
- **Md Zuki et al. (2025)** utilizes Sequential Decision-Making Theory to model the complex, long-term patterns of user behavior in persuasive technologies, adjusting to progress, setbacks, and motivational shifts.
- **Pastrakis et al. (2025)** argues that tourist personas are dynamic and must adapt to the fact that user preferences actively evolve following increased exposure to new cultural experiences.

**Triggers for Adaptation: Explicit Feedback, Implicit Behavioral Drift, and Context Change** Adaptation in these dynamic models is triggered by three primary mechanisms:

- **Explicit Feedback:** Some systems rely on the user directly telling the system to adjust. **Umbrico et al. (2021)** personalizes robotic assembly line support by updating profile weights via explicit operator feedback at the end of every task. Similarly, **Huang et al. (2025)** relies on textual feedback from users regarding environmental scans to continually adjust their personal accessibility model, and **Delle Monache et al. (2022)** relies on explicit survey feedback to calibrate sleep music profiles.
- **Implicit Behavioral Drift:** Adaptation occurs silently as the system observes changes in interaction patterns. **Freire et al. (2021)** uses "inverse foraging" to estimate changing interests purely from how much time a user spends looking at a display. **Araujo & Junior (2026)** dynamically updates psychological profiling by logging real-time navigation variables like reading patterns, backspace usage, and menu dwell time. **Virvou & Tsihrintzis (2025)** specify that updates trigger automatically when user clicks or views significantly diverge from initial assumptions.
- **Context Change:** The environment or situational framing prompts a preference shift. **Cham & Kefalidou (2025)** found that users skeptical of autonomous vehicles ("rejectors") exhibit profound preference changes when the context shifts from partial autonomy to full autonomy. **Festus et al. (2024)** triggers adaptations through IoT sensors identifying new temporal or physical contexts (e.g., stepping onto a pressure pad between 2:00 PM and 5:00 PM triggers a sleep lighting preference). **Tran et al. (2021)** notes that temporary emotional states act as a contextual trigger, dramatically altering preferences (e.g., desiring electronic music when happy, but jazz when depressed).

**Papers Treating Preferences as Static Profiles** While dynamic modeling is growing, several systems still rely on static or fixed profiling:

- **Tamah Al-Shammari (2025)** utilizes rule-based "cold-start" personalization for a heritage app. Because it avoids behavioral tracking or data retention to protect privacy, the chosen persona (e.g., scholar, tourist, child) remains static throughout the interaction.
- **Liu et al. (2023)** extracts semantic connections from mobility data (UrbanKG) but largely uses it to statically classify a user's demographic traits, income level, and occupation based on their historical home and workplace locations.
- **Tang et al. (2024)** and **Alsaadi & Alahmadi (2021)** describe user portraits formed predominantly through fixed demographic tags (gender, age, ethnicity) and basic functional tracking without accounting for temporal evolution.
- **Tran et al. (2021)** highlights that in many recommender systems, the _personality_ component of a user profile (e.g., Big Five traits) is mathematically treated as "domain-independent" and "context-independent", meaning it is assumed to be a static baseline.

Are you particularly interested in exploring how these adaptive models are implemented in a specific domain, like healthcare or smart home environments?
