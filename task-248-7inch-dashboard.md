# Task 248 — 7" Monitor TUI Dashboard

**Goal:** A terminal dashboard running permanently on the Pi's 7" HDMI display showing live Shelly readings and system health.

---

## Subtasks

| # | Subtask |
|---|---------|
| 1 | Test existing 7" monitors on Pi |
| 2 | Build ncurses dashboard (`dashboard_tui.py`) |
| 3 | Populate with live Shelly data |
| 4 | Mount on demo board |

---

## Implementation

**Script:** `dashboard_tui.py`
**Language:** Python `curses` (stdlib, no extra deps)
**Data source:** `/run/pi-shelly/latest.json` written by `shelly_monitor.py` every 60s
**Refresh rate:** 5 seconds

---

## Layout (80×24 — fits 7" at 1024×600)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ SA4CPS — Pi Monitor Console            [rasp-001]         2026-03-04 14:32  │
├──────────────────────────────────────────────────────────────────────────────┤
│ DEVICE         STATUS    POWER(W)  ENERGY(kWh)  VOLTAGE  CURRENT   PF       │
│ dev-a3f9..     ● ONLINE    342.1      12.47      230.2    1.49    0.97      │
│ dev-b7c2..     ○ OFFLINE      -          -          -       -       -       │
├──────────────────────────────────────────────────────────────────────────────┤
│ SYSTEM  CPU: 12%  MEM: 34%  DISK: 18%  Uptime: 2d 4h    WiFi: gecad-home   │
│ NETWORK  IP: 192.168.1.42   Tailscale: 100.119.37.39                        │
├──────────────────────────────────────────────────────────────────────────────┤
│ Last update: 14:31:58   Next transmit: tomorrow 02:00    [q] quit            │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Color coding:**
- Green — device ONLINE
- Red — device OFFLINE
- Yellow — stale data (last reading >2 min ago)

**Edge cases:**
- If `latest.json` absent → shows "Waiting for monitoring data..."
- If all devices offline → full red state

---

## Systemd unit — `pi-shelly-dashboard.service`

```ini
[Service]
Type=simple
Restart=always
StandardOutput=tty
TTYPath=/dev/tty1
ExecStart=/usr/bin/python3 /opt/pi-shelly/dashboard_tui.py
After=pi-shelly-monitor.service
```

Runs directly on TTY1 (the HDMI output), no desktop environment needed.

---

## Files

```
phd-vault/rasp/
├── dashboard_tui.py
└── systemd/
    └── pi-shelly-dashboard.service
```
