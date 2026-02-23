## "Dual-Stage" Connection

This is the tutorial to setup and connect your Shelly and Pi.

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