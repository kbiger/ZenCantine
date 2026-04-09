# 🛠 Guide d'Installation Complet

> 📖 **Documentation disponible en:** [English](setup_guide.en.md) | [Français](setup_guide.md)

Ce guide détaille la procédure pour configurer le système ZenCantine de zéro.

## Phase 1 : Préparation du Raspberry Pi (Le Serveur)

1. **Installation OS :** Installer Raspberry Pi OS sur la carte SD via *Raspberry Pi Imager*.
2. **Connexion :** Se connecter en SSH (`ssh admin@raspberrypi.local`).
   
   > 💡 **Hostname :** Le hostname par défaut est `raspberrypi`. Vous pouvez le changer avec `sudo raspi-config` > System Options > Hostname. Utilisez ensuite `http://votrehhostname.local` pour accéder à l'interface web.
3. **Création du Hotspot Wi-Fi :**
   Le Raspberry doit devenir un routeur autonome.
   ```bash
   sudo nmcli device wifi hotspot ssid "ZEN_CANTINE" password "cantine2026" ifname wlan0
   sudo nmcli connection modify ZEN_CANTINE connection.autoconnect yes
   ```
4. **Fixer l'IP de la Lampe WLED (DHCP statique) :**
   ```bash
   echo "dhcp-host=AA:BB:CC:DD:EE:FF,10.42.0.10" | sudo tee /etc/NetworkManager/dnsmasq.d/wled_static.conf
   ```
   Remplacez `AA:BB:CC:DD:EE:FF` par l'adresse MAC de votre lampe.
5. **Installation du script serveur :**
   Copier `server_raspberry/app.py` dans `/home/admin/`.
6. **Lancement automatique :**
   Ajouter à la fin de `crontab -e` :
   ```bash
   @reboot sleep 30 && python3 /home/admin/app.py &
   ```
7. Redémarrer :
   ```bash
   sudo reboot
   ```

## Phase 2 : Configuration de la Lampe WLED

La lampe WLED doit être configurée pour se connecter au hotspot du Raspberry Pi.

1. Éteindre le Raspberry Pi pour isoler le réseau.
2. Activer le partage de connexion Wi-Fi sur un smartphone :
   - SSID : identique à celui défini sur le Raspberry Pi.
   - Mot de passe : identique à celui défini sur le Raspberry Pi.
   - Bande : 2.4 GHz.
3. Appairer la lampe WLED sur le smartphone.
4. Couper le partage de connexion du téléphone.
5. Rallumer le Raspberry Pi.
6. Vérifier que la lampe est joignable sur `10.42.0.10`.

## Phase 3 : Programmation du M5StickC Plus 2 (Le Micro)

1. Ouvrir le projet `sensor_m5stick/ZenCantine_Mic_ino.ino` dans Arduino IDE.
2. Installer les bibliothèques suivantes :
   - `M5Unified`
   - `M5GFX`
3. Préparer le fichier de configuration :
   - Renommez `sensor_m5stick/config/config_template.h` en `sensor_m5stick/config/config.h`.
   - Mettez à jour les variables :
     ```cpp
     const char* WIFI_SSID = "ZEN_CANTINE";
     const char* WIFI_PASS = "cantine2026";
     const char* TARGET_IP = "10.42.0.1";
     const int TARGET_PORT = 4210;
     ```
4. Sélectionner la carte `M5StickCPlus2` dans Arduino IDE.
5. Sélectionner le port USB correspondant.
6. Téléverser le sketch.

## Phase 4 : Utilisation

1. Brancher le Raspberry Pi.
2. Brancher la lampe WLED.
3. Brancher le M5Stick.
4. Attendre 60 secondes.
5. Vert = calme / Orange = bruit moyen / Rouge = bruit élevé / Clignotant = critique.

## Phase 5 : Configuration via l'Interface Web

Une fois le système démarré, accédez à l'interface web pour affiner la configuration :

1. **Connexion :** Ouvrez un navigateur web et allez sur `http://10.42.0.1` ou `http://raspberrypi.local`
2. **Réglage de l'heure :** Si nécessaire, ajustez l'heure système dans la section "Réglage de l'Heure Système"
3. **Configuration des seuils :**
   - **Seuil d'Alerte** : Niveau en dB pour passer au rouge (recommandé : 65 dB)
   - **Seuil de Reset** : Niveau en dB pour revenir au vert (recommandé : 55 dB)
   - **Taille du Buffer** : Lissage du signal (recommandé : 10)
4. **Test :** Parlez fort près du M5Stick pour vérifier les changements
5. **Sauvegarde :** Les modifications sont automatiquement sauvegardées

### Fonctionnalités avancées :
- **Dashboard temps réel** : Suivi du volume actuel et statistiques du jour
- **Graphiques d'historique** : Visualisation des mesures sur 1h ou 24h
- **Reset** : Bouton pour remettre tous les paramètres aux valeurs par défaut

## Notes importantes

- `server_raspberry/app.py` écoute sur `10.42.0.1:4210`.
- Le message UDP attendu est de la forme `vol:<valeur_en_dB>` envoyé par le M5Stick.
- UDP sert uniquement à faire remonter les mesures du capteur vers le serveur.
- `server_raspberry/config/config.py` est destiné à `server_raspberry/app.py` (dashboard WLED).
