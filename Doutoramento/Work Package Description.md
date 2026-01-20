**WP 1: Literature Review**
WP1 focuses on conducting a systematic and continuous review of the state of the art, especially regarding intelligent buildings, user modelling targeting the preferences with context awareness using Graph Neural Networks (GNNs), LLMs and SLMs regarding Model Context Protocol (MCP) and user interaction. These concepts will be reviewed with a particular focus on edge devices or low powered devices. Additionally, this work package will identify the key challenges and gaps on the current literature.

Tasks: 
- T1.1 – Define search strings, inclusion/exclusion criteria 
- T1.2 – Execute systematic literature review 
 
Outcomes: 
- State of the art review; 
- Systematic literature report, considering (PRISMA);

**WP 2: System Design and Requirements Specification**
WP2 regards the conception and design of the overall system, defining how each component will interact and communicate with each other. The technical aspect of the requirements, use cases, functional specifications, and performance indicators of the project will be defined here. The objective is to design a scalable distributed architecture that can handle real-time interactions and personalization, using microservice oriented principles.

Tasks: 
- T2.1 – Define the functional and non-functional requirements 
- T2.2 – Describe the use cases 
- T2.3 – Identify KPIs and Metrics 
- T2.4 – Design the system architecture 
- T2.5 - Define the framework’s data management plan

Outcomes: 
- Requirements specification document 
- Data Management document 
- System Architecture Design

**WP 3: Distributed Digital Twin Infrastructure** 
WP3 is dedicated to building the core technical infrastructure, including the development of the simulated building environment, and the creation of the agent communication structure and data protocols. Additionally, it focuses on establishing the inter-agent communication protocol, which will support both direct agent-to-agent and remote connectivity, enabling peer-to-peer resource sharing.

Tasks:
- T3.1 – Create a data ingestion pipeline, using Kafka 
- T3.2 – Implement Inter-agent Communication 
- T3.3 – Build the digital twin environment 
- T3.4 – Build an initial basic frontend prototype 
- T3.5 – Develop tools to allow the LLM operation

Outcomes: 
- Data Ingestion Pipeline 
- Digital Twin Software Prototype 
- Real-Time dashboard

**WP 4: User Preference and Context Modeling**
WP4 focuses on creating a dynamic model of users and their environments. Using heterogeneous graphs to understand and predict their needs and using dialogue to gather information. The heterogeneity will allow the model to capture the different relations between the different entities, such as users, preferences and context. The objective is to accurately model often unstated human preferences from indirect and potentially noisy sensor data and to infer latent needs rather than simply reacting to explicit commands. One of the key enablers is the robust modeling of context, given that it has a significant role in the definition of the latent preference.

Tasks: 
- T4.1 – Design the heterogeneous graph schema 
- T4.2 – Define the model’s training methodology, including metrics 
- T4.3 – Conceive the algorithm for conflict identification 
- T4.4 – Implement the training loop, evaluation scripts and conflict identification model 
- T4.5 – Develop the LLM/SML interaction model

Outcomes:
- GNN preference model 
- User interaction component using LLMs and SMLs


**WP 5: Human-centric Agent-based Adaptive Intelligent Communities Framework**
This WP focuses on the agent’s ability to manage the system and acting autonomously. This includes making decisions, negotiating between users, sharing resources with other agents, and dynamically deploying new services as needed. The agent will also interact proactively with the user when taking decisions above its autonomy.

Tasks:
- T5.1 - Create the JSON schema for the MCP that will be used to prime the LLMs
- T5.2 – Develop the agent’s decision logic, considering the constraints of Bounded Autonomy 
- T5.3 – Develop the service discovery and management mechanism 
- T5.4 – Implement peer-to-peer resource sharing 
- T5.5 – Implement the agent’s core control and interaction with the user 

Outcomes: 
- Agent Control Software 
- Dynamic Service Provisioning Framework

**WP6: Test and Validation using realistic scenarios and real pilots**
WP6 ensures the individual components from the previous WPs work together seamlessly, as a single system. Then the proposed solution is tested to prove that the system meets the goals defined in WP2. The use cases will be executed and analyzed to perform iterative refinement of the models and agents.

Tasks:
- T6.1 – Create the deployment configuration for the entire application stack 
- T6.2 – Define the initial state for each use case 
- T6.3 – Develop and validate the measurement procedures for the KPIs and metrics
- T6.4 – Implement the integration configurations and automated deployment scripts 
- T6.5 – Execute the experimental scenarios within the Digital Twin 
- T6.6 - Analyze and evaluate the experiments in the realistic environment

Outcomes:
- Integrated System Prototype 
- Demonstration of each use case 
- Evaluation Report

**WP 7: Dissemination and Communication**
WP7 regards the dissemination and communication of the research activities and results. The goal is to publish a minimum of 10 open-access scientific papers, where at least 4 will be in SCIE-indexed journals and the rest in international conferences. These numbers are considering the historic number of publications of the applicant. In order to ensure broader dissemination of the results and contribute to open science, the datasets, models, and software developed during the PhD. This research could also contribute to R&D projects running in GECAD/ISEP, namely Sa4CPS (ITEA: 22007, Compete2030: FEDER-00368800 – 12737), EnergyP2P (Compete2030: FEDER-00960500–14646), and AdOff (Compete2030:FEDER- 01236200 ITEA: 23048).

Tasks:
- T7.1 - Document with the dissemination plan 
- T7.2 - Annual and final reports for FCT 
- T7.3 - Final Technical Report and Publications 


**Milestones**: 
MS1- Definition of requirements and design of the architecture 
MS2- Distributed Digital Twin infrastructure operational 
MS3 – Preference modeling mechanism 
MS4 – Stable Human-centric Agent-based Adaptive Intelligent Communities Framework