
The experimental work is a real-world, multi-node deployment of the **Caravels** distributed architecture, meant to validate the practical applicability, modularity, and scalability of the approach for intelligent buildings organized as an energy community. Caravels treats each building as an autonomous "caravel" (a System of Systems node) orchestrated with Kubernetes, where the community is the cluster and each building is a node.

The testbed is **seven Raspberry Pi 4B nodes (4 GB RAM)**, each running MicroK8s and representing one caravel, each with access to a subset of IoT devices (energy meters, light/PV sensors). Four containerized services were developed and deployed across nodes: **Energy Monitoring, Storage, Energy Forecasting (pre-trained SVM), and Display** (E-Ink). MQTT handles intra-building service data; a Kubernetes HTTP overlay handles inter-node communication.

The evaluation is a **three-part case study**:

1. **Service Modularity** — per-node service composition, historical energy aggregation over 24 h, and dynamic Display service that adapts to whichever services a node runs.
2. **User Preference Modeling** — a graph-based (tree-like) per-user preference structure with node types (User, Preference, Condition, Context, Value) and operations (planting, weeding, harvesting, trimming, grafting, flourishing). Value nodes adapt from logged interactions over one week; a **Q-learning RL agent** is embedded as an isolated value node (reward −1 on manual override, +1 otherwise; γ=0.9, α=0.1, ε-greedy, 1000 episodes). Multi-user conflict is resolved by trimming and grafting structures into a temporary merged structure using a dynamic weight-based strategy. Preference portability across caravels is demonstrated (User B visiting another household).
3. **Inter-Building Data Sharing** — peer-to-peer sharing over a **Headscale/WireGuard VPN** with zero-trust ACLs. Scenario A shares an IoT device (weather station) route; Scenario B shares a hosted weather-forecasting service to a resource-constrained caravel.

Reproducibility artifacts (MicroK8s manifests, Headscale config, ACL policies, deployment runbook) are published on Zenodo; full detail is in the associated MSc dissertation.

## 2. Findings

**System performance (multi-phase stress test, caravels 1–4):**
- CPU: cluster averaged 49.6 % under stress (1.9× baseline); peak node 69.5 % (highest container density, 9 vs 7–8 containers).
- Memory: stable, 1.23 → 1.26 GB (+2.1 %).
- MQTT: cluster peak throughput 9,345 msg/s; 40,000 messages (256-byte payload) across 4 brokers, peak 8,986 msg/s on best node, p95 latency < 0.02 ms, zero errors.
- Thermal: baseline 48.4 °C → avg 53.3 °C, peak 65.7 °C, within safety limits.
- HTTP API: 140,000 requests, throughput 239–265 req/s, p50 ≈ 35 ms.

**Inter-building sharing:**
- Shared forecasting service: mean response 71.12 ms, 100 % uptime, concurrent access by two caravels without disruption.
- IoT data-sharing latency test: avg 53.04 ms, jitter 8.86 ms; owner retained full control and revoked access cleanly.

**Preference modeling:**
- Individual adaptation (unitary averaging, range EWMA shift with smoothing 0.1, list with temporal decay) and multi-user conflict resolution both worked in a transparent, user-understandable way.
- Isolating the RL agent as a discrete value node prevented adaptive updates in one branch from degrading the broader model.
- Preference structures ported across caravels without user reconfiguration.

**Overall:** Caravels runs on resource-constrained SBCs with stable deployment/recovery, low latency, and data/computation sovereignty (VPN isolation, per-container blast-radius containment, no public internet exposure).

## 3. Alignment with the PhD Planning

| PhD WP theme | Covered by this experiment |
|---|---|
| **WP3** – data ingestion, frontend prototype, inter-agent communication | ✅ MQTT ingestion pipeline (Monitoring → Storage → aggregation), Display/Web frontend, HTTP overlay for node-to-node communication |
| **WP5** – service discovery, P2P resource sharing, bounded-autonomy agent | ✅ P2P inter-building service/data sharing over Headscale VPN; catalog-based service announcement; shared computation delegation |
| **WP6** – K8s deployment, integration testing, KPI validation, experimental scenarios | ✅ 7-node MicroK8s cluster, three-part integration case study, CPU/memory/thermal/throughput/latency KPIs |
| **WP4** – user preference modeling, conflict resolution | ⚠️ Partial: graph-based preference modeling and multi-user conflict resolution are demonstrated, but with a tree/Q-learning approach, not the planned heterogeneous GNN |

The experiment directly serves the PhD's core thesis: **decentralized, edge-based, human-centered intelligence for buildings/communities that preserves autonomy and privacy.** It provides a validated infrastructure baseline the later WPs build on.

## 4. What Is Missing (relative to the PhD planning)

**WP4 — user preference modeling (the largest gap):**
- No **heterogeneous GNN**. The current model is a hand-built tree of typed nodes with a Q-learning agent, not a learned graph neural network over a heterogeneous graph.
- No **Neo4j / Jena** graph-store backing (planned for the graph representation).
- No **LLM/SLM interaction** with the preference structure (planned for natural-language preference elicitation / conflict explanation).
- Conflict "fairness" weighting is acknowledged as statistically unsolved as concurrent users grow; grafting across heterogeneous structures with inconsistent branch ordering is unresolved.

**WP3:**
- Ingestion uses **MQTT, not Kafka**; no **digital twin** component yet.
- Inter-agent communication is service-level HTTP, not a formal agent-communication layer.

**WP5:**
- No **MCP (Model Context Protocol) JSON schema** and no formal **bounded-autonomy agent** — sharing is manual/policy-driven, discovery is basic API announcement.

**WP6 / evaluation:**
- Scale is small (7 nodes; stress test only 4). Horizontal scalability is argued from literature, not measured at community scale.
- Per-service independent benchmarking is flagged as needed (results depend heavily on the deployed service).
- No end-to-end KPI validation against the project's experimental scenarios.

**Cross-cutting:**
- Energy/optimization outcomes (savings, forecasting accuracy, demand-response) are not evaluated — the study is infrastructure- and mechanism-focused, not application-impact-focused.

## 5. Summary

The experimental work delivers a **validated infrastructure and mechanism baseline**: container orchestration, personalized preference modeling with conflict resolution, and secure inter-building P2P sharing, all running on edge SBC hardware with measured performance. It strongly supports WP3/WP5/WP6 groundwork and part of WP4. The main outstanding items are the **GNN-based preference model, LLM/SLM integration, MCP-based bounded-autonomy agents, Kafka/digital-twin ingestion, and community-scale evaluation** — these define the next phase of the PhD.
