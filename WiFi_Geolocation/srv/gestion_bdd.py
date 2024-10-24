import paho.mqtt.client as mqtt
import psycopg2
import sqlite3
import json
import os
from dotenv import load_dotenv

#POSTGRES
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

# Si on veux utiliser SQLite, il faut utiliser la fonction persist_data_sqlite
#SQLite
DB_FILE = 'data/geoloc_data.db'


def persist_data(device_name, lat, lon, wifi_json, db_type='sqlite'):
    """Insère les données reçues dans la base de données"""
    if db_type == 'sqlite':
        persist_data_sqlite(device_name, lat, lon, wifi_json)
    elif db_type == 'postgres':
        persist_data_postgres(device_name, lat, lon, wifi_json)
    else:
        print("Type de base de données inconnu.")


def persist_data_postgres(device_name, lat, lon, wifi_json):
    """Insère les données reçues dans la base de données PostgreSQL"""
    try:
        # Connexion à la base de données PostgreSQL
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            dbname=POSTGRES_DATABASE,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        cursor = conn.cursor()

        # Création de la table si elle n'existe pas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS locations (
                id SERIAL PRIMARY KEY,
                device_name TEXT,
                timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                latitude REAL,
                longitude REAL,
                wifi_networks JSON
            )
        ''')

        # Insertion des données dans la table
        cursor.execute('''
            INSERT INTO locations (device_name, latitude, longitude, wifi_networks)
            VALUES (%s, %s, %s, %s)
        ''', (device_name, lat, lon, wifi_json))

        # Validation de l'insertion dans la base de données
        conn.commit()
        cursor.close()
        conn.close()

        print(f"Les données pour {device_name} ont été enregistrées dans la base de données PostgreSQL.")
    
    except Exception as e:
        print(f"Erreur lors de l'enregistrement dans la base de données PostgreSQL: {e}")

def persist_data_sqlite(device_name, lat, lon, wifi_json):
    """Insère les données reçues dans la base de données SQLite"""
    try:
        # Connexion à la base de données SQLite
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        # Création de la table si elle n'existe pas
        c.execute('''CREATE TABLE IF NOT EXISTS locations
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    device_name TEXT, 
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
                    latitude REAL, 
                    longitude REAL,
                    wifi_networks TEXT)''')  # Colonne pour le JSON des réseaux WiFi
        
        # Insertion des données dans la table
        c.execute("INSERT INTO locations (device_name, latitude, longitude, wifi_networks) VALUES (?, ?, ?, ?)",
                (device_name, lat, lon, wifi_json))
        
        # Validation de l'insertion dans la base de données
        conn.commit()
        conn.close()
    
        print(f"Les données pour {device_name} ont été enregistrées dans la base de données locale SQLite.")
    
    except Exception as e:
        print(f"Erreur lors de l'enregistrement dans la base de données locale SQLite: {e}")