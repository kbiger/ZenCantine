import socket
import json
import time

# ==========================================
# ⚙️ CONFIGURATION RÉSEAU (PROD)
# ==========================================
# Le Raspberry Pi (Server)
MY_PI_IP = "10.42.0.1"
UDP_PORT = 4210

# La Lampe Govee (Actuator)
GOVEE_IP = "10.42.0.169"
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
SEUIL_TRIGGER = 80       # Seuil pour passer au ROUGE
SEUIL_RESET = 60         # Seuil pour revenir au VERT

# ==========================================
# 🔧 FONCTIONS
# ==========================================

def send_govee_color(r, g, b):
    """Envoie une commande couleur à la lampe Govee via UDP"""
    msg = {
        "msg": {
            "cmd": "color",
            "data": {
                "color": {
                    "r": r,
                    "g": g,
                    "b": b
                }
            }
        }
    }
    try:
        sock_govee = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        json_data = json.dumps(msg).encode('utf-8')
        sock_govee.sendto(json_data, (GOVEE_IP, GOVEE_PORT))
    except Exception as e:
        print(f"❌ Erreur Govee: {e}")

# ==========================================
# 🚀 DÉMARRAGE
# ==========================================

print("🚀 Démarrage ZenCantine...")
print(f"👂 Écoute sur {MY_PI_IP}:{UDP_PORT}")
print(f"💡 Lampe cible: {GOVEE_IP}")

# Configuration du socket UDP (Serveur)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Cette ligne permet de relancer le script sans attendre si le port est bloqué
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    sock.bind((MY_PI_IP, UDP_PORT))
except Exception as e:
    print(f"❌ Erreur liaison serveur: {e}")
    exit()

# Variables d'état
volume_buffer = []
is_red = False

# Initialisation : On met la lampe au vert au démarrage
send_govee_color(0, 255, 0)
print("🟢 Démarrage : Lampe VERTE")

# ==========================================
# 🔄 BOUCLE PRINCIPALE
# ==========================================
while True:
    try:
        # 1. Réception du message du M5Stick
        data, addr = sock.recvfrom(1024)
        message = data.decode('utf-8')
        
        # On attend un JSON type {"vol": 45}
        if "vol" in message:
            data_json = json.loads(message)
            vol = data_json["vol"]
            
            # 2. Ajout au buffer (Moyenne glissante)
            volume_buffer.append(vol)
            if len(volume_buffer) > BUFFER_SIZE:
                volume_buffer.pop(0)
            
            # Calcul de la moyenne
            avg_vol = sum(volume_buffer) / len(volume_buffer)
            
            # Affichage console (Optionnel, pour debug)
            # print(f"Vol: {vol} | Moy: {int(avg_vol)}")

            # 3. Prise de décision
            if not is_red and avg_vol > SEUIL_TRIGGER:
                # C'est trop fort -> ROUGE
                print(f"🔴 BRUIT DÉTECTÉ ! Moyenne: {int(avg_vol)}")
                send_govee_color(255, 0, 0)
                is_red = True
            
            elif is_red and avg_vol < SEUIL_RESET:
                # C'est calmé -> VERT
                print(f"🟢 Retour au calme. Moyenne: {int(avg_vol)}")
                send_govee_color(0, 255, 0)
                is_red = False

    except json.JSONDecodeError:
        print("⚠️ Erreur lecture JSON")
    except Exception as e:
        print(f"⚠️ Erreur: {e}")