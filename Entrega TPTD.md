**Problem Statement:**
The field of artificial intelligence is rapidly transforming various sectors, and its application in intelligent buildings presents a significant opportunity to enhance human-centric adaptation [1], [2]. The core challenge is to create systems that are adaptive to human needs, interactive in a natural way, and ensuring privacy and responsiveness [3].

In user modeling, general solutions focus more on behavioral modeling, using approaches such as deterministic, stochastic, or agent-based [4]. However, for preference modeling, more traditional solutions rely on rule-based methods [5] that while providing many advantages such as explainability, do not capture nuanced variations in human preferences or handle the complexity in multi-occupant scenarios [6]. The emergence of graph-based representations [7], [8], [9], particularly knowledge graphs has provided a more robust method for modeling the connections between users, devices, spaces, and context, when compared with machine learning solutions which typically capture behavioral patterns from sensor data [10].

From an architectural standpoint, the dominant paradigm has been centralized, cloud-based systems [11]. While powerful, this approach introduces problems in latency, reliability, privacy, and security [12], [13]. In response, a shift towards distributed and edge computing has gained momentum [14], [15], [16], aiming to process data closer to its source and, also, agent systems have been explored for decentralized control [17], [18].

Interaction between human and buildings has evolved from simple dashboards to voice-activated commands. While an improvement, these forms of interaction often lack context-awareness, and are largely transactional and reactive [19]. The integration of large language models (LLM) [20], [21], [22] and small language models (SLM) [23], [24] present an opportunity to create fluid interaction and, also, enable proactive assistance. The primary gap is to integrate these language models with real-time and structured system context so they can leverage proactive preference elicitation, personalized system behavior, and handle conflict mediation [25], [26].

In conclusion, while the literature presents advances in user preference modeling, distributed systems, and language models, there is a gap in research that combines these concepts into a unified framework. The work will evolve from the model proposed by the candidate in [27], [28]. This project directly addresses this multi-faceted gap, aiming to deliver a holistic solution that is more adaptive, interactive, and resilient than the current state of the art.

**Objectives:**
O1 — Characterize the landscape and gaps
Systematically identify and synthesize the state of the art in user modeling and user profiling, LLMs/SLMs on constrained devices, and context-aware adaptation in intelligent building environments, surfacing open research challenges.

O2 — Heterogeneous relational user modeling
Design and evaluate a heterogeneous GNN architecture for dynamic, context-aware inference of latent occupant preferences from noisy sensor data.

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
