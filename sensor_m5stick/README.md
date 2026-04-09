# 🎤 Capteur Micro - M5StickC Plus 2

> 📖 **Documentation disponible en:** [English](README.en.md) | [Français](README.md)

Ce dossier contient le code source (C++ / Arduino) pour le module de détection sonore.
Il mesure le volume ambiant et l'envoie via UDP au serveur Raspberry Pi.

## ⚠️ Note Importante (Anti-Crash)
Ce projet utilise spécifiquement la librairie **M5Unified** et non la librairie standard *M5StickCPlus2*.
L'utilisation de la librairie standard provoque un conflit matériel entre le Haut-Parleur et le Micro, entraînant un redémarrage en boucle (Bootloop).

## 🛠 Pré-requis Logiciels

### 1. Arduino IDE
Télécharger et installer [Arduino IDE](https://www.arduino.cc/en/software).

### 2. Gestionnaire de Cartes (Board Manager)
Dans les préférences de l'IDE, ajouter l'URL :
`https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/arduino/package_m5stack_index.json`

Puis dans **Tools > Board > Boards Manager**, installer :
* **M5Stack** (version officielle)

### 3. Bibliothèques (Library Manager)
Dans **Sketch > Include Library > Manage Libraries**, installer :
* **M5Unified** (par M5Stack) - *Indispensable pour la gestion d'énergie et du micro.*
* **M5GFX** (par M5Stack) - *Gère l'affichage.*

## ⚙️ Configuration du Code

Avant de téléverser, ouvrez le fichier `.ino` et vérifiez les lignes suivantes au début du fichier :

```cpp
// Configuration du Réseau Wi-Fi du Raspberry Pi
const char* WIFI_SSID = "ZEN_CANTINE";
const char* WIFI_PASS = "cantine2026";
// Adresse IP du Serveur (Raspberry Pi)
const char* TARGET_IP = "10.42.0.1";
const int TARGET_PORT = 4210;
```

Pour éviter de mettre vos identifiants dans le sketch, copiez `config_template.h` en `config.h` et remplissez ces valeurs.

Le M5Stick envoie ensuite le message UDP suivant au serveur :

```txt
vol:<valeur_en_dB>
```

Le niveau sonore est calculé en **dB SPL** (Sound Pressure Level) avec la formule :
`dB = 20 × log₁₀(amplitude + 1) + 20`

## Installation

1. Connectez le M5StickC Plus 2 en USB au Mac/PC.
2. Sélectionnez le bon modèle de carte :
    Tools > Board > M5Stack > M5StickCPlus2
3. Sélectionnez le port :
    Tools > Port > /dev/cu.usbserial... (ou COMx sur Windows)
4. Cliquez sur Upload (Flèche droite).

## 🟢 Indicateurs Visuels
- Écran Bleu "WIFI OK" : Connecté au réseau ZenCantine.
- Écran Vert : Niveau sonore acceptable.
- Écran Rouge : Seuil de bruit dépassé (Alerte envoyée).
