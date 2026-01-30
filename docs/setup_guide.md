# 🛠 Guide d'Installation Complet

Ce guide détaille la procédure pour configurer le système ZenCantine de zéro.

## Phase 1 : Préparation du Raspberry Pi (Le Serveur)

1. **Installation OS :** Installer Raspberry Pi OS sur la carte SD via *Raspberry Pi Imager*.
2. **Connexion :** Se connecter en SSH (`ssh admin@raspberrypi.local`).
3. **Création du Hotspot Wi-Fi :**
   Le Raspberry doit devenir un routeur autonome.
   ```bash
   sudo nmcli device wifi hotspot ssid "SSID_WIFI" password "PWD_WIFI" ifname wlan0
   sudo nmcli connection modify ZenCantine connection.autoconnect yes
4. Fixer l'IP de la Lampe (Bail Statique) : Pour que la lampe ait toujours l'adresse .169 :
    ```bash
    echo "dhcp-host=5C:E7:53:0E:6A:56,10.42.0.169" | sudo tee /etc/NetworkManager/dnsmasq.d/govee_static.conf
    (Remplacez l'adresse MAC 5C:E7... par celle de votre lampe).
5. Installation du Script : Copier le fichier cantine_server.py dans /home/admin/.
6. Lancement Automatique : crontab -e -> Ajouter à la fin :
    ```bash
    @reboot sleep 30 && python3 /home/admin/cantine_server.py &
7. Redémarrer : sudo reboot.

## Phase 2 : Configuration de la Lampe Govee

La lampe ne peut pas se connecter directement à un réseau sans internet. Il faut utiliser la technique du "Cheval de Troie".

1. Éteindre le Raspberry Pi (pour couper le Wi-Fi ZenCantine).
2. Configurer un partage de connexion sur un Smartphone :
    - SSID : SSID_WIFI
    - Mdp : PWD_WIFI
    - Bande : 2.4 GHz
3. Appairage :
    - Reset de la lampe (Bouton Power + 4 clics).
    - Ajouter la lampe dans l'appli Govee Home via le Wi-Fi du téléphone.
4. Basculer :
    - Couper le partage de connexion du téléphone
    - Rallumer le Raspberry Pi.
    - La lampe se connectera automatiquement au Raspberry.

## Phase 3 : Programmation du M5StickC Plus 2 (Le Micro)

1. Logiciel : Ouvrir le projet dans Arduino IDE.
2. Librairies : Installer M5Unified (PAS M5StickCPlus2 standard) et M5GFX.
3. Configuration : Vérifier dans le code .ino :
    C++
    const char* WIFI_SSID = MODIFIEZ;
    const char* WIFI_PASS = MODIFIEZ;
    const char* TARGET_IP = "10.42.0.1";
4. Téléverser le code.

## Phase 4 : Utilisation

1. Brancher le Raspberry Pi.
2. Brancher la Lampe.
3. Brancher le M5Stick.
4. Attendre 60 secondes.
5. Vert = Calme / Rouge = Bruit.