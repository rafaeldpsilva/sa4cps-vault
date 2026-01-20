### Paper 1: Convergence of GNNs, LLMs, and Edge Computing in User-Centric Smart Environments: A Systematic Review
(WP1)

**General Problem:** The field of intelligent buildings is rapidly expanding, with isolated advancements in disparate domains such as User Modeling (GNNs), Natural Language Interaction (LLMs), and Distributed Infrastructure (Edge Computing).

**Specific Problem:** Despite these individual advances, there is a lack of comprehensive synthesis in the literature that articulates how these technologies can be integrated into a unified, privacy-preserving, and context-aware framework. Current reviews typically focus on one technology in isolation (e.g., only LLMs in IoT), failing to identify the interoperability challenges and architectural gaps required for a holistic solution.
   
**A Research Gap:** It is not known how the convergence of Graph Neural Networks and Large Language Models can be architected on edge-constrained devices to support real-time, human-centric adaptation.
   
**Importância:** Without this synthesis, researchers lack a clear roadmap for integration, leading to redundant efforts and fragmented solutions that fail to address the complexity of modern smart communities.

--- 

**Research Question:** How can Large Language Models and Knowledge Graphs be integrated to construct a dynamic Digital User Representation that evolves through continuous natural language interaction?

---
### Paper 2: _A Distributed Digital Twin Architecture for Edge-Based Intelligent Communities_
Arquitetura (WP 2 & WP 3)

**General Problem:** The dominant paradigm for intelligent building management relies heavily on centralized, cloud-native architectures. While powerful, these systems suffer from inherent latency issues, single points of failure, and significant privacy vulnerabilities when handling sensitive user data.
   
**Specific Problem:** Current decentralized or edge-based alternatives often lack the necessary structural coherence to support complex, real-time Digital Twin synchronisation. There is limited knowledge on how to design a scalable, microservice-oriented architecture that maintains data consistency and agent communication across low-power edge devices without relying on a central authority.
   
**A Research Gap:** Absent from the literature is a validated architectural framework that successfully combines the resilience of distributed edge computing with the synchronization requirements of a real-time Digital Twin for multi-user facilities.
   
**Importância:** Addressing this allows for the deployment of smart facility systems that are resilient to internet outages and inherently private, a critical requirement for critical infrastructure and user trust.

### Paper 3: _Context-Aware User Preference Elicitation using Heterogeneous Graph Neural Networks_
Core Model (WP 4)

**General Problem:** Traditional user preference modeling in smart environments relies on static rule-based systems or purely behavioral machine learning models. These approaches typically react to explicit commands or historical patterns, failing to capture the nuance of _why_ a preference exists relative to the current context.
   
**Specific Problem:** Existing methods struggle to model the complex relationships between users, sensors, and spatial contexts. Specifically, current research has not adequately explored how Heterogeneous Graph Neural Networks (HGNNs) can be utilized to infer latent (unstated) user needs from sparse and noisy sensor data in dynamic, multi-occupant environments.
   
**A Research Gap:** It is not known to what extent heterogeneous graph representations can improve the accuracy of latent preference inference compared to traditional sequence-based or rule-based models in variable building contexts.
   
**Importância:** Solving this enables systems that "understand" rather than just "obey," transitioning smart buildings from reactive automation to proactive, empathetic assistance.

### Paper 4: _Bridging the Gap: Integrating LLMs with Model Context Protocol (MCP) for Grounded Agentic Control_
Interaction (WP4 e WP5)

**General Problem:** Large Language Models (LLMs) and Small Language Models (SLMs) offer unprecedented natural language capabilities for human-computer interaction. However, in cyber-physical systems, these models prone to "hallucinations" and lack real-time awareness of the system's physical state.
   
**Specific Problem:** There is a disconnect between the linguistic capabilities of LLMs and the structured, deterministic requirements of building control systems. The literature lacks robust methodologies for "grounding" LLMs using structured context protocols (like MCP) to ensure that agent responses are not only conversationally fluid but also operationally safe, accurate, and conflict-aware.
   
**A Research Gap:** We do not know effective mechanisms for dynamically priming LLMs/SLMs with real-time graph-based context to enable agents that can negotiate and explain their decisions without hallucinating system capabilities.
   
**Importância:** This bridges the valley between "chatbots" and "control systems," enabling natural dialogue that can reliable manipulate physical reality.

### Paper 5: _Bounded Autonomy in Multi-Agent Systems: Conflict Resolution and Resource Sharing in Intelligent Communities_
Autonomy (WP 5 e WP 6)

**General Problem:** As intelligent buildings evolve into communities of autonomous agents, conflicts inevitably arise regarding shared resources (e.g., energy, space, computational power) and divergent user preferences.
   
**Specific Problem:** Current multi-agent negotiation frameworks are often too computationally heavy for edge deployment or too rigid to handle the nuances of human social friction. There is a lack of adaptive "Bounded Autonomy" frameworks that allow agents to autonomously resolve peer-to-peer resource conflicts while dynamically recognizing when to escalate decisions to human users.
  
**A Research Gap:** Absent from the literature is a validated control framework that balances autonomous peer-to-peer resource optimization with user-centric conflict mediation constraints in a distributed, resource-constrained environment.
  
**Importância:** This research is critical for scaling smart technologies from single homes to interconnected communities, preventing systemic deadlocks and ensuring fairness in resource distribution.