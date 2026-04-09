import socket
import threading
import sqlite3
import time
import requests
import datetime
from collections import deque
from flask import Flask, render_template, jsonify, request

# --- IMPORT DE LA CONFIGURATION ---
import config

app = Flask(__name__)

# Variables globales
current_volume = 0
is_alert_state = False

# Seuils configurables (initialisés depuis config)
seuil_trigger = config.SEUIL_TRIGGER
seuil_reset = config.SEUIL_RESET
buffer_size = config.BUFFER_SIZE

# Buffer pour la moyenne glissante (Lissage du bruit)
volume_buffer = deque(maxlen=buffer_size)

# Offset de temps pour ajustement manuel (secondes)
time_offset = config.TIME_OFFSET

# Fonction pour obtenir l'heure actuelle ajustée
def get_current_time():
    return time.time() + time_offset

# --- BASE DE DONNEES ---
def get_db_connection():
    conn = sqlite3.connect(config.DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS mesures 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  timestamp REAL, 
                  volume INTEGER, 
                  is_alert INTEGER)''')
    conn.commit()
    conn.close()

# --- PILOTAGE WLED ---
def set_wled_color(alert):
    global is_alert_state
    if alert == is_alert_state: return

    try:
        if alert:
            # ROUGE : Pleine puissance
            payload = {"on": True, "bri": 255, "seg": [{"col": [[255, 0, 0]], "fx": 0}]}
        else:
            # VERT : Puissance réduite (plus doux)
            payload = {"on": True, "bri": 100, "seg": [{"col": [[0, 255, 0]], "fx": 0}]}
        
        requests.post(f"http://{config.WLED_IP}/json/state", json=payload, timeout=0.5)
        is_alert_state = alert
        print(f"Changement état: {'ROUGE' if alert else 'VERT'}")
    except Exception as e:
        print(f"Erreur WLED: {e}")

# --- ECOUTE UDP ET LOGIQUE ---
def udp_listener():
    global current_volume
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((config.UDP_IP, config.UDP_PORT))
    
    last_record = 0
    print(f"📡 Ecoute UDP sur le port {config.UDP_PORT}")
    
    while True:
        try:
            data, _ = sock.recvfrom(1024)
            msg = data.decode('utf-8')
            
            if "vol:" in msg:
                # 1. Récupération de la valeur en dB (float)
                try:
                    raw_vol = float(msg.split(":")[1])
                except ValueError:
                    print(f"Erreur parsing volume: {msg}")
                    continue
                
                # 2. Ajout au buffer (Moyenne glissante)
                volume_buffer.append(raw_vol)
                
                # 3. Calcul de la moyenne des N dernières valeurs
                avg_vol = sum(volume_buffer) / len(volume_buffer)
                current_volume = round(avg_vol, 1)  # Arrondi à 1 décimale
                
                # 4. Décision (Hystérésis) - seuils ajustés pour dB
                if current_volume > seuil_trigger:
                    set_wled_color(True)
                elif current_volume < seuil_reset:
                    set_wled_color(False)
                
                # 5. Enregistrement DB (Toutes les 2 sec)
                now = get_current_time()
                if now - last_record > 2:
                    conn = get_db_connection()
                    conn.execute("INSERT INTO mesures (timestamp, volume, is_alert) VALUES (?, ?, ?)", 
                                 (now, current_volume, 1 if is_alert_state else 0))
                    conn.commit()
                    conn.close()
                    last_record = now

        except Exception as e:
            print(f"Erreur boucle UDP: {e}")

# --- API WEB (Reste inchangée visuellement) ---
@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/now')
def api_now():
    return jsonify({"volume": current_volume, "alert": is_alert_state})

@app.route('/api/stats')
def api_stats():
    conn = get_db_connection()
    now = get_current_time()
    midnight = now - (now % 86400)
    
    alerts = conn.execute("SELECT COUNT(*) FROM mesures WHERE is_alert=1 AND timestamp > ?", (midnight,)).fetchone()[0]
    max_vol = conn.execute("SELECT MAX(volume) FROM mesures WHERE timestamp > ?", (midnight,)).fetchone()[0]
    avg_vol = conn.execute("SELECT AVG(volume) FROM mesures WHERE timestamp > ?", (midnight,)).fetchone()[0]
    conn.close()
    
    return jsonify({
        "alerts_today": alerts if alerts else 0,
        "max_volume": max_vol if max_vol else 0,
        "avg_volume": int(avg_vol) if avg_vol else 0
    })

@app.route('/api/history')
def api_history():
    period = request.args.get('range', 'hour')
    conn = get_db_connection()
    now = get_current_time()
    
    if period == 'day':
        start_time = now - 86400
        # Moyenne par 5 min pour 24h
        query = "SELECT AVG(volume) as vol, MIN(timestamp) as time FROM mesures WHERE timestamp > ? GROUP BY CAST(timestamp / 300 AS INTEGER) ORDER BY time ASC"
    else:
        start_time = now - 3600
        # Toutes les données pour 1h
        query = "SELECT volume as vol, timestamp as time FROM mesures WHERE timestamp > ? ORDER BY time ASC"

    rows = conn.execute(query, (start_time,)).fetchall()
    conn.close()
    
    data = []
    for row in rows:
        data.append({
            "time": row['time'],
            "vol": int(row['vol'])
        })
        
    return jsonify(data)

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify({
        "seuil_trigger": seuil_trigger,
        "seuil_reset": seuil_reset,
        "buffer_size": buffer_size
    })

@app.route('/api/config', methods=['POST'])
def update_config():
    global seuil_trigger, seuil_reset, buffer_size, volume_buffer
    data = request.get_json()
    
    # Validation des paramètres
    try:
        new_trigger = int(data.get('seuil_trigger'))
        new_reset = int(data.get('seuil_reset'))
        new_buffer = int(data.get('buffer_size'))
    except (TypeError, ValueError):
        return jsonify({"error": "Tous les paramètres doivent être des entiers"}), 400
    
    if new_trigger <= new_reset:
        return jsonify({"error": "Le seuil d'alerte doit être supérieur au seuil de reset"}), 400
    
    if new_buffer < 1 or new_buffer > 100:
        return jsonify({"error": "La taille du buffer doit être entre 1 et 100"}), 400
    
    if new_trigger < 30 or new_trigger > 100 or new_reset < 30 or new_reset > 100:
        return jsonify({"error": "Les seuils doivent être entre 30 et 100 dB"}), 400
    
    seuil_trigger = new_trigger
    seuil_reset = new_reset
    
    # Si buffer_size change, recréer le buffer
    if buffer_size != new_buffer:
        buffer_size = new_buffer
        volume_buffer = deque(volume_buffer, maxlen=buffer_size)  # Garde les données existantes si possible
    
    # Sauvegarder dans le fichier config.py pour persistance
    try:
        with open('/Users/kevin/dev/ZenCantine/server_raspberry/config/config.py', 'r') as f:
            content = f.read()
        
        # Remplacer les valeurs
        content = content.replace(f'SEUIL_TRIGGER = {config.SEUIL_TRIGGER}', f'SEUIL_TRIGGER = {seuil_trigger}')
        content = content.replace(f'SEUIL_RESET = {config.SEUIL_RESET}', f'SEUIL_RESET = {seuil_reset}')
        content = content.replace(f'BUFFER_SIZE = {config.BUFFER_SIZE}', f'BUFFER_SIZE = {buffer_size}')
        
        with open('/Users/kevin/dev/ZenCantine/server_raspberry/config/config.py', 'w') as f:
            f.write(content)
        
        # Recharger le module config pour les futures importations
        import importlib
        importlib.reload(config)
        
        return jsonify({"message": "Configuration mise à jour"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/config/reset', methods=['POST'])
def reset_config():
    global seuil_trigger, seuil_reset, buffer_size, volume_buffer, time_offset
    
    # Valeurs par défaut depuis le template
    default_trigger = 65
    default_reset = 55
    default_buffer = 10
    
    seuil_trigger = default_trigger
    seuil_reset = default_reset
    buffer_size = default_buffer
    time_offset = 0.0
    volume_buffer = deque(maxlen=buffer_size)
    
    # Sauvegarder dans le fichier config.py
    try:
        with open('/Users/kevin/dev/ZenCantine/server_raspberry/config/config.py', 'r') as f:
            content = f.read()
        
        # Remplacer les valeurs
        content = content.replace(f'SEUIL_TRIGGER = {config.SEUIL_TRIGGER}', f'SEUIL_TRIGGER = {seuil_trigger}')
        content = content.replace(f'SEUIL_RESET = {config.SEUIL_RESET}', f'SEUIL_RESET = {seuil_reset}')
        content = content.replace(f'BUFFER_SIZE = {config.BUFFER_SIZE}', f'BUFFER_SIZE = {buffer_size}')
        
        # Gérer TIME_OFFSET
        import re
        content = re.sub(r'TIME_OFFSET = [\d.-]+', f'TIME_OFFSET = {time_offset}', content)
        
        with open('/Users/kevin/dev/ZenCantine/server_raspberry/config/config.py', 'w') as f:
            f.write(content)
        
        import importlib
        importlib.reload(config)
        
        return jsonify({"message": "Configuration remise aux valeurs par défaut"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/time', methods=['POST'])
def set_current_time():
    global time_offset
    data = request.get_json()
    
    try:
        # Accepter soit un timestamp Unix, soit une string ISO
        if 'timestamp' in data:
            user_timestamp = float(data['timestamp'])
        elif 'datetime' in data:
            # Parser la string ISO 8601
            from datetime import datetime
            dt = datetime.fromisoformat(data['datetime'].replace('Z', '+00:00'))
            user_timestamp = dt.timestamp()
        else:
            return jsonify({"error": "Paramètre 'timestamp' (float) ou 'datetime' (ISO string) requis"}), 400
        
        # Calculer l'offset
        current_system_time = time.time()
        time_offset = user_timestamp - current_system_time
        
        # Sauvegarder l'offset dans config.py
        try:
            with open('/Users/kevin/dev/ZenCantine/server_raspberry/config/config.py', 'r') as f:
                content = f.read()
            
            # Remplacer ou ajouter TIME_OFFSET
            if 'TIME_OFFSET =' in content:
                import re
                content = re.sub(r'TIME_OFFSET = [\d.-]+', f'TIME_OFFSET = {time_offset}', content)
            else:
                content += f'\nTIME_OFFSET = {time_offset}'
            
            with open('/Users/kevin/dev/ZenCantine/server_raspberry/config/config.py', 'w') as f:
                f.write(content)
            
            import importlib
            importlib.reload(config)
        except Exception as e:
            print(f"Erreur sauvegarde offset: {e}")
        
        return jsonify({"message": f"Heure ajustée. Offset: {time_offset:.1f}s"})
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Format de date/heure invalide: {str(e)}"}), 400

@app.route('/api/time', methods=['GET'])
def get_current_time_api():
    return jsonify({
        "current_time": get_current_time(),
        "system_time": time.time(),
        "offset": time_offset
    })

if __name__ == '__main__':
    init_db()
    t = threading.Thread(target=udp_listener)
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', port=80, debug=False)