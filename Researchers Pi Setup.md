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
docker exec -it headscale headscale users create {USER}

# List users (to get the user ID)
docker exec -it headscale headscale users list

# Generate a reusable, non-expiring pre-auth key
docker exec -it headscale headscale preauthkeys create --user {USER_ID} --reusable --expiration 0
```

### On the Raspberry Pi
Save the `preauthkey-from-above` on the python script:

```bash
# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Join the Headscale network using the pre-auth key
sudo tailscale login --login-server https://headscale.gecad.isep.ipp.pt \
  --authkey <preauthkey-from-above>
```


```bash
scp pi_shelly_setup.py admin@{PI_IP}:/home/admin/
```
### Configure wifi-connect

**wifi-connect** (not in apt, install via official script):
```bash
# For Pi 4/5 (aarch64)
curl -fsSL https://github.com/balena-os/wifi-connect/releases/download/v4.11.84/wifi-connect-aarch64-unknown-linux-gnu.tar.gz \
  | sudo tar -xz -C /usr/local/bin/ && cp /usr/local/bin/wifi-connect /usr/local/sbin

# For Pi 3 (armv7)
curl -fsSL https://github.com/balena-os/wifi-connect/releases/latest/download/wifi-connect-v4-linux-armv7hf.tar.gz \
  | sudo tar -xz -C /usr/local/bin/ && cp /usr/local/bin/wifi-connect 
```


### Verify everything is installed
```bash
python3 --version
nmcli --version
iwlist --version
wifi-connect --version
python3 -c "import requests; print('requests ok')"
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