# WP5-E — MCP Context Builder Agent

## Identity
| Field | Value |
|---|---|
| **ID** | WP5-E |
| **Name** | MCP Context Builder Agent |
| **WP** | WP5 |
| **RQ Addressed** | RQ2, RQ3 |
| **Type** | On-demand (called before every SLM invocation) |
| **Status** | Planned |

---

## Purpose
Assembles the real-time Model Context Protocol (MCP) JSON payload used to prime the SLM (WP4-D) before every dialogue session or autonomous agent LLM call. This agent is what prevents hallucinations: by serialising the actual current system state into a structured, schema-validated context, it ensures the SLM can only reference facts that are true right now. It is tightly coupled with WP4-D and must be co-designed with it.

---

## Inputs
| Source | Description |
|---|---|
| WP3-B DT state (REST) | Current zone state: sensor readings, actuator states, occupancy |
| WP4-A preference vector | Current user preference predictions and confidence scores |
| WP4-C interaction style profile | User modality, verbosity preference, trust level (for response style hints) |
| WP4-B conflict graph | Active conflicts (if any) involving the user |
| Safety constraint store | Hard bounds per zone (immutable, from T2.1 NFR1) |
| Resource availability | Current resource levels from WP5-C negotiation state |
| Token budget | Maximum context size for the target SLM model |

---

## Outputs
| Artifact | Description |
|---|---|
| MCP JSON payload | Structured, schema-validated context document passed to WP4-D SLM |
| Truncation log | If token budget exceeded: log of which fields were dropped and why (for debugging hallucination events) |
| Staleness flag | If any DT data is older than a configurable threshold: flagged in payload |

---

## Core Behaviour
1. **State fetch** — calls WP3-B REST API for current zone state; times out at 200 ms (must not block SLM invocation)
2. **Preference assembly** — fetches current preference vector + confidence scores from WP4-A cache (not a fresh inference — uses last computed result)
3. **Conflict inclusion** — if active conflicts exist in WP4-B, includes affected users and their preferences in payload
4. **Safety constraint injection** — appends immutable hard constraints (cannot be overridden by SLM)
5. **Schema validation** — validates assembled payload against MCP JSON schema before dispatch; rejects malformed payloads
6. **Token budget management** — if payload exceeds SLM token limit:
   - Priority 1 (always include): safety constraints, current sensor readings, user preferences
   - Priority 2 (include if space): conflict information, resource availability
   - Priority 3 (drop first): historical context, verbose descriptions
7. **Staleness detection** — if any sensor reading is older than T_stale (configurable, default 30s): marks field as `stale: true` in payload; SLM instructed not to assert facts from stale data
8. **Dispatch** — sends validated payload to WP4-D immediately before SLM session begins

---

## MCP JSON Schema (full)
```json
{
  "$schema": "haaic/mcp/v1",
  "timestamp": "ISO8601",
  "staleness_threshold_s": 30,
  "zone": {
    "id": "string",
    "temperature_c": {"value": "number", "stale": "boolean"},
    "humidity_pct": {"value": "number", "stale": "boolean"},
    "co2_ppm": {"value": "number", "stale": "boolean"},
    "lux": {"value": "number", "stale": "boolean"},
    "occupancy_count": "integer"
  },
  "actuators": [{
    "id": "string",
    "type": "enum[HVAC, lighting, blinds, ventilation]",
    "current_state": "any",
    "controllable_range": {"min": "number", "max": "number"},
    "current_setpoint": "number"
  }],
  "user_preferences": {
    "thermal": {"value": "number", "confidence": "number"},
    "lux": {"value": "number", "confidence": "number"},
    "co2_max": {"value": "number", "confidence": "number"},
    "acoustic": {"value": "string", "confidence": "number"}
  },
  "active_conflicts": [{
    "with_user_anon_id": "string",
    "dimension": "string",
    "their_preference": "number"
  }],
  "safety_constraints": {
    "min_temperature_c": "number",
    "max_temperature_c": "number",
    "min_lux": "number",
    "co2_hard_limit_ppm": "number"
  },
  "resource_availability": {
    "energy_remaining_kwh": "number",
    "grid_constraint_active": "boolean"
  },
  "interaction_style_hints": {
    "verbosity": "enum[low, medium, high]",
    "explanation_depth": "enum[minimal, standard, detailed]"
  }
}
```

---

## Interfaces
| Agent / System | Direction | Description |
|---|---|---|
| WP3-B DT Sync Agent | ← | Real-time zone sensor and actuator state |
| WP4-A Preference Inference | ← | Current preference vector and confidence scores |
| WP4-B Conflict Detection | ← | Active conflict graph |
| WP4-C Relational Psychographics | ← | Interaction style hints |
| WP4-D Preference Elicitation Dialogue | → | Delivers MCP payload immediately before SLM session |
| WP5-A Building Unit Agent | → | Also delivers payload when WP5-A needs an LLM call |

---

## KPIs Contributed
- **M-WP5-03:** Hallucination Rate (≤ 5%) — this agent is the **primary mechanism** for this KPI
- The quality of this agent's output directly determines the quality of WP4-D

---

## Implementation Notes
- This is the **most important dependency of WP4-D** — a poorly built MCP payload produces hallucinations regardless of SLM quality; invest in this agent early
- The MCP schema must be versioned (semantic versioning) and validated at both assembly and consumption — use JSON Schema validation library (jsonschema in Python)
- Token budget management strategy must be documented and tested: what gets dropped under pressure, and does it lead to hallucinations? Test empirically with the target SLM
- Staleness handling: during a network partition, DT state becomes stale — the SLM must be instructed to acknowledge uncertainty rather than assert stale values
- The MCP schema specification itself is a WP5 technical deliverable and a contribution of Paper 4 — design it carefully and document the design rationale
- Anonymous conflict IDs: active conflict section must not reveal the other user's identity — use anonymised IDs derived per-session
