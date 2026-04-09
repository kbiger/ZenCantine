# 🎤 Micro Sensor - M5StickC Plus 2

This folder contains the source code (C++ / Arduino) for the sound detection module.
It measures ambient volume and sends it via UDP to the Raspberry Pi server.

## ⚠️ Important Note (Anti-Crash)
This project specifically uses the **M5Unified** library and not the standard *M5StickCPlus2* library.
Using the standard library causes hardware conflict between the Speaker and Microphone, leading to bootloop.

## 🛠 Software Prerequisites

### 1. Arduino IDE
Download and install [Arduino IDE](https://www.arduino.cc/en/software).

### 2. Board Manager
In IDE preferences, add the URL:
`https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/arduino/package_m5stack_index.json`

Then in **Tools > Board > Boards Manager**, install:
* **M5Stack** (official version)

### 3. Library Manager
In **Sketch > Include Library > Manage Libraries**, install:
* **M5Unified** (by M5Stack) - *Essential for power management and microphone.*
* **M5GFX** (by M5Stack) - *Handles display.*

## ⚙️ Code Configuration

Before uploading, open the `.ino` file and check the following lines at the beginning:

```cpp
// Raspberry Pi Wi-Fi Network Configuration
const char* WIFI_SSID = "ZEN_CANTINE";
const char* WIFI_PASS = "cantine2026";
// Server IP Address (Raspberry Pi)
const char* TARGET_IP = "10.42.0.1";
const int TARGET_PORT = 4210;
```

To avoid putting your credentials in the sketch, copy `config_template.h` to `config.h` and fill in the values.

The M5Stick then sends the following UDP message to the server:

```txt
vol:<dB_value>
```

The sound level is calculated in **dB SPL** (Sound Pressure Level) using the formula:
`dB = 20 × log₁₀(amplitude + 1) + 20`

## Installation

1. Connect the M5StickC Plus 2 via USB to Mac/PC.