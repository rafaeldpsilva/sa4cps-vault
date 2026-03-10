# WP6-A — KPI Monitoring Agent

## Identity
| Field | Value |
|---|---|
| **ID** | WP6-A |
| **Name** | KPI Monitoring Agent |
| **WP** | WP6 |
| **RQ Addressed** | RQ0, RQ1, RQ2, RQ3, RQ4 (validates all) |
| **Type** | Continuous |
| **Status** | Planned |

---

## Purpose
Continuously computes all 29 KPIs defined in T2.2 from live system logs and event streams. Updates the 5 composite scores (SIS, AQI, PUBS, IRI, HCVS) in real time. Triggers alerts when metrics breach thresholds. Feeds the Grafana dashboard and generates the evaluation data for WP6 reports and thesis Papers 3–5.

---

## Inputs
| Source | Description |
|---|---|
| WP5-A audit log | Every decision: action, justification, latency, boundary check result |
| WP4-A model metrics | HR@5, confidence scores, drift flags, model update events |
| WP4-D dialogue session logs | Task completion, turns count, hallucination flags, satisfaction survey responses |
| WP5-C negotiation logs | Session outcomes, deadlock events, round counts |
| WP5-D deployment logs | Deployment attempts, success/failure, health-check results |
| WP3-B DT metrics | Sync accuracy, recovery events, uptime |
| WP3-A ingestion metrics | Latency histograms, throughput counters, Kafka lag |
| WP2-B DP budget ledger | Per-user budget expenditure and compliance status |
| User survey responses | Comfort, satisfaction, explainability ratings |

---

## Outputs
| Artifact | Description |
|---|---|
| Live KPI dashboard | Grafana dashboard with all 29 KPIs and 5 composite scores, updated in real time |
| Threshold alerts | Prometheus alertmanager notifications when KPI breaches target |
| Evaluation report | Periodic (weekly + final) structured KPI report for WP6 deliverable |
| Composite scores | SIS, AQI, PUBS, IRI, HCVS updated at configurable intervals |
| Anomaly flags | When multiple KPIs degrade simultaneously (potential systemic issue) |

---

## Core Behaviour

### KPI Computation per Category

**Model Quality (WP4):**
- HR@5: computed from feedback event stream (accepted vs. predicted top-5)
- NDCG@5: from explicit survey ratings
- Drift adaptation speed: from model update event timestamps + HR@5 recovery trace
- ECE: from confidence score histogram vs. binary outcome labels
- HGNN vs. baseline: from parallel model evaluation logs

**Interaction Quality (WP5/WP4):**
- TCR: `preference_committed / total_sessions` from session logs
- Turns-to-consensus: mean turns per completed session
- Hallucination rate: from automated state-oracle cross-reference log
- User satisfaction: from in-app Likert survey responses
- Escalation precision: from user "was this necessary?" feedback

**Agent Performance (WP5):**
- Decision latency: P95 from WP5-A audit log timestamps
- Boundary adherence: 1 - (out-of-envelope / total) from audit log
- FER / MER: from escalation feedback log
- Negotiation success: from WP5-C session outcome log
- Deployment success: from WP5-D lifecycle log

**Infrastructure (WP3):**
- Ingestion latency P95: from WP3-A Prometheus histogram
- Kafka throughput: from Kafka JMX / exporter metrics
- DT sync accuracy: from WP3-B divergence check log
- DT recovery time: from WP3-B recovery event log

**Privacy (WP2):**
- DP budget compliance: from WP2-B ledger
- MIA success rate: from scheduled adversarial evaluation runs
- LDP accuracy loss: from ablation comparison log
- P2P data minimization: from WP5-C message payload audit

**Scalability (WP6):**
- Latency degradation: from load test results at N=1,5,10,25,50 agents
- MTTR per component: from WP6-B chaos test logs
- Offline P2P availability: from WP5-C offline mode test results
- System availability: from uptime monitor

**User-Centric (WP6):**
- Comfort score: from daily micro-survey aggregation
- Conflict resolution acceptance: from post-resolution user rating
- Interaction frequency: from session log, user-initiated filter
- Explainability score: from sampled post-decision survey
- Energy efficiency: from building meter data + occupancy normalisation

### Composite Score Computation
```python
SIS  = 0.35*norm(HR5) + 0.25*norm(TCR) + 0.20*norm(CRacc) + 0.20*(1-norm(HalRate))
AQI  = 0.30*norm(ABA) + 0.30*(1-norm(MER)) + 0.20*(1-norm(FER)) + 0.20*norm(EscPrec)
PUBS = 0.40*norm(BCR) + 0.35*norm(HR5_DP) + 0.25*(1-norm((MIA-0.5)/0.5))
IRI  = 0.25*norm(IngestLat) + 0.25*norm(LatDeg) + 0.25*norm(Avail) + 0.25*norm(MTTR)
HCVS = 0.35*norm(Comfort) + 0.25*norm(Explain) + 0.20*norm(CRS) + 0.20*norm(Energy)
```

---

## Technologies
- Prometheus (metrics scraping from all agents)
- Grafana (live dashboard)
- InfluxDB / TimescaleDB (KPI time series storage)
- Kafka consumer (event log processing)
- Python (KPI computation workers)
- Alertmanager (threshold breach notifications)

---

## Interfaces
| Agent / System | Direction | Description |
|---|---|---|
| All agents (WP3–WP5) | ← | Metrics, logs, event streams |
| Prometheus + Grafana | → | KPI metrics export and visualisation |
| WP6-B Chaos Agent | ← | Receives resilience test results |
| WP6-C User Study Coordinator | ← | Receives survey response data |
| Researcher (thesis reports) | → | Evaluation data exports for Papers 3, 4, 5 |

---

## KPIs Contributed
Computes and tracks all 29 KPIs and 5 composite scores as defined in T2.2.

---

## Implementation Notes
- This agent should be deployed **from the beginning of WP3** (not just WP6) so that infrastructure KPIs are measured from the first integration test
- Normalisation functions for composite scores need careful definition: `norm(x)` must be defined with min/max bounds anchored to the baseline, not the current measurement — document this in the T2.2 measurement methodology
- Survey data collection (M-WP5-04, M-USR-01, M-USR-04) requires a companion mobile app or web UI — this is a frontend dependency that must be scoped in WP3
- MIA evaluation (M-PRI-02) is scheduled, not continuous — run weekly or monthly using a shadow model evaluation harness; not part of the real-time dashboard
- Energy data (M-USR-05) may come from a building BMS or smart meter API — integrate via WP3-D External Integration Agent
