- [ ] Implement edge learning on nodes for energy prediction

- [ ] Integrate personal models per household or group with privacy constraints

- [x] Connect models with IoT data streams in real-time

- [ ] Flexibility forecast

- [ ] Implement desk monitors

- [ ] Design safeguards against unauthorized or malicious actuation

- [ ] Integrate user involvement with XAI to make daily summaries

- [ ] Flexibility activation

- [ ] Develop enhanced interfaces for energy communities, including import/export views

- [x] Virtual energy community

# Demo 2 Sprint Planning

**Project:** Sa4CPS (ITEA 22007)
**Demo target:** 8 weeks (4 × 2-week sprints)
**Last updated:** 2026-03-10

---

## Feature → WBS Mapping

| # | Demo 2 Feature | WBS Components |
|---|---|---|
| 1 | Edge learning for energy prediction | C8.2, C8.4, C4.4 |
| 2 | Personal models w/ privacy constraints | C8.1, C8.3, C11.1, B10.4 |
| 3 | Connect models to IoT streams | C2.1, C2.2, B7.1, C4.1 |
| 4 | Flexibility forecast | C4.2, C4.3, C5.2 |
| 5 | Desk monitors | B5.1, B7.4, B5.3 |
| 6 | Safeguards against malicious actuation | C10.1–C10.4, B10.3 |
| 7 | XAI daily summaries | C7.1–C7.3, C3.3, B5.3 |
| 8 | Flexibility activation | C5.1, C5.3, C5.4 |
| 9 | Community interfaces (import/export) | C6.3, C6.4, C7.2, B5.1 |
| 10 | Virtual energy community | C6.1, C6.2, C9.1, C9.3, C9.4 |

---

## Sprint 1 — Foundation & Infrastructure (Weeks 1–2)

**Theme:** Real-time data pipeline, desk UI, security baseline

### Feature 3 – IoT Stream Integration
- [ ] C2.1 Connect energy meters and IoT devices to ingestion layer
- [ ] C2.2 Configure Node-RED + Kafka/Redis data pipeline
- [ ] B7.1 Validate real-time streaming latency and throughput
- [ ] C4.1 Data preprocessing pipeline for forecasting models

### Feature 5 – Desk Monitors
- [ ] B5.1 Create desk-level energy monitor UI component (Vue.js)
- [ ] B7.4 Expose desk-level metrics via REST API
- [ ] B5.3 Add personalized energy usage notifications per desk

---

## Sprint 2 — Edge Intelligence & Privacy (Weeks 3–4)

**Theme:** Federated learning on edge, personal preference models

### Feature 1 – Edge Learning
- [ ] C8.2 Prune/quantize energy prediction model for edge constraints
- [ ] C8.4 Deploy model to edge nodes (Raspberry Pi / caravel)
- [ ] C4.4 Enable distributed inference at edge nodes
- [ ] Test prediction accuracy: edge vs. centralized baseline

### Feature 2 – Personal Models with Privacy
- [ ] C8.1 Select and configure FL framework (Flower or TFF)
- [ ] C8.3 Implement FL communication & synchronization protocol
- [ ] C11.1 Define per-household preference graph schema (Neo4j/Jena)
- [ ] B10.4 Apply differential privacy to FL aggregation
- [ ] Validate FL round with ≥2 simulated households

### Feature 6 – Safeguards (hardening)
- [ ] C10.3 Apply RBAC for actuation commands in K8s
- [ ] C10.4 Deploy anomaly detection for suspicious actuation patterns
- [ ] B10.3 Fine-grained role authorization by zone

---

## Sprint 3 — Forecasting, Flexibility & XAI Core (Weeks 5–6)

**Theme:** Forecasting pipeline, DR activation, XAI backbone

### Feature 4 – Flexibility Forecast
- [ ] C4.2 Train Temporal Fusion Transformer (energy usage/availability)
- [ ] C4.3 Add probabilistic confidence output to forecasts
- [ ] C5.2 RL-based flexibility estimation per user/device

### Feature 8 – Flexibility Activation
- [ ] C5.1 Integrate OpenADR protocol with grid operator API
- [ ] C5.3 Implement local DR auction/bidding mechanism
- [ ] C5.4 Design incentive and fairness policy for flexibility rewards

### Feature 7 – XAI (backbone)
- [ ] C7.1 Integrate SHAP/LIME for prediction model explanations
- [ ] C7.3 Connect XAI to control and forecasting modules

---

## Sprint 4 — UX, Community & Demo Polish (Weeks 7–8)

**Theme:** Community interfaces, virtual community, XAI summaries

### Feature 7 – XAI Daily Summaries
- [ ] C7.2 Build XAI visualization dashboard (Grafana or Vue.js)
- [ ] C3.3 Surface daily summaries in frontend chat/notification UI
- [ ] B5.3 Push automated daily summary notifications to users

### Feature 9 – Community Interfaces
- [ ] C6.3 Build trading ledger with import/export views
- [ ] C6.4 Link trading interface to forecasting data
- [ ] B5.1 Web dashboard enhancements for community import/export

### Feature 10 – Virtual Energy Community
- [ ] C6.1 Define P2P trade protocol (offer / demand / matching rules)
- [ ] C6.2 Implement reputation and credit system
- [ ] C9.1 Build scenario generator for community behavior simulation
- [ ] C9.3 Connect simulation engine with community agents
- [ ] C9.4 Visualization and KPI report generator for virtual community
