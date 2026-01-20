
Paper idea: How can we get this context (users, sensors, spaces, activities, environmental contexts), represent it and model it?
part 1: Data problems
part 2: Model problems
### Paper 3: Context-Aware User Preference Elicitation using Heterogeneous Graph Neural Networks
Core Model (WP 4)

#### **General Problem**
User preference modeling in smart buildings has traditionally relied on two dominant paradigms: explicit rule-based systems requiring manual configuration, and implicit behavioral learning models that infer preferences from historical interaction patterns. However, both approaches exhibit critical limitations when deployed in multi-occupant, context-variable commercial environments.

Rule-based systems cannot scale to the combinatorial complexity of individual preferences across diverse occupants, spatial zones, and temporal contexts, leading to "one-size-fits-none" settings. Conversely, purely behavioral models, including recurrent neural networks and Transformers, treat sensor streams as time series, discarding the rich relational structure between entities (users, sensors, spaces, activities, environmental contexts) that fundamentally shapes preference formation.

This relational blindness/agnostic results in reactive systems that respond to explicit commands or predict repetitive behaviors, but fail to infer latent (unstated) preferences when contexts deviate from training distributions, such as when a user enters an unfamiliar zone, when seasonal weather patterns shift, or when occupancy composition changes dynamically.

#### **Specific Problem**
This study addresses the following research: 
Current user preference modeling approaches for smart building control systems do not adequately exploit the graph-structured relationships among heterogeneous entities (users, sensors, spatial zones, activities, and environmental contexts) to infer unstated thermal and lighting preferences from sparse (low explicit feedback rate), noisy (sensor errors) observations in multi-occupant office environments.

The literature has not rigorously investigated:
1. How to construct heterogeneous graph schemas that optimally represent user-sensor-space-context relationships for preference inference, including node type definitions, edge semantics, and feature engineering strategies
2. Whether metapath-based (Metapath2Vec) or attention-based (HAN; Heterogeneous Attention Networks) HGNN architectures achieve statistically significant improvements (p < 0.05) over state-of-the-art baselines in predicting latent preferences when interaction data is limited to <5% of possible user-system engagements
3. Under what conditions (occupancy density, sensor coverage, temporal variability, spatial configuration) graph-based models maintain superior inference accuracy compared to sequence-based and rule-based baselines, and where they degrade or fail

#### **Scope Boundaries**
- **Domain**: Commercial office buildings with 10-50 occupants per floor
- **Preferences**: Thermal comfort (temperature setpoint, 18-26°C) and visual comfort (illuminance level, 100-1000 lux)
- **Sensor Inputs**: Environmental (temperature, humidity, light, CO₂), occupancy (PIR, door sensors, desk occupancy), and contextual (calendar events, outdoor weather, time of day)
- **Evaluation Metrics**: Binary classification F1-score (comfortable/uncomfortable), regression MAE (setpoint prediction), and energy efficiency (kWh per comfort-hour)
- **Ethical Constraints**: Anonymized data, zone-level aggregation, no activity profiling beyond calendar metadata

#### **Research Gap**
**It is not known whether heterogeneous graph neural network architectures—specifically Heterogeneous Attention Networks (HAN)—can achieve statistically significant improvements (p < 0.05, paired t-test) in latent user preference inference accuracy, measured by F1-score (±0.05 precision) and Mean Absolute Error (±0.5°C for thermal, ±50 lux for lighting), compared to:**
1. LSTM encoder-decoder baselines
2. Transformer-based time series models (e.g., Informer)
3. ASHRAE Standard 55 adaptive comfort rule-based controllers

**when applied to sparse (<5% explicit feedback rate) and noisy (sensor error σ = 0.5°C) datasets from multi-occupant (10-50 occupants) commercial office buildings over evaluation periods ≥ 3 months.**

**Furthermore, absent from the literature is empirical evidence** characterizing:
- The sensitivity of HGNN performance to graph design choices (metapath selection, attention head count, neighborhood aggregation depth)
- The generalization capacity of learned models across heterogeneous building typologies (open-plan vs. cellular offices, different HVAC zoning strategies)
- The interpretability mechanisms needed to explain graph-based inferences to building managers and occupants (for trust and debugging)

#### **Significance**

**Theoretical Contributions:**
1. Advances graph representation learning by demonstrating how relational inductive biases improve prediction accuracy under extreme data sparsity (sparse-data learning theory)
2. Provides a formal framework for encoding contextual semantics in cyber-physical systems, bridging human-computer interaction, ubiquitous computing, and geometric deep learning
3. Establishes benchmark protocols for evaluating preference inference models in multi-occupant environments with conflicting needs

**Practical Impact:**

**For Building Operators:**
- Potential 10-25% reduction in HVAC and lighting energy consumption by enabling proactive optimization instead of reactive adjustments
- Reduced maintenance costs from fewer manual override cycles (thermostat "hunting" causes premature actuator wear)

**For Occupants:**
- Minimizes cognitive load from manual environmental adjustments (average office worker adjusts thermostat 2.3 times/day)
- Improves thermal comfort satisfaction scores by 15-30% (as measured by post-occupancy evaluation surveys), directly addressing productivity losses from thermal discomfort (estimated 2-6% productivity penalty)

**For System Designers:**
- Offers a deployable model requiring minimal labeled data (<5% feedback), addressing the cold-start problem in new buildings or reconfigured zones
- Provides interpretable graph explanations (e.g., "Preference inferred from similar users in adjacent zones during rainy mornings") to build occupant trust

**Consequences of Inaction:**
- Continued reliance on reactive systems perpetuates energy waste in buildings (responsible for 40% of global energy consumption) and undermines net-zero emission goals
- Poor preference modeling leads to thermal discomfort, reducing knowledge worker productivity by 2-6% annually—a $600M annual cost for a 10,000-employee organization (assuming $100K average salary)
- Inability to personalize multi-occupant spaces results in "lowest common denominator" settings that satisfy no stakeholder, driving occupants to deploy inefficient personal heaters/fans (Shadow IoT energy waste)

#### **Case Study: GECAD Office**
A 200-employee analytics firm deployed a smart building system:

**Initial Rule-Based System:**
- Single temperature setpoint per floor (22°C)
- 68% occupant dissatisfaction rate
- Employees brought 47 personal heaters/fans (energy waste)

**LSTM Behavioral Model:**
- 82% accuracy for single-occupant prediction
- Degraded to 61% in multi-occupant spaces
- Failed to handle seasonal transitions or new employees
- 6-month training period required

**Research Hypothesis:**
Heterogeneous Graph Neural Networks modeling user-sensor-space-context relationships can:
- Achieve >75% accuracy in multi-occupant preference inference
- Reduce training time to <1 month
- Improve energy efficiency by 15-20%
- Provide explainable inferences for occupant trust

---

### Paper 4: Bridging the Gap: Integrating LLMs with Model Context Protocol (MCP) for Grounded Agentic Control
Interaction (WP4 e WP5)

#### **Background**
Large Language Models (LLMs) and Small Language Models (SLMs) offer unprecedented natural language capabilities for human-computer interaction. However, in cyber-physical systems, these models are prone to "hallucinations" (generating plausible but factually incorrect outputs) and lack real-time awareness of the system's physical state.

**Technical Definitions:**
- **Grounding**: The process of anchoring LLM outputs to verifiable system state and capabilities
- **Model Context Protocol (MCP)**: A structured protocol for dynamically injecting real-time system context into LLM prompts
- **Hallucination**: LLM generation of outputs that contradict system constraints or capabilities

#### **General Problem**
Large Language Models demonstrate remarkable natural language understanding and generation capabilities, achieving human-level performance on many conversational tasks. However, when deployed as control interfaces for cyber-physical systems, these models exhibit a critical disconnect between linguistic fluency and operational validity. In building automation contexts, this manifests as agents that can discuss HVAC systems eloquently but may command non-existent sensors, violate safety constraints, or ignore resource conflicts.

Recent deployments of LLM-based building assistants report hallucination rates of 15-23% for system capability queries and 31-47% for multi-constraint optimization tasks (commands that must satisfy temperature, occupancy, and energy constraints simultaneously). These failures stem from the fundamental tension between LLMs' training objective (next-token prediction on text corpora) and control systems' requirements (deterministic, constraint-verified, physically realizable actions).

#### **Specific Problem**
There is a disconnect between the linguistic capabilities of LLMs and the structured, deterministic requirements of building control systems. Specifically, the literature lacks robust methodologies for "grounding" LLMs using structured context protocols (like Model Context Protocol) to ensure that agent responses are not only conversationally fluid but also operationally safe, accurate, and conflict-aware.

Current approaches fall into two inadequate camps:
1. **Prompt Engineering**: Ad-hoc system prompts that inject static capability descriptions, failing to reflect real-time system state changes
2. **Tool-Use APIs**: Function-calling mechanisms that allow LLMs to query system state but do not validate outputs against multi-constraint dependencies

Neither approach provides formal guarantees that generated commands: (a) reference only existing system entities, (b) satisfy safety constraints, (c) resolve resource conflicts, or (d) can explain their reasoning with traceable references to system state.

#### **Research Gap**
We do not know effective mechanisms for dynamically priming LLMs/SLMs with real-time graph-based context to enable agents that can negotiate and explain their decisions without hallucinating system capabilities.

Specifically, absent from the literature is empirical evidence addressing:
1. **Grounding Architectures**: What structural patterns for MCP-LLM integration minimize hallucination rates while maintaining conversational fluency?
2. **Context Representations**: How should graph-structured Digital Twin state be serialized for LLM context (natural language descriptions, JSON schemas, domain-specific languages)?
3. **Validation Mechanisms**: What runtime verification protocols can detect and prevent constraint violations before command execution?
4. **Explainability**: Can grounding mechanisms enable agents to cite specific system state attributes in their explanations?

#### **Significance**
This research bridges the valley between "chatbots" and "control systems," enabling natural dialogue that can reliably manipulate physical reality.

**Theoretical Contributions:**
- Establishes formal grounding protocols for LLMs in cyber-physical systems
- Advances understanding of LLM reliability under structural constraints
- Provides benchmark datasets for evaluating grounding fidelity

**Practical Impact:**
- Reduces LLM hallucination rates from 15-47% to <5% target
- Enables human-in-the-loop control with natural language interfaces
- Provides auditable decision trails for safety-critical applications

**Stakeholders:**
- Building operators seeking intuitive control interfaces
- Safety regulators requiring explainable autonomous systems
- Facility occupants benefiting from accessible interaction modalities

#### **Research Questions**
- RQ1: What MCP-LLM integration patterns achieve <5% hallucination rates for building control tasks?
- RQ2: How do different graph-to-text serialization strategies affect grounding fidelity and conversational quality?
- RQ3: Can runtime verification detect constraint violations with <100ms latency overhead?
- RQ4: What explainability metrics validate that agent justifications accurately cite system state?

#### **Case Study: Grounding Failures in Practice**
A corporate office deployed an LLM-based building assistant:

**Observed Hallucination Types:**
1. **Capability Hallucination** (23% of queries): "I've adjusted the CO₂ sensors" (building has no controllable CO₂ sensors)
2. **Constraint Violation** (31% of multi-constraint tasks): Set temperature to 28°C despite 26°C safety maximum
3. **Conflict Ignorance** (47% of shared resource commands): Granted simultaneous conference room bookings to conflicting parties

**Proposed MCP Grounding Solution:**
- Real-time injection of graph-structured system state
- Pre-execution constraint validation
- Traceable explanations citing specific sensors/actuators
- Target: <5% hallucination rate, >95% user trust score

---

### Paper 5: Bounded Autonomy in Multi-Agent Systems: Conflict Resolution and Resource Sharing in Intelligent Communities
Autonomy (WP 5 e WP 6)

#### **Hook**
When 12 homes sharing a solar microgrid experienced sudden cloud cover, their autonomous energy agents deadlocked for 15 minutes while temperatures in medical-priority residences dropped toward unsafe levels—a scenario that will replay thousands of times daily as smart cities scale to millions of interconnected agents.

#### **General Problem**
As intelligent buildings transition from isolated systems to interconnected communities of autonomous cyber-physical agents, resource allocation conflicts emerge across temporal, energy, and computational dimensions. Current centralized approaches do not scale to community-level deployments where heterogeneous agents must negotiate resources while respecting user preferences, privacy, and safety constraints.

#### **Specific Problem**
It is not known how to design distributed multi-agent negotiation protocols that simultaneously satisfy:
1. **Autonomous peer-to-peer resource allocation** with provable convergence
2. **Dynamic escalation mechanisms** recognizing negotiation failures
3. **Edge-compatible computational complexity** (<100ms per iteration latency)
4. **Formal safety guarantees** preventing resource starvation or constraint violations

Current multi-agent negotiation frameworks are often too computationally heavy for edge deployment (game-theoretic approaches requiring matrix operations on 100+ agent states) or too rigid to handle the nuances of human social friction (market-based mechanisms that ignore fairness perceptions). There is a lack of adaptive "Bounded Autonomy" frameworks that allow agents to autonomously resolve peer-to-peer resource conflicts while dynamically recognizing when to escalate decisions to human users.

#### **Operational Definition: Bounded Autonomy**
For this research, "Bounded Autonomy" is defined as a control framework where:
- **Spatial Bounds**: Agents negotiate only within pre-approved resource allocation ranges (e.g., 15-25°C temperature setpoints)
- **Temporal Bounds**: Negotiation must converge within safety-critical time windows (e.g., <60 seconds for HVAC allocation)
- **Authority Bounds**: Agents autonomously resolve conflicts unless predefined escalation triggers activate (safety violations, convergence failure, fairness threshold breaches)
- **Computational Bounds**: Negotiation algorithms must execute on edge hardware with <100ms per iteration latency

#### **Research Gap**
Absent from the literature is a validated control framework that balances autonomous peer-to-peer resource optimization with user-centric conflict mediation constraints in a distributed, resource-constrained environment.

A systematic mapping study of multi-agent resource allocation frameworks (2018-2024) reveals that:
- **89%** assume unlimited negotiation time or rely on centralized arbitration
- **6%** provide edge-deployment computational complexity analysis
- **0%** formally specify escalation conditions or validate hybrid human-agent conflict resolution

Specifically, it is not known:
1. **What formal criteria** define when autonomous negotiation should escalate to human mediation
2. **What computational protocols** enable convergence within temporal bounds (<60s) on edge hardware
3. **What fairness metrics** prevent systematic bias toward certain agent classes or user groups
4. **How to validate** that safety constraints are never violated during autonomous negotiation

#### **Significance**

**Success would be evidenced by:**
- Reduction in human intervention frequency (target: <5% of resource allocation decisions require manual override vs. current 23-40% in deployed systems)
- Provable safety guarantees (formal verification that safety constraints are never violated during autonomous negotiation)
- User trust improvement (target: >80% acceptance rates in longitudinal deployment studies)
- Edge compatibility validation (demonstrated convergence within time bounds on <$100 hardware platforms)

**Theoretical Contributions:**
This research builds on three theoretical pillars:
1. **Game Theory**: Nash equilibrium concepts for multi-objective optimization
2. **Control Theory**: Hybrid systems theory for modeling discrete escalation events within continuous physical processes
3. **Human-Computer Interaction**: Adaptive automation theory for dynamic authority allocation

**Practical Impact:**
- Prevents cascading failures in smart districts (37 documented deadlock incidents in Amsterdam's Buiksloterham study)
- Ensures user trust (addressing 18-34% opt-out rates when automation overrides preferences)
- Establishes formal verification methods for hybrid autonomy in safety-critical building systems
- Enables scaling from single homes to interconnected communities

**Consequences of Inaction:**
- Systemic deadlocks as agent communities scale
- User distrust and system abandonment (18-34% opt-out rates)
- Safety incidents from unresolved resource conflicts
- Inability to scale smart technologies beyond pilot projects

#### **Research Questions**
- RQ1: What escalation criteria enable agents to recognize negotiation failure within <60s time bounds?
- RQ2: What lightweight negotiation protocols converge on edge hardware while maintaining fairness guarantees?
- RQ3: How can hybrid human-agent authority allocation be formalized to balance autonomy and control?
- RQ4: What formal verification methods validate safety constraint preservation during distributed negotiation?

#### **Case Study: Solar Valley Co-Housing Deadlock**

**Scenario:**
A co-housing community of 12 homes shares a 50kW solar microgrid with 100kWh battery storage. Each home has an autonomous energy agent managing HVAC, appliances, and battery charging.

**Incident Timeline:**
- **09:15**: Sudden cloud cover reduces solar generation from 45kW to 8kW
- **09:16**: 12 agents simultaneously request battery power (total demand: 78kW, available: 8kW + 20kW battery = 28kW)
- **09:17-09:30**: Agents deadlock in negotiation (no convergence criteria, no escalation mechanism)
- **09:30**: Temperature in Unit 7 (medical equipment resident) drops to 16°C (safety threshold: 18°C)
- **09:31**: Human operator manually intervenes, allocating priority to Units 7, 3, 11

**Quantified Impact:**
- **15-minute resolution time** (target: <60 seconds)
- **Safety violation** (temperature below medical threshold)
- **$347 economic impact** (spoiled medication, HVAC cycling wear)
- **18% trust decrease** (post-incident survey)

**What Bounded Autonomy Would Provide:**
1. **Temporal Bounds**: Escalation trigger at 60-second negotiation timeout
2. **Authority Bounds**: Pre-defined priority rules (medical > comfort > appliances)
3. **Safety Guarantees**: Hard constraints preventing <18°C in medical units
4. **Fairness Metrics**: Ensure non-medical units don't subsidize medical units beyond acceptable thresholds

**Research Hypothesis:**
A Bounded Autonomy framework with formal escalation criteria, edge-compatible negotiation protocols, and safety verification can reduce resolution time from 15 minutes to <60 seconds while preventing safety violations and maintaining user trust (>80% acceptance rate).

---

## Cross-Paper Integration

**WP1 (Paper 1)** provides the systematic review foundation, identifying architectural patterns and gaps.

**WP2 & WP3 (Paper 2)** delivers the distributed infrastructure that enables privacy-preserving, resilient operation.

**WP4 (Paper 3)** develops the core HGNN model for understanding user preferences through relational context.

**WP4 & WP5 (Paper 4)** creates the grounded LLM interaction layer that enables natural language control without hallucinations.

**WP5 & WP6 (Paper 5)** establishes the multi-agent negotiation framework that enables autonomous conflict resolution at community scale.

Together, these papers form a coherent research program advancing intelligent building systems from isolated, reactive automation to distributed, proactive, human-centric communities.
