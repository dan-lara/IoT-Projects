import paho.mqtt.client as mqtt
import psycopg2
import sqlite3
import json
import os
from dotenv import load_dotenv

# Configurations de la base de données PostgreSQL
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

# Si on veux utiliser SQLite, il faut utiliser la fonction persist_data_sqlite
# Configurations de la base de données SQLite
DB_FILE = 'data/temp_hum.db'


def persist_data(device_name, temperature, humidity, received_at, db_type='sqlite'):
    """Insère les données reçues dans la base de données"""
    if db_type == 'sqlite':
        persist_data_sqlite(device_name, temperature, humidity, received_at)
    elif db_type == 'postgres':
        persist_data_postgres(device_name, temperature, humidity, received_at)
    else:
        print("Type de base de données inconnu.")


def persist_data_postgres(device_name, temperature, humidity, received_at):
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
            CREATE TABLE IF NOT EXISTS sensor_data (
                id SERIAL PRIMARY KEY,
                device_name TEXT,
                timestamp TIMESTAMPTZ,
                temperature REAL,
                humidity REAL
            )
        ''')

        # Insertion des données dans la table
        cursor.execute('''
            INSERT INTO sensor_data (device_name, temperature, humidity, timestamp)
            VALUES (%s, %s, %s, %s)
        ''', (device_name, temperature, humidity, received_at))

        # Validation de l'insertion dans la base de données
        conn.commit()
        cursor.close()
        conn.close()

        print(f"Les données pour {device_name} ont été enregistrées dans la base de données PostgreSQL.")
    
    except Exception as e:
        print(f"Erreur lors de l'enregistrement dans la base de données PostgreSQL: {e}")

def persist_data_sqlite(device_name, temperature, humidity, received_at):
    """Insère les données reçues dans la base de données SQLite"""
    try:
        # Connexion à la base de données SQLite
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        # Création de la table si elle n'existe pas
        c.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    device_name TEXT, 
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
                    temperature REAL,
                    humidity REAL
                  )''')  
        
        # Insertion des données dans la table
        c.execute('''
            INSERT INTO sensor_data (device_name, temperature, humidity, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (device_name, temperature, humidity, received_at))
        
        # Validation de l'insertion dans la base de données
        conn.commit()
        conn.close()
    
        print(f"Les données pour {device_name} ont été enregistrées dans la base de données locale SQLite.")
    
    except Exception as e:
        print(f"Erreur lors de l'enregistrement dans la base de données locale SQLite: {e}")