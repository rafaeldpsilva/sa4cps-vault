In this research, I not only want to capture "smart preferences" such as comfort ones, but what Im really after is how the user is, how does he likes to interact with systems, his personality and what he expects from the systems. Moving from Environmental Modeling, such as thermostat settings, to Cognitive and Behavioral Modeling (psychology and interaction design)

Similar concepts of the literature:
- Human-Centric Intelligent Environments
- Socially-Aware Smart Builings

This means that the system is not only modeling a "resident", but modeling a "persona".

## Research Question
*To what extent have existing approaches applied relational or generative AI methods to infer and model the psychological and interactional dimensions of occupants (personality traits, interaction styles, and expectations) within intelligent or smart buildings?*

## What is the domain of this review?
This research is focused on the "Human-in-the-loop" aspcet, specifically looking at how AI decodes human nature within physical spaces.

**The where**: The context is intelligent or smart buildings. Smart communities may serve as a broader deployment context, but the locus of user modeling is always the building level.

**The who**: The model target is Relational Psychographics/ Psychographic Profiling. This includes personality traits (e.g., Big Five or MBTI-derived traits), interaction styles (e.g., Preferred modality (voice/touch), agency level (proactive/reactive), and feedback loops), and expectation management (e.g., trust levels in automation, anticipated system reliability, transparency, and "intelligence" level)

**The how**:
**LLMs:** Used as "Psychological Engines" to infer personality from natural language feedback or behavioral logs. Acting as "Feature Extractors" to translate raw interaction logs into the semantic nodes (personality/expectations) that populate the GNN.
**GNNs:** Building heterogeneous graphs where edges represent the _strength of relationship_ between a user's personality and their interaction choices. This allows for Cross-User Comparison (graph isomorphism or alignment).

## Scope Statement
This review investigates the intersection of User Profiling (UP) and User Modeling (UM) within intelligent or smart buildings, with a specific focus on the occupant's psychological and interactional dimensions. Moving beyond environmental setpoints, this research centers on modeling the occupant as a complex entity defined by its personality traits, interaction styles, and expectations.

Central to this scope is the use of Heterogeneous Graph Neural Networks (HGNNs) to map the multi-dimensional relationships between these psychological entities and observed behaviors, enabling the comparison of structural "User Graphs" to identify common interaction archetypes. Furthermore, we examine the role of Large Language Models (LLMs) as reasoning engines that interpret qualitative user data to synthesize the nodes and attributes within these relational models.

The scope is bounded by research that addresses the overall lifecycle of such system, from user data, to profiling, to modeling, and finally to personalization. We exclude papers focused solely on social network analysis or generic occupancy sensing. The goal is to provide a roadmap for developing "expectation-aware" systems that adapt their logic to the structural psychological profile of the user, rather than just their physical preferences.

## Keywords

A valid paper should cover at least three of these.

Category A (Tech):
- Large Language Models
- Generative AI
- Foundation Models (??)
- Prompt Engineering
- Multi-modal LLMs

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
- Smart Communities / Intelligent Buildings
- Built Environments
- Ambient Intelligence
- IoT User Experience

## Inclusion and Exclusion Criteria

### ✅ Inclusion Criteria
1. Peer-reviewed: Must be from a journal or a top-tier conference
2. Approach: Must utilize at least one relational or generative method
3. Human-Centric: Must model at least one psychological or interactional trait %%personality, expection, style%%
4. Context: Must be situated in a built environment
### ❌ Exclusion Criteria
1. Focusing only on environment modeling (occupancy sensing, thermal comfort) without modeling the user's nature
2. User profiling for sentimental analysis or ad-targetting on web platforms
3. Deep learning papers that don't provide a "model" representation

## Search Strings

## V1
Total: 107

User Modeling OR User Profiling
Smart Building* OR Intelligent Environment* OR Smart Communit* 

(TS=("User Modeling" OR "User Profiling") 
AND TS=("Smart Building*" OR "Intelligent Environment*" OR "Smart Communit*") 
AND TS=("LLM" OR "Large Language Model*" OR "GNN" OR "Graph Neural Network*" OR "Knowledge Graph*") 
AND TS=("Personality" OR "Interaction Style" OR "Expectation*" OR "Psychographic*"))

### WOS: 
```
(((ALL=(User Modeling OR User Profiling)) AND ALL=(Smart Building* OR Intelligent Environment* OR Smart Communit* )) AND ALL=(LLM OR Large Language Model* OR GNN OR Graph Neural Network* OR Knowledge Graph* )) AND ALL=(Personality OR Interaction Style OR Expectation* OR Psychographic*)
```
Results: 15
### ACM:
```
[[**All**: "user modeling"] **OR** [**All**: "user profiling"]] **AND** [[**All**: "smart building*"] **OR** [**All**: "intelligent environment*"] **OR** [**All**: "smart communit*"]] **AND** [[**All**: llm] **OR** [**All**: "large language model*"] **OR** [**All**: gnn] **OR** [**All**: "graph neural network*"] **OR** [**All**: "knowledge graph*"]] **AND** [[**All**: personality] **OR** [**All**: "interaction style"] **OR** [**All**: expectation*] **OR** [**All**: psychographic*]]
```
Results: 51

### IEEE Xplore:
```
("All Metadata":User Modeling OR "All Metadata":User Profiling) AND ("All Metadata":Smart Building* OR "All Metadata":Intelligent Environment* OR "All Metadata":Smart Communit*) AND ("All Metadata":LLM OR "All Metadata":Large Language Model* OR "All Metadata":GNN OR "All Metadata":Graph Neural Network* OR "All Metadata":Knowledge Graph*) AND ("All Metadata":Personality OR "All Metadata":Interaction Style OR "All Metadata":Expectation* OR "All Metadata":Psychographic*)
```
Results: 41


### V2
Total: 
user modeling OR user profiling 
profile AND preferences
(intelligent OR smart OR cognitive) AND (home* OR communit* OR building*)
### WOS: 
```
(ALL=(user modeling AND user profiling) AND ALL=(intelligent OR smart OR cognitive) AND ALL=(home* OR communit* OR building*))
```
Results: 267
### ACM:
```
[**All**: "user modeling"] **AND** [**All**: "user profiling"] **AND** [**All**: profile] **AND** [**All**: preferences] **AND** [[**All**: intelligent] **OR** [**All**: smart] **OR** [**All**: cognitive]] **AND** [[**All**: home*] **OR** [**All**: communit*] **OR** [**All**: building*]]
```
Results: 132

### IEEE Xplore:
```
("All Metadata":User Modeling OR "All Metadata":User Profiling) AND ("All Metadata":Smart Building* OR "All Metadata":Intelligent Environment* OR "All Metadata":Smart Communit*) AND ("All Metadata":LLM OR "All Metadata":Large Language Model* OR "All Metadata":GNN OR "All Metadata":Graph Neural Network* OR "All Metadata":Knowledge Graph*) AND ("All Metadata":Personality OR "All Metadata":Interaction Style OR "All Metadata":Expectation* OR "All Metadata":Psychographic*)
```
Results: 41
