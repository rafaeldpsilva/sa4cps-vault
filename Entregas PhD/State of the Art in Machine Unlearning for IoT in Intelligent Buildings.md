<!--
=============================================================
  CCC STRUCTURE MAP
=============================================================
WHOLE PAPER
  [C1 – Context]     §1 Introduction + §2 Background + §3 IoT in IBs
  [C2 – Content]     §4 Machine Unlearning in IoT/IBs + §5 Case Studies
  [C3 – Conclusion]  §6 Open Challenges + §7 Future Directions + §8 Conclusion

SECTION (repeated for every section)
  [C1] Opening paragraph — situates the section within the paper's argument
  [C2] Core subsections — the substance
  [C3] Closing paragraph — synthesises findings, exposes the gap that motivates the next section

PARAGRAPH (implied throughout)
  Topic sentence (C1) → evidence / discussion (C2) → synthesis / transition sentence (C3)
=============================================================
-->

<!-- ══════════════════════════════════════════════════════
     WHOLE-PAPER C1 – CONTEXT  (§1–§3)
     Goal: establish WHY this survey is needed
     ══════════════════════════════════════════════════════ -->

## 1. Introduction
<!-- PARAGRAPH CCC:
     C1 – IoT data explosion + privacy risk in intelligent buildings
     C2 – machine unlearning as a solution; GDPR "right to be forgotten"
     C3 – scope statement: this survey reviews MU methods for IoT/IBs
-->

The proliferation of Internet of Things (IoT) devices within intelligent building environments has led to an exponential increase in data generation, much of which is sensitive and personal [1]. This pervasive data collection, while enabling advanced functionalities, concurrently introduces significant privacy and security vulnerabilities, as machine learning models deployed in these settings may inadvertently memorize or leak sensitive information [2]. In response to these challenges, machine unlearning has emerged as a crucial technique for selectively removing the influence of specific data points from trained models, thereby enhancing privacy protection and model security [3]. This capability is particularly vital for compliance with stringent data protection regulations such as the GDPR, which mandate the "right to be forgotten" and necessitate mechanisms for data removal without compromising model utility [4]. Consequently, machine unlearning methods are designed to achieve this data excision either by retraining models from scratch on the reduced dataset or by incrementally updating the existing models to forget specific information. This survey explores the current state-of-the-art in machine unlearning methodologies, focusing on their applicability and challenges within the specialized context of IoT deployments in intelligent buildings.

<!-- SECTION CLOSE (transition):
     One paragraph summarising the structure of the paper (roadmap),
     linking each section to a step in the argument. -->

---

## 2. Background on Machine Unlearning
<!-- SECTION CCC:
     C1 – Opening paragraph: why the ML community needed an "undo" mechanism;
          regulatory pressure (GDPR Art. 17) and the impracticality of full retraining
     C2 – Definitions, motivations, taxonomy (§2.1–§2.3)
     C3 – Closing paragraph: current approaches are designed for centralised,
          static models — this creates a gap for distributed, resource-constrained IoT -->

<!-- SECTION OPENING (C1):
     Set up the problem: data is hard to delete from trained ML models;
     GDPR Article 17 creates a legal obligation; full retraining is computationally prohibitive.
     This motivates the formalisation of machine unlearning as a research field. -->

### 2.1 Motivations for Machine Unlearning
<!-- PARAGRAPH CCC:
     C1 – legal/ethical drivers (GDPR Art. 17, CCPA, user consent revocation)
     C2 – technical problem: gradient descent "bakes in" training data;
          membership inference attacks demonstrate leakage
     C3 – these pressures together establish unlearning as a necessary capability -->

### 2.2 Definition and Formal Principles
<!-- PARAGRAPH CCC:
     C1 – informal intuition: the model after unlearning should behave as if
          the forgotten data was never seen
     C2 – formal definitions (certified removal, approximate unlearning, differential-privacy framing)
     C3 – the diversity of definitions reflects the lack of a single accepted standard -->

### 2.3 Taxonomy of Unlearning Approaches
<!-- PARAGRAPH CCC:
     C1 – two high-level families: exact vs. approximate unlearning
     C2 – exact: SISA training, data sharding; approximate: gradient-based,
          influence functions, model editing, knowledge distillation
     C3 – exact methods offer strong guarantees but are expensive;
          approximate methods are practical but hard to verify — a trade-off
          that is especially acute in IoT settings (§4) -->

<!-- SECTION CLOSE (C3):
     Summarise the state of unlearning research: rich body of work in centralised,
     homogeneous settings. The missing piece is the intersection with
     distributed, heterogeneous, resource-limited systems — namely IoT in buildings.
     This motivates §3. -->

---

## 3. IoT in Intelligent Buildings
<!-- SECTION CCC:
     C1 – Opening paragraph: intelligent buildings as a socio-technical system
          that depends on continuous ML inference over sensitive occupancy/behavioural data
     C2 – architecture, data challenges, ML role (§3.1–§3.3)
     C3 – Closing paragraph: the combination of strict privacy obligations,
          heterogeneous hardware, and real-time constraints creates unique
          unlearning requirements not addressed by existing methods -->

<!-- SECTION OPENING (C1):
     Frame the intelligent building as a system where privacy and utility
     are in constant tension: fine-grained sensing enables energy optimisation
     and comfort, but also creates detailed behavioural profiles of occupants. -->

### 3.1 IoT Architectures in Intelligent Buildings
<!-- PARAGRAPH CCC:
     C1 – layered architecture: sensors/actuators → edge gateways → cloud/fog
     C2 – protocols (MQTT, Zigbee, BACnet), data volumes, heterogeneity,
          latency constraints; typical ML deployment points
     C3 – distributed nature means model state is replicated across tiers,
          complicating data deletion -->

### 3.2 Data Management and Privacy Challenges
<!-- PARAGRAPH CCC:
     C1 – types of sensitive data: occupancy patterns, energy usage, biometrics
     C2 – regulatory landscape (GDPR, ePrivacy), data minimisation principles,
          consent lifecycle management
     C3 – consent revocation is common in occupant-facing systems,
          creating frequent unlearning requests that must be handled efficiently -->

### 3.3 Role of Machine Learning in Intelligent Building Systems
<!-- PARAGRAPH CCC:
     C1 – ML tasks: occupancy prediction, HVAC optimisation, anomaly detection,
          user preference modelling
     C2 – model types deployed (time-series, GNNs, federated models),
          training regimes (online, periodic batch)
     C3 – online and federated training regimes mean the "snapshot to retrain from"
          is ill-defined — standard unlearning assumptions break down -->

<!-- SECTION CLOSE (C3):
     The distinctive properties of IoT/IB environments — distributed state,
     resource constraints, online training, high request frequency — mean that
     unlearning methods from §2 cannot be applied directly.
     §4 examines what has actually been attempted at this intersection. -->

---
<!-- ══════════════════════════════════════════════════════
     WHOLE-PAPER C2 – CONTENT  (§4–§5)
     Goal: report WHAT has been done
     ══════════════════════════════════════════════════════ -->

## 4. Machine Unlearning in IoT and Intelligent Buildings
<!-- SECTION CCC:
     C1 – Opening paragraph: the intersection of MU and IoT/IBs is nascent;
          most work adapts centralised methods with varying success
     C2 – research landscape, domain-specific challenges, existing frameworks,
          evaluation metrics (§4.1–§4.4)
     C3 – Closing paragraph: existing approaches address isolated sub-problems
          but no integrated framework covers the full IB stack;
          §5 instantiates this through concrete application scenarios -->

<!-- SECTION OPENING (C1):
     Characterise the maturity of the field: volume of publications,
     where it sits relative to adjacent areas (federated learning, differential privacy),
     and what sub-problems have attracted the most attention. -->

### 4.1 Current State of Research
<!-- PARAGRAPH CCC:
     C1 – survey scope: how papers were selected, period covered, source databases
     C2 – quantitative overview (volume, venue, topic clustering);
          dominant problem formulations addressed so far
     C3 – the literature is fragmented: few papers target IBs explicitly;
          most adapt FL-unlearning or edge-unlearning work -->

### 4.2 Specific Challenges of Unlearning in IB-IoT Environments
<!-- PARAGRAPH CCC:
     C1 – why IB-IoT is harder than the general case
     C2 – resource constraints (memory, compute on edge), model heterogeneity,
          multi-tenancy (multiple occupants / data owners per device),
          real-time availability requirements, federated topology
     C3 – these constraints impose design requirements that §4.3 methods only partially satisfy -->

### 4.3 Existing Approaches and Frameworks
<!-- PARAGRAPH CCC:
     C1 – categorise by architecture tier: cloud-side, edge-side, federated
     C2 – review each category: methods, assumptions, reported performance,
          limitations; highlight which IB challenges each addresses
     C3 – no single approach satisfies all constraints; trade-offs between
          efficiency, verifiability, and model utility remain open -->

### 4.4 Evaluation Metrics and Benchmarks
<!-- PARAGRAPH CCC:
     C1 – evaluation is inconsistent across papers, hindering comparison
     C2 – metrics: unlearning completeness (membership inference, activation analysis),
          model utility retention, computational cost, communication overhead
     C3 – lack of IB-specific benchmarks is itself an open problem;
          standardisation is needed before practical deployment -->

<!-- SECTION CLOSE (C3):
     The reviewed methods provide partial solutions; §5 illustrates
     how they perform (or fail) in concrete IB scenarios. -->

---

## 5. Case Studies and Applications
<!-- SECTION CCC:
     C1 – Opening paragraph: case studies ground abstract methods in operational
          IB contexts and reveal practical bottlenecks
     C2 – three representative scenarios (§5.1–§5.3)
     C3 – Closing paragraph: across scenarios a common pattern emerges —
          approximate unlearning dominates because exact methods are infeasible;
          verification remains the weakest link -->

### 5.1 Unlearning Personal Data in Smart Home Systems
<!-- C1 – scenario: occupant requests deletion after moving out
     C2 – method applied, results, failure modes
     C3 – lesson extracted for the broader challenge -->

### 5.2 Model Retraction in Energy Management Systems
<!-- C1 – scenario: erroneous/biased data identified post-deployment
     C2 – method applied, impact on HVAC model accuracy
     C3 – lesson: utility degradation is the main cost -->

### 5.3 Privacy-Preserving Updates in Building Automation
<!-- C1 – scenario: multi-tenant building, per-tenant consent revocation
     C2 – federated unlearning approach, communication overhead
     C3 – lesson: federated topology amplifies verification difficulty -->

<!-- SECTION CLOSE (C3):
     Case studies confirm the gap identified in §4: no method handles
     all three scenarios well. This motivates a structured articulation
     of open challenges in §6. -->

---
<!-- ══════════════════════════════════════════════════════
     WHOLE-PAPER C3 – CONCLUSION  (§6–§8)
     Goal: synthesise WHAT IS MISSING and WHERE TO GO
     ══════════════════════════════════════════════════════ -->

## 6. Challenges and Open Research Questions
<!-- SECTION CCC:
     C1 – Opening paragraph: despite recent progress, several fundamental
          obstacles prevent production deployment in IBs
     C2 – four challenge clusters (§6.1–§6.4)
     C3 – Closing paragraph: these challenges are interdependent;
          solving scalability without solving verification is insufficient;
          §7 proposes directions that address them jointly -->

### 6.1 Scalability and Efficiency in Large-Scale IoT
### 6.2 Verification and Formal Guarantees of Unlearning
### 6.3 Regulatory and Ethical Considerations
### 6.4 Interoperability and Standardisation

<!-- SECTION CLOSE (C3):
     The challenges form a research agenda; §7 maps emerging techniques
     onto this agenda. -->

---

## 7. Future Directions and Opportunities
<!-- SECTION CCC:
     C1 – Opening paragraph: recent advances in adjacent fields (FL, TEEs,
          PETs, LLMs) open new solution pathways for each challenge in §6
     C2 – three promising directions (§7.1–§7.3)
     C3 – Closing paragraph: realising these directions requires
          cross-disciplinary collaboration (systems, ML, law, HCI);
          a community benchmark and reference architecture would accelerate progress -->

### 7.1 Federated Unlearning in Distributed IoT Architectures
<!-- Addresses §6.1 (scalability) and §6.2 (verification in federated settings) -->

### 7.2 Hardware-Accelerated and On-Device Unlearning
<!-- Addresses §6.1 (edge compute constraints) -->

### 7.3 Integration with Privacy-Enhancing Technologies
<!-- Addresses §6.2 (verifiability via TEEs/ZKPs) and §6.3 (regulatory compliance) -->

<!-- SECTION CLOSE (C3):
     Progress on these fronts will collectively close the gap between
     the theoretical guarantees of §2 and the operational reality of §3–§5. -->

---

## 8. Conclusion
<!-- PARAGRAPH CCC:
     C1 – restate the problem: ML models in IBs accumulate sensitive data;
          unlearning is the privacy-preserving answer; existing methods fall short
     C2 – summary of what the survey found: taxonomy of approaches (§2),
          IoT/IB constraints (§3), state of the art at the intersection (§4–§5),
          open challenges (§6), promising directions (§7)
     C3 – closing claim: machine unlearning for IoT in intelligent buildings
          is a critical and underserved research area; the community
          needs benchmarks, reference architectures, and formal verification
          frameworks before real-world deployment can be responsibly achieved -->
