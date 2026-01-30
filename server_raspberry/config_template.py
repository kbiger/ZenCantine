# RENOMMEZ CE FICHIER EN "config.py"


# ==========================================
# ⚙️ CONFIGURATION RÉSEAU (PROD)
# ==========================================
# Le Raspberry Pi (Server)
MY_PI_IP = "0.0.0.0"
UDP_PORT = 4210

# La Lampe Govee (Actuator)
GOVEE_IP = "192.168.1.xxx"
GOVEE_PORT = 4003

# ==========================================
# 🎚️ RÉGLAGES SENSIBILITÉ (CANTINE)
# ==========================================
# Taille de la mémoire tampon (Moyenne glissante)
# 5  = Très réactif (Test)
# 20 = Équilibré (Production - env. 2 sec)
# 50 = Lent (Très stable)
BUFFER_SIZE = 20
# Seuils de volume (0 à 120)
SEUIL_TRIGGER = 80 # Seuil pour passer au ROUGE
SEUIL_RESET = 60 # Seuil pour revenir au VERT
