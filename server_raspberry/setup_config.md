# Configuration Système Raspberry Pi

## 1. Création du Hotspot
```bash
sudo nmcli device wifi hotspot ssid "WIFI_SSID" password "WIFI_PASSWORD" ifname wlan0
sudo nmcli connection modify ZenCantine connection.autoconnect yes

## 2. IP Statique pour la lampe Govee
```bash
sudo nmcli device wifi hotspot ssid "ZenCantine" password "cantine2026" ifname wlan0
echo "dhcp-host=ADRESSE_MAC_LAMPE_GOVEE,10.42.0.169" | sudo tee /etc/NetworkManager/dnsmasq.d/govee_static.conf

## 2. Lancement automatique
Ajouter dans crontab -e :
```bash
@reboot sleep 30 && python3 /home/admin/cantine_server.py &