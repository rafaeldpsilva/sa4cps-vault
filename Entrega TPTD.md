**Problem Statement:**
Intelligent buildings today react to explicit commands rather than genuinely understanding the people inside them. When occupants share spaces, conflicts go unresolved or require manual intervention. Existing personalization approaches treat preferences as static, centralized, and explicitly stated — none of which holds in practice.

What doesn't exist yet (the gap):
  - No framework jointly addresses: preference inference from noisy sensor data + multi-occupant conflict + autonomous agent action + LLM-mediated dialogue + privacy at the edge — as a unified, deployable system
  - Graph-based relational user modeling (HGNNs) is underexplored in building environments
  - Agents in smart buildings either act with no autonomy (pure rule-based) or unconstrained autonomy — neither is acceptable for users
  - LLMs/SLMs are used for chatbots, not as context-aware mediators embedded in physical systems
  - P2P resource sharing between building agents without a central broker is an open problem

**Objectives:**
O1 — Characterize the landscape and gaps
Systematically identify and synthesize the state of the art in user modeling and user profiling, LLMs/SLMs on constrained devices, and context-aware adaptation in intelligent building environments, surfacing open research challenges.

O2 — Heterogeneous relational user modeling
Design and evaluate a heterogeneous GNN architecture for dynamic, context-aware inference of latent occupant preferences from noisy sensor data, incorporating differential privacy guarantees for edge-deployed settings.

O3 — Grounded LLM/SLM interaction for preference elicitation
Propose and assess a structured interaction model (grounded via MCP context schemas) enabling LLMs and SLMs to elicit, clarify, and negotiate occupant preferences in real-time — including conflict mediation in multi-occupant scenarios.

O4 — Bounded-autonomy agent model for intelligent communities
Define and validate a bounded-autonomy agent architecture capable of inferring latent needs, proactively discovering and deploying containerized services, and sharing resources via P2P mechanisms across a community of agents while preserving individual privacy.

O5 — Integrated framework validation
Design and evaluate the HAAIC framework holistically against human-centric KPIs in realistic scenarios (Digital Twin and real pilots), assessing the emergent system behavior when all components operate together.             

**Research Questions:**
RQ1. How can intelligent buildings dynamically model and adapt to the user’s individual and group preferences using graph-based heterogeneous representations? 

RQ2. In what ways can LLMs and SLMs be employed, not only to infer user intent and contextual relevance, but also to interact with occupants through dialog for clarification, negotiation, and preference definition? 

RQ3. How can an agent identify a user's latent needs and autonomously discover, negotiate for, and deploy and use containerized services to address them? 

RQ4. What mechanisms are required to enable peer-to-peer sharing of resources, such as computational availability and sensor data, between the autonomous agents of different users while preserving privacy and individual control?
