## "Dual-Stage" Connection

This is the tutorial to setup and connect your Shelly and Pi.

### Stage A: The Shelly Setup (Pi as Client)
1. 
2. **Boot Up:** The Pi turns on and looks for the factory Shelly AP (e.g., `ShellyProEM-XXXXXX`).
3. 
    
4. **Handshake:** The Pi connects to the Shelly’s open WiFi.
    
5. **Command:** The Pi sends a JSON payload to `http://192.168.33.1/rpc/WiFi.SetConfig` containing a **unique "Community Setup" SSID/Password** that you have pre-defined.
    
6. **Verification:** The Shelly reboots and connects to the Pi’s future "Setup Hotspot."
    

### Stage B: The User Setup (Pi as Access Point)

1. The Pi now switches modes and becomes a **Hotspot** (using `balena-wifi-connect` or similar).
    
2. The User connects their phone to the Pi and enters their **Home WiFi** credentials.
    
3. **The "Bridge":** The Pi saves those credentials and pushes them to the Shelly (which is already connected to the Pi’s hotspot).
    
4. **Final Jump:** Both the Pi and the Shelly disconnect from each other and join the Home WiFi simultaneously.