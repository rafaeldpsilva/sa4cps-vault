# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

This is an **Obsidian vault** that serves as the research workspace for Rafael Silva's PhD at GECAD/ISEP. It doubles as a task management hub, infrastructure reference, and knowledge base for two main research contexts:

- **Doutoramento/** — PhD research on intelligent buildings, user preference modeling (GNNs), LLMs/SLMs, and agent-based systems
- **Sa4CPS/** — ITEA project (22007) on Situational Awareness for Cyber-Physical Systems

## Vikunja Task Management

The primary tool for task operations is `vikunja_client.py`, a reusable Python REST client.

```python
from vikunja_client import VikunjaClient
client = VikunjaClient(URL, TOKEN)
```

Key projects:
- **Inbox-RDPDS** — `project_id=9` (personal inbox, main entry point)
- **Sa4CPS** — `project_id=12`
- **GECAD F** — `project_id=3` (shared team tasks)
- **Tasks Globais** — `project_id=-8` (aggregated view, read-only)

Credentials and URL are stored in `TasksAPP.md` and in `memory/MEMORY.md`.

### Important API behaviour
- `update_task()` in `vikunja_client.py` only accepts `title`, `description`, `done`, `hex_color`. For other fields (e.g. `due_date`, `bucket_id`), call the API directly via `requests.post(f"{URL}/api/v1/tasks/{id}", json={...})`.
- Sending a partial POST update **resets omitted fields**. Always include `hex_color` alongside `due_date` (and vice versa) to avoid losing data.
- Kanban buckets are scoped to a view: `GET /api/v1/projects/{id}/views` → find the Kanban view → `GET /api/v1/projects/{id}/views/{view_id}/buckets`.
- Subtask relations use: `PUT /api/v1/tasks/{parent_id}/relations` with `{"other_task_id": child_id, "relation_kind": "subtask"}`.

## Sa4CPS Project Structure

Work packages and their Vikunja task IDs:

| WP | Task ID | Deliverables (task IDs) |
|----|---------|------------------------|
| WP1 | 178 | D1.3v2 (192) |
| WP2 | 179 | D2.3 (185) |
| WP3 | 180 | D3.3v1 (186), D3.3v2 (193), D3.4 (198) |
| WP4 | 181 | D4.3v1 (187), D4.3v2 (194), D4.4 (199) |
| WP5 | 182 | D5.3v1 (188), D5.3v2 (195), D5.4 (200) |
| WP6 | 183 | D6.3 (189), D6.4 (190), D6.5 (196), D6.6 (201) |
| WP7 | 184 | D7.3 (191), D7.5 (202) |

WP colors (pastel): WP1 `#a8c8ff`, WP2 `#f9a8c9`, WP3 `#a8d5a2`, WP4 `#ffd599`, WP5 `#d4a8e8`, WP6 `#f5a8a3`, WP7 `#a8e6ef`.

## Infrastructure (SSH Hosts)

Defined in `sshpilot_config.json`:

| Host | Address | Role |
|------|---------|------|
| KubernetesMaster | 192.168.2.91 | K8s master (also runs Vikunja) |
| Docker1 | 192.168.2.68 | Docker node |
| Docker3 | 192.168.2.63 | Docker node |
| rasp / raspllm | Tailscale | Raspberry Pi (edge/LLM) |
| caravel1–7 | 10.8.91.x | Caravel cluster (via VPN) |
| mac | Tailscale | Mac Mini |
| HAGecad | 192.168.3.79 | Home Assistant |

VPN config for GECAD network: `gecadvpn.ovpn`.

## PhD Research Focus (Doutoramento)

Core technical themes across WPs:
- **WP3**: Kafka data ingestion, digital twin, inter-agent communication, frontend prototype
- **WP4**: Heterogeneous GNNs for user preference modeling (Neo4j/Jena), conflict resolution, LLM/SLM interaction
- **WP5**: MCP (Model Context Protocol) JSON schema, bounded autonomy agent, service discovery, P2P resource sharing
- **WP6**: K8s deployment, integration testing, KPI validation, experimental scenarios

Key tech stack references are in `Sa4CPS/Building.md` (building platform WBS) and `Sa4CPS/Community.md` (community platform WBS).
