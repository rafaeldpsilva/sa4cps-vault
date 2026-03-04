# Task 249 — 13" Community Manager Web UI

**Goal:** A browser-based dashboard for the community manager role, mounted on the demo board, showing aggregated energy data across multiple homes.

---

## Subtasks

| # | Subtask |
|---|---------|
| 1 | Mount 13" monitor(s) on demo board |
| 2 | Build FastAPI backend + HTML dashboard |
| 3 | Test navigation/interaction on the monitor |
| 4 | Final installation on expositor |

---

## Implementation

**Backend:** FastAPI (Python) + uvicorn, served on `localhost:8080`
**Frontend:** Server-rendered HTML, `<meta http-equiv="refresh" content="10">` — no JS framework
**Display:** Chromium in kiosk mode

---

## API Routes

| Route | Description |
|-------|-------------|
| `GET /` | HTML community manager dashboard |
| `GET /api/summary` | JSON: totals (power, energy, homes, devices) |
| `GET /api/devices` | JSON: per-device latest readings |

---

## Dashboard Layout

```
SA4CPS — Community Energy Manager
Comunidade: GECAD Researchers  |  3 homes active  |  2026-03-04 14:32
Auto-refresh: 10s

╔══════════════╦══════════════╦══════════════════╗
║ Total Power  ║ Total Energy ║ Active Devices   ║
║   1.24 kW   ║  45.3 kWh   ║     5 / 6        ║
╠══════════════╩══════════════╩══════════════════╣
║ HOME     DEVICES   POWER    STATUS   LAST SEEN ║
║ Home A      2       342W     OK       1m ago   ║
║ Home B      1        87W     OK       2m ago   ║
║ Home C      2         0W    OFFLINE  15m ago   ║
╠════════════════════════════════════════════════╣
║  [24h energy per home — horizontal bar chart] ║
╚════════════════════════════════════════════════╝
```

Bar chart rendered as HTML `<div>` blocks (no JS charting lib needed).

---

## Data source

- Reads from the same SQLite at `/var/pi-shelly/data.db`
- Groups by a `home_id` field (set at provisioning, stored in `/etc/pi-shelly/config.json`)
- For demo: multiple homes can be simulated from a single Pi by labeling data with different `home_id` values in config

---

## Chromium kiosk launch

```bash
chromium-browser --kiosk --noerrdialogs --disable-infobars \
  --app=http://localhost:8080 --start-fullscreen
```

---

## Systemd units

| Unit | Role |
|------|------|
| `pi-shelly-webui.service` | Runs FastAPI/uvicorn |
| `pi-shelly-kiosk.service` | Launches Chromium after webui is ready |

`pi-shelly-kiosk.service` uses `After=pi-shelly-webui.service` and a small startup delay to ensure the server is up before Chromium opens.

---

## Files

```
phd-vault/rasp/
├── dashboard_web.py
├── templates/
│   └── index.html
└── systemd/
    ├── pi-shelly-webui.service
    └── pi-shelly-kiosk.service
```
