# 🛠 Complete Installation Guide

This guide details the procedure to configure the ZenCantine system from scratch.

## Phase 1: Raspberry Pi Preparation (The Server)

1. **OS Installation:** Install Raspberry Pi OS on the SD card via *Raspberry Pi Imager*.
2. **Connection:** Connect via SSH (`ssh admin@raspberrypi.local`).
   
   > 💡 **Hostname:** The default hostname is `raspberrypi`. You can change it with `sudo raspi-config` > System Options > Hostname. Then use `http://yourhostname.local` to access the web interface.
3. **Wi-Fi Hotspot Creation:**
   The Raspberry must become an autonomous router.
   ```bash
   sudo nmcli device wifi hotspot ssid "ZEN_CANTINE" password "cantine2026" ifname wlan0
   sudo nmcli connection modify ZEN_CANTINE connection.autoconnect yes
   ```
4. **Set WLED Lamp IP (Static DHCP):**
   ```bash
   echo "dhcp-host=AA:BB:CC:DD:EE:FF,10.42.0.10" | sudo tee /etc/NetworkManager/dnsmasq.d/wled_static.conf
   ```
   Replace `AA:BB:CC:DD:EE:FF` with your lamp's MAC address.
5. **Server Script Installation:**
   Copy `server_raspberry/app.py` to `/home/admin/`.
6. **Automatic Startup:**
   Add to the end of `crontab -e`:
   ```bash
   @reboot sleep 30 && python3 /home/admin/app.py &
   ```
7. Reboot:
   ```bash
   sudo reboot
   ```

## Phase 2: WLED Lamp Configuration

The WLED lamp must be configured to connect to the Raspberry Pi hotspot.

1. Turn off the Raspberry Pi to isolate the network.
2. Enable Wi-Fi hotspot sharing on a smartphone:
   - SSID: same as defined on the Raspberry Pi.
   - Password: same as defined on the Raspberry Pi.
   - Band: 2.4 GHz.
3. Pair the WLED lamp on the smartphone.
4. Turn off the phone's hotspot sharing.
5. Turn on the Raspberry Pi.
6. Verify that the lamp is reachable on `10.42.0.10`.

## Phase 3: M5StickC Plus 2 Programming (The Micro)

1. Open the project `sensor_m5stick/ZenCantine_Mic_ino.ino` in Arduino IDE.
2. Install the following libraries:
   - `M5Unified`
   - `M5GFX`
3. Prepare the configuration file:
   - Rename `sensor_m5stick/config/config_template.h` to `sensor_m5stick/config/config.h`.
   - Update the variables:
     ```cpp
     const char* WIFI_SSID = "ZEN_CANTINE";
     const char* WIFI_PASS = "cantine2026";
     const char* TARGET_IP = "10.42.0.1";
     const int TARGET_PORT = 4210;
     ```
4. Select the `M5StickCPlus2` board in Arduino IDE.
5. Select the corresponding USB port.
6. Upload the sketch.

## Phase 4: Usage

1. Power on the Raspberry Pi.
2. Power on the WLED lamp.
3. Power on the M5Stick.
4. Wait 60 seconds.
5. Green = calm / Orange = medium noise / Red = high noise / Flashing = critical.

## Phase 5: Configuration via Web Interface

Once the system is started, access the web interface to fine-tune the configuration:

1. **Connection:** Open a web browser and go to `http://10.42.0.1` or `http://raspberrypi.local`
2. **Time Setting:** If needed, adjust the system time in the "System Time Settings" section
3. **Threshold Configuration:**
   - **Alert Threshold**: dB level to switch to red (recommended: 65 dB)
   - **Reset Threshold**: dB level to return to green (recommended: 55 dB)
   - **Buffer Size**: Signal smoothing (recommended: 10)
4. **Testing:** Speak loudly near the M5Stick to verify changes
5. **Saving:** Modifications are automatically saved

### Advanced Features:
- **Real-time Dashboard**: Current volume tracking and daily statistics
- **History Charts**: Measurement visualization for 1h or 24h
- **Reset**: Button to restore all parameters to default values

## Important Notes

- `server_raspberry/app.py` listens on `10.42.0.1:4210`.
- The expected UDP message is in the format `vol:<dB_value>` sent by the M5Stick.
- UDP is used only to transmit sensor measurements to the server.
- `server_raspberry/config/config.py` is intended for `server_raspberry/app.py` (WLED dashboard).