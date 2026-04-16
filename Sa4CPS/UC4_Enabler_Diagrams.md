# UC4 — Enabler Concept Architectures

---

## Perception

---

### #1 · Autonomous Detection and Mitigation of Voltage Issues

```mermaid
flowchart LR

    classDef input   fill:#a8c8ff,stroke:#3a6fc4,color:#1a1a1a
    classDef proc    fill:#f5a8a3,stroke:#c04040,color:#1a1a1a
    classDef output  fill:#a8d5a2,stroke:#3a8a3a,color:#1a1a1a

    MI("Meter Readings")
    NS("Network State")

    TD["Threshold Detector"]
    STF["Short-term Forecaster"]
    MT["Mitigation Trigger"]

    VE("Voltage Event")
    FR("Flexibility Request")

    MI --> TD
    NS --> TD
    TD --> STF
    STF --> VE
    STF --> MT
    MT --> FR

    class MI,NS input
    class TD,STF,MT proc
    class VE,FR output
```

---

### #2 · Secure Data Ingestion & Validation Layer

```mermaid
flowchart LR

    classDef input   fill:#a8c8ff,stroke:#3a6fc4,color:#1a1a1a
    classDef proc    fill:#a8c8ff,stroke:#1a4a9a,color:#1a1a1a
    classDef output  fill:#a8d5a2,stroke:#3a8a3a,color:#1a1a1a
    classDef reject  fill:#f5a8a3,stroke:#c04040,color:#1a1a1a
    classDef log     fill:#e8e8e8,stroke:#909090,color:#1a1a1a

    DM("Device Message")

    AUTH["Authentication"]
    SV["Schema Validator"]
    PC["Plausibility Checker"]
    AUTH --> SV --> PC

    VS("Validated Data Stream")
    DLQ("Dead Letter Queue")
    AL("Audit Log")

    DM --> AUTH
    PC --> VS
    AUTH -->|rejected| DLQ
    SV  -->|invalid|  DLQ
    PC  -->|implausible| DLQ
    AUTH -.-> AL
    SV   -.-> AL
    PC   -.-> AL

    class DM input
    class AUTH,SV,PC proc
    class VS output
    class DLQ reject
    class AL log
```

---

### #3 · Consent-Aware Energy Data Perception Module

```mermaid
flowchart LR

    classDef input   fill:#a8c8ff,stroke:#3a6fc4,color:#1a1a1a
    classDef proc    fill:#f9a8c9,stroke:#b84080,color:#1a1a1a
    classDef full    fill:#a8d5a2,stroke:#3a8a3a,color:#1a1a1a
    classDef partial fill:#ffd599,stroke:#c68000,color:#1a1a1a
    classDef blocked fill:#e8e8e8,stroke:#909090,color:#1a1a1a

    ID("Incoming Data Stream")
    CR("Consent Registry")

    CL["Consent Lookup"]
    DC["Data Classifier"]
    RE["Routing Engine"]
    CL --> DC --> RE

    FDS("Full Data Stream")
    ADS("Anonymised Stream")
    BL("Blocked")

    ID --> CL
    CR --> CL
    RE -->|full consent|    FDS
    RE -->|partial consent| ADS
    RE -->|no consent|      BL

    class ID,CR input
    class CL,DC,RE proc
    class FDS full
    class ADS partial
    class BL blocked
```

---

## Comprehension

---

### #4 · Digital Twin for Electricity Distribution Network

```mermaid
flowchart LR

    classDef input  fill:#a8c8ff,stroke:#3a6fc4,color:#1a1a1a
    classDef proc   fill:#a8d5a2,stroke:#3a8a3a,color:#1a1a1a
    classDef output fill:#a8d5a2,stroke:#1a6a1a,color:#1a1a1a

    RD("Real Meter Data")
    SD("Simulated Meter Data")
    BS("Battery State")

    SU["State Updater"]
    NM["Network Model"]
    PF["Power Flow Engine"]
    SU --> NM --> PF

    NS("Network State\nvoltages · flows · SoC")

    RD --> SU
    SD --> SU
    BS --> SU
    PF --> NS

    class RD,SD,BS input
    class SU,NM,PF proc
    class NS output
```

---

### #5 · Dashboard for Energy Community Management

```mermaid
flowchart LR

    classDef input  fill:#a8c8ff,stroke:#3a6fc4,color:#1a1a1a
    classDef proc   fill:#a8e6ef,stroke:#2a8a96,color:#1a1a1a
    classDef output fill:#a8d5a2,stroke:#3a8a3a,color:#1a1a1a

    NS("Network State")
    VE("Voltage Events")
    FC("Forecasts")
    FL("Flexibility Log")
    XAI("XAI Explanations")

    DA["Data Aggregator"]
    API["API Layer"]
    DA --> API

    CO("Community Overview")
    VM("Voltage Map")
    FP("Forecast Panel")
    FLV("Flexibility Log")

    NS  --> DA
    VE  --> DA
    FC  --> DA
    FL  --> DA
    XAI --> DA
    API --> CO
    API --> VM
    API --> FP
    API --> FLV

    class NS,VE,FC,FL,XAI input
    class DA,API proc
    class CO,VM,FP,FLV output
```

---

### #6 · Activation of Flexible Resources

```mermaid
flowchart LR

    classDef input  fill:#a8c8ff,stroke:#3a6fc4,color:#1a1a1a
    classDef proc   fill:#ffd599,stroke:#c68000,color:#1a1a1a
    classDef guard  fill:#f5a8a3,stroke:#c04040,color:#1a1a1a
    classDef output fill:#a8d5a2,stroke:#3a8a3a,color:#1a1a1a

    FR("Flexibility Request")
    BS("Battery State")

    SG["Safeguards"]
    FC["Feasibility Check"]
    PS["Pre-act Simulation"]
    AE["Actuation Engine"]
    XG["XAI Generator"]

    SG --> FC
    FC --> PS
    PS -->|verified| AE
    AE --> XG

    DC("Discharge Command")
    EX("XAI Explanation")
    AR("Activation Record")

    FR --> FC
    BS --> FC
    BS --> SG
    AE --> DC
    XG --> EX
    AE --> AR

    class FR,BS input
    class FC,PS,AE,XG proc
    class SG guard
    class DC,EX,AR output
```

---

### #7 · Energy Community Situational Comprehension Engine

```mermaid
flowchart LR

    classDef input  fill:#a8c8ff,stroke:#3a6fc4,color:#1a1a1a
    classDef proc   fill:#d4a8e8,stroke:#7b4fa6,color:#1a1a1a
    classDef output fill:#a8d5a2,stroke:#3a8a3a,color:#1a1a1a

    MU("FL Model Updates")
    RR("Meter Readings")
    NS("Network State")
    TS("Trust Scores")

    FLA["FL Aggregator"]
    CF["Consumption Forecaster"]
    FE["Flexibility Estimator"]
    SS["Situational Summariser"]

    FLA --> CF
    CF  --> FE
    FE  --> SS

    HF("Household Forecasts")
    FEO("Flexibility Estimate")
    SUM("Situational Summary")

    MU --> FLA
    RR --> CF
    TS --> CF
    NS --> FE
    CF --> HF
    FE --> FEO
    SS --> SUM

    class MU,RR,NS,TS input
    class FLA,CF,FE,SS proc
    class HF,FEO,SUM output
```

---

### #8 · Trust & Data Quality Assessment Engine

```mermaid
flowchart LR

    classDef input  fill:#a8c8ff,stroke:#3a6fc4,color:#1a1a1a
    classDef proc   fill:#f9a8c9,stroke:#b84080,color:#1a1a1a
    classDef output fill:#a8d5a2,stroke:#3a8a3a,color:#1a1a1a

    RR("Meter Readings")

    CT["Communication Tracker"]
    PLQ["Plausibility Scorer"]
    TA["Trust Aggregator"]

    CT  --> TA
    PLQ --> TA

    TSC("Trust Score per Node")

    RR --> CT
    RR --> PLQ
    TA --> TSC

    class RR input
    class CT,PLQ,TA proc
    class TSC output
```
