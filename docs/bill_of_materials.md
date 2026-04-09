# 🛒 Liste du Matériel (Bill of Materials)

> 📖 **Documentation disponible en:** [English](bill_of_materials.en.md) | [Français](bill_of_materials.md)

Voici la liste des composants nécessaires pour assembler une unité "ZenCantine".

## 📦 Matériel Principal

| Composant | Modèle Recommandé | Qté | Description |
| :--- | :--- | :---: | :--- |
| **Cerveau / Serveur** | Raspberry Pi 3B+, 4, ou Zero 2 W | 1 | Sert de routeur Wi-Fi et de serveur de contrôle. |
| **Carte MicroSD** | 16 Go minimum | 1 | Classe 10 recommandée pour l'OS du Raspberry. |
| **Capteur Sonore** | M5StickC Plus 2 | 1 | Micro-contrôleur avec écran et micro intégré (ESP32). |
| **Indicateur Lumineux** | WLED compatible (ruban LED ou bande) | 1 | Lampe connectée compatible WLED et contrôle HTTP. |

## 📦 Matériel Testé et Approuvé

| Composant | Description |
| :--- | :--- |
| **Cerveau / Serveur** | Kit Raspberry Pi Zéro 2 W,WH - Starter - De chez Kubii
| **Carte MicroSD** | Carte intégrée dans le Kit |
| **Capteur Sonore** | M5Stack M5StickC PLUS2 Kit de développement IoT ESP32 | WiFi, IR | IMU 6 axes, microphone, RTC, LCD, batterie intégrée, buzzer passif  |
| **Indicateur Lumineux** | Bande LED contrôlée par WLED, RGB(W) ou RGBIC | 1 | Bande LED compatible WLED pour affichage couleur via HTTP. |

## 🔌 Alimentation & Câbles

| Composant | Détails | Qté |
| :--- | :--- | :---: |
| **Alimentation RPi** | USB-C ou Micro-USB (selon modèle) | 1 | 5V / 2.5A minimum recommandé. |
| **Câble USB-C** | USB-A vers USB-C | 1 | Pour alimenter le M5StickC Plus 2. |
| **Support de fixation** | (Optionnel) | 1 | Pour fixer le M5Stick au mur ou plafond. |

## 💻 Logiciels Requis

* **Raspberry Pi OS** (Lite).
* **Arduino IDE** (pour programmer le M5Stick).
* **Interface WLED** ou **WLED mobile** pour la configuration initiale.
