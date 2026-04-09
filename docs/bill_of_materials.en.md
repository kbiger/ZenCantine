# 🛒 Bill of Materials

Here is the list of components needed to assemble a "ZenCantine" unit.

## 📦 Main Hardware

| Component | Recommended Model | Qty | Description |
| :--- | :--- | :---: | :--- |
| **Brain / Server** | Raspberry Pi 3B+, 4, or Zero 2 W | 1 | Serves as Wi-Fi router and control server. |
| **MicroSD Card** | 16 GB minimum | 1 | Class 10 recommended for Raspberry OS. |
| **Sound Sensor** | M5StickC Plus 2 | 1 | Microcontroller with screen and integrated microphone (ESP32). |
| **Light Indicator** | WLED compatible (LED strip or band) | 1 | Connected lamp compatible with WLED and HTTP control. |

## 📦 Tested and Approved Hardware

| Component | Description |
| :--- | :--- |
| **Brain / Server** | Raspberry Pi Zero 2 W,WH - Starter Kit - From Kubii
| **MicroSD Card** | Card included in the Kit |
| **Sound Sensor** | M5Stack M5StickC PLUS2 IoT Development Kit ESP32 | WiFi, IR | 6-axis IMU, microphone, RTC, LCD, integrated battery, passive buzzer |
| **Light Indicator** | LED strip controlled by WLED, RGB(W) or RGBIC | 1 | WLED compatible LED strip for color display via HTTP. |

## 🔌 Power & Cables

| Component | Details | Qty |
| :--- | :--- | :---: |
| **RPi Power Supply** | USB-C or Micro-USB (depending on model) | 1 | 5V / 2.5A minimum recommended. |
| **USB-C Cable** | USB-A to USB-C | 1 | To power the M5StickC Plus 2. |
| **Mounting Support** | (Optional) | 1 | To fix the M5Stick to wall or ceiling. |

## 💻 Required Software

* **Raspberry Pi OS** (Lite).
* **Arduino IDE** (to program the M5Stick).
* **WLED Interface** or **WLED mobile** for initial configuration.