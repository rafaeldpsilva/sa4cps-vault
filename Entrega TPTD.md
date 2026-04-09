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

**O1.** Analyze and synthesize existing approaches to occupant modeling, preference inference, and proactive adaptation in intelligent buildings, identifying the representational and architectural gaps that prevent systems from continuously anticipating and fulfilling individual and collective occupant needs — completed by the end of Year 1.

**O2.** Evaluate the suitability of heterogeneous relational representations for dynamic occupant profiling, analyzing their capacity to integrate behavioral, environmental, and interaction data and support downstream preference inference, assessed by expressiveness, coverage, and consistency with elicited occupant states — completed by the end of Year 2.

**O3.** Investigate and assess mechanisms for inferring occupant preferences and contextual intent from dynamic profiles across varying conditions and temporal patterns, analyzing how inference accuracy and adaptation quality evolve as profile richness increases in controlled building scenarios — completed by the end of Year 2.

**O4.** Analyze the conditions under which latent occupant needs can be identified from real-time contextual signals and evaluate a proactive engagement model that autonomously initiates building adaptations and dialog-based interactions, measured by intervention appropriateness and occupant acceptance rates — completed by the end of Year 3.

**O5.** Analyze conflict patterns arising from competing occupant preferences in shared spaces and compare resolution strategies against fairness, satisfaction, and individual autonomy criteria to determine the conditions under which multi-occupant adaptation remains effective — completed by the end of Year 3.

**O6.** Evaluate the integrated framework in a representative intelligent building deployment, assessing the contribution of each component — profiling, inference, proactive engagement, and conflict resolution — to the system's overall capacity to continuously anticipate and fulfill individual and collective occupant needs — completed by the end of Year 4.
