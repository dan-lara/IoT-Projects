from streamlit_folium import st_folium
from dotenv import load_dotenv 
import streamlit as st
import pandas as pd
import folium
# import locale
import os
from sqlalchemy import create_engine

# locale.setlocale(locale.LC_TIME, 'fr_FR')

load_dotenv()
POSTGRES_HOST = str(os.getenv('POSTGRES_HOST'))
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
BDD_PATH = os.getenv('BDD_PATH')

# Mettre en cache la connexion à la base de données
def init_connection():
    try:
        conn_str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
        conn = create_engine(conn_str)
        # conn = psycopg2.connect(
        #     host=POSTGRES_HOST,
        #     port=POSTGRES_PORT,
        #     dbname=POSTGRES_DATABASE,
        #     user=POSTGRES_USER,
        #     password=POSTGRES_PASSWORD,
        #     client_encoding='utf8'
        # )
        # conn.autocommit = True
        return conn
    except Exception as e:
        st.error(f"Erreur de connexion à la base de données : {str(e)}")
        return None

# Mettre en cache la fonction de récupération des données
@st.cache_data(ttl=300)  # Cache par 5 minutes
def fetch_data():
    try:
        conn = init_connection()
        query = """
            SELECT id, device_name, timestamp, latitude, longitude, wifi_networks
            FROM locations
            ORDER BY timestamp DESC
        """
        df = pd.read_sql(query, conn)

        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_convert('Europe/Paris')
        return df
    
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {str(e)}")
        return pd.DataFrame()

# Mettre en cache la fonction de récupération des noms d'appareils
@st.cache_data
def get_device_names(df):
    return sorted(df['device_name'].unique())

@st.cache_data
def get_wifi_database():
    return pd.read_csv(BDD_PATH, delimiter=';', encoding='ISO-8859-1')

# Fonction pour filtrer le dataframe en fonction des sélections
def filter_dataframe(df, selected_devices, date_range):
    mask = (
        (df['device_name'].isin(selected_devices)) &
        (df['timestamp'].dt.date >= date_range[0]) &
        (df['timestamp'].dt.date <= date_range[1])
    )
    return df[mask]

def process_wifi_networks(networks):
    # Charger les données JSON dans un DataFrame
    networks_df = pd.DataFrame(networks)
    networks_df = networks_df.sort_values('RSSI', ascending=False)
    return networks_df

def fetch_locations(networks):
    # Charger les données JSON dans un DataFrame
    networks_df = pd.DataFrame(networks)
    networks_df.columns = ['MAC', 'RSSI']

    bdd_df = get_wifi_database()
    bdd_df.columns = ['MAC', 'SSID', 'RSSI', 'Latitude', 'Longitude', 'Altitude', 'Acuracy', 'Type']
    
    # Fusionner le DataFrame WiFi avec le DataFrame de localisation en fonction de l'adresse MAC
    location_df = pd.merge(networks_df, bdd_df, on='MAC', how='inner')
    # Renommer la colonne RSSI pour éviter les conflits
    location_df.rename(columns={'RSSI_x': 'RSSI'}, inplace=True)
    # Supprimer les colonnes inutiles
    location_df.drop(['RSSI_y', 'Type'], axis=1, inplace=True)
    # Convertir les colonnes de localisation en type float
    location_df[['Latitude', 'Longitude', 'Altitude', 'Accuracy']] = location_df[['Latitude', 'Longitude', 'Altitude', 'Acuracy']].astype(float)
    # Convertir la colonne RSSI en type int
    location_df['RSSI'] = location_df['RSSI'].astype(int)
    return location_df

def plot_map(latitude, longitude, networks):
    
    try:
        # Vérifier le type de texture et créer la carte
        # Créer la carte
        map = folium.Map(location=[latitude, longitude], zoom_start=18)
        folium.Marker(
            location=[latitude, longitude],
            popup=f"Position Estimée<br>Latitude: {latitude}<br>Longitude: {longitude}",
            icon=folium.Icon(color='green')
        ).add_to(map)

        location_df = fetch_locations(networks)

    except Exception as e:
        st.error(f"Erreur lors de la récupération des endroits : {str(e)}")
    try:
        # Ajouter des cercles pour chaque point avec SSID et RSSI
        for i in range(location_df.shape[0]):
            folium.Marker(
                location=[location_df.iloc[i]['Latitude'], location_df.iloc[i]['Longitude']],
                popup=f"{location_df.iloc[i]['SSID']}<br>RSSI: {location_df.iloc[i]['RSSI']}",
                icon=folium.Icon(color='red')
            ).add_to(map)

        # Affichage de la carte
        st_folium(map, width=800)
        
    except Exception as e:
        st.error(f"Erreur lors de l'affichage de la carte : {str(e)}")

# Main Streamlit app
def main():
    st.set_page_config(page_title="Géolocalisation WiFi", page_icon=":earth_africa:", layout="wide")
    LOGO_PATH = os.getenv('LOGO_PATH')
    ICON_PATH = os.getenv('ICON_PATH')
    st.logo(
        image = LOGO_PATH,
        icon_image = ICON_PATH,
        size = "large")
    st.title("Visualiseur de Localisation des Appareils")
    
    # Récupérer les données initiales
    try:
        df = fetch_data()
    except Exception as e:
        st.error(f"Erreur de connexion à la base de données: {str(e)}")
        return

    # Sidebar filtres
    st.sidebar.header("Filtres")

    # Sélection de l'appareil
    device_names = get_device_names(df)
    selected_devices = st.sidebar.multiselect(
        "Sélectionner l'appareil",
        options=device_names,
        default=device_names
    )
    
    # Sélection de la plage de dates
    min_date = df['timestamp'].dt.date.min()
    max_date = df['timestamp'].dt.date.max()
    try:
        date_range = st.sidebar.date_input(
            "Sélectionner la Plage de Dates",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        # S'assurer que date_range est un tuple de deux dates
        if isinstance(date_range, tuple):
            start_date, end_date = date_range
        else:
            start_date = end_date = date_range
    except Exception as e:
        st.warning("Vous devez sélectionner une plage de dates")
        return
    
    # Filtrer les données en fonction des sélections
    filtered_df = filter_dataframe(df, selected_devices, (start_date, end_date))
    
    # Afficher les données filtrées
    col1, col2 = st.columns([5, 3])
    
    
    with col2: 
        st.subheader("Détails du Point Sélectionné")
        select_line = st.empty()
        st.subheader("Points de Données")
        
        display_df = filtered_df.copy()
        display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d, %H:%M')

        st.dataframe(
            display_df[['id', 'device_name', 'timestamp', 'latitude', 'longitude']],
            hide_index=True,
            height=540,
            use_container_width=True
        )
    
    with col2:
        selected_id = select_line.selectbox(
            "Sélectionner l'ID du Point",
            options=filtered_df['id'].tolist(),
            format_func=lambda x: f"ID: {x} ({filtered_df[filtered_df['id'] == x]['timestamp'].iloc[0].strftime('%Y-%m-%d %H:%M')})"
        )
        
        if selected_id:
            selected_row = filtered_df[filtered_df['id'] == selected_id].iloc[0]
            
            st.sidebar.write("Appareil:", selected_row['device_name'])
            st.sidebar.write("Date :", selected_row['timestamp'].strftime('%Y-%m-%d, %H:%M'))
            st.sidebar.write("Latitude:", selected_row['latitude'])
            st.sidebar.write("Longitude:", selected_row['longitude'])
            with col1:
                try:
                    plot_map(
                        latitude=selected_row['latitude'],
                        longitude=selected_row['longitude'],
                        networks=selected_row['wifi_networks']
                    )
                except Exception as e:
                    st.error(f"Erreur lors de l'affichage de la carte: {str(e)}")
                

if __name__ == "__main__":
    main()