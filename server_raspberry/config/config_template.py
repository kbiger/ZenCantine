# RENOMMEZ CE FICHIER EN "config.py"


# ==========================================
# ⚙️ CONFIGURATION RÉSEAU (RASPBERRY & WLED)
# ==========================================

# Adresse de la lampe WLED (Celle définie dans WLED > Config > WiFi)
WLED_IP = "10.42.0.10"
WLED_PORT = 80

# Port d'écoute UDP (Pour recevoir le son du M5Stick)
UDP_PORT = 4210
UDP_IP = "0.0.0.0" # On écoute sur toutes les interfaces

# Nom du fichier de base de données
DB_FILE = "zencantine.db"

# ==========================================
# 🎚️ RÉGLAGES SENSIBILITÉ (CANTINE)
# ==========================================

# Seuils de volume en dB SPL (valeurs typiques : 30-80 dB)
# Ajuste ces valeurs lors du premier repas !
SEUIL_TRIGGER = 65  # Niveau pour passer au ROUGE (Alerte) - environ 65 dB
SEUIL_RESET   = 55  # Niveau pour revenir au VERT (Calme) - environ 55 dB

# Lissage (Moyenne Glissante)
# Permet d'éviter que la lumière clignote sur un bruit bref (chute d'objet)
# 1  = Réactif immédiat (Pas de lissage)
# 10 = Moyenne sur env. 1 seconde (Recommandé)
# 30 = Très lent (Moyenne sur 3 secondes)
BUFFER_SIZE = 10
