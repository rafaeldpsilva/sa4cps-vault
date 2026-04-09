## Problem Statement:
The field of artificial intelligence is rapidly transforming various sectors, and its application in intelligent buildings presents a significant opportunity to enhance human-centric adaptation [1], [2]. The core challenge is to create systems that are adaptive to human needs, interactive in a natural way, and ensuring privacy and responsiveness [3].

In user modeling, general solutions focus more on behavioral modeling, using approaches such as deterministic, stochastic, or agent-based [4]. However, for preference modeling, more traditional solutions rely on rule-based methods [5] that while providing many advantages such as explainability, do not capture nuanced variations in human preferences or handle the complexity in multi-occupant scenarios [6]. The emergence of graph-based representations [7], [8], [9], particularly knowledge graphs has provided a more robust method for modeling the connections between users, devices, spaces, and context, when compared with machine learning solutions which typically capture behavioral patterns from sensor data [10].

From an architectural standpoint, the dominant paradigm has been centralized, cloud-based systems [11]. While powerful, this approach introduces problems in latency, reliability, privacy, and security [12], [13]. In response, a shift towards distributed and edge computing has gained momentum [14], [15], [16], aiming to process data closer to its source and, also, agent systems have been explored for decentralized control [17], [18].

Interaction between human and buildings has evolved from simple dashboards to voice-activated commands. While an improvement, these forms of interaction often lack context-awareness, and are largely transactional and reactive [19]. The integration of large language models (LLM) [20], [21], [22] and small language models (SLM) [23], [24] present an opportunity to create fluid interaction and, also, enable proactive assistance. The primary gap is to integrate these language models with real-time and structured system context so they can leverage proactive preference elicitation, personalized system behavior, and handle conflict mediation [25], [26].

In conclusion, while the literature presents advances in user preference modeling, distributed systems, and language models, there is a gap in research that combines these concepts into a unified framework. The work will evolve from the model proposed by the candidate in [27], [28]. This project directly addresses this multi-faceted gap, aiming to deliver a holistic solution that is more adaptive, interactive, and resilient than the current state of the art.

## Research Questions:
**Main RQ.** How can an intelligent building system continuously model and profile its occupants to proactively anticipate and fulfill their individual and collective needs?

**RQ1.** How can a dynamic occupant profile be constructed from behavioral, environmental, and interaction data in an intelligent building environment?

**RQ2.** How can occupant preferences be inferred from a profile across varying contexts and over time?

**RQ3.** How can an intelligent building system proactively engage with its occupants based on the recognition of latent intent from real-time signals and inferred preferences?
	Que decisões podem ser tomadas pelo sistema de forma autónoma? ou que métodos existem que podem ser adotados

**RQ4.** How can an intelligent building system model the preferences and intents of multiple occupants and support preference negotiation in a shared occupancy context?

**RQ5.** How can a community of intelligent buildings share resources and contextual knowledge to improve individual and collective adaptation while preserving occupant privacy?
## Objectives:

**O1.** Characterize existing approaches to occupant modeling in intelligent buildings by conducting a systematic literature review, producing a structured taxonomy of representation methods, identified limitations, and open gaps — completed by the end of Year 1.

**O2.** Design a dynamic occupant profiling mechanism that integrates heterogeneous behavioral, environmental, and interaction data to construct and continuously update individual occupant representations, validated against ground-truth preference data from a controlled building environment — completed by the end of Year 2.

**O3.** Develop a context-aware preference inference model that derives and updates occupant preferences from dynamic profiles across varying environmental conditions and temporal patterns, assessed by precision and recall against elicited user preferences in a real or simulated building scenario — completed by the end of Year 2.

**O4.** Design a proactive engagement mechanism that recognizes latent occupant intent from real-time signals and inferred preferences, and initiates autonomous building adaptations or dialog-based interactions, evaluated by intervention accuracy and occupant satisfaction ratings — completed by the end of Year 3.

**O5.** Develop a multi-occupant preference negotiation model that identifies and resolves conflicts between individual profiles in shared occupancy contexts while preserving individual autonomy, assessed using fairness and satisfaction metrics in multi-user scenarios — completed by the end of Year 3.

**O6.** Evaluate the integrated occupant-centric intelligent building framework in a representative deployment environment, measuring end-to-end performance across profiling accuracy, preference inference, proactive engagement, and conflict resolution against pre-defined KPIs — completed by the end of Year 4.
