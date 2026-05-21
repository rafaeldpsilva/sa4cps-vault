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

Intelligent buildings operate as socio-technical systems in which continuous machine-learning inference over occupant-sensitive streams underpins routine operation [[40]]. HVAC control, lighting scheduling, occupancy-driven ventilation, and security monitoring all depend on models that ingest fine-grained sensor data in real time, and the value of these services scales with the granularity at which occupants are observed. The same granularity, however, produces a detailed behavioural record of the people whose activities generated it — a tension between utility and privacy that is intrinsic to the deployment context rather than an artefact of any particular system design [[41]]. Compounding this tension, occupants may revoke consent at any point in the building's operational lifetime — when tenants vacate a unit, when policies are revised, or when individuals object to specific processing — placing deletion obligations on infrastructure that was architected for retention, replication, and continuous training rather than for erasure [[15]]. The following subsections decompose this setting along three axes: the layered architecture that distributes model state (§3.1), the data and privacy regime that governs its collection and lifecycle (§3.2), and the machine-learning workloads that consume it (§3.3). Together these axes define the constraint surface against which §4 evaluates existing unlearning methods.

### 3.1 IoT Architectures in Intelligent Buildings

<!-- PARAGRAPH CCC:
     C1 – layered architecture: sensors/actuators → edge gateways → cloud/fog
     C2 – protocols (MQTT, Zigbee, BACnet), data volumes, heterogeneity,
          latency constraints; typical ML deployment points at each tier
     C3 – because model state is replicated across tiers, a single
          deletion request may require coordinated updates across
          multiple devices — a challenge absent in centralised settings -->

IB-IoT deployments converge on a three-tier topology that organises devices by their distance from the physical environment they observe [[42]]. The **perception tier** comprises the sensors and actuators that interface directly with the building: occupancy detectors, passive-infrared (PIR) sensors, CO₂ and air-quality probes, smart meters, cameras, wearables, and legacy building-management-system (BMS) field devices. These are hosted on resource-tight microcontrollers with limited local storage, intermittent connectivity, and energy budgets that preclude all but the simplest local processing. Above them sits the **edge or gateway tier**, populated by Raspberry-Pi-class single-board computers through to rack-mounted industrial gateways, which aggregate upstream traffic, translate between protocols, and increasingly host lightweight machine-learning workloads under the TinyML and quantised-model paradigms [[43]]. The **cloud or backend tier** — typically a centralised data centre or a private on-premises cluster — concentrates the resource-intensive operations: model training, long-term storage, cross-building analytics, and operator dashboards. Although the cloud is resource-rich, its latency and bandwidth costs make it unsuitable for closed-loop control, which pushes inference responsibilities progressively downward toward the edge and, where feasible, the perception tier itself.

The communication fabric tying these tiers together is markedly heterogeneous. Perception-tier devices typically expose data over low-power radio standards such as Zigbee or Z-Wave, or over legacy BMS protocols including BACnet, KNX, and Modbus that pre-date the IP-based IoT stack [[44]]. Edge gateways translate these dialects into IP-friendly protocols such as MQTT for publish–subscribe telemetry and CoAP for constrained REST interactions, while long-range deployments may rely on LoRaWAN for low-rate links spanning entire campuses [[45]]. The volume of data flowing through this fabric is substantial: per-building sensor streams sampled at sub-second rates routinely aggregate to minute-resolution time series totalling terabytes per year across portfolio-scale deployments [[46]]. Heterogeneity is intrinsic rather than incidental — device generations, vendor silos, and asynchronous firmware drift coexist on the same network — and it precludes a uniform model substrate across the installed base [[47]]. Latency requirements further constrain placement: comfort and safety loops such as HVAC actuation, occupancy-driven lighting, and intrusion alarms demand sub-second inference, forcing model replicas to live at the edge rather than depending on a round trip to the cloud [[48]]. The resulting division of labour is consistent across surveyed deployments: the cloud trains models, performs periodic federated aggregation, and fits anomaly detectors; the edge runs live inference, performs online fine-tuning, and acts as the federated client; and the perception tier, where it carries any model at all, runs heavily quantised classifiers, keyword-spotting kernels, or simple threshold logic.

This architecture has structural consequences for unlearning. Model state is **replicated across tiers** — a trained reference in the cloud, a distilled or quantised derivative at the edge, and possibly a threshold variant at the perception tier — so a single deletion request must propagate to every tier holding a derived copy, requiring coordination that centralised methods do not provide. The lossy transforms producing those replicas also sever the **provenance link** between training samples and deployed weights, leaving certified-removal procedures such as SISA [[22]] unable to retroactively reach edge derivatives [[49]]. Intermittent connectivity then admits **partial-unlearn states** in which some tiers have forgotten while others have not — a failure mode no unlearning definition in §2.2 accommodates. These three properties — replicated state, broken provenance, and asynchronous propagation — recur as structural constraints in §4.2.

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

IB-IoT systems generate four categories of sensitive data. **Occupancy traces** — presence flags, room-level localisation, dwell time, and movement paths derived from PIR, BLE, Wi-Fi probes, or camera analytics — expose routines, social ties, and work patterns [[50]]. **Energy and consumption profiles** captured by per-circuit or per-appliance smart meters are equally revealing: NILM techniques disaggregate them into device-level usage and infer activities such as cooking, sleeping, or showering [[51]]. **Environmental and biometric signals** — CO₂, temperature, and humidity as proxies for occupant count, alongside wearable telemetry and biometric access control — sit between ambient sensing and direct identification [[52]]. **Derived inferences** such as comfort preferences, schedules, and health proxies are often more sensitive than the raw inputs because they surface latent attributes the occupant never disclosed [[53]]. All four qualify as personal data under GDPR once tied to an identifiable occupant, and the identifiability threshold is low — a device MAC, a lease record, or a behavioural fingerprint suffices [[13]].

The regulatory regime has three load-bearing components. **GDPR Art. 5** establishes data minimisation, purpose limitation, and storage limitation; **Art. 17** codifies the right to erasure; **Art. 25** imposes data protection by design [[13]]. The **ePrivacy Directive** governs electronic communications metadata, directly relevant to occupancy data carried over building networks [[54]]. Standard data-minimisation practices — edge aggregation, differential-privacy noise, bounded retention — reduce raw exposure but leave statistical traces in already-trained models untouched [[55]]. Consent in multi-tenant buildings must be granted per-tenant and per-purpose, updated on policy revision, and revoked on move-out or objection. Shared spaces create **overlapping consent domains** where one occupant's revocation cannot unmix their contribution from co-occupant data captured by the same sensor [[56]]. **Data-controller ambiguity** compounds this: owner, facility manager, vendor cl oud, and tenant may each be controller for different streams, leaving unlearning responsibility undefined [[57]].

The consequence is high-throughput, multi-source revocations rather than the rare deletions §2 assumes. Tenant turnover, short-term occupancy, and visitors make revocations a continuous arrival process, demanding throughput orders of magnitude above centralised baselines. Requests routinely span multiple subjects' entangled records in shared spaces, so the unit of unlearning is rarely a clean single-sample slice. Derived inferences must be **transitively unlearned** — erasing raw occupancy does not remove a downstream preference model trained on it — and the dependency graph linking raw streams to derived models is rarely tracked end-to-end [[58]]. High arrival rate, multi-subject entanglement, and transitive scope set the requirements §4 measures existing methods against.

### 3.3 Role of Machine Learning in Intelligent Building Systems

<!-- PARAGRAPH CCC:
     C1 – ML tasks in IBs: occupancy prediction, HVAC optimisation,
          anomaly detection, user preference modelling
     C2 – model types deployed (time-series, GNNs, federated models)
          and training regimes (online, periodic batch, federated)
     C3 – online and federated regimes mean the "clean snapshot to
          retrain from" is ill-defined — the core assumption of most
          exact unlearning methods breaks down here -->

Machine learning underpins most operational decisions in IB systems. **Occupancy prediction and detection** drives HVAC scheduling and lighting control via time-series classifiers over PIR, CO₂, and BLE streams [[59]]. **HVAC setpoint optimisation** uses regression and reinforcement learning to balance comfort against energy cost over weather, occupancy, and price [[60]]. **Anomaly and fault detection** flags sensor drift, equipment failure, and intrusion through unsupervised or semi-supervised models [[61]]. **User-preference modelling** encodes per-occupant comfort profiles, often as heterogeneous GNNs over user–device–space graphs [[62]]. **NILM** and **load forecasting** apply sequence models to smart-meter streams, while **biometric access control** deploys face, gait, or fingerprint classifiers at entry points [[63], [64]]. Personal data thus flows through many independently trained models, multiplying the surface an unlearning obligation must cover.

Model families and training regimes diverge sharply. Classical time-series methods (ARIMA, state-space) coexist with deep sequence architectures (LSTM, Transformer), GNNs for user-preference and digital-twin tasks, and RL policies for closed-loop control [[65]]. Training regimes split along a sharper axis: **online/streaming** updates weights continuously from live telemetry [[66]]; **periodic batch** retrains nightly or weekly on accumulated windows; **federated** training keeps raw data on the edge and shares only gradients with a coordinator [[67]]; **continual** learning expands the model as new occupants, sensors, or spaces appear, with no clean initial state [[68]]. These regimes coexist within a single deployment, mirroring the §3.1 tier split — heavy training in the cloud, fine-tuning at the edge, quantised inference at the perception tier.

The consequence is that no clean snapshot exists from which to retrain. Online and continual regimes produce a non-stationary parameter trajectory in which gradient updates from sample $z$ are interleaved with millions of others — "the model before $z$ was seen" is not a well-defined state [[69]]. Federated training removes the central dataset SISA presupposes: the coordinator never sees raw samples and cannot retrain a shard on $D \setminus \{z\}$ [[70]]. RL policies are harder still — $z$'s influence propagates through state–action visitations, undermining the linearisation behind influence-function methods [[71]]. GNN-based user models entangle each user's data with neighbours via message passing, so node removal demands subgraph re-propagation rather than local deletion [[72]]. The foundational §2 assumption — a clean baseline to compare against — fails across every dominant IB-IoT regime; §4 examines the partial workarounds proposed and where each breaks down.

<!-- SECTION CLOSE (C3):
     The distinctive properties of IB-IoT — distributed state,
     resource constraints, online training, high deletion frequency —
     mean that methods from §2 cannot be applied directly.
     §4 examines what has actually been attempted at this intersection. -->

---

<!-- ══════════════════════════════════════════════════════
     WHOLE-PAPER C2 – CONTENT  (§4)
     Goal: report WHAT has been done; ground in concrete scenarios
     ══════════════════════════════════════════════════════ -->

## 4. Machine Unlearning in IoT and Intelligent Buildings

<!-- SECTION CCC:
     C1 – Opening paragraph: the intersection of MU and IoT/IBs is nascent;
          most work adapts centralised methods with varying success.
          Case-grounded: each sub-claim illustrated with an operational
          IB scenario rather than a standalone case-study section.
     C2 – research landscape, constraint dimensions, stack-tier coverage
          with embedded scenarios, evaluation gap (§4.1–§4.4)
     C3 – Closing paragraph: existing approaches address isolated sub-
          problems; no integrated framework covers the full IB stack —
          motivating the challenges + directions in §5 -->

<!-- SECTION OPENING (C1):
     Characterise the maturity of the field: volume of publications,
     position relative to adjacent areas (federated learning, differential
     privacy), and which sub-problems have attracted the most attention. -->

<!-- RULE 7 — SUBSECTION HEADERS ARE DECLARATIVE CLAIMS.
     Each header below states the logical conclusion of that subsection
     so that the reader can fact-check it. After writing, these headers
     become the logical spine of the section argument. -->

**§4 opener — maturity of the field.**
- Intersection of MU and IoT/IBs is young (≈ 2021–2026); volume rising but small relative to centralised MU literature [[73]].
- Most contributions adapt centralised methods (SISA, gradient-based) to FL or edge — IB-specific constraints rarely modelled jointly.
- Adjacent fields drive borrowing: federated learning (gradient correction, client dropout), differential privacy (DP-SGD), edge ML (TinyML, quantisation) [[74]].
- Sub-problems with most attention: federated unlearning + edge inference. Underserved: verification, multi-tenant consent, transitive unlearning of derived models.
- Forward pointer: §4.1 scope, §4.2 constraints, §4.3 stack-tier coverage with vignettes, §4.4 benchmark gap.

### 4.1 Research at the Intersection of Machine Unlearning and IB-IoT Remains Nascent and Fragmented

<!-- PARAGRAPH CCC:
     C1 – survey scope: databases searched, time period, inclusion criteria
     C2 – quantitative overview (paper count, venue distribution, topic
          clusters); most work targets general IoT or FL settings —
          few papers explicitly model IB constraints
     C3 – fragmentation means findings are hard to compare and
          no consensus method has emerged for this domain -->

**C1 — survey scope.**
- Databases: IEEE Xplore, ACM DL, Scopus, Web of Science, arXiv (cs.LG, cs.CR, cs.DC).
- Time window: 2015 (Cao & Yang, original "machine unlearning" paper [[75]]) → 2026.
- Inclusion criteria: explicit unlearning mechanism **and** IoT / edge / federated / IB context. Pure FL papers without an unlearning hook excluded.
- Search strings: `("machine unlearning" OR "data deletion" OR "right to be forgotten") AND ("IoT" OR "edge" OR "federated" OR "smart building" OR "intelligent building")`.
- Snowballing: backward refs from seed papers (SISA [[22]], FedEraser [[76]]).

**C2 — quantitative overview.**
- ~$N$ papers retained (placeholder pending final count); ≈70% target FL or generic IoT, <15% explicitly model IB constraints.
- Venue spread: ML venues (NeurIPS, ICML), security (CCS, USENIX), IoT systems (SenSys, IoTDI), some domain-specific (BuildSys). No single home venue.
- Topic clusters: federated unlearning (largest), edge / on-device unlearning, verifiable unlearning (TEEs, ZKPs), DP-grounded unlearning.
- IB-specific work concentrated on smart-home + HVAC scenarios; multi-tenant offices nearly absent.

**C3 — consequence.**
- Fragmentation → no shared experimental protocol, no shared dataset, no cross-paper comparability.
- No consensus method for IB-IoT has emerged; the field is pre-paradigmatic in Kuhn's sense.
- Sets up §4.2 (why no method satisfies the constraints) and §4.4 (why benchmarks are missing).

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

**C1 — four constraint dimensions distinguishing IB-IoT.**
- Drawn from the IB-IoT properties in §3 (architecture, data regime, ML regimes).
- Form a four-axis envelope no centralised method was designed to occupy.

**C2 — the four dimensions.**
- **(a) Edge resource limits**: MCU-class RAM (kB–MB), no GPU, energy budget for inference but not retraining → exact methods (SISA) infeasible on-device [[43]].
- **(b) Model heterogeneity across tiers**: cloud reference / edge distilled / sensor quantised replicas with broken provenance link → unlearning must coordinate non-identical artefacts [[49]].
- **(c) Multi-tenancy + overlapping consent**: shared sensors encode multiple data subjects' contributions; deletion request rarely maps to one clean slice [[56]].
- **(d) Real-time availability + federated topology**: closed-loop control cannot tolerate downtime; clients drop in/out; no central dataset for retraining [[67], [70]].

**C3 — combined effect.**
- Each constraint individually challenges one method family; combined, they exclude every surveyed method from full coverage.
- Used as the evaluation rubric in §4.3 (which constraints each method addresses / ignores).

### 4.3 Current Approaches Address Only Isolated Sub-Problems of IB-IoT Unlearning

<!-- PARAGRAPH CCC + EMBEDDED CASE-STUDY VIGNETTES:
     C1 – categorise by where in the IB stack the method operates:
          cloud-side, edge-side, federated
     C2 – for each category: method, assumptions, reported performance,
          and which of the §4.2 constraints it addresses or ignores.
          Each category illustrated by one IB scenario as concrete evidence:
            • Cloud-side  → smart-home occupant move-out deletion
                            (lightweight approximate methods work for
                             single-tenant settings but cannot verify)
            • Edge-side   → energy-management model retraction after
                            biased sensor data is detected
                            (utility degradation dominates; approximate
                             unlearning degrades performance non-uniformly)
            • Federated   → multi-tenant building with per-tenant
                            consent revocation
                            (federated topology amplifies verification
                             difficulty; weakest node is bottleneck)
     C3 – cloud-side methods ignore edge constraints;
          edge-side methods ignore federated coordination;
          federated methods weaken unlearning guarantees —
          no single approach satisfies all four §4.2 constraint dimensions -->

**C1 — categorisation by stack tier.**
- Three categories tracking the §3.1 tier model: cloud-side, edge-side, federated.
- Each tier hosts a different unlearning operating model and addresses a different subset of §4.2 constraints.

**C2a — Cloud-side methods + vignette.**
- Methods: SISA-style sharding [[22]], retrain-on-shard, gradient-based correction on the full model, knowledge distillation [[39]].
- Assumptions: centralised dataset, ample compute, infrequent deletions.
- Addresses §4.2 (c) partially (subject-slice deletion). Ignores (a), (b), (d).
- *Vignette — Smart-home occupant move-out.* Tenant vacates; backend unlearns their data via approximate gradient updates [[33]]. Works in single-tenant deployment but yields no verifiable certificate of erasure; edge replicas on the in-home hub remain unchanged until next sync [[77]].

**C2b — Edge-side methods + vignette.**
- Methods: gradient ascent on forget set [[38]], neuron pruning [[37]], on-device fine-tune with replay buffer.
- Assumptions: local data still available; small model; isolated device.
- Addresses §4.2 (a) and partial (b). Ignores (c) multi-tenant + (d) federated coordination.
- *Vignette — Energy management retraction.* Biased sensor stream detected post-deployment; edge HVAC model patched via local gradient ascent on the affected window [[78]]. Utility drops non-uniformly across occupancy regimes — comfort degrades for occupants whose data was unaffected by the bias [[20]].

**C2c — Federated methods + vignette.**
- Methods: FedEraser [[76]], gradient-rollback aggregation, client-side unlearning with coordinator re-averaging, federated SISA variants [[79]].
- Assumptions: synchronous-enough clients, trusted aggregator, no raw data leaves clients.
- Addresses §4.2 (d). Partial (c). Weakens guarantee strength: unlearning becomes statistical, not certified.
- *Vignette — Multi-tenant building with per-tenant revocation.* Per-edge federated client; revocation triggers rollback of contributions from that client's history [[80]]. Verification difficulty amplified — the weakest / least-attestable node bottlenecks the global guarantee; offline clients leave stale weights in their local model [[81]].

**C3 — coverage gap.**
- Cloud-side: ignores (a) edge + (b) replica heterogeneity.
- Edge-side: ignores (c) multi-tenancy + (d) federation.
- Federated: weakens guarantee strength; ignores (a) deeply.
- No surveyed approach satisfies all four §4.2 dimensions simultaneously.

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

**C1 — heterogeneity of evaluation.**
- Each paper picks its own metrics, datasets, and threat model → no apples-to-apples comparison.
- IB-IoT lacks a canonical dataset analogous to MNIST/CIFAR for centralised MU benchmarks.

**C2 — metrics + datasets catalogue.**
- *Completeness*: membership-inference attack (MIA) accuracy [[16]], activation-distance analysis [[82]], gradient-residual probes [[83]].
- *Utility retention*: post-unlearn accuracy on retained data, downstream task drift, control-loop stability for HVAC.
- *Computational cost*: wall-clock unlearn time, FLOPs, energy (Joules) — last especially relevant for edge.
- *Communication overhead*: bytes exchanged per revocation in federated setting.
- *Datasets used*: CIFAR / MNIST adapted (non-IB), ECO / REDD for energy [[84]], occupancy CSV traces from KTH / Sutton, synthetic FL benchmarks (LEAF) — none jointly cover IB sensor mix + multi-tenancy.
- *Threat models*: rarely specified; honest-but-curious aggregator default; physical-edge-attacker considered in <5% of surveyed work.

**C3 — implication.**
- Claims of "efficient" / "complete" unlearning are not falsifiable across papers.
- Standardisation = prerequisite for production deployment + for regulator-facing audits.
- Direct setup for §5.4 (interoperability + standardisation direction).

<!-- SECTION CLOSE (C3):
     Across the four sub-claims, the dominant pattern is the same:
     approximate methods deploy because exact methods are infeasible
     under IB-IoT constraints, and verification remains the weakest
     link in every category. §5 articulates the structural problems
     this leaves open and the directions that could close them. -->

**§4 close.** Approximate methods deploy because exact methods are infeasible under IB-IoT constraints; verification is the weakest link in every category; no method covers all four §4.2 dimensions. §5 articulates the structural challenges this leaves open and the matched directions that could close them.

---

<!-- ══════════════════════════════════════════════════════
     WHOLE-PAPER C3 – CONCLUSION  (§5–§6)
     Goal: synthesise WHAT IS MISSING and WHERE TO GO
     ══════════════════════════════════════════════════════ -->

## 5. Open Challenges and Research Directions

<!-- SECTION CCC:
     C1 – Opening paragraph: §4 surfaces four structural obstacles that
          prevent responsible IB-IoT deployment; recent advances in
          adjacent fields (FL, TEEs, PETs) open partial pathways.
     C2 – one subsection per challenge; each subsection contains both
          the challenge framing and its proposed research direction
          (§5.1–§5.4)
     C3 – Closing paragraph: the four are interdependent —
          scalability without verification is insufficient.
          Realising the directions requires cross-disciplinary
          collaboration (systems, ML, law, HCI); a community benchmark
          and reference architecture would provide the shared foundation.

  RULE 4 – PARALLELISM:
     Each subsection has the same internal structure:
     **Challenge:** what is broken and why §4 methods do not solve it.
     **Direction:** the proposed pathway, its technical basis, and
                    what is still needed to realise it. -->

**§5 opener.**
- §4 surfaces four interdependent obstacles: scalability, verification, regulation, interoperability.
- Adjacent advances open partial pathways: FL maturity, TEEs (Intel SGX, ARM TrustZone), ZKP toolchains (Halo2, Plonk), TinyML runtimes.
- Each subsection pairs **Challenge** (what is broken) with **Direction** (proposed pathway + technical basis + what is still needed).

### 5.1 Scalability and Efficiency in Large-Scale IoT
<!-- Challenge: edge compute/memory limits + revocation throughput.
     Direction: hardware-accelerated and on-device unlearning
                (TinyML kernels, sparse update primitives, MCU runtimes). -->

**Challenge.**
- Edge devices have MCU-class RAM (kB–MB) and no GPU → SISA / full gradient methods do not fit on-device.
- Revocation throughput is high (§3.2) → unlearn pipeline must run continuously, not as a rare event.
- Cloud-only unlearning leaves edge replicas stale until sync; sync windows can span hours/days.
- Energy budget: training-class workloads exceed harvest rates on battery / PoE-limited devices.

**Direction.**
- **Sparse / structured update primitives**: restrict unlearning to a small fraction of parameters (LoRA-style adapters, slice updates) → fits MCU memory [[85]].
- **TinyML unlearning kernels**: compile unlearning ops to MCU runtimes (TFLM, microTVM) [[86]].
- **Hardware-accelerated paths**: NPU/DSP unlearning primitives; on-die accumulator zeroing for influence-tracked weights [[87]].
- **Two-tier unlearn**: heavy retrain in cloud + lightweight residual patch pushed to edge → bounded edge cost.

**Still needed.**
- Benchmarks for unlearn time / energy on Cortex-M-class targets.
- Formal bounds on residual error when sparse updates replace full retrain.
- Compiler support for unlearn ops in TinyML stacks.

### 5.2 Verification and Formal Guarantees of Unlearning
<!-- Challenge: approximate methods dominate but offer no auditable
                certificate of erasure — regulator-facing gap.
     Direction: verifiable unlearning via PETs — TEEs for trusted
                attestation of the unlearning procedure, ZKPs for
                proof-of-erasure without revealing model internals. -->

**Challenge.**
- Approximate methods dominate (§4.3) but offer no auditable certificate of erasure.
- MIA-based empirical evaluation is regulator-unfriendly: "low attack accuracy" is not a legal proof.
- §2.2 definitional fragmentation (certified / approximate / DP) means no single guarantee is agreed.
- Federated topology amplifies: any node may be malicious / faulty → trust assumption unrealistic.

**Direction.**
- **TEE-attested unlearning**: run unlearn procedure inside Intel SGX / ARM TrustZone / AMD SEV enclave; attestation report = cryptographic evidence that procedure ran on stated inputs [[88]].
- **ZKP proof-of-erasure**: prove (in zero knowledge) that final weights = $U(\theta, z)$ for declared $U$ and $z$, without revealing $\theta$ [[89]].
- **DP composition tracking**: each unlearning event consumes privacy budget → auditable ledger of remaining capacity [[28]].
- **Hybrid**: TEE for runtime attestation + ZKP for post-hoc audit + DP accounting for cumulative guarantee.

**Still needed.**
- ZKP cost reduction for million-parameter models (current proving time prohibitive).
- TEE memory limits incompatible with full-model unlearning → enclave-friendly model partitioning.
- Legal framework mapping "ZKP proof-of-erasure" to GDPR Art. 17 compliance — currently no precedent.

### 5.3 Regulatory and Ethical Considerations
<!-- Challenge: GDPR Art. 17 + controller ambiguity + multi-tenant
                overlapping consent domains have no technical mapping
                in current methods.
     Direction: compliance-by-design unlearning pipelines that bind
                technical erasure certificates to the legal data-subject
                lifecycle (consent, sub-letting, move-out). -->

**Challenge.**
- GDPR Art. 17 requires erasure "without undue delay" — undefined latency target; no technical SLA in current methods.
- **Controller ambiguity** (§3.2): which entity (owner / FM / vendor / tenant) executes the request is legally + technically unclear.
- **Overlapping consent domains** in shared spaces: revocation by one occupant cannot legally cascade to co-occupants' data nor unmix sensor records.
- Transitive scope: derived inferences (preference models, health proxies) inherit deletion obligations but rarely tracked.
- Ethics: model "forgetting" can harm utility for retained users (fairness) — under-explored.

**Direction.**
- **Compliance-by-design pipelines**: data-subject lifecycle (grant → update → revoke) as a first-class state machine wired to unlearn triggers [[90]].
- **Provenance ledgers**: tamper-evident log linking raw streams → models → derived inferences; deletion request walks the graph [[91]].
- **Consent ontology** for IB-IoT: per-modality, per-purpose, per-space consent atoms → machine-readable revocation [[92]].
- **Cross-controller protocols**: standardised inter-controller API for forwarding revocations (owner → vendor cloud → edge gateway).

**Still needed.**
- Legal-technical mapping: which `(metric, threshold)` pair satisfies "erasure" under Art. 17.
- Fairness audits of post-unlearn models.
- Reference consent ontology adopted by IB vendor consortia.

### 5.4 Interoperability and Standardisation
<!-- Challenge: heterogeneous tiers, vendor silos, federated topology
                → no shared substrate for cross-system unlearning.
     Direction: a federated reference architecture and shared benchmark
                that defines APIs, evaluation metrics, and minimum
                interoperability contracts across cloud / edge / device. -->

**Challenge.**
- IB-IoT stacks span vendor silos (Siemens / Honeywell / Schneider / Tridium) with proprietary BMS protocols (§3.1).
- No shared substrate for cross-system unlearning → revocations cannot propagate across vendor boundaries.
- §4.4 benchmark gap: each paper picks own metrics / datasets → no comparability, no certification path.
- Federated topology amplifies: each client may run a different unlearning algorithm with different guarantee.

**Direction.**
- **Federated reference architecture**: open spec defining unlearning APIs at cloud / edge / device interfaces (`POST /unlearn`, status, attestation) [[93]].
- **Shared IB-IoT unlearning benchmark**: canonical dataset (multi-modal sensor + multi-tenant) + metric suite (completeness, utility, energy, comms) + reference threat models — analogous to LEAF [[94]] for FL.
- **Minimum interoperability contracts**: vendor commitments on unlearn latency SLA, attestation format, audit interface.
- **Integration with existing IB stacks**: BACnet / KNX / Haystack tag extensions for consent + unlearn-state fields [[95]].

**Still needed.**
- Community consortium to host benchmark + maintain ground truth.
- Conformance test suite for vendors.
- Bridge to existing FL frameworks (Flower, FedML) so unlearning is not bolted on.

<!-- SECTION CLOSE (C3):
     The four challenge–direction pairs form a coherent research agenda
     that collectively closes the gap between the theoretical guarantees
     of §2 and the operational reality of §3–§4. -->

**§5 close.** Interdependence: scalability without verification = unauditable; verification without standardisation = vendor-local; regulation without scalability = unenforceable. Solving any single pair is insufficient; the four directions must advance jointly. Cross-disciplinary collaboration (systems, ML, law, HCI) + community benchmark + reference architecture = shared foundation.

---

## 6. Conclusion

**C1 — restate the problem.**
- ML models in IBs retain statistical traces of occupant data (§2.1).
- §3 constraints + §4 fragmentation → existing methods insufficient for IB-IoT; regulatory obligation (GDPR Art. 17) currently unmet.

**C2 — what the survey found.**
- Taxonomy of unlearning (§2): exact / approximate, with three competing definitions.
- IB-IoT operational requirements (§3): three-tier architecture, multi-tenant consent regime, multi-regime ML training.
- State of the art (§4): nascent, fragmented, no method covers the four §4.2 constraint dimensions; verification is universally the weakest link.
- Open challenges + matched directions (§5): scalability, verification, regulation, interoperability — interdependent agenda.

**Middle — survey limitations.**
- Coverage window 2015–2026; arXiv inclusion may surface non-peer-reviewed work.
- Search strings biased toward English-language venues; possible miss of EU / Asian regional literature.
- IB-specific deployments rare → many vignettes generalise from FL or generic IoT settings.
- No quantitative meta-analysis (cost / accuracy aggregation) — paper count too small for power.

**C3 — broader significance.**
- Machine unlearning for IB-IoT is critical + underserved: legal obligation + privacy risk + deployment scale.
- Community must produce: shared benchmarks, reference architectures, formal verification frameworks.
- Without these, responsible deployment in occupant-facing buildings remains out of reach.

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
          fragmented state of the art with case-grounded failure modes (§4),
          four interdependent challenges + matched research directions (§5)
     C3 – closing claim: machine unlearning for IB-IoT is a critical,
          underserved area; the community needs shared benchmarks,
          reference architectures, and formal verification frameworks
          before deployment can be responsibly achieved -->
