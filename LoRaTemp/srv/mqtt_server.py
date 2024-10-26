import paho.mqtt.client as mqtt
import psycopg2
import json
import os
from dotenv import load_dotenv
from gestion_bdd import persist_data

DEBUG = False
BDD = 'postgres' # 'sqlite' ou 'postgres'
# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Configurations MQTT à partir du .env
MQTT_BROKER = os.getenv('MQTT_BROKER')
MQTT_USERNAME = os.getenv('MQTT_USERNAME')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')
MQTT_TOPIC = os.getenv('MQTT_TOPIC')

def on_connect(client, userdata, flags, rc):
    """Callback lors de la connexion au broker MQTT"""
    if rc == 0:
        print("Connecté au broker MQTT!")
        client.subscribe(MQTT_TOPIC)
    else:
        print("Échec de la connexion. Code de retour:", rc)

def on_message(client, userdata, msg):
    """Callback lors de la réception d'un message"""
    try:
        # Décoder le payload du message en JSON
        payload = json.loads(msg.payload.decode())
        
        # Extraire 'device_id'
        device_id = payload.get('end_device_ids', {}).get('device_id', 'inconnu')
        if DEBUG:
            print("Device ID:", device_id)
        # Extraire 'received_at'
        received_at = payload.get('received_at', 'inconnu')
        if DEBUG:
            print("Reçu:", received_at)
        # Extraire 'Uplink_message -> decoded_payload'
        decoded_payload = payload.get('uplink_message', {}).get('decoded_payload', {})
        
        # Exemple de manipulation des données du payload
        if decoded_payload:
            if DEBUG:
                print(f"Payload décodé: {decoded_payload}")
            # Exemple: itérer sur une liste de WiFis dans le decoded_payload, si elle existe
            temperature = float(decoded_payload.get('Temperature', None))
            humidity = float(decoded_payload.get('Humidity', None))
            if DEBUG:
                print(f"Température: {temperature}")
                print(f"Humidité: {humidity}")
            # Persister les données dans la base de données
            persist_data(device_id, temperature, humidity, received_at, db_type=BDD)
        else:
            print("Payload décodé absent ou vide.")

        
    except json.JSONDecodeError as e:
        print(f"Erreur lors du décodage JSON: {e}")
    except KeyError as e:
        print(f"Erreur de clé manquante dans le JSON: {e}")

client = mqtt.Client()
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

# Se connecter au broker et démarrer la boucle
client.connect(MQTT_BROKER, 1883, 60)
client.loop_forever()
