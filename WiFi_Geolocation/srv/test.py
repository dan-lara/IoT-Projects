import paho.mqtt.client as mqtt
import sqlite3
import json
from triangulateur import estimate_position
from localisateur import *
# Configurações MQTT
MQTT_BROKER = "eu1.cloud.thethings.network"
MQTT_PORT = 1883
MQTT_USERNAME = "tp2-iot-dfl@ttn"
MQTT_PASSWORD = "NNSXS.VDCYE6UKMRW5KPSCDLKC3LX3EXUEOPXDAHUXX2A.5XYMCW3M44VVBMA3OY7FWUIWKZOYM6V2HKLLJUBRMSIHKM5AP64Q"
MQTT_TOPIC = "#"

# Configuração do banco de dados SQLite
DB_FILE = 'data/geoloc_data.db'

def persist_data(device_name, lat, lon, wifi_json):
    """Insere os dados recebidos no banco de dados SQLite"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS locations
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  device_name TEXT, 
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
                  latitude REAL, 
                  longitude REAL,
                  wifi_networks TEXT)''')  # Coluna para o JSON das redes WiFi
    
    c.execute("INSERT INTO locations (device_name, latitude, longitude, wifi_networks) VALUES (?, ?, ?, ?)",
              (device_name, lat, lon, wifi_json))
    
    conn.commit()
    conn.close()

def on_connect(client, userdata, flags, rc):
    """Callback quando conectado ao broker MQTT"""
    if rc == 0:
        print("Conectado ao broker MQTT!")
        client.subscribe(MQTT_TOPIC)
    else:
        print("Falha na conexão. Código de retorno:", rc)

def on_message(client, userdata, msg):
    """Callback quando uma mensagem é recebida"""
    try:
        # Decodifica o payload da mensagem em JSON
        payload = json.loads(msg.payload.decode())
        
        # Extrair 'device_id'
        device_id = payload.get('end_device_ids', {}).get('device_id', 'desconhecido')
        print("Device ID:", device_id)
        # Extrair 'received_at'
        received_at = payload.get('received_at', 'desconhecido')
        print("Received:", received_at)
        # Extrair 'Uplink_message -> decoded_payload'
        decoded_payload = payload.get('uplink_message', {}).get('decoded_payload', {})
        
        # Exemplo de manipulação dos dados do payload
        if decoded_payload:
            print(f"Decoded Payload: {decoded_payload}")
            # Exemplo: iterar sobre uma lista de WiFis no decoded_payload, caso exista
            wifis = decoded_payload.get('Networks', [])
            wifi_count = len(wifis)
            
            # Converter a lista de WiFis para JSON string
            wifi_json = json.dumps(wifis)
            # print(f"WiFi JSON: {wifi_json}")
            # Processa cada ponto de acesso Wi-Fi (RSSI, BSSID, etc.)
            for wifi in wifis:
                bssid = wifi.get('MAC')
                signal_strength = wifi.get('RSSI')
                print(f"WiFi MAC: {bssid}, RSSI: {signal_strength}")
    
            bdd = read_DB_csv_file('BDD.csv')
            wifis = json.dumps(wifis)
            location_df = fetch_locations(bdd, wifis)
            
            print("Size of Location DataFrame: \n", location_df.shape[0])
            if location_df.shape[0] < 3:
                print("O DataFrame de localização deve ter pelo menos 3 linhas.")
                return
            # Calcular a posição estimada do dispositivo
            print(location_df)
            position = estimate_position(location_df)[0:2]
            print(f"Posição estimada: {position}")
            # Persistir os dados no SQLite (substitua lat/lon por valores reais se aplicável)
            persist_data(device_id, position[0], position[1], wifi_json)  # Substitua por lat/lon calculados e rssi apropriado
            print(f"Dados recebidos e salvos para {device_id} em {received_at}: Payload Decoded com {wifi_count} WiFis")
            return position
        else:
            print("Payload decodificado ausente ou vazio.")
            wifi_json = json.dumps([])  # Caso não haja redes, salvar uma lista vazia

        
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
    except KeyError as e:
        print(f"Erro de chave faltando no JSON: {e}")

# Configuração do cliente MQTT
client = mqtt.Client()
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

# Conectar ao broker e iniciar o loop
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
