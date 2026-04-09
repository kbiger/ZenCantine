# Raspberry Pi System Configuration

> 📖 **Documentation available in:** [English](README.en.md) | [Français](README.md)

## 1. Hotspot Creation

```bash
sudo nmcli device wifi hotspot ssid "ZEN_CANTINE" password "cantine2026" ifname wlan0
sudo nmcli connection modify ZEN_CANTINE connection.autoconnect yes
```

## 2. Static IP for WLED Lamp

```bash
echo "dhcp-host=WLED_LAMP_MAC_ADDRESS,10.42.0.10" | sudo tee /etc/NetworkManager/dnsmasq.d/wled_static.conf
```

Replace `WLED_LAMP_MAC_ADDRESS` with your lamp's actual MAC address.

## 3. Automatic Startup

Add to `crontab -e`:

```bash
@reboot sleep 30 && python3 /home/admin/app.py &
```

## 4. Configuration Notes

- `server_raspberry/app.py` listens for UDP packets from M5Stick on `10.42.0.1:4210`.
- Configure `server_raspberry/config/config.py` or `server_raspberry/config/config_template.py` for WLED.

## 5. Web Interface

The Flask server provides a web interface accessible at `http://10.42.0.1:80` or `http://raspberrypi.local:80` (or your Raspberry Pi's IP/hostname).

### Main Features:
- **Real-time Dashboard**: Current volume, alert status, daily statistics
- **Threshold Configuration**: Adjust alert and reset levels (30-100 dB), buffer size
- **Time Settings**: Manual system time correction for offline systems
- **History**: Volume charts for 1 hour or 24 hours
- **Reset**: Restore all parameters to default values

### Available APIs:
- `GET /` : Main interface
- `GET /api/now` : Real-time data
- `GET /api/stats` : Daily statistics
- `GET /api/history?range=hour|day` : History data
- `GET/POST /api/config` : Threshold configuration
- `POST /api/config/reset` : Reset to defaults
- `GET/POST /api/time` : System time management