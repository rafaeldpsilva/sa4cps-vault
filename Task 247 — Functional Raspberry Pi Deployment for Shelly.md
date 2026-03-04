**Goal:** Full pipeline from Shelly discovery to encrypted, privacy-preserving data transmission to GECAD.

---

## Subtasks (in order)

| #   | Subtask                            | Script                |
| --- | ---------------------------------- | --------------------- |
| 1   | Shelly wifi (re)configuration      | `shelly_configure.py` |
| 2   | Shelly discovery on home network   | `shelly_discover.py`  |
| 3   | Monitoring daemon                  | `shelly_monitor.py`   |
| 4   | Transmission to GECAD with privacy | `shelly_transmit.py`  |

---

## 1. Shelly (re)configuration — `shelly_configure.py`

Extracted and refactored from the existing Stage B in `pi_shelly_setup.py`. Makes it callable standalone for reconfiguration without re-running the full wifi setup.

- Scans for Shelly AP (`ShellyProEM` prefix)
- Connects Pi to Shelly AP (`192.168.33.1`)
- Pushes WiFi credentials via `POST /rpc/WiFi.SetConfig`
- Triggers reboot and waits for Shelly to rejoin home network

---

## 2. Shelly discovery — `shelly_discover.py`

Finds Shelly devices already on the home network (post-configuration).

- Reads home subnet from default gateway
- Scans ARP table + HTTP probes to `/rpc/Shelly.GetDeviceInfo`
- Falls back to Shelly Cloud API if local scan fails
- Saves results to `/etc/pi-shelly/devices.json`

---

## 3. Monitoring daemon — `shelly_monitor.py`

Polls each device in `devices.json` every 60 seconds.

- Calls `GET /rpc/EM.GetStatus` on each Shelly
- **Pseudonymizes** device ID at write time: `HMAC-SHA256(mac_address, per-pi salt)`
- Stores in SQLite at `/var/pi-shelly/data.db`:
  ```
  readings(id, device_hash, timestamp, power_w, energy_kwh, voltage, current, pf)
  ```
- Also writes latest readings to `/run/pi-shelly/latest.json` (for dashboard)
- Runs as `pi-shelly-monitor.service` (restart on failure)

---

## 4. Transmission to GECAD — `shelly_transmit.py`

Daily job that sends previous day's data to GECAD.

- Reads rows with `timestamp < yesterday midnight` not yet transmitted
- Serializes to JSON
- Encrypts payload: AES-256-GCM, key at `/etc/pi-shelly/transmit.key`
- POSTs to GECAD HTTPS endpoint (configurable in `/etc/pi-shelly/config.json`) via Tailscale
- Marks rows as transmitted in DB
- Supports `--dry-run` flag (prints payload, no POST)

**Privacy model:**
- Raw MAC addresses never stored — pseudonymized at collection time
- 24h buffer: data leaves the home only the day after it was collected
- In-transit encryption: AES-256-GCM + HTTPS/Tailscale

---

## Systemd units

| Unit | Type | Trigger |
|------|------|---------|
| `pi-shelly-monitor.service` | simple daemon | boot |
| `pi-shelly-transmit.service` | oneshot | triggered by timer |
| `pi-shelly-transmit.timer` | timer | daily @ 02:00 |

---

## Files

```
phd-vault/rasp/
├── shelly_configure.py
├── shelly_discover.py
├── shelly_monitor.py
├── shelly_transmit.py
└── systemd/
    ├── pi-shelly-monitor.service
    ├── pi-shelly-transmit.service
    └── pi-shelly-transmit.timer
```

Reuses: `pi_shelly_setup.py` (Stage A ✅ done, Stage B → refactored into `shelly_configure.py`)
