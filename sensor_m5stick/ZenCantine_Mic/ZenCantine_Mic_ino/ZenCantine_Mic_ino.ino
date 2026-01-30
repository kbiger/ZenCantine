#include <M5Unified.h>
#include <WiFi.h>
#include <WiFiUdp.h>

// ==========================================
// ⚙️ CONFIGURATION WIFI
// ==========================================
const char* WIFI_SSID = "SSID_WIFI"; // MODIFIER
const char* WIFI_PASS = "PWD_WIFI"; // ODIFIER
const char* TARGET_IP = "10.42.0.1"; // Ton Raspberry Pi
const int TARGET_PORT = 4210;

WiFiUDP udp;

void setup() {
    // 1. CONFIGURATION ANTI-CRASH
    auto cfg = M5.config();
    
    cfg.serial_baudrate = 115200;
    cfg.internal_mic = true;   // ✅ ON VEUT LE MICRO
    cfg.internal_spk = false;  // ❌ ON TUE LE HAUT-PARLEUR (Empêche le bootloop)
    cfg.internal_imu = false;  // Pas besoin de l'accéléromètre
    
    M5.begin(cfg);

    // 2. Ecran
    M5.Display.setRotation(3);
    M5.Display.setBrightness(128);
    M5.Display.fillScreen(TFT_BLACK);
    M5.Display.setTextSize(2);
    M5.Display.setTextColor(TFT_WHITE);

    // 3. WiFi
    M5.Display.println("Connexion WiFi...");
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        M5.Display.print(".");
    }

    M5.Display.fillScreen(TFT_BLUE);
    M5.Display.setCursor(10, 10);
    M5.Display.println("WIFI OK");
    delay(1000);
    
    // 4. Démarrage du Micro via M5Unified (Plus stable)
    M5.Mic.begin();
}

void loop() {
    M5.update();
    
    // --- Lecture du Micro ---
    // On enregistre un petit échantillon
    int16_t raw_data[256];
    if (M5.Mic.record(raw_data, 256, 16000)) {
        
        // Calcul du volume (Moyenne)
        long sum = 0;
        for (int i = 0; i < 256; i++) {
            sum += abs(raw_data[i]);
        }
        float mean = sum / 256.0;
        
        // Gain (Ajuste le 0.05 si nécessaire)
        int volume = (int)(mean * 0.05);
        if (volume > 120) volume = 120;
        
        // --- Affichage ---
        if (volume > 60) {
            M5.Display.fillScreen(TFT_RED);
            M5.Display.setTextColor(TFT_WHITE);
        } else {
            M5.Display.fillScreen(TFT_GREEN);
            M5.Display.setTextColor(TFT_BLACK);
        }
        
        M5.Display.setCursor(50, 40);
        M5.Display.setTextSize(4);
        M5.Display.printf("%d", volume);

        // --- Envoi UDP ---
        udp.beginPacket(TARGET_IP, TARGET_PORT);
        udp.printf("{\"vol\": %d}", volume);
        udp.endPacket();
    }
    
    delay(50);
}
