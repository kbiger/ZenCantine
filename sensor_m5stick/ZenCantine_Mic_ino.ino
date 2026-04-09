#include <M5Unified.h>
#include <WiFi.h>
#include <WiFiUdp.h>
#include "config.h"

WiFiUDP udp;
static int16_t record_data[256];

// Fonction pour calculer les dB à partir de l'amplitude
float calculateDB(int amplitude) {
    if (amplitude <= 0) return 0.0;
    // Formule approximative : dB = 20 * log10(amplitude / référence)
    // On utilise une référence arbitraire et on ajoute un offset pour des valeurs positives
    return 20.0 * log10((float)amplitude + 1.0) + 20.0;  // +20 pour avoir des valeurs positives
}

void setup() {
    auto cfg = M5.config();
    cfg.internal_spk = false; 
    M5.begin(cfg);
    
    M5.Display.setRotation(3);
    M5.Display.setTextSize(2);
    
    // --- Config Micro ---
    auto mic_cfg = M5.Mic.config();
    mic_cfg.sample_rate = 16000;
    mic_cfg.magnification = 128; 
    M5.Mic.config(mic_cfg);
    M5.Mic.begin();

    // --- Connexion Wi-Fi ---
    M5.Display.fillScreen(TFT_BLUE);
    M5.Display.setCursor(0, 0);
    M5.Display.println("Connexion...");
    M5.Display.println(WIFI_SSID); // Affiche le nom du réseau
    
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    
    // Boucle d'attente
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        M5.Display.print(".");
    }
    
    // --- Succès ---
    M5.Display.fillScreen(TFT_GREEN);
    M5.Display.setCursor(0, 0);
    M5.Display.setTextColor(TFT_BLACK);
    M5.Display.println("WIFI OK !");
    M5.Display.printf("Cible: %s", TARGET_IP);
    delay(2000);
}

void loop() {
    M5.update();
    
    // Enregistrement du son
    if (M5.Mic.record(record_data, 256, 16000)) {
        long sum = 0;
        for (int i = 0; i < 256; i++) sum += abs(record_data[i]);
        int raw_volume = (sum / 256) / 3; 
        
        // Calcul du niveau en dB
        float db_level = calculateDB(raw_volume);

        // Envoi UDP en utilisant les variables de config.h
        udp.beginPacket(TARGET_IP, TARGET_PORT);
        udp.printf("vol:%.1f", db_level);  // Envoi avec 1 décimale
        udp.endPacket();

        // --- Affichage Visuel ---
        M5.Display.setCursor(0, 40);
        
        // Seuil visuel local (juste pour l'écran du micro) - ajusté pour dB
        if(db_level > 70) M5.Display.fillScreen(TFT_RED);
        else M5.Display.fillScreen(TFT_BLACK);
        
        M5.Display.setCursor(10, 60);
        M5.Display.setTextColor(TFT_WHITE);
        M5.Display.setTextSize(3);
        M5.Display.printf("%.1f dB", db_level);
        
        delay(20); 
    }
}