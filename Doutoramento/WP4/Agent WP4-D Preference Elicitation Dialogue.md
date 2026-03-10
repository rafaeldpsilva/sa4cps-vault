# WP4-D — Preference Elicitation Dialogue Agent

## Identity
| Field | Value |
|---|---|
| **ID** | WP4-D |
| **Name** | Preference Elicitation Dialogue Agent |
| **WP** | WP4 / WP5 |
| **RQ Addressed** | RQ2 |
| **Type** | On-demand (user-initiated or agent-triggered) |
| **Status** | Planned |

---

## Purpose
MCP-primed SLM that conducts natural language dialogues with users to elicit, clarify, or update preferences. Triggered when WP4-A has low confidence on a preference dimension, or when WP5-B determines that a decision requires user confirmation. Converts free-text user utterances into structured preference updates committed to the user graph. This agent is the primary answer to RQ2.

---

## Inputs
| Source | Description |
|---|---|
| WP5-E MCP context payload | Real-time structured context: current DT state, active preferences, safety constraints, available actuators |
| Elicitation trigger | From WP4-A (low confidence flag) or WP5-B (escalation event) |
| User utterance | Natural language input from user (text or voice-to-text) |
| WP4-C interaction style profile | User's preferred modality, verbosity, explanation depth |
| Dialogue history | Previous turns in the current session |

---

## Outputs
| Artifact | Description |
|---|---|
| Dialogue turn response | Natural language response to user, grounded in MCP context |
| Structured preference update | Extracted preference: `{dimension, value, confidence, source: "explicit"}` |
| Preference commit signal | Sent to WP4-A when user confirms a preference update |
| Abandonment signal | If user abandons session without committing (tracked for M-WP5-01) |
| Interaction log | Full session log forwarded to WP4-C for psychographic update |

---

## Core Behaviour
1. **MCP priming** — before each session, receives MCP context payload from WP5-E; uses it to ground all responses in actual system state
2. **Trigger handling** — two entry points:
   - *Low confidence:* "I noticed you adjusted the temperature earlier — would you prefer I keep it around 21°C in the morning?"
   - *Escalation:* "I'm not sure how to balance your preference with [other user]'s. Can you help me understand your priority?"
3. **Dialogue management** — tracks dialogue state machine: `{eliciting → confirming → committing | abandoning}`
4. **Slot filling** — extracts structured preference slots from utterances: dimension, value, context qualifier (e.g., "only in the morning")
5. **Hallucination prevention** — all factual claims in responses must be derived from MCP context; no invented sensor values, setpoints, or capabilities
6. **Turn efficiency** — targets ≤ 4 turns to consensus; uses confirmation shortcut on turn 3: "So you want: [summary]. Shall I apply this?"
7. **Style adaptation** — adjusts response verbosity and formality based on WP4-C interaction style profile
8. **Commit + log** — on user confirmation: sends preference update to WP4-A; writes full session to interaction log for WP4-C

---

## Technologies
- Local SLM inference: Raspberry Pi (raspllm) or equivalent edge model (Phi-3, Mistral 7B, or similar)
- MCP (Model Context Protocol) JSON schema for context priming
- Whisper (speech-to-text, optional voice modality)
- FastAPI websocket / REST (dialogue session management)
- Function-calling / structured output (preference slot extraction)

---

## MCP Context Schema (summary)
```json
{
  "zone": {"id": "A3", "temperature": 22.1, "lux": 380, "co2": 720, "occupancy": 2},
  "actuators": [{"id": "hvac_A3", "type": "HVAC", "range": [18, 26], "current": 22}],
  "user_preferences": {"thermal": {"value": 21.5, "confidence": 0.45}},
  "safety_constraints": {"min_temp": 18, "max_temp": 26},
  "active_conflicts": [{"with_user": "B", "dimension": "thermal", "their_preference": 24}],
  "timestamp": "2026-03-09T10:30:00Z"
}
```

---

## Interfaces
| Agent / System | Direction | Description |
|---|---|---|
| WP5-E MCP Context Builder | ← | Receives MCP payload before each session |
| WP4-A Preference Inference Agent | ↔ | Triggered by low confidence; sends confirmed preference updates |
| WP5-B Escalation Agent | ← | Triggered by escalation events needing user input |
| WP4-C Relational Psychographics Agent | ↔ | Receives style profile; sends session interaction log |
| User (via app / voice) | ↔ | Direct dialogue interface |
| WP6-A KPI Monitor | → | Reports M-WP5-01 (TCR), M-WP5-02 (turns), M-WP5-03 (hallucination), M-WP5-04 (satisfaction) |

---

## KPIs Contributed
- **M-WP5-01:** Task Completion Rate (≥ 85%) — **Primary**
- **M-WP5-02:** Dialogue Efficiency (≤ 4 turns) — Secondary
- **M-WP5-03:** Hallucination Rate (≤ 5%) — **Primary**
- **M-WP5-04:** User Satisfaction with Dialogue (≥ 3.8/5) — **Primary**

---

## Implementation Notes
- The SLM must run locally (< 5 s response target on edge hardware) — model selection and quantisation (GGUF 4-bit) need early benchmarking on the Raspberry Pi / raspllm node
- MCP grounding is what separates this from a generic chatbot — the hallucination rate KPI (M-WP5-03) is primarily validated by the quality of the MCP payload (WP5-E dependency)
- Function-calling / structured output mode is essential for reliable slot extraction — generic free-text parsing is too fragile for a production system
- Hallucination detection automation: maintain a state oracle (ground truth DT values) and cross-reference extracted claims — document this in the WP6 evaluation methodology
- This agent is co-authored in Paper 4: "Bridging the Gap: Integrating LLMs with MCP for Grounded Agentic Control"
