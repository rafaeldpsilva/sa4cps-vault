
The experimental work is a real-world, multi-node deployment of the **Caravels**, a distributed architecture, meant to validate the practical applicability, modularity, and scalability of the approach for intelligent buildings organized as an energy community. Caravels treats each building as an autonomous "caravel" (a System of Systems node) orchestrated with Kubernetes, where the community is the cluster and each building is a node.
![[Pasted image 20260706142816.png]]

The testbed is seven Raspberry Pi 4B nodes (4 GB RAM), each running MicroK8s and representing one caravel, each with access to a subset of IoT devices (energy meters, light/PV sensors). Four containerized services were developed and deployed across nodes: Energy Monitoring, Storage, Energy Forecasting (pre-trained SVM), and Display (E-Ink). MQTT handles intra-building service data, and a Kubernetes HTTP overlay handles inter-node communication.

The evaluation is a three-part case study:
1. Service Modularity — per-node service composition, historical energy aggregation over 24 h, and dynamic Display service that adapts to whichever services a node runs.
2. User Preference Modeling — a graph-based (tree-like) per-user preference structure with node types (User, Preference, Condition, Context, Value) and operations (planting, weeding, harvesting, trimming, grafting, flourishing). Value nodes adapt from logged interactions over one week, a Q-learning RL agent is embedded as an isolated value node. Multi-user conflict is resolved by trimming and grafting structures into a temporary merged structure using a dynamic weight-based strategy. Preference portability across caravels is demonstrated (User B visiting another household).
3. Inter-Building Data Sharing — peer-to-peer sharing over a Headscale VPN with zero-trust ACLs. Scenario A shares an IoT device (weather station) route between caravels and Scenario B shares a hosted weather-forecasting service to a resource-constrained caravel.
## Findings
System performance (multi-phase stress test, caravels 1–4):
- CPU: cluster averaged 49.6 % under stress (1.9× baseline); peak node 69.5 % (highest container density, 9 vs 7–8 containers).
- Memory: stable, 1.23 → 1.26 GB (+2.1 %).
- MQTT: cluster peak throughput 9,345 msg/s; 40,000 messages (256-byte payload) across 4 brokers, peak 8,986 msg/s on best node, p95 latency < 0.02 ms, zero errors.
- Thermal: baseline 48.4 °C → avg 53.3 °C, peak 65.7 °C, within safety limits.
- HTTP API: 140,000 requests, throughput 239–265 req/s, p50 ≈ 35 ms.

Inter-building sharing:
- Shared forecasting service: mean response 71.12 ms, 100 % uptime, concurrent access by two caravels without disruption.
- IoT data-sharing latency test: avg 53.04 ms, jitter 8.86 ms; owner retained full control and revoked access cleanly.

Preference modeling:
- Individual adaptation and multi-user conflict resolution both worked in a transparent, user-understandable way.
- Isolating the RL agent as a discrete value node prevented adaptive updates in one branch from degrading the broader model.
- Preference structures ported across caravels without user reconfiguration.

Caravels runs on resource-constrained SBCs with stable deployment/recovery, low latency, and data/computation sovereignty (VPN isolation, per-container blast-radius containment, no public internet exposure).

## Alignment with the PhD Planning

| PhD WP                                                                                | Covered by this experiment                                                                                                                                           |
| ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **WP3** – data ingestion, frontend prototype, inter-agent communication               | MQTT ingestion pipeline (Monitoring → Storage → aggregation), Display/Web frontend, HTTP overlay for node-to-node communication                                      |
| **WP5** – service discovery, P2P resource sharing, bounded-autonomy agent             | P2P inter-building service/data sharing over Headscale VPN; catalog-based service announcement; shared computation delegation                                        |
| **WP6** – K8s deployment, integration testing, KPI validation, experimental scenarios | 7-node MicroK8s cluster, three-part integration case study, CPU/memory/thermal/throughput/latency KPIs                                                               |
| **WP4** – user preference modeling, conflict resolution                               | Partial: graph-based preference modeling and multi-user conflict resolution are demonstrated, but with a tree/Q-learning approach, not the planned heterogeneous GNN |

The experiment directly serves the PhD's core thesis: decentralized, edge-based, human-centered intelligence for buildings/communities that preserves autonomy and privacy. It provides a validated infrastructure baseline the later WPs build on.

## What Is Missing

The experimental work shows an infrastructure and mechanism baseline: container orchestration, personalized preference modeling with conflict resolution, and secure inter-building P2P sharing, all running on edge SBC hardware with measured performance. It supports WP3, WP5, WP6 groundwork and part of preliminary concept of WP4. The main missing items are the GNN-based preference model, LLM/SLM integration, MCP-based bounded-autonomy agents, digital-twin ingestion, and community-scale evaluation.
