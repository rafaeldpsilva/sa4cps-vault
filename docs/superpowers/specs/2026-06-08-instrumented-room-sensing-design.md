# Instrumented Room — Sensing Foundation (Design)

**Date:** 2026-06-08
**Author:** Rafael Silva
**Status:** Approved design → ready for implementation plan
**Thesis link:** WP3 (data ingestion, digital twin), WP4 (context modeling, GNN substrate)

## Goal

Stand up the **sensing foundation** for a single instrumented room: continuously
perceive room world-state from camera + microphone, store it over time, and
materialize a semantic world-model. This is the data substrate every later
component (JEPA world-model, voice agent, proactive nudges, preference modeling)
feeds on.

Explicitly **deferred** to later cycles (own spec each):
- Idea 1 — LeCun JEPA world-model (will re-process the raw buffer).
- Idea 3 — agent voice communication (**already largely built** in
  `local-voice-ai`; later cycle feeds world-state into its context).
- Idea 5 — manipulative / proactive behavior (needs actuation surface; nudges
  later via Home Assistant).

This spec covers ideas **2 (capture image + sound)**, **6 (map world-state)**,
**4 (knowledge DB over time)**.

## Scope decisions (locked)

| Decision | Choice |
|----------|--------|
| Room | Home / personal room, runs 24/7 |
| Compute | mac-mini (Apple Silicon) — pulls stream, runs all models, hosts DBs |
| Camera | **Reolink E1 Pro/Zoom**, wall-mounted, local **RTSP/ONVIF** (cloud disabled) |
| Capture model | Edge-derive structured state **+** keep rolling raw buffer (10-day ring) for later re-processing |
| Knowledge DB | **Time-series (Timescale) + Graph (Neo4j) split** |
| Bus | Plain local queue / function calls now; Kafka deferred (WP3, multi-room) |
| World-state v1 | **Full schema incl. tidiness** |
| Tidiness method | **Local VLM rubric** (Qwen-VL via reused llama.cpp endpoint) |

## Architecture

```
Reolink E1 ──RTSP(video+audio)──> mac-mini
                                     │
   ┌──────────────────────────────────┼──────────────────────────────────┐
   │ capture-svc      vision-svc        audio-svc        state-fuser       │
   │ (pull RTSP,     (frame →          (clip →          (merge →           │
   │  raw ring buf)   scene state)      sound class)     world-state)      │
   └──────────────────────────────────┼──────────────────────────────────┘
                                       ▼
                           TSDB (Timescale)  ← high-freq state stream
                                       │  (periodic rollup)
                                       ▼
                           Neo4j  ← semantic world-model (WP4 substrate)

   reused, separate process:  local-voice-ai → llama.cpp endpoint (LLAMA_BASE_URL)
                              vision-svc calls it over HTTP for VLM tidiness
   parallel, future:          Home Assistant → light/motion/presence + nudge actuator
```

### Components (each isolated, own interface)

- **capture-svc** — sole owner of the camera. Pulls RTSP, writes rolling raw
  buffer (10-day ring of `.mp4` + `.wav` segments), emits frames + audio clips
  to the local bus. Interface: `subscribe() -> Frame|AudioClip`.
- **vision-svc** — frame → scene state. YOLO (person + objects), frame luminance
  + color-temp, frame-diff motion, local VLM (tidiness rubric) over HTTP to the
  reused llama.cpp endpoint. Models wrapped behind an interface so tests mock
  the model and exercise the glue. Interface: `derive(frame) -> VisionState`.
- **audio-svc** — audio clip → sound classification (YAMNet) + RMS level.
  Interface: `derive(clip) -> AudioState`.
- **state-fuser** — merges vision + audio (+ optional HA sensors later) into one
  timestamped `world-state` record. Writes TSDB every fast tick; materializes
  Neo4j snapshot on rollup. Interface: `fuse(vision, audio) -> WorldState`.
- **TSDB (Timescale)** — raw high-freq state stream.
- **Neo4j** — semantic world-model; the WP4 substrate (later: attach
  preference/persona nodes here).

### Reuse of `local-voice-ai`

`~/Documents/doutoramento/local-voice-ai` is a working local voice stack
(STT Nemotron/Whisper + LLM llama.cpp Qwen3-4B + TTS Kokoro, LiveKit Agents,
async supervisor, env-driven config, Apple-Silicon/Metal).

- **Mirror its patterns:** async process **supervisor** for the sensing children;
  **env-driven config** with "manage-X / point at base URL" philosophy.
- **Reuse its LLM host:** VLM tidiness (Qwen-VL GGUF) served from the same
  llama.cpp infra; vision-svc calls it over HTTP via `LLAMA_BASE_URL`. No new
  inference server.
- **Build sensing as a sibling repo**, not inside the voice container — different
  deps (opencv, vision torch, timescale, neo4j driver). Communicate over HTTP.
- **Idea 3 is already this project.** Later integration cycle: voice agent
  subscribes to world-state / queries the DBs for context. Out of scope here.

## World-state schema (data contract)

One timestamped `world-state` record per fast tick.

| Field | Type | Source | Method |
|-------|------|--------|--------|
| `ts` | datetime | clock | — |
| `occupancy` | int | vision | YOLO person detector |
| `lighting_level` | float 0–1 | vision | frame luminance |
| `light_temp` | enum warm/neutral/cool | vision | frame color temperature |
| `activity` | enum still/moving/absent | vision | frame-diff motion |
| `tidiness` | float 0–1 + label | vision | **local VLM rubric** |
| `objects_present` | list[str] | vision | object detector / VLM tags |
| `sound_class` | enum quiet/speech/music/appliance/other | audio | YAMNet |
| `sound_level` | float dB | audio | RMS |
| `confidence` | per-field float | all | model scores |
| `*_ts` | datetime | fuser | freshness stamp for slow (carried-forward) fields |

## Data flow, cadence, retention

VLM tidiness is slow (~seconds/frame) → **tiered cadence**:

| Tier | Fields | Rate |
|------|--------|------|
| Fast | occupancy, lighting_level, light_temp, activity, sound_class, sound_level | every 2–5 s |
| Slow | tidiness, objects_present (VLM) | every 1–5 min, or on motion-settle |

- One `world-state` row per fast tick. Slow fields carried-forward, each
  stamped with its own `*_ts` so freshness is explicit.
- **Raw buffer:** rolling ring, **10 days** default (config, tunable). Oldest
  auto-pruned. `.mp4` + `.wav` segments on mac-mini disk.
- **Neo4j rollup:** every N min, materialize a semantic snapshot from the TSDB
  window.

## Storage layout

**TSDB (Timescale, Docker on mac-mini):**

```
world_state hypertable:
  ts (PK, time), occupancy int, lighting_level real, light_temp text,
  activity text, sound_class text, sound_level real,
  tidiness real, tidiness_label text, tidiness_ts timestamptz,
  objects jsonb, objects_ts timestamptz, confidence jsonb
```

Fast ticks insert here; slow fields nullable / carried-forward.

**Neo4j (Docker on mac-mini):** materialized every N min from a TSDB rollup:

```
(:Room {id})-[:OBSERVED {ts}]->(:State {lighting, light_temp, tidiness, occupancy, sound_class, activity})
(:State)-[:NEXT]->(:State)              // temporal chain
(:Occupant)-[:PRESENT_IN {ts}]->(:Room)
```

This graph is the WP4 substrate. Later cycles attach preference / persona nodes.

**Raw buffer:** `raw/YYYY-MM-DD/HHMMSS.mp4` + `.wav`, ring-pruned at 10 days.
`raw_index` table maps each segment → time range, for later re-processing
(JEPA, idea 1).

## Testing & validation

- **Per-service unit tests** — fixed sample frame / audio clip → assert state
  output. Model wrapped behind an interface; tests mock the model, test the glue.
- **Schema / contract test** — every `world-state` record validates against the
  schema; missing / malformed fields rejected.
- **Pipeline integration** — replay a short recorded clip end-to-end → assert
  rows land in TSDB and a Neo4j snapshot is built.
- **Tidiness VLM validation** — small hand-labeled set (~20 frames scored
  organized/messy by hand) → check VLM correlation. Doubles as research
  validation of the proxy.
- **Retention** — unit-test ring pruning at the 10-day boundary.

## Privacy notes

- Raw media stays on mac-mini (LAN only); Reolink cloud disabled, RTSP local.
- Raw buffer auto-pruned at 10 days; structured state is the durable record.
- Personal room — single occupant consents (self).

## Open items for the implementation plan

- Exact fast-tick interval + rollup interval (start 3 s / 2 min, tune).
- Reolink RTSP URL / credential handling.
- Which YOLO + YAMNet + Qwen-VL GGUF weights; Metal/MPS execution on mac-mini.
- Local bus mechanism (asyncio queue vs. lightweight broker).
- Supervisor: extend `local-voice-ai`'s pattern vs. minimal own supervisor.
- Home Assistant: stand up home instance now (parallel layer) or later.
