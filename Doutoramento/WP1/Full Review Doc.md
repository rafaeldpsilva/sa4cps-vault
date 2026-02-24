In this research, I not only want to capture "smart preferences" such as comfort ones, but what Im really after is how the user is, how does he likes to interact with systems, his personality and what he expects from the systems. Moving from Environmental Modeling, such as thermostat settings, to Cognitive and Behavioral Modeling (psychology and interaction design)

Similar concepts of the literature:
- Human-Centric Intelligent Environments
- Socially-Aware Smart Builings

This means that the system is not only modeling a "resident", but modeling a "persona".

### What is the domain of this review?
This research is focused on the "Human-in-the-loop" aspcet, specifically looking at how AI decodes human nature within physical spaces.

**The where**: The context is physical environments such as Intelligent/Smart Communities and Buildings.

**The who**: The model target is Relational Psychographics/ Psychographic Profiling. This includes personality traits (e.g., Big Five or MBTI-derived traits), interaction styles (e.g., Preferred modality (voice/touch), agency level (proactive/reactive), and feedback loops), and expectation management (e.g., trust levels in automation, anticipated system reliability, transparency, and "intelligence" level)

**The how**:
**LLMs:** Used as "Psychological Engines" to infer personality from natural language feedback or behavioral logs. Acting as "Feature Extractors" to translate raw interaction logs into the semantic nodes (personality/expectations) that populate the GNN.
**GNNs:** Building heterogeneous graphs where edges represent the _strength of relationship_ between a user's personality and their interaction choices. This allows for Cross-User Comparison (graph isomorphism or alignment).

## Scope Statement
This review investigates the intersection of User Profiling (UP) and User Modeling (UM) within Intelligent Buildings and Smart Communities, with a specific focus on the occupant's psychological and interactional dimensions. Moving beyond environmental setpoints, this research centers on modeling the occupant as a complex entity defined by its personality traits, interaction styles, and expectations.

Central to this scope is the use of Heterogeneous Graph Neural Networks (HGNNs) to map the multi-dimensional relationships between these psychological entities and observed behaviors, enabling the comparison of structural "User Graphs" to identify common interaction archetypes. Furthermore, we examine the role of Large Language Models (LLMs) as reasoning engines that interpret qualitative user data to synthesize the nodes and attributes within these relational models.

The scope is bounded by research that addresses the overall lifecycle of such system, from user data, to profiling, to modeling, and finally to personalization. We exclude papers focused solely on social network analysis or generic occupancy sensing. The goal is to provide a roadmap for developing "expectation-aware" systems that adapt their logic to the structural psychological profile of the user, rather than just their physical preferences.

## Keywords and Strings

We categorized keywords into four categories. A valid paper should cover at least three of these.

Category A (Tech):
- Large Language Models
- Generative AI
- Foundation Models (??)
- Prompt Engineering
- Multi-modal LLMs
Traditional models user if statements logic. LLMs are included because they can perform Zero-Shot Reasoning, meaning that they can look at a user's sentence and infer "This person is anxious and expects high transparency" without a pre-defined rule.
Foundational Models capture the ability to use pre-trained models that already understand human language and social norms, applying them to the intelligent communities and buildings sector.

Category B (Human):
- Personality Traits
- Interaction Style/Modality
- User Expectation
- Cognitive Modeling
- Behavioral Archetypes

Category C (Graph/Relations):
- Heterogeneous Information Networks
- Graph Neural Networks
- Knowledge Graphs
- Graph Alignment/Isomorphism
- Relational Embedding

Category D (Context):
- Smart Buildings/Homes
- Intelligent Communities
- Built Environments
- Ambient Intelligence
- IoT User Experience

