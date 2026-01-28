# 🧘 ZenCantine

**Apaisez le bruit de la cantine grâce à un feedback visuel ludique.**

ZenCantine est une solution IoT Open-Source conçue pour réduire le volume sonore dans les réfectoires scolaires. Le système écoute l'ambiance sonore et change la couleur des murs (Vert/Rouge) en temps réel pour indiquer aux enfants quand le volume devient trop élevé.

### 🛠 Architecture
* **Oreilles (Capteurs) :** M5StickC Plus2 (ESP32) avec microphone I2S.
* **Cerveau (Serveur) :** Raspberry Pi Zero 2 W (Python + UDP).
* **Yeux (Actionneurs) :** Bandeaux LED Govee Neon pilotés en LAN local.

### 🚀 Objectifs
* **Coût réduit :** Moins de 500€ pour équiper une grande salle.
* **Privacy :** Analyse locale du volume uniquement, aucun enregistrement audio.
* **Open-Source :** Code sous licence GPLv3, reproductible par n'importe quelle école ou parent bricoleur.
