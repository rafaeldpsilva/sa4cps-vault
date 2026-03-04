## "Dual-Stage" Connection

This is the tutorial to setup and connect your Shelly and Pi.

## Requirements

### System Packages
```bash
sudo apt install network-manager wireless-tools
```

**wifi-connect** (not in apt):
```bash
bash <(curl -sf https://raw.githubusercontent.com/balena-os/wifi-connect/master/scripts/raspbian-install.sh)
```

### Python
- Python 3.10+ (Ubuntu 24 LTS ships with 3.12 ✓)

```bash
sudo pip3 install requests
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
The setup is automated by `pi_shelly_setup.py`. To run on boot, see the systemd service setup in the step-by-step guide.

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