## Abstract
<!-- ══════════════════════════════════════════════════════════
     RULE 5 — ABSTRACT  (complete CCC story in miniature)
     ══════════════════════════════════════════════════════════
     C1 (Context, ~2–3 sentences):
       Broad field → narrow to specific gap.
       • Sentence 1: IoT in IBs generates personal data at scale.
       • Sentence 2: ML models retain statistical traces of that data
                     even after deletion — a privacy liability.
       • Sentence 3: Regulations (GDPR Art. 17) demand a technical
                     solution, yet existing machine unlearning methods
                     were designed for centralised, static settings
                     and do not address IB-IoT constraints.
                     [← this is the GAP that locks the key]

     C2 (Content, ~2 sentences — "Here we…"):
       • Here we survey … (scope + method of the survey)
       • We identify … (the key findings — what methods exist,
                         what they can and cannot do)

     C3 (Conclusion, ~2 sentences):
       • Our analysis reveals … (answer to the gap question)
       • Broader significance: without benchmarks / verification
         frameworks / reference architectures, responsible deployment
         remains out of reach — calling the community to act.
-->
<!--
WRITE THE ABSTRACT HERE following the CCC template above. Aim for ~200 words. Write it last, after the body is stable. -->

## 1. Introduction

<!-- RULE 6 — GAP PROGRESSION (one paragraph per scale of gap):



  Para 2 — SUBFIELD-LEVEL GAP
    C1: Machine unlearning has emerged as the technical answer:
        selectively erasing the influence of specific training samples
        without full retraining.
    C2: A rich body of methods exists — exact (SISA, data sharding)
        and approximate (gradient-based, influence functions, model editing)
        — validated in centralised, homogeneous settings.
    C3: However, these methods assume static models on powerful hardware
        with infrequent deletion requests — assumptions that break down
        in IB-IoT environments.

  Para 3 — SPECIFIC GAP (the one this paper fills)
    C1: Intelligent building IoT systems are characterised by resource-
        constrained edge devices, distributed and replicated model state,
        high-frequency consent revocations, real-time availability
        requirements, and heterogeneous federated topologies.
    C2: No existing survey or framework addresses unlearning in this
        combined setting. Work at the intersection remains fragmented:
        methods are borrowed from federated learning or edge ML without
        validating the unlearning guarantees in IB-specific conditions.
    C3: This gap is not merely academic — GDPR Article 17 creates
        legal obligations that buildings operators cannot currently meet.

  Para 4 — WHAT THIS PAPER DOES (summary of results; Rule 6 last paragraph)
    Compact summary: this survey covers X papers from Y to Z,
    taxonomises existing approaches, identifies four structural
    challenges specific to IB-IoT, evaluates methods against those
    challenges, and proposes a research agenda to close the gap.
    Does NOT need to re-establish context (already done above).
    Only briefly previews the conclusion.
-->
The proliferation of Internet of Things (IoT) devices within intelligent buildings has led to an exponential increase in fine-grained data, including occupancy energy use, biometrics and movement patterns, which can be leveraged to optimize performance and enhance security . However, while this pervasive data collection enables advanced functionalities, they also preserve a detailed digital footprint of occupants’ activities even after raw data is deleted [[1]]. This constant data feed introduces significant privacy and security vulnerabilities, as machine learning models deployed in these settings may inadvertently memorize or leak sensitive information they were designed to process [[2]]. This capability is particularly vital for compliance with stringent data protection regulations such as the GDPR, which mandate the "right to be forgotten" and necessitate mechanisms for data removal without compromising model utility [[4]]. Consequently, machine unlearning methods are designed to achieve this data excision either by retrain models from scratch on the reduced dataset or by incrementally update the existing models to forget specific information.

There is a growing number of machine unlearning methods [[5]]. These methods address the fundamental challenge of efficiently eliminating the impact of specific training data without incurring the computational expense of complete model retraining [[6]]. However, the application of machine unlearning specifically within the context of IoT in intelligent buildings presents unique complexities due to the distributed nature of data, real-time processing requirements, and heterogeneity of devices [[7], [8]].

An intelligent building IoT system is characterized by resource-contrained edge devices, distributed deployments, high-frequency consent revocations, real-time availabiltiy requirements, and diverse data modalities. Current research does not fully address these challenges of machine unlearning on the context of intelligent buildings [[9]]. Additionally, this problem moves beyond merely academic purposes, complying with regulations such as the GDPR’s “right to be forgotten” and other data protection policies[[10]].

This survey will explore the current state-of-the-art in machine unlearning methodologies, particularly focusing on their applicability and challenges within the specialized context of IoT deployments in intelligent buildings.

## 2. Background on Machine Unlearning

> SECTION CCC: C1 – Opening paragraph: why the ML community needed an "undo" mechanism;  
> regulatory pressure (GDPR Art. 17) and the impracticality of full retraining  
> C2 – Motivations, definitions, taxonomy (§2.1–§2.3)  
> C3 – Closing paragraph: current approaches are designed for centralised,  
> static models — this creates a gap for distributed, resource-constrained IoT

Machine unlearning addresses the need to expunge or modify predictions generated by machine learning models, which is increasingly critical for privacy, security, and fairness considerations [[11]]. The core principle behind machine unlearning is to eliminate the influence of particular training data points from a trained model without having to retrain the model, effectively making the model behave as if those data points were never part of the training set.

## 2. Background on Machine Unlearning

<!-- SECTION CCC:
     C1 – Opening paragraph: why the ML community needed an "undo" mechanism;
          regulatory pressure (GDPR Art. 17) and the impracticality of full retraining
     C2 – Motivations, definitions, taxonomy (§2.1–§2.3)
     C3 – Closing paragraph: current approaches are designed for centralised,
          static models — this creates a gap for distributed, resource-constrained IoT -->

<!-- SECTION OPENING (C1):
     Set up the problem: data is hard to delete from trained ML models;
     GDPR Article 17 creates a legal obligation; full retraining is
     computationally prohibitive. This motivates machine unlearning
     as a formalised research field. -->

### 2.1 Motivations for Machine Unlearning

<!-- PARAGRAPH CCC:
     C1 – legal/ethical drivers (GDPR Art. 17, CCPA, user consent revocation)
     C2 – technical problem: gradient descent "bakes in" training data;
          membership inference attacks demonstrate leakage [cite]
     C3 – regulatory pressure + demonstrated leakage together establish
          unlearning as a necessary — not optional — capability -->

### 2.2 Definition and Formal Principles

<!-- PARAGRAPH CCC:
     C1 – informal intuition: a model after unlearning should behave
          as if the forgotten data was never seen
     C2 – formal definitions: certified removal [cite], approximate
          unlearning [cite], differential-privacy framing [cite]
     C3 – the diversity of competing definitions reflects the absence
          of a single accepted standard — itself an open problem -->

### 2.3 Taxonomy of Unlearning Approaches

<!-- PARAGRAPH CCC:
     C1 – two high-level families: exact vs. approximate unlearning
     C2 – exact: SISA training [cite], data sharding; approximate:
          gradient-based [cite], influence functions [cite],
          model editing [cite], knowledge distillation [cite]
     C3 – exact methods offer strong guarantees but are computationally
          expensive; approximate methods are practical but hard to verify —
          a trade-off especially acute in IoT settings (§4.2) -->

<!-- SECTION CLOSE (C3):
     Summarise: machine unlearning has matured in centralised,
     homogeneous settings. The missing piece is the intersection with
     distributed, heterogeneous, resource-limited systems.
     §3 establishes exactly what those systems look like. -->

---

## 3. IoT in Intelligent Buildings

<!-- SECTION CCC:
     C1 – Opening paragraph: intelligent buildings as a socio-technical
          system dependent on continuous ML inference over sensitive data
     C2 – architecture, privacy challenges, ML role (§3.1–§3.3)
     C3 – Closing paragraph: the combination of strict privacy obligations,
          heterogeneous hardware, and real-time constraints creates
          unlearning requirements no existing method satisfies -->

<!-- SECTION OPENING (C1):
     Frame the intelligent building as a system where privacy and utility
     are in constant tension: fine-grained sensing enables energy
     optimisation and comfort, but also produces detailed behavioural
     profiles of occupants who may later revoke consent. -->

### 3.1 IoT Architectures in Intelligent Buildings

<!-- PARAGRAPH CCC:
     C1 – layered architecture: sensors/actuators → edge gateways → cloud/fog
     C2 – protocols (MQTT, Zigbee, BACnet), data volumes, heterogeneity,
          latency constraints; typical ML deployment points at each tier
     C3 – because model state is replicated across tiers, a single
          deletion request may require coordinated updates across
          multiple devices — a challenge absent in centralised settings -->

### 3.2 Data Management and Privacy Challenges

<!-- PARAGRAPH CCC:
     C1 – types of sensitive data generated: occupancy patterns,
          energy usage profiles, biometric/environmental signals
     C2 – regulatory landscape (GDPR, ePrivacy Directive), data
          minimisation principles, consent lifecycle management in
          multi-occupant buildings
     C3 – consent revocations are frequent and unpredictable in
          occupant-facing systems, creating a high-throughput stream
          of unlearning requests that must be handled efficiently -->

### 3.3 Role of Machine Learning in Intelligent Building Systems

<!-- PARAGRAPH CCC:
     C1 – ML tasks in IBs: occupancy prediction, HVAC optimisation,
          anomaly detection, user preference modelling
     C2 – model types deployed (time-series, GNNs, federated models)
          and training regimes (online, periodic batch, federated)
     C3 – online and federated regimes mean the "clean snapshot to
          retrain from" is ill-defined — the core assumption of most
          exact unlearning methods breaks down here -->

<!-- SECTION CLOSE (C3):
     The distinctive properties of IB-IoT — distributed state,
     resource constraints, online training, high deletion frequency —
     mean that methods from §2 cannot be applied directly.
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
     C2 – research landscape, domain-specific challenges, existing
          frameworks, evaluation metrics (§4.1–§4.4)
     C3 – Closing paragraph: existing approaches address isolated sub-
          problems but no integrated framework covers the full IB stack;
          §5 instantiates this through concrete scenarios -->

<!-- SECTION OPENING (C1):
     Characterise the maturity of the field: volume of publications,
     position relative to adjacent areas (federated learning, differential
     privacy), and which sub-problems have attracted the most attention. -->

<!-- RULE 7 — SUBSECTION HEADERS ARE DECLARATIVE CLAIMS.
     Each header below states the logical conclusion of that subsection
     so that the reader can fact-check it. After writing, these headers
     become the logical spine of the section argument. -->

### 4.1 Research at the Intersection of Machine Unlearning and IB-IoT Remains Nascent and Fragmented

<!-- PARAGRAPH CCC:
     C1 – survey scope: databases searched, time period, inclusion criteria
     C2 – quantitative overview (paper count, venue distribution, topic
          clusters); most work targets general IoT or FL settings —
          few papers explicitly model IB constraints
     C3 – fragmentation means findings are hard to compare and
          no consensus method has emerged for this domain -->

### 4.2 IB-IoT Environments Impose Constraints That Existing Unlearning Methods Cannot Satisfy

<!-- PARAGRAPH CCC:
     C1 – four constraint dimensions that distinguish IB-IoT from
          the centralised settings in which most methods were designed
     C2 – (a) edge resource limits (memory, compute),
          (b) model heterogeneity across tiers,
          (c) multi-tenancy (multiple data owners per device),
          (d) real-time availability and federated topology
     C3 – each constraint individually complicates unlearning;
          in combination they are unsolved by any single existing method -->

### 4.3 Current Approaches Address Only Isolated Sub-Problems of IB-IoT Unlearning

<!-- PARAGRAPH CCC:
     C1 – categorise by where in the IB stack the method operates:
          cloud-side, edge-side, federated
     C2 – for each category: method, assumptions, reported performance,
          and which of the §4.2 constraints it addresses or ignores
     C3 – cloud-side methods ignore edge constraints;
          edge-side methods ignore federated coordination;
          federated methods weaken unlearning guarantees —
          no single approach satisfies all four constraint dimensions -->

### 4.4 The Absence of IB-Specific Benchmarks Prevents Systematic Comparison

<!-- PARAGRAPH CCC:
     C1 – evaluation metrics used across the surveyed papers vary widely
     C2 – metrics catalogue: unlearning completeness (membership
          inference [cite], activation analysis [cite]), model utility
          retention, computational cost, communication overhead;
          datasets used and their representativeness for IBs
     C3 – without shared benchmarks and agreed metrics, claims of
          "efficient" or "complete" unlearning cannot be compared;
          standardisation is a prerequisite for production deployment -->

<!-- SECTION CLOSE (C3):
     Existing methods address isolated fragments of the problem.
     §5 illustrates how this plays out in three operational IB scenarios,
     making the gaps concrete rather than abstract. -->

---

## 5. Case Studies and Applications

<!-- SECTION CCC:
     C1 – Opening paragraph: case studies ground abstract method limitations
          in operational IB contexts and surface practical bottlenecks
     C2 – three representative scenarios (§5.1–§5.3)
     C3 – Closing paragraph: across all scenarios, approximate unlearning
          dominates because exact methods are computationally infeasible;
          verification remains the weakest link in every case -->

### 5.1 Unlearning Personal Data in Smart Home Systems

<!-- C1 – scenario: occupant requests deletion of their data after moving out
     C2 – method applied, system configuration, results, failure modes
     C3 – lesson: lightweight approximate methods work for single-tenant
          settings but cannot provide verifiable guarantees -->

### 5.2 Model Retraction in Energy Management Systems

<!-- C1 – scenario: erroneous or biased sensor data identified post-deployment
     C2 – method applied, impact on HVAC model accuracy, retraining cost
     C3 – lesson: utility degradation is the dominant cost; approximate
          unlearning degrades model performance non-uniformly -->

### 5.3 Privacy-Preserving Updates in Building Automation

<!-- C1 – scenario: multi-tenant building with per-tenant consent revocation
     C2 – federated unlearning approach, communication overhead, coordination
     C3 – lesson: federated topology amplifies verification difficulty;
          the weakest node in the federation becomes the bottleneck -->

<!-- SECTION CLOSE (C3):
     All three scenarios confirm the analysis in §4: no existing method
     handles the full combination of IB-IoT constraints.
     §6 provides a structured articulation of the open research problems. -->

---

<!-- ══════════════════════════════════════════════════════
     WHOLE-PAPER C3 – CONCLUSION  (§6–§8)
     Goal: synthesise WHAT IS MISSING and WHERE TO GO
     ══════════════════════════════════════════════════════ -->

## 6. Open Challenges

<!-- SECTION CCC:
     C1 – Opening paragraph: the case studies in §5 surface four structural
          obstacles that prevent responsible deployment in IBs
     C2 – one subsection per challenge (§6.1–§6.4)
     C3 – Closing paragraph: the challenges are interdependent —
          solving scalability without solving verification is insufficient;
          §7 proposes directions that address them jointly

  RULE 4 – PARALLELISM:
     §6 challenges map 1-to-1 onto §7 directions.
     §6.1 (scalability)   → §7.2 (hardware-accelerated unlearning)
     §6.2 (verification)  → §7.3 (PETs: TEEs, ZKPs)
     §6.3 (regulation)    → §7.3 (compliance-by-design)
     §6.4 (interop/stds)  → §7.1 (federated reference architecture) -->

### 6.1 Scalability and Efficiency in Large-Scale IoT

### 6.2 Verification and Formal Guarantees of Unlearning

### 6.3 Regulatory and Ethical Considerations

### 6.4 Interoperability and Standardisation

<!-- SECTION CLOSE (C3):
     The four challenges form a coherent research agenda.
     §7 maps each challenge onto a concrete research direction. -->

---

## 7. Future Research Directions

<!-- SECTION CCC:
     C1 – Opening paragraph: recent advances in adjacent fields (FL,
          trusted execution environments, PETs) open new solution
          pathways for the challenges identified in §6
     C2 – three directions, each mapped to one or more §6 challenges (§7.1–§7.3)
     C3 – Closing paragraph: realising these directions requires
          cross-disciplinary collaboration (systems, ML, law, HCI);
          a community benchmark and reference architecture would
          provide the shared foundation needed

  RULE 4 – PARALLELISM:
     Each subsection has the same internal structure:
     (a) which §6 challenge(s) it targets,
     (b) the proposed direction and its technical basis,
     (c) what is still needed to realise it. -->

### 7.1 Federated Unlearning Architectures for Distributed IB-IoT
<!-- Targets §6.1 (scalability) and §6.4 (interoperability / standardisation) -->

### 7.2 Hardware-Accelerated and On-Device Unlearning
<!-- Targets §6.1 (edge compute constraints) -->

### 7.3 Verifiable Unlearning via Privacy-Enhancing Technologies
<!-- Targets §6.2 (formal guarantees via TEEs / ZKPs) and §6.3 (compliance) -->

<!-- SECTION CLOSE (C3):
     Progress on these fronts will collectively close the gap between
     the theoretical guarantees established in §2 and the operational
     reality demonstrated in §3–§5. -->

---

## 8. Conclusion

<!-- RULE 8 — DISCUSSION / CONCLUSION STRUCTURE:
     First paragraph: recapitulate the central finding (fills the gap
     stated in the introduction — locks the key).
     Middle: limitations of the survey itself (coverage, search strategy,
     recency) — credibility requires acknowledging caveats.
     Last paragraph: broader significance — what the community must do
     and why it matters beyond this paper.

  PARAGRAPH CCC:
     C1 – restate the problem: ML models in IBs retain sensitive data;
          existing unlearning methods are insufficient for IB-IoT constraints
     C2 – what the survey found: taxonomy (§2), IB-IoT requirements (§3),
          fragmented state of the art (§4), concrete failure modes (§5),
          four open challenges (§6), three research directions (§7)
     C3 – closing claim: machine unlearning for IB-IoT is a critical,
          underserved area; the community needs shared benchmarks,
          reference architectures, and formal verification frameworks
          before deployment can be responsibly achieved -->
