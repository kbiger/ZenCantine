# Configuration Système Raspberry Pi

> 📖 **Documentation disponible en:** [English](README.en.md) | [Français](README.md)

## 1. Création du Hotspot

```bash
sudo nmcli device wifi hotspot ssid "ZEN_CANTINE" password "cantine2026" ifname wlan0
sudo nmcli connection modify ZEN_CANTINE connection.autoconnect yes
```

## 2. IP Statique pour la lampe WLED

```bash
echo "dhcp-host=ADRESSE_MAC_LAMPE_WLED,10.42.0.10" | sudo tee /etc/NetworkManager/dnsmasq.d/wled_static.conf
```

Remplacez `ADRESSE_MAC_LAMPE_WLED` par l'adresse MAC réelle de votre lampe.

## 3. Lancement automatique

Ajouter dans `crontab -e` :

```bash
@reboot sleep 30 && python3 /home/admin/app.py &
```

## 4. Notes de configuration

- `server_raspberry/app.py` écoute les paquets UDP du M5Stick sur `10.42.0.1:4210`.
- Configurez `server_raspberry/config/config.py` ou `server_raspberry/config/config_template.py` pour WLED.

## 5. Interface Web

Le serveur Flask fournit une interface web accessible sur `http://10.42.0.1:80` ou `http://raspberrypi.local:80` (ou l'IP/hostname de votre Raspberry).

### Fonctionnalités principales :
- **Dashboard temps réel** : Volume actuel, état d'alerte, statistiques du jour
- **Configuration des seuils** : Ajustement des niveaux d'alerte et de reset (30-100 dB), taille du buffer
- **Réglage de l'heure** : Correction manuelle de l'heure système pour systèmes non connectés
- **Historique** : Graphiques du volume sur 1 heure ou 24 heures
- **Reset** : Remise aux valeurs par défaut de tous les paramètres

### API disponibles :
- `GET /` : Interface principale
- `GET /api/now` : Données temps réel
- `GET /api/stats` : Statistiques journalières
- `GET /api/history?range=hour|day` : Historique
- `GET/POST /api/config` : Configuration des seuils
- `POST /api/config/reset` : Reset aux valeurs par défaut
- `GET/POST /api/time` : Gestion de l'heure système
