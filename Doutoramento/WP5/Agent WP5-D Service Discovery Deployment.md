# WP5-D — Service Discovery & Deployment Agent

## Identity
| Field | Value |
|---|---|
| **ID** | WP5-D |
| **Name** | Service Discovery & Deployment Agent |
| **WP** | WP5 |
| **RQ Addressed** | RQ3 |
| **Type** | On-demand |
| **Status** | Planned |

---

## Purpose
When a WP5-A Building Unit Agent identifies a capability gap (a needed function it cannot perform itself), this agent queries a service registry, evaluates candidate microservices, initiates autonomous deployment to the Kubernetes cluster, validates the deployed service, and returns a usable endpoint. This agent is the primary mechanism for RQ3: autonomous identification of latent needs and dynamic service provisioning.

---

## Inputs
| Source | Description |
|---|---|
| WP5-A capability gap request | `{capability_needed, context, priority, constraints}` — e.g., "I need an HVAC tuning optimiser for zone A3" |
| Service registry | Catalogue of available containerised microservices with capability descriptions, resource requirements, health endpoints |
| K8s cluster state | Current resource availability (CPU, RAM) across KubernetesMaster and worker nodes |
| Security policy | Allowed image registries, resource limits, network policies |

---

## Outputs
| Artifact | Description |
|---|---|
| Deployed service endpoint | URL/gRPC address of the successfully deployed and validated service |
| Deployment failure report | If deployment fails: reason, attempted alternatives |
| Health-check confirmation | Service is live and responding correctly before endpoint is returned |
| Lifecycle record | Deployment log: image, version, resource usage, deployment timestamp |
| Teardown signal | When service is no longer needed, agent terminates the deployment |

---

## Core Behaviour
1. **Capability gap parsing** — interprets the gap request; maps it to a canonical capability identifier (e.g., `hvac.optimise`, `occupancy.forecast`, `conflict.resolve`)
2. **Registry query** — queries service registry for microservices matching the capability; retrieves metadata: image, version, resource requirements, trust score
3. **Candidate ranking** — ranks candidates by: capability match score, resource cost, trust/reputation, deployment success history
4. **Resource feasibility check** — queries K8s cluster state to confirm sufficient CPU/RAM for top candidate
5. **Deployment initiation** — applies K8s deployment manifest (generated from service metadata template); sets resource limits, network policy, liveness probe
6. **Health validation** — polls health-check endpoint until service responds correctly or timeout (configurable, default 60s)
7. **Endpoint delivery** — returns validated endpoint to WP5-A; service is now callable
8. **Teardown management** — monitors service usage; terminates deployment when WP5-A signals it is no longer needed

---

## Technologies
- Kubernetes Python client (`kubernetes` library) for deployment management
- Service registry: custom REST API or OCI registry + metadata sidecar
- Docker Hub / private registry (image source)
- Health-check: HTTP GET `/healthz` or gRPC health protocol
- Kafka (lifecycle event logging)

---

## Deployment Manifest Template (simplified)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: "{{ service_id }}-{{ unit_id }}"
spec:
  replicas: 1
  template:
    spec:
      containers:
        - name: "{{ service_id }}"
          image: "{{ image }}:{{ version }}"
          resources:
            limits:
              cpu: "{{ cpu_limit }}"
              memory: "{{ memory_limit }}"
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 10
```

---

## Interfaces
| Agent / System | Direction | Description |
|---|---|---|
| WP5-A Building Unit Agent | ← | Receives capability gap request; → returns service endpoint |
| Kubernetes cluster (KubernetesMaster: 192.168.2.91) | ↔ | Manages deployments, monitors pod health |
| Service registry | ← | Queries available microservices |
| WP6-A KPI Monitor | → | Reports M-WP5-11 (deployment success rate) |

---

## KPIs Contributed
- **M-WP5-11:** Service Discovery & Deployment Success Rate (≥ 85%) — **Primary**

---

## Implementation Notes
- The service registry is a dependency that must be designed and populated before this agent is useful — define the registry schema and seed it with at least 5–10 real microservices (HVAC optimiser, occupancy forecaster, conflict resolver, energy calculator, air quality model) in WP5
- Security is critical: agent must only pull images from trusted registries; implement image signing validation (Cosign or equivalent)
- Resource limits per deployment must be conservative enough to not starve the Building Unit Agent process running on the same node
- The "autonomous identification of latent needs" claim (RQ3) requires the capability gap to be detected by WP5-A without explicit user instruction — document this inference mechanism carefully (it's a research contribution, not just engineering)
- Teardown must be proactive: unused deployed services accumulate resource cost; implement an idle timeout (e.g., teardown after 30 minutes of no calls)
- Test the full deploy-validate-teardown cycle on the Docker1 (192.168.2.68) or Docker3 (192.168.2.63) nodes before caravel cluster testing
