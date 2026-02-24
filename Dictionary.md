## **User Modeling Paradigms**

| Concept                               | Definition                                                                                                     |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Smart Preferences**                 | Surface-level user preferences (e.g., comfort settings, thermostat), the baseline this research moves *beyond* |
| **Environmental Modeling**            | Traditional approach to modeling users via physical setpoints (e.g., temperature, lighting)                    |
| **Cognitive and Behavioral Modeling** | Broader approach encompassing psychology and interaction design, replacing pure environmental modeling         |
| **Resident (model)**                  | The conventional, minimal model of a building occupant — what this research is moving away from                |
| **Persona (model)**                   | A richer model of the occupant that captures personality, interaction style, and expectations                  |
| **User Profiling (UP)**               | The process of collecting and organizing data about a user to characterize them                                |
| **User Modeling (UM)**                | Building a computational representation of the user that drives system adaptation                              |
| **Occupant Modeling**                 | Domain-specific framing of UM/UP within built environments                                                     |

---

## Psychological & Interactional Dimensions

| Concept                                                 | Definition                                                                                                               |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **Relational Psychographics / Psychographic Profiling** | The central modeling target — capturing personality, interaction style, and expectations as relational entities          |
| **Personality Traits**                                  | Stable psychological characteristics of the user (operationalized via Big Five or MBTI frameworks)                       |
| **Big Five**                                            | A widely-used psychological model of personality (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism) |
| **MBTI-derived traits**                                 | Traits derived from the Myers-Briggs Type Indicator framework                                                            |
|                                                         |                                                                                                                          |
|                                                         |                                                                                                                          |
| **Agency Level**                                        | Whether the user prefers to be proactive (initiating) or reactive (responding) in system interactions                    |
|                                                         |                                                                                                                          |
|                                                         |                                                                                                                          |
| **Trust in Automation**                                 | The degree to which a user relies on or delegates control to automated systems                                           |
| **Anticipated System Reliability**                      | User's expectation of how consistently and correctly the system will perform                                             |
| **Transparency**                                        | The degree to which a system explains its actions/decisions to the user                                                  |
| **Intelligence Level (expected)**                       | The user's expectation of how "smart" or capable the system should appear/behave                                         |

---

## Environment & Context

| Concept | Definition |
|---|---|
| **Intelligent/Smart Buildings** | Physical environments with embedded sensing, actuation, and AI-driven control |
| **Smart Communities** | Broader socio-physical spaces incorporating intelligent infrastructure and inter-building coordination |
| **Human-Centric Intelligent Environments** | Literature term for environments designed around human needs and preferences |
| **Socially-Aware Smart Buildings** | Literature term for buildings that account for social context and interpersonal dynamics |
| **Physical Spaces** | The built environment context in which AI decodes human nature |

---

## AI / Computational Methods

| Concept | Definition |
|---|---|
| **Human-in-the-loop (HITL)** | Design paradigm that keeps the human as an active participant in system decision-making |
| **LLMs (Large Language Models)** | AI models used as reasoning engines to interpret natural language and behavioral data |
| **Psychological Engines** | Role of LLMs — inferring personality from language and behavioral logs |
| **Feature Extractors** | Role of LLMs — translating raw interaction logs into structured semantic nodes |
| **Behavioral Logs** | Raw records of user interaction events used as input to the modeling pipeline |
| **Natural Language Feedback** | Qualitative user input (text/speech) processed by LLMs to infer psychological attributes |
| **GNNs (Graph Neural Networks)** | Neural networks that operate on graph-structured data, used here to model user relationships |
| **HGNNs (Heterogeneous Graph Neural Networks)** | GNNs that handle graphs with multiple node/edge types, central to the proposed architecture |
| **Heterogeneous Graphs** | Graphs with diverse node and edge types (e.g., personality nodes, behavior nodes, relationship edges) |
| **Semantic Nodes** | Graph nodes representing psychological/behavioral concepts (personality, expectations) populated by LLMs |
| **Edge Strength** | The weight of a graph edge, representing the relationship intensity between personality and interaction choices |
| **User Graphs** | Structural graph representations of individual users encoding their psychological profile |
| **Cross-User Comparison** | Comparing User Graphs across individuals to find patterns — enabled via graph isomorphism/alignment |
| **Graph Isomorphism / Alignment** | Mathematical technique to compare structural similarity between graphs |
| **Interaction Archetypes** | Common structural patterns in User Graphs identified through cross-user comparison |

---

## System Lifecycle Concepts

| Concept | Definition |
|---|---|
| **Personalization** | Adapting system behavior to match the individual user's profile |
| **Expectation-Aware Systems** | Systems that adapt their logic to the user's psychological and expectation profile, not just physical preferences |
| **Psychological Profile** | The complete structural representation of a user's personality, interaction style, and expectations |
| **Qualitative User Data** | Non-numerical user input (text, speech, feedback) interpreted by LLMs |
| **System Lifecycle** | The full pipeline: user data → profiling → modeling → personalization |
| **Occupancy Sensing** | Generic detection of presence in a space — explicitly excluded from this review's scope |
| **Social Network Analysis** | Graph-based analysis of social relationships — also explicitly excluded from scope |
