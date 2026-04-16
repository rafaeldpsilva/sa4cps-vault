# UC4 — Architecture Diagram (Draft)

```mermaid
flowchart TD

    subgraph SOURCES["Data Sources"]
        RP["Raspberry Pi nodes\nreal houses · Tailscale"]
        SIM["Simulation Script\nCSV profiles → MQTT"]
        BMSAPI["GECAD Battery BMS\nexisting REST/MQTT API"]
    end

    MQTT["MQTT Broker\nTLS · device authentication"]

    subgraph PERC["Perception Layer"]
        E2["#2 Secure Data Ingestion\n& Validation Layer\nDigitalmente"]
        E3["#3 Consent-Aware\nPerception Module\nDigitalmente · CEL"]
        E1["#1 Voltage Detection\n& Mitigation\nISEP"]
    end

    subgraph KAFKA["Message Bus · Kafka"]
        KR[/"raw-readings"/]
        KT[/"twin-state"/]
        KV[/"voltage-events"/]
        KF[/"flexibility-requests"/]
        KC[/"comprehension-outputs"/]
        KTR[/"trust-scores"/]
    end

    subgraph COMP["Comprehension Layer"]
        E4["#4 Digital Twin\nPandapower · sync loop\nISEP"]
        E8["#8 Trust & Data Quality\nAssessment Engine\nDigitalmente"]
        E7["#7 Situational Comprehension\nEngine\nDigitalmente · CEL · ISEP"]
        E6["#6 Activation of\nFlexible Resources\nISEP"]
        E5["#5 Dashboard\nFastAPI · Vue.js\nISEP"]
    end

    %% Sources → broker
    RP -->|MQTT| MQTT
    SIM -->|MQTT| MQTT

    %% Broker → ingestion → consent → Kafka
    MQTT --> E2
    E2 --> E3
    E3 --> KR

    %% raw-readings fans out to perception + twin + trust
    KR --> E1
    KR --> E4
    KR --> E8

    %% Digital twin publishes state
    E4 --> KT

    %% Trust engine publishes scores
    E8 --> KTR

    %% Voltage detector reads both raw and twin-state
    KT --> E1

    %% Voltage detector outputs
    E1 --> KV
    E1 --> KF

    %% Comprehension engine inputs
    KR --> E7
    KT --> E7
    KTR --> E7

    %% Comprehension engine output
    E7 --> KC

    %% Flexibility activation
    KF --> E6
    E6 -->|discharge command| BMSAPI
    BMSAPI -->|SoC · power output| E6
    E6 -->|battery state update| KT

    %% Dashboard consumes everything
    KT --> E5
    KV --> E5
    KC --> E5
    KF --> E5
```

## Component summary

| # | Enabler | Layer | Party | Core technology |
|---|---------|-------|-------|----------------|
| 1 | Voltage Detection & Mitigation | Perception | ISEP | Kafka consumer · threshold + forecast |
| 2 | Secure Data Ingestion & Validation | Perception | Digitalmente | Schema validation · dead-letter queue |
| 3 | Consent-Aware Perception Module | Perception | Digitalmente · CEL | Consent registry · message router |
| 4 | Digital Twin | Comprehension | ISEP | Pandapower · sync loop |
| 5 | Dashboard | Comprehension | ISEP | FastAPI · Vue.js |
| 6 | Activation of Flexible Resources | Comprehension | ISEP | BMS API · XAI · safeguards |
| 7 | Situational Comprehension Engine | Comprehension | Digitalmente · CEL · ISEP | Federated learning · consumption forecast |
| 8 | Trust & Data Quality Engine | Comprehension | Digitalmente | Per-node trust scores |

## Key data flows

- **raw-readings** — validated per-household meter readings (voltage, power, timestamp) after consent filtering
- **twin-state** — Pandapower outputs: per-bus voltage, line loadings, battery SoC, published every sync interval
- **voltage-events** — NORMAL / WARNING / CRITICAL per node, emitted by #1
- **flexibility-requests** — structured trigger events (node, deviation magnitude, urgency) from #1 or operator
- **trust-scores** — per-node data quality weights [0–1], consumed by #7
- **comprehension-outputs** — consumption forecasts, aggregate forecast, flexibility estimate, situational summary
