## "Dual-Stage" Connection

This is the tutorial to setup and connect your Shelly and Pi.

## Requirements

### System Packages
Python 3.10+ (Ubuntu 24 LTS ships with 3.12 ✓)
```bash
sudo apt install python3-pip python3-requests
```

## Tailscale Setup

### On the Headscale Server (Docker)
```bash
# Create a user
docker exec -it headscale headscale users create test

# List users (to get the user ID)
docker exec -it headscale headscale users list

# Generate a reusable, non-expiring pre-auth key (replace 2 with the actual user ID)
docker exec -it headscale headscale preauthkeys create --user 2 --reusable --expiration 0
```

### On the Raspberry Pi
```bash
# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Join the Headscale network using the pre-auth key
sudo tailscale login --login-server https://headscale.gecad.isep.ipp.pt \
  --authkey <preauthkey-from-above>
```

### Configure wifi-connect

**wifi-connect** (not in apt, install via official script):
```bash
# For Pi 4/5 (aarch64)
curl -fsSL https://github.com/balena-os/wifi-connect/releases/download/v4.11.84/wifi-connect-aarch64-unknown-linux-gnu.tar.gz \
  | sudo tar -xz -C /usr/local/bin/

# For Pi 3 (armv7)
curl -fsSL https://github.com/balena-os/wifi-connect/releases/latest/download/wifi-connect-v4-linux-armv7hf.tar.gz \
  | sudo tar -xz -C /usr/local/bin/
bash <(curl -L https://github.com/balena-io/wifi-connect/raw/master/scripts/raspbian-install.sh)
```

Automated script (deprecated):
```bash
bash <(curl -L https://github.com/balena-io/wifi-connect/raw/master/scripts/raspbian-install.sh)
```

### Verify everything is installed
```bash
python3 --version
nmcli --version
iwlist --version
wifi-connect --version
python3 -c "import requests; print('requests ok')"
```

### Python code
```
#!/usr/bin/env python3
"""
Pi-Shelly Dual-Stage WiFi Setup
Automates the process of capturing home WiFi credentials via hotspot
and pushing them to a Shelly Pro EM device.

Run as root: sudo python3 pi_shelly_setup.py
"""

import subprocess
import time
import json
import sys
import requests
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
CREDENTIALS_FILE = Path("/etc/pi-shelly/wifi_creds.json")
SHELLY_AP_PREFIX  = "ShellyProEM"
SHELLY_IP         = "192.168.33.1"
PORTAL_SSID       = "PiSetup"
WIFI_IFACE        = "wlan0"
SHELLY_TIMEOUT    = 30  # seconds to wait for Shelly to reboot
# ─────────────────────────────────────────────────────────────────────────────


def run(cmd: str, check=True) -> subprocess.CompletedProcess:
    print(f"  $ {cmd}")
    return subprocess.run(cmd, shell=True, check=check,
                          capture_output=True, text=True)


# ── Stage A: Hotspot + capture credentials ────────────────────────────────────

def start_hotspot():
    """
    Start wifi-connect captive portal. The user connects their phone,
    submits home WiFi credentials, and wifi-connect joins that network.
    Credentials are then read from NetworkManager and saved to file.
    """
    print("\n[Stage A] Starting hotspot...")
    CREDENTIALS_FILE.parent.mkdir(parents=True, exist_ok=True)

    # wifi-connect blocks until the user submits credentials and the Pi
    # successfully joins the home WiFi — no --output flag exists.
    result = subprocess.run(
        f"wifi-connect --portal-ssid '{PORTAL_SSID}' --portal-interface {WIFI_IFACE}",
        shell=True, text=True
    )
    if result.returncode != 0:
        print("ERROR: wifi-connect failed.")
        sys.exit(1)

    # Read credentials from NetworkManager after successful connection
    ssid = subprocess.run(
        "nmcli -t -f active,ssid dev wifi | grep '^yes' | cut -d: -f2",
        shell=True, capture_output=True, text=True
    ).stdout.strip()

    password = subprocess.run(
        f"nmcli -s -g 802-11-wireless-security.psk connection show '{ssid}'",
        shell=True, capture_output=True, text=True
    ).stdout.strip()

    if not ssid:
        print("ERROR: Could not determine connected SSID from NetworkManager.")
        sys.exit(1)

    with open(CREDENTIALS_FILE, "w") as f:
        json.dump({"ssid": ssid, "password": password}, f)

    print(f"  Credentials saved — SSID: {ssid}")


def load_credentials() -> dict:
    if not CREDENTIALS_FILE.exists():
        print("ERROR: No credentials file found. Run Stage A first.")
        sys.exit(1)
    with open(CREDENTIALS_FILE) as f:
        return json.load(f)


# ── Stage B: Find Shelly AP, configure it, reconnect Pi ──────────────────────

def find_shelly_ap() -> str | None:
    """Scan for a Shelly factory access point and return its SSID."""
    print("\n[Stage B] Scanning for Shelly AP...")
    result = run(f"sudo iwlist {WIFI_IFACE} scan", check=False)
    for line in result.stdout.splitlines():
        line = line.strip()
        if "ESSID" in line:
            ssid = line.split('"')[1]
            if ssid.startswith(SHELLY_AP_PREFIX):
                print(f"  Found: {ssid}")
                return ssid
    return None


def connect_to_ap(ssid: str):
    """Connect the Pi to a given WiFi SSID (open network)."""
    print(f"  Connecting to {ssid}...")
    run(f"sudo nmcli dev wifi connect '{ssid}' ifname {WIFI_IFACE}")
    time.sleep(3)


def push_wifi_to_shelly(ssid: str, password: str):
    """Send home WiFi credentials to Shelly via its RPC API."""
    print(f"  Pushing WiFi config to Shelly at {SHELLY_IP}...")
    payload = {
        "config": {
            "sta": {
                "ssid": ssid,
                "pass": password,
                "enable": True
            }
        }
    }
    try:
        r = requests.post(
            f"http://{SHELLY_IP}/rpc/WiFi.SetConfig",
            json=payload,
            timeout=10
        )
        r.raise_for_status()
        print(f"  Shelly response: {r.json()}")
    except requests.RequestException as e:
        print(f"ERROR: Failed to configure Shelly: {e}")
        sys.exit(1)


def reboot_shelly():
    """Trigger a Shelly reboot."""
    print("  Rebooting Shelly...")
    try:
        requests.get(f"http://{SHELLY_IP}/rpc/Shelly.Reboot", timeout=5)
    except requests.RequestException:
        pass  # Expected — Shelly drops connection on reboot


def reconnect_pi(ssid: str, password: str):
    """Reconnect the Pi to the home WiFi network."""
    print(f"\n  Reconnecting Pi to home WiFi: {ssid}")
    run(f"sudo nmcli dev wifi connect '{ssid}' password '{password}' ifname {WIFI_IFACE}")
    time.sleep(5)


def verify_shelly_online(home_ssid: str) -> bool:
    """
    Wait for the Shelly to reboot and appear on the home network.
    Polls ARP table for a new device — adjust if you know the Shelly's MAC.
    """
    print(f"  Waiting up to {SHELLY_TIMEOUT}s for Shelly to join {home_ssid}...")
    for _ in range(SHELLY_TIMEOUT // 5):
        time.sleep(5)
        result = run("arp -n", check=False)
        # A new device appearing is a good sign; refine with MAC if needed
        if result.returncode == 0 and result.stdout.strip():
            print("  Network neighbours detected — Shelly likely online.")
            return True
    print("  WARNING: Could not confirm Shelly is online. Check manually.")
    return False


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=== Pi-Shelly Dual-Stage WiFi Setup ===\n")

    # Stage A — only run if no credentials saved yet
    if not CREDENTIALS_FILE.exists():
        start_hotspot()
    else:
        print("[Stage A] Credentials already saved, skipping hotspot.")

    creds = load_credentials()
    home_ssid     = creds["ssid"]
    home_password = creds["password"]

    # Stage B
    shelly_ssid = find_shelly_ap()
    if not shelly_ssid:
        print("ERROR: No Shelly AP found. Is the device in factory mode?")
        sys.exit(1)

    connect_to_ap(shelly_ssid)
    push_wifi_to_shelly(home_ssid, home_password)
    reboot_shelly()
    reconnect_pi(home_ssid, home_password)
    verify_shelly_online(home_ssid)

    print("\n=== Setup complete ===")
    print(f"  Pi connected to : {home_ssid}")
    print(f"  Shelly configured to join: {home_ssid}")


if __name__ == "__main__":
    if subprocess.run("id -u", shell=True, capture_output=True, text=True).stdout.strip() != "0":
        print("Please run as root: sudo python3 pi_shelly_setup.py")
        sys.exit(1)
    main()

```

### Automation Script

1. Copy the script to a system location
```bash
sudo cp pi_shelly_setup.py /usr/local/bin/pi_shelly_setup.py
sudo chmod +x /usr/local/bin/pi_shelly_setup.py
```

  2. Create the service file
```bash
sudo nano /etc/systemd/system/pi-shelly-setup.service
```

  Paste this:
```
[Unit]
Description=Pi-Shelly Dual-Stage WiFi Setup
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /usr/local/bin/pi_shelly_setup.py
RemainAfterExit=yes
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

  3. Enable it
```bash
sudo systemctl daemon-reload
sudo systemctl enable pi-shelly-setup.service
```

  4. Test without rebooting
```bash
sudo systemctl start pi-shelly-setup.service
sudo journalctl -u pi-shelly-setup.service -f
```

  ---
  Type=oneshot means it runs once per boot and stops — which is exactly what you want. Since the script skips Stage A if credentials are already saved, subsequent reboots
   will go straight to Stage B (Shelly config) without showing the hotspot again.

  If you want the hotspot to appear on every boot (e.g. for re-provisioning), delete the credentials file:
  sudo rm /etc/pi-shelly/wifi_creds.json

The setup is automated by `pi_shelly_setup.py`. To run on boot, see the systemd service setup in the step-by-step guide.

---

## Stage A: The User Setup (Pi as Access Point)

1. The Pi turns on and becomes a **Hotspot** (using `gecad-wifi-connect` or similar).
    
2. The User connects their phone to the Pi and enters their **Home WiFi** credentials.
    
3. **The "Bridge":** The Pi saves those credentials and pushes them to the Shelly
    
4. **Final Stage:** Both the Pi and the Shelly disconnect from each other and join the Home WiFi simultaneously.

## Stage B: The Shelly Setup (Pi as Client)
1. **Boot Up:** The Pi looks for the factory Shelly AP (e.g., `ShellyProEM-XXXXXX`).
    
2. **Handshake:** The Pi connects to the Shelly’s open WiFi.
    
3. **Command:** The Pi sends a JSON payload to `http://192.168.33.1/rpc/WiFi.SetConfig` containing the **SSID/Password** that was previously defined.
    
4. **Verification:** The Shelly reboots and connects to your home wifi.