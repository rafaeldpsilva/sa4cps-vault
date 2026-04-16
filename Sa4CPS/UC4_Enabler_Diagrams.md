# UC4 — Enabler Concept Architectures

---

## Perception

---

### #1 · Autonomous Detection and Mitigation of Voltage Issues

```mermaid
flowchart LR

    classDef src   fill:#dce8ff,stroke:#3a6fc4,color:#1a1a1a
    classDef proc  fill:#f5a8a3,stroke:#c04040,color:#1a1a1a
    classDef dst   fill:#dcf0dc,stroke:#3a8a3a,color:#1a1a1a

    subgraph SRC["Data Sources"]
        HH["Smart Meters"]
        DT["Digital Twin"]
    end

    subgraph EN["Voltage Detection & Mitigation"]
        TD["Threshold Detector"]
        STF["Short-term Forecaster"]
        MT["Mitigation Trigger"]
        TD --> STF --> MT
    end

    subgraph DST["Outputs"]
        DASH["Operator Dashboard"]
        FC["Flexibility Coordinator\n(battery activation)"]
    end

    HH  -->|voltage & power readings| TD
    DT  -->|bus voltages · line loadings| TD
    STF -->|voltage event\nNORMAL · WARNING · CRITICAL| DASH
    MT  -->|flexibility request| FC

    class HH,DT src
    class TD,STF,MT proc
    class DASH,FC dst
```

---

### #2 · Secure Data Ingestion & Validation Layer

```mermaid
flowchart LR

    classDef src  fill:#dce8ff,stroke:#3a6fc4,color:#1a1a1a
    classDef proc fill:#a8c8ff,stroke:#1a4a9a,color:#1a1a1a
    classDef dst  fill:#dcf0dc,stroke:#3a8a3a,color:#1a1a1a
    classDef rej  fill:#ffe0e0,stroke:#c04040,color:#1a1a1a

    subgraph SRC["Data Sources"]
        RP["Raspberry Pi Nodes\n(real households)"]
        SA["Simulation Agent\n(virtual households)"]
    end

    subgraph EN["Secure Data Ingestion & Validation"]
        AUTH["Authentication"]
        SV["Schema Validator"]
        PC["Plausibility Checker"]
        AUTH --> SV --> PC
    end

    subgraph DST["Outputs"]
        PLAT["Community Platform\n(validated data stream)"]
        DLQ["System Administrator\n(rejected messages)"]
        AL["Audit Log\n(compliance record)"]
    end

    RP --> |raw energy readings| AUTH
    SA --> |synthetic load data| AUTH
    PC  -->|valid message| PLAT
    AUTH -->|auth failure| DLQ
    SV   -->|invalid format| DLQ
    PC   -->|impossible reading| DLQ
    AUTH -.->|event| AL
    SV   -.->|event| AL
    PC   -.->|event| AL

    class RP,SA src
    class AUTH,SV,PC proc
    class PLAT,AL dst
    class DLQ rej
```

---

### #3 · Consent-Aware Energy Data Perception Module

```mermaid
flowchart LR

    classDef src     fill:#dce8ff,stroke:#3a6fc4,color:#1a1a1a
    classDef proc    fill:#f9a8c9,stroke:#b84080,color:#1a1a1a
    classDef full    fill:#dcf0dc,stroke:#3a8a3a,color:#1a1a1a
    classDef partial fill:#fff3dc,stroke:#c68000,color:#1a1a1a
    classDef blocked fill:#e8e8e8,stroke:#909090,color:#1a1a1a

    subgraph SRC["Inputs"]
        DS["Validated Data Stream\n(from ingestion layer)"]
        HM["Household Members\n(manage consent preferences)"]
    end

    subgraph EN["Consent-Aware Perception Module"]
        CR[("Consent Registry")]
        CL["Consent Lookup"]
        DC["Data Classifier"]
        RE["Routing Engine"]
        CR --> CL --> DC --> RE
    end

    subgraph DST["Data Destinations"]
        CA["Comprehension Engine\n(full granular data)"]
        AN["Anonymised Analytics\n(aggregated data only)"]
        BL["Local Household Storage\n(data not shared with community)"]
    end

    DS  --> CL
    HM  -->|set preferences| CR
    RE  -->|full consent| CA
    RE  -->|partial consent| AN
    RE  -->|no consent| BL

    class DS,HM src
    class CR,CL,DC,RE proc
    class CA full
    class AN partial
    class BL blocked
```

---

## Comprehension

---

### #4 · Digital Twin for Electricity Distribution Network

```mermaid
flowchart LR

    classDef src  fill:#dce8ff,stroke:#3a6fc4,color:#1a1a1a
    classDef proc fill:#a8d5a2,stroke:#3a8a3a,color:#1a1a1a
    classDef mid  fill:#c8e8c8,stroke:#3a8a3a,color:#1a1a1a
    classDef dst  fill:#dcf0dc,stroke:#1a6a1a,color:#1a1a1a

    subgraph SRC["Data Sources"]
        RH["Real Households\n(Raspberry Pi smart meters)"]
        VH["Virtual Households\n(simulation agents)"]
        BMS["Battery Bank\n(GECAD Lab BMS)"]
    end

    subgraph EN["Digital Twin"]
        SU["State Updater"]
        NM["Network Model\n(virtual grid topology)"]
        PF["Power Flow Engine"]
        SU --> NM --> PF
    end

    NS("Network State\nbus voltages · line loadings · battery SoC")

    subgraph DST["Consumed by"]
        VM["Voltage Monitor"]
        FLC["Flexibility Coordinator"]
        DB["Dashboard"]
        CE["Comprehension Engine"]
    end

    RH  -->|real-time consumption & voltage| SU
    VH  -->|synthetic load profiles| SU
    BMS -->|state of charge · power output| SU
    PF  --> NS
    NS  --> VM
    NS  --> FLC
    NS  --> DB
    NS  --> CE

    class RH,VH,BMS src
    class SU,NM,PF proc
    class NS mid
    class VM,FLC,DB,CE dst
```

---

### #5 · Dashboard for Energy Community Management

```mermaid
flowchart LR

    classDef src  fill:#dce8ff,stroke:#3a6fc4,color:#1a1a1a
    classDef proc fill:#a8e6ef,stroke:#2a8a96,color:#1a1a1a
    classDef dst  fill:#dcf0dc,stroke:#3a8a3a,color:#1a1a1a

    subgraph SRC["Data Sources"]
        DT["Digital Twin\n(network state)"]
        VM["Voltage Monitor\n(alerts & events)"]
        CE["Comprehension Engine\n(forecasts · situational summary)"]
        FLC["Flexibility Coordinator\n(activation log · XAI explanations)"]
    end

    subgraph EN["Dashboard"]
        DA["Data Aggregator"]
        API["API Layer"]
        DA --> API
    end

    subgraph DST["Users"]
        CM["Community Manager\n(overview · flexibility log)"]
        GO["Grid Operator\n(voltage map · alerts)"]
        RES["Residents\n(consumption · forecast)"]
    end

    DT  --> DA
    VM  --> DA
    CE  --> DA
    FLC --> DA
    API --> CM
    API --> GO
    API --> RES

    class DT,VM,CE,FLC src
    class DA,API proc
    class CM,GO,RES dst
```

---

### #6 · Activation of Flexible Resources

```mermaid
flowchart LR

    classDef src   fill:#dce8ff,stroke:#3a6fc4,color:#1a1a1a
    classDef guard fill:#f5a8a3,stroke:#c04040,color:#1a1a1a
    classDef proc  fill:#ffd599,stroke:#c68000,color:#1a1a1a
    classDef dst   fill:#dcf0dc,stroke:#3a8a3a,color:#1a1a1a

    subgraph SRC["Triggers & Context"]
        VM["Voltage Monitor\n(automated request)"]
        OP["Grid Operator\n(manual request via dashboard)"]
        BMS["Battery Bank BMS\n(state of charge · available power)"]
        DT["Digital Twin\n(pre-act simulation environment)"]
    end

    subgraph EN["Flexibility Coordinator"]
        SG["Safeguards\n(SoC floor · rate limits · cooldown)"]
        FC["Feasibility Check"]
        PS["Pre-act Simulation\n(verify effect before committing)"]
        AE["Actuation Engine"]
        XG["XAI Generator"]
        SG --> FC --> PS -->|verified| AE --> XG
    end

    subgraph DST["Outputs"]
        BAT["Battery Bank\n(discharge command)"]
        DASH["Dashboard\n(explanation for operators & residents)"]
        LOG["Activation Record\n(history & reporting)"]
    end

    VM  -->|flexibility request| FC
    OP  -->|manual request| FC
    BMS -->|current state| SG
    BMS -->|current state| FC
    DT  -->|simulation result| PS
    AE  -->|discharge command| BAT
    XG  -->|why · what · expected effect| DASH
    AE  -->|record| LOG

    class VM,OP,BMS,DT src
    class SG guard
    class FC,PS,AE,XG proc
    class BAT,DASH,LOG dst
```

---

### #7 · Energy Community Situational Comprehension Engine

```mermaid
flowchart LR

    classDef src  fill:#dce8ff,stroke:#3a6fc4,color:#1a1a1a
    classDef proc fill:#d4a8e8,stroke:#7b4fa6,color:#1a1a1a
    classDef dst  fill:#dcf0dc,stroke:#3a8a3a,color:#1a1a1a

    subgraph SRC["Inputs"]
        RP["Raspberry Pi Nodes\n(locally trained FL models\nno raw data leaves the household)"]
        DP["Data Pipeline\n(validated meter readings)"]
        DT["Digital Twin\n(network state)"]
        TE["Trust Engine\n(per-node reliability weights)"]
    end

    subgraph EN["Situational Comprehension Engine"]
        FLA["FL Aggregator\n(combines local household models)"]
        CF["Consumption Forecaster\n(per household & community aggregate)"]
        FE["Flexibility Estimator\n(available battery capacity + sheddable load)"]
        SS["Situational Summariser\n(community health snapshot)"]
        FLA --> CF --> FE --> SS
    end

    subgraph DST["Outputs"]
        DASH["Dashboard\n(forecasts · community health)"]
        FLC["Flexibility Coordinator\n(available flexibility estimate)"]
    end

    RP --> FLA
    DP --> CF
    TE --> CF
    DT --> FE
    CF --> DASH
    SS --> DASH
    FE --> FLC

    class RP,DP,DT,TE src
    class FLA,CF,FE,SS proc
    class DASH,FLC dst
```

---

### #8 · Trust & Data Quality Assessment Engine

```mermaid
flowchart LR

    classDef src  fill:#dce8ff,stroke:#3a6fc4,color:#1a1a1a
    classDef proc fill:#f9a8c9,stroke:#b84080,color:#1a1a1a
    classDef dst  fill:#dcf0dc,stroke:#3a8a3a,color:#1a1a1a

    subgraph SRC["Input"]
        DP["Data Pipeline\n(validated meter readings\nfrom all households)"]
    end

    subgraph EN["Trust & Data Quality Engine"]
        CT["Communication Tracker\n(is the node reporting consistently?)"]
        PS["Plausibility Scorer\n(are the readings physically possible?)"]
        TA["Trust Aggregator\n(rolling per-node score · 0 to 1)"]
        CT --> TA
        PS --> TA
    end

    subgraph DST["Outputs"]
        CE["Comprehension Engine\n(weights each household's contribution\nto community forecasts)"]
        DASH["Dashboard\n(low-trust node alerts\nfor system administrators)"]
    end

    DP --> CT
    DP --> PS
    TA -->|trust score per node| CE
    TA -->|degraded node alert| DASH

    class DP src
    class CT,PS,TA proc
    class CE,DASH dst
```
