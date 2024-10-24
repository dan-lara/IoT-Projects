import paho.mqtt.client as mqtt
import psycopg2
import json
import os
from dotenv import load_dotenv
from triangulateur import estimate_position
from localisateur import *

def get_location_df(wifis):
    bdd = read_DB_csv_file('BDD.csv')
    wifis = json.dumps(wifis)
    location_df = fetch_locations(bdd, wifis)
    return location_df

DEBUG = False
BDD = 'postgres' # 'sqlite' ou 'postgres'
# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações MQTT a partir do .env
MQTT_BROKER = os.getenv('MQTT_BROKER')
MQTT_USERNAME = os.getenv('MQTT_USERNAME')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')
MQTT_TOPIC = os.getenv('MQTT_TOPIC')

# Configurações do banco de dados PostgreSQL
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

from gestion_bdd import persist_data

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
        if DEBUG:
            print("Device ID:", device_id)
        # Extrair 'received_at'
        received_at = payload.get('received_at', 'desconhecido')
        if DEBUG:
            print("Received:", received_at)
        # Extrair 'Uplink_message -> decoded_payload'
        decoded_payload = payload.get('uplink_message', {}).get('decoded_payload', {})
        
        # Exemplo de manipulação dos dados do payload
        if decoded_payload:
            if DEBUG:
                print(f"Decoded Payload: {decoded_payload}")
            # Exemplo: iterar sobre uma lista de WiFis no decoded_payload, caso exista
            wifis = decoded_payload.get('Networks', [])
            wifi_count = len(wifis)
            
            # Converter a lista de WiFis para JSON string
            wifi_json = json.dumps(wifis)
            # print(f"WiFi JSON: {wifi_json}")
            # Processa cada ponto de acesso Wi-Fi (RSSI, BSSID, etc.)
            if DEBUG:
                for wifi in wifis:
                    bssid = wifi.get('MAC')
                    signal_strength = wifi.get('RSSI')
                    print(f"WiFi MAC: {bssid}, RSSI: {signal_strength}")
        
            location_df = get_location_df(wifis)

            if DEBUG:
                print("Size of Location DataFrame: \n", location_df.shape[0])
            if location_df.shape[0] < 3:
                print("O DataFrame de localização deve ter pelo menos 3 linhas.")
                return
            position = estimate_position(location_df)[0:2]
            persist_data(device_id, float(position[0]), float(position[1]), wifi_json,BDD)
            print(f"Dados recebidos e salvos para {device_id} em {received_at}: Payload Decoded com {wifi_count} WiFis")
            return position
        else:
            print("Payload decodificado ausente ou vazio.")
            wifi_json = json.dumps([])  # Caso não haja redes, salvar uma lista vazia

        
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
    except KeyError as e:
        print(f"Erro de chave faltando no JSON: {e}")

client = mqtt.Client()
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

# Conectar ao broker e iniciar o loop
client.connect(MQTT_BROKER, 1883, 60)
client.loop_forever()
