You are an expert in human-computer interaction, distributed AI systems,and intelligent buildings research. You will help define the KPIs (Key Performance Indicators) and evaluation metrics for a PhD research project.                                        

## Research Context

**Title:** Human-centric Agent-based Adaptive Intelligent Communities (HAAIC)

**Abstract:** A novel distributed, adaptive intelligence framework for
intelligent buildings that models, mediates, and responds to human preferences
and contextual dynamics in real time. The system uses autonomous agents,
heterogeneous Graph Neural Networks (HGNNs), and LLMs/SLMs to provide
personalized, context-aware building control with differential privacy
guarantees.

## Research Questions
- **RQ0:** How can agents effectively manage an intelligent community?
- **RQ1:** How can intelligent buildings dynamically model and adapt to user
  preferences using heterogeneous graph representations?
- **RQ2:** How can LLMs/SLMs be used to infer user intent and interact through
  dialogue for clarification, negotiation, and preference definition?
- **RQ3:** How can an agent identify latent user needs and autonomously
  discover, deploy, and use containerized services to address them?
- **RQ4:** What mechanisms enable peer-to-peer resource sharing between agents
  while preserving privacy?

## System Architecture (5 subsystems)
1. **Data Ingestion & Digital Twin** — Kafka pipeline, real-time building
   state synchronization
2. **User Preference & Context Model** — HGNN trained with DP-SGD,
   incremental updates, confidence scores
3. **LLM/SLM Interaction Layer** — MCP JSON schema, dialogue interface,
   proactive preference elicitation
4. **Agent Control & Bounded Autonomy Engine** — Decision loop, configurable
   autonomy envelope, inter-agent coordination
5. **Monitoring & Frontend** — Real-time dashboard, REST API

## Key Technical Requirements (for grounding KPIs)
**Performance baselines defined in NFRs:**
- Data ingestion latency: < 500 ms end-to-end
- Agent decision cycle (sense → infer → act): < 2 seconds
- SLM response time (local): < 5 seconds
- HGNN inference: < 1 second per user query
- System scale: ≥ 50 concurrent building agents
- Kafka throughput: ≥ 10,000 events/second
- Graph scale: ≥ 500 users, 10,000 sensor nodes, 1,000,000 edges
- Digital Twin recovery after failure: < 30 seconds
- Edge hardware target: ≥ 4 GB RAM, ≥ 4-core ARM/x86
**Privacy requirements:**
- Differential privacy budget tracking per user (ε, δ)
- Local Differential Privacy (LDP) at sensor/edge level
- Budget composition via Rényi DP / zCDP
- Data minimization in P2P exchanges
- GDPR compliance
**Autonomy requirements:**
- Configurable bounded autonomy envelope per agent
- Escalation to user when decisions exceed the envelope
- Audit logs for all agent decisions

## Your Task
Define a comprehensive, structured set of **KPIs and evaluation metrics** for
this research project. Organize them into the following dimensions:

### 1. Model Quality (WP4 – Preference Modeling)
Metrics assessing the accuracy, adaptability, and robustness of the HGNN
preference model. Consider:
- Preference prediction accuracy (implicit vs. explicit feedback)
- Adaptation speed to preference drift
- Performance in multi-occupant conflict scenarios
- Confidence calibration of preference scores
- Comparison against baselines (rule-based, standard GNN, collaborative
  filtering)

### 2. Interaction Quality (WP4/WP5 – LLM/SLM Layer)
Metrics assessing the quality of the natural language dialogue interface.
Consider:
- Task completion rate (did the user successfully express/update preferences?)
- Dialogue efficiency (turns needed to reach consensus)
- Hallucination rate (responses grounded in real system context)
- User satisfaction (qualitative/survey)
- Proactive escalation precision (did the system correctly decide when to
  involve the user?)

### 3. Agent Performance & Autonomy (WP5 – Agent Control)
Metrics assessing agent decision quality and autonomy behavior. Consider:
- Decision latency (full sense→infer→act cycle)
- Autonomy boundary adherence rate
- False escalation rate (unnecessary user confirmations)
- Missed escalation rate (decisions that should have been escalated)
- Multi-agent coordination efficiency (resource negotiation success rate)
- Service discovery and deployment success rate

### 4. Infrastructure Performance (WP3 – Digital Twin & Pipeline)
Metrics assessing the technical infrastructure. Consider:
- Data ingestion latency and throughput
- Digital Twin synchronization accuracy and recovery time
- System availability (uptime)
- Edge resource utilization (CPU, RAM on constrained devices)

### 5. Privacy & Security (NFR3)
Metrics assessing privacy preservation effectiveness. Consider:
- ε-DP compliance rate (budget exhaustion events vs. total queries)
- Empirical privacy leakage (membership inference attack success rate)
- LDP perturbation overhead vs. utility trade-off
- Data minimization compliance in P2P exchanges

### 6. Scalability & Resilience (NFR2/NFR4)
Metrics assessing system behavior under load and failure. Consider:
- Performance degradation with increasing number of agents
- Fault recovery time per component
- P2P resource sharing availability in offline scenarios

### 7. User-Centric Outcomes (Cross-cutting)
High-level, human-relevant metrics that validate the system's real-world
impact. Consider:
- User comfort satisfaction score
- Preference conflict resolution success rate (autonomous vs. escalated)
- System adoption and interaction frequency
- Perceived system explainability (NFR7)
- Energy/resource efficiency improvement over baseline

## Output Format Requirements
For **each KPI**, provide:
| Field | Content |
|-------|---------|
| **ID** | Unique identifier (e.g., M-WP4-01) |
| **Name** | Short descriptive name |
| **Definition** | Precise mathematical or operational definition |
| **Unit** | Measurement unit (%, ms, score 1–5, etc.) |
| **Target / Threshold** | Acceptable value or range |
| **Measurement Method** | How to measure it (automated logs, user survey, simulation, etc.) |
| **RQ Addressed** | Which research question(s) it validates |
| **Measurement Phase** | WP/phase when this metric is measured (e.g., WP4, WP6) |
| **Baseline** | What comparison baseline is used |
Additionally:
1. Flag any KPI where measurement is non-trivial and suggest how to address
   it.
2. Highlight which KPIs are **primary** (directly answer a research question)
   vs. **secondary** (supporting/diagnostic).
3. Suggest 3–5 aggregate composite scores that can summarize system
   performance across multiple dimensions for the final evaluation report.
4. Identify any KPIs that require a **real pilot** vs. those measurable
   purely in the Digital Twin simulation.
