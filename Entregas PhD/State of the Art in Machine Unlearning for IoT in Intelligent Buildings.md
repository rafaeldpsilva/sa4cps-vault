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

<!-- SECTION CCC:
     C1 – Opening paragraph: why the ML community needed an "undo" mechanism;
          regulatory pressure (GDPR Art. 17) and the impracticality of full retraining
     C2 – Motivations, definitions, taxonomy (§2.1–§2.3)
     C3 – Closing paragraph: current approaches are designed for centralised,
          static models — this creates a gap for distributed, resource-constrained IoT -->

Machine learning models do not simply consume training data — they absorb it. The iterative optimization process of gradient descent encodes statistical traces of individual data points into model parameters, making it fundamentally difficult to remove a data point's influence after training [[11]]. Deleting the original data from storage does not undo this encoding: the model retains learned patterns that can, under adversarial probing, reveal information about data it was trained on. The most straightforward remedy — retraining the model from scratch on the reduced dataset — becomes computationally prohibitive as model sizes and training corpora grow, often requiring days of GPU time for a single retraining cycle [[12]]. Machine unlearning has therefore emerged as a dedicated research area focused on selectively removing the influence of specific training samples from a deployed model without incurring the full cost of retraining.

### 2.1 Motivations for Machine Unlearning

The motivations for machine unlearning span legal, security, and fairness dimensions. On the regulatory front, the General Data Protection Regulation (GDPR) enshrines the "right to erasure" in Article 17, granting data subjects the right to request deletion of their personal data and, by extension, of any derived representations [[13]]. The California Consumer Privacy Act (CCPA) establishes analogous rights under U.S. law, while sector-specific regulations such as HIPAA impose additional constraints on health-related data [[14]]. In multi-occupant environments such as intelligent buildings, consent revocations may occur frequently and unpredictably — for example, when a tenant vacates a unit or withdraws consent for occupancy monitoring — creating a continuous stream of legally binding deletion obligations [[15]].

Beyond regulatory compliance, security concerns provide an independent motivation for unlearning. Membership inference attacks have demonstrated that an adversary can determine, with non-trivial accuracy, whether a specific data point was part of a model's training set [[16]]. Model inversion attacks go further, reconstructing approximations of training samples from model outputs alone [[17]]. These attack vectors are not merely theoretical: Shokri et al. [[16]] showed that overfitted models are particularly vulnerable, and subsequent work has confirmed that even well-regularized models leak information through prediction confidence scores [[18]]. In IoT settings where models process sensitive behavioral data — movement patterns, energy usage profiles, biometric signals — such leakage poses concrete risks to occupant privacy.

A third motivation arises from the need to correct models that have absorbed biased, poisoned, or otherwise erroneous data. Data poisoning attacks can inject adversarial samples during training to manipulate model behavior at inference time [[19]]. When such contamination is detected post-deployment, the affected model must be cleansed of the poisoned influence without discarding the legitimate knowledge it has acquired. Similarly, if a training dataset is found to contain systematic biases — for instance, occupancy models trained predominantly on data from one demographic group — unlearning provides a mechanism to selectively remove the biased influence and retrain on a corrected subset [[20]].

Taken together, these three drivers — regulatory mandates that create legal obligations, demonstrated privacy attacks that reveal technical vulnerabilities, and data quality concerns that demand corrective action — establish machine unlearning not as a convenience but as a necessary capability for any system that trains on personal data. The following subsections formalize what unlearning means (§2.2) and how existing methods attempt to achieve it (§2.3).

### 2.2 Definition and Formal Principles

<!-- PARAGRAPH CCC:
     C1 – informal intuition: a model after unlearning should behave
          as if the forgotten data was never seen
     C2 – formal definitions: certified removal [cite], approximate
          unlearning [cite], differential-privacy framing [cite]
     C3 – the diversity of competing definitions reflects the absence
          of a single accepted standard — itself an open problem -->

The intuitive goal of machine unlearning is deceptively simple: after processing a deletion request for data point $z$, the resulting model should behave as if $z$ had never been included in the training set. Formalizing this intuition, however, has produced several competing definitions, each encoding different trade-offs between guarantee strength and computational feasibility.

The strongest formalization is **certified removal**, introduced by Guo et al. [[21]]. Given a learning algorithm $A$, a dataset $D$, and a data point $z \in D$, an unlearning mechanism $U$ achieves certified removal if the distribution of $U(A(D), z)$ is identical to the distribution of $A(D \setminus \{z\})$. In other words, the unlearned model is statistically indistinguishable from one that was retrained from scratch on the reduced dataset. This definition provides the strongest guarantee — an adversary with full access to the model parameters cannot determine whether $z$ was unlearned or never seen — but achieving it typically requires specially structured training procedures, such as the SISA framework [[22]], which partitions the dataset into disjoint shards and trains independent sub-models that can be individually retrained.

Recognizing that certified removal is computationally prohibitive for large-scale models, **approximate unlearning** relaxes the distributional identity requirement to a bounded divergence. Golatkar et al. [[23]] define approximate unlearning by requiring that the parameter distribution of the unlearned model lies within an $\epsilon$-ball of the retrained distribution, typically measured by KL divergence or total variation distance. Neel et al. [[24]] further formalize this through the lens of algorithmic stability, establishing that learning algorithms with bounded sensitivity to individual data points admit efficient approximate unlearning procedures. The key advantage is practical: approximate methods — including gradient-based approaches, influence function corrections, and Newton-step updates — can process deletion requests in time sublinear to the training cost. The disadvantage is that the residual $\epsilon$ error means some statistical trace of the deleted data may persist, and quantifying this residual precisely remains an open problem [[25]].

A third formalization connects unlearning to the established framework of **differential privacy (DP)**. Ginart et al. [[26]] frame the unlearning requirement as an $(\epsilon, \delta)$-indistinguishability condition: for any output set $S$, the probability that the unlearned model falls in $S$ must satisfy $\Pr[U(A(D), z) \in S] \leq e^{\epsilon} \cdot \Pr[A(D \setminus \{z\}) \in S] + \delta$. This definition directly mirrors the DP guarantee and allows unlearning methods to inherit the composability and post-processing properties of the DP framework [[27]]. Sekhari et al. [[28]] build on this connection to derive theoretical lower bounds on the number of samples that can be deleted before a model must be fully retrained, showing that the deletion capacity depends on the model class complexity and the desired privacy level. The DP framing provides formal privacy semantics and enables integration with existing privacy-preserving pipelines, but it inherits the fundamental utility–privacy trade-off: tighter $\epsilon$ values yield stronger forgetting guarantees at the cost of increased model degradation.

The coexistence of these three definitions — each with different strength, cost, and verifiability profiles — reflects a field that has not yet converged on a single accepted standard. This definitional fragmentation is not merely a theoretical concern: it complicates the evaluation and comparison of unlearning methods (§4.4) and makes it difficult for practitioners to determine whether a given method satisfies regulatory requirements such as GDPR Article 17, which does not specify a formal threshold for "erasure" [[29]]. Resolving this definitional ambiguity remains an open problem that directly affects deployment in privacy-critical settings such as intelligent buildings.

### 2.3 Taxonomy of Unlearning Approaches

<!-- PARAGRAPH CCC:
     C1 – two high-level families: exact vs. approximate unlearning
     C2 – exact: SISA training [cite], data sharding; approximate:
          gradient-based [cite], influence functions [cite],
          model editing [cite], knowledge distillation [cite]
     C3 – exact methods offer strong guarantees but are computationally
          expensive; approximate methods are practical but hard to verify —
          a trade-off especially acute in IoT settings (§4.2) -->

Existing machine unlearning methods divide into two broad families — **exact** and **approximate** — distinguished by the strength of the guarantee they provide relative to the definitions formalized in §2.2. Exact methods produce a model whose output distribution is provably identical to one retrained from scratch; approximate methods trade guarantee strength for computational efficiency, producing a model that is close to, but not identical with, the retrained baseline. Table 1 summarizes the key methods in each family along their guarantee type, computational cost, and assumptions.

#### 2.3.1 Exact Unlearning

Exact unlearning methods achieve certified removal by structuring the training process so that deletion requests can be satisfied through partial retraining rather than full retraining. The foundational approach is **SISA (Sharded, Isolated, Sliced, and Aggregated) training**, proposed by Bourtoule et al. [[22]]. SISA partitions the training dataset into $k$ disjoint shards, trains an independent sub-model on each shard, and aggregates their predictions at inference time. When a deletion request targets data point $z$, only the sub-model whose shard contains $z$ requires retraining — reducing the computational cost by a factor of approximately $k$. Within each shard, SISA further organizes training into incremental slices with saved checkpoints, enabling retraining to resume from the most recent unaffected checkpoint rather than from initialization.

While SISA provides the strongest unlearning guarantee, its applicability depends on assumptions that may not hold in all settings. Sharding reduces each sub-model's effective training set, which can degrade accuracy — particularly for complex tasks or small datasets [[30]]. The aggregation mechanism introduces inference latency proportional to the number of shards, and the storage overhead of maintaining per-shard checkpoints scales linearly with both $k$ and the number of slices. Extensions to SISA have addressed some of these limitations: Yan et al. [[31]] propose adaptive sharding strategies that account for data heterogeneity, and Chen et al. [[32]] introduce graph-structured partitioning for relational data. Nevertheless, exact methods share a common limitation: they require the training procedure to be designed for unlearning from the outset, making them inapplicable to already-deployed models trained without such provisions.

#### 2.3.2 Approximate Unlearning

Approximate unlearning methods operate on already-trained models, modifying their parameters post-hoc to reduce the influence of targeted data points. These methods do not guarantee distributional identity with the retrained model but aim to minimize the residual influence to within a tolerable bound. Four principal techniques have emerged.

**Gradient-based methods** apply corrective updates to the model parameters using gradient information computed on the data to be forgotten. Golatkar et al. [[23]] use the Fisher information matrix to compute a Newton step that approximately inverts the effect of the targeted data on the model parameters. Graves et al. [[33]] propose "amnesiac unlearning," which stores the per-sample gradient updates during training and subtracts them at deletion time. These methods are computationally efficient — typically requiring a single pass over the forget set — but their accuracy depends on the convexity of the loss landscape, and they degrade for highly non-convex models such as deep neural networks.

**Influence function methods** estimate the effect of removing a data point on model parameters without explicit retraining. Originating from robust statistics [[34]], influence functions compute the change in model parameters that would result from infinitesimally up-weighting or down-weighting a training sample. Koh and Liang [[35]] adapted this technique to deep learning, enabling approximate leave-one-out retraining at the cost of a single Hessian-vector product computation. However, influence functions rely on a second-order Taylor approximation that becomes unreliable for large parameter perturbations — such as those caused by removing an entire user's data rather than a single sample — and computing the inverse Hessian remains expensive for large models [[36]].

**Model editing methods** directly modify specific parameters or representations associated with the targeted data. Becker and Liebig [[37]] identify neurons most responsive to the forget set through activation analysis and selectively prune or reinitialize them. Jang et al. [[38]] propose "knowledge unlearning" through gradient ascent on the forget set, effectively maximizing the loss on the data to be removed. These methods are fast and require no access to the retained training data, but they risk degrading model performance on unrelated tasks — a phenomenon known as catastrophic forgetting of retained knowledge — and provide no formal bound on residual data influence.

**Knowledge distillation methods** train a new "student" model to replicate the behavior of the original "teacher" model on all data except the forget set. Chundawat et al. [[39]] propose a competent-incompetent teacher framework where the student simultaneously learns to match the teacher's outputs on retained data and to match a randomly initialized model's outputs on the forget set. This approach naturally preserves utility on retained data while degrading performance on forgotten data, but it requires access to a representative retained dataset and incurs the full cost of training a new model — approaching the cost of retraining from scratch for large forget sets.

#### 2.3.3 Comparison and Trade-offs

The choice between exact and approximate unlearning involves a three-way trade-off among guarantee strength, computational cost, and deployment flexibility. Exact methods provide certified removal but require forward-compatible training design, substantial storage for checkpoints, and per-shard retraining that scales with deletion frequency. Approximate methods can be applied to existing models without architectural changes, handle deletion requests in sublinear time, but offer weaker and harder-to-verify guarantees. Table 1 summarizes this landscape.

| Method Family | Representative Work | Guarantee | Compute Cost | Needs Training Redesign | Verification |
|---|---|---|---|---|---|
| SISA / sharding | Bourtoule et al. [[22]] | Certified | $O(n/k)$ retrain | Yes | By construction |
| Gradient-based | Golatkar et al. [[23]], Graves et al. [[33]] | Approximate ($\epsilon$-bounded) | $O(|D_f|)$ gradient steps | No | Empirical (MIA) |
| Influence functions | Koh & Liang [[35]] | Approximate (first-order) | $O(np)$ Hessian-vector | No | Empirical (MIA) |
| Model editing | Jang et al. [[38]], Becker & Liebig [[37]] | Heuristic | $O(|D_f|)$ gradient steps | No | Empirical (MIA, activation) |
| Knowledge distillation | Chundawat et al. [[39]] | Approximate | $O(n)$ distillation | No | Empirical (MIA) |

*Table 1: Taxonomy of machine unlearning approaches. $n$ = training set size, $k$ = number of shards, $|D_f|$ = forget set size, $p$ = number of parameters. MIA = membership inference attack.*

This trade-off becomes especially acute in resource-constrained environments. Exact methods demand storage and compute budgets that edge devices cannot provide; approximate methods are lightweight but lack the verifiable guarantees that regulators may require. This tension — between what is provable and what is deployable — runs through the remainder of this survey and motivates the domain-specific analysis in §4.2.

<!-- SECTION CLOSE (C3): -->

The methods surveyed in this section have been developed and validated primarily in centralized, homogeneous settings: single models trained on static datasets hosted on powerful hardware. The definitions of §2.2 and the taxonomy of §2.3 provide the theoretical and methodological foundation against which any domain-specific adaptation must be evaluated. However, intelligent building IoT systems present a fundamentally different operational context — one characterized by distributed model state, heterogeneous hardware, continuous data streams, and frequent consent revocations. Section 3 establishes the concrete properties of these systems before §4 examines what happens when unlearning methods from this section encounter real IB-IoT constraints.

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

- Intelligent buildings operate as socio-technical systems where continuous ML inference over occupant-sensitive streams underpins routine operation [[40]].
- A standing tension defines the setting: fine-grained sensing enables HVAC, energy, and comfort optimisation, while simultaneously producing detailed behavioural profiles of the occupants generating that data [[41]].
- Occupants may revoke consent at any point — tenancy changes, policy updates, or individual objection — placing deletion obligations on a system architected for retention, not erasure [[15]].
- The following subsections decompose this setting along three axes: the layered architecture that distributes model state (§3.1), the data and privacy regime that governs it (§3.2), and the ML workloads that consume it (§3.3). Together they define the constraint surface §4 evaluates existing unlearning methods against.

### 3.1 IoT Architectures in Intelligent Buildings

<!-- PARAGRAPH CCC:
     C1 – layered architecture: sensors/actuators → edge gateways → cloud/fog
     C2 – protocols (MQTT, Zigbee, BACnet), data volumes, heterogeneity,
          latency constraints; typical ML deployment points at each tier
     C3 – because model state is replicated across tiers, a single
          deletion request may require coordinated updates across
          multiple devices — a challenge absent in centralised settings -->

**C1 — Layered architecture.** IB-IoT deployments converge on a three-tier topology [[42]]:
- **Perception tier** — occupancy sensors, PIR, CO₂, smart meters, cameras, wearables, and legacy BMS field devices. Hosted on resource-tight MCUs with intermittent connectivity and minimal local storage.
- **Edge/gateway tier** — Raspberry-Pi-class to industrial gateways performing aggregation, protocol translation, and local inference; commonly the site of lightweight ML (TinyML, quantised models) [[43]].
- **Cloud/backend tier** — training, long-term storage, cross-building analytics, and operator dashboards; resource-rich but latency- and bandwidth-bound, which pushes inference work downward.

**C2 — Protocols, volumes, heterogeneity, ML placement.**
- Protocol mix spans **MQTT** (lightweight pub/sub), **CoAP** (constrained REST), **Zigbee / Z-Wave** (low-power mesh), legacy BMS stacks (**BACnet, KNX, Modbus**), and **LoRaWAN** for long-range low-rate links [[44], [45]].
- Data volume: per-building sensor streams aggregate from sub-second sampling to minute-resolution time series, reaching TB-scale per year across building portfolios [[46]].
- Heterogeneity is intrinsic — device generations, vendor silos, and firmware drift coexist on the same network, precluding a uniform model substrate [[47]].
- Latency budget: comfort and safety loops (HVAC actuation, occupancy-driven lighting, alarms) demand sub-second inference, forcing model replicas to live at the edge rather than only in the cloud [[48]].
- Typical ML placement per tier:
    - *Cloud*: model training, periodic federated aggregation, anomaly model fitting.
    - *Edge*: live inference, online fine-tuning, federated client role.
    - *Perception*: rare deployments — keyword spotting, threshold classifiers, heavily quantised models.

**C3 — Implication for unlearning.**
- Model state is **replicated across tiers**: the cloud holds the trained model, the edge runs a distilled or quantised copy, and a sensor may carry a further-reduced threshold variant.
- A single deletion request therefore demands **coordinated updates across every tier holding a derived artifact** — a coordination problem absent from the centralised settings assumed in §2.
- Quantisation and distillation sever the **provenance link** between individual training samples and edge weights; even certified-removal procedures such as SISA [[22]] cannot retroactively reach an edge replica produced by a lossy transform [[49]].
- Intermittent connectivity blocks synchronous propagation of revocations, so the system must tolerate **partial-unlearn states** in which some tiers have forgotten and others have not — a failure mode no existing unlearning definition (§2.2) explicitly handles.

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
