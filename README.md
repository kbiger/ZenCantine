![Logo ZenCantine](assets/ZenCantine_logo_full.png)
# 🤫 ZenCantine

Système autonome de surveillance du niveau sonore pour cantine scolaire.
Le système affiche une alerte lumineuse (Lampe Govee) et visuelle (M5Stick) lorsque le bruit dépasse un seuil défini.

## 📡 Architecture Réseau

Le Raspberry Pi agit comme routeur Wi-Fi autonome (Hotspot).

| Appareil | Rôle | IP (Fixe) | MAC Address |
|---|---|---|---|
| **Raspberry Pi** | Serveur / Routeur | `10.42.0.1` | N/A |
| **M5StickC Plus 2** | Micro / Capteur | (DHCP) | - |
| **Lampe Govee** | Indicateur Lumineux | `10.42.0.169` | `A RECUPERER SUR APP GOVEE` |

* **SSID Wi-Fi :** `A DEFINIR`
* **Mot de passe :** `A DEFINIR`

## 🚀 Installation & Démarrage

Le système est conçu pour démarrer automatiquement à la mise sous tension.

### 1. Raspberry Pi (Server)
Le script se trouve dans `/home/admin/cantine_server.py`.
Il est lancé au démarrage via `crontab`.

### 2. M5Stick (Micro)
Le code Arduino utilise la librairie `M5Unified` pour éviter les conflits hardware.
Il envoie le volume via UDP sur le port `4210` vers le Raspberry.

### 3. Lampe Govee
La lampe est configurée avec une IP statique via `dnsmasq` sur le Raspberry pour garantir la connexion.
