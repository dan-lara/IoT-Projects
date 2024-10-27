from streamlit_folium import st_folium
from dotenv import load_dotenv 
import streamlit as st
import pandas as pd
import psycopg2
import folium
import locale
import os


from localisateur import read_DB_csv_file

st.set_page_config(layout="wide")
locale.setlocale(locale.LC_TIME, 'fr_FR')

load_dotenv()

POSTGRES_HOST = str(os.getenv('POSTGRES_HOST'))
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
BDD_PATH = os.getenv('BDD_PATH')

# Cache the database connection
@st.cache_resource
def init_connection():
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            dbname=POSTGRES_DATABASE,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            client_encoding='utf8'
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to database: {str(e)}")
        return None

# Cache the data fetching function
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_data():
    with init_connection() as conn:
        try:
            query = """
                SELECT id, device_name, timestamp, latitude, longitude, wifi_networks
                FROM locations
                ORDER BY timestamp DESC
            """
            df = pd.read_sql(query, conn)
            # Convert timestamp to local timezone
            df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_convert('Europe/Paris')
            return df
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
            return pd.DataFrame()

# Function to get unique device names
@st.cache_data
def get_device_names(df):
    return sorted(df['device_name'].unique())

# Function to get unique device names
@st.cache_data
def get_wifi_database():
    return read_DB_csv_file(BDD_PATH)

# Function to filter dataframe based on selections
def filter_dataframe(df, selected_devices, date_range):
    mask = (
        (df['device_name'].isin(selected_devices)) &
        (df['timestamp'].dt.date >= date_range[0]) &
        (df['timestamp'].dt.date <= date_range[1])
    )
    return df[mask]

def process_wifi_networks(networks):
    # Convert list of dictionaries to DataFrame for better handling
    networks_df = pd.DataFrame(networks)
    # Sort by RSSI strength (less negative is stronger)
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
        st.error(f"Error fetching locations: {str(e)}")
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
        st.error(f"Error plotting map: {str(e)}")

# Main Streamlit app
def main():
    st.title("Device Location Viewer")
    
    # Fetch initial data
    try:
        df = fetch_data()
    except Exception as e:
        st.error(f"Error connecting to database: {str(e)}")
        return

    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Device selection
    device_names = get_device_names(df)
    selected_devices = st.sidebar.multiselect(
        "Select Devices",
        options=device_names,
        default=device_names
    )
    
    # Date range selection
    min_date = df['timestamp'].dt.date.min()
    max_date = df['timestamp'].dt.date.max()
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Ensure date_range is a tuple of two dates
    if isinstance(date_range, tuple):
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range
    
    # Filter data based on selections
    filtered_df = filter_dataframe(df, selected_devices, (start_date, end_date))
    
    # Display filtered data
    col1, col2 = st.columns([5, 3])
    
    
    with col2: 
        st.subheader("Selected Point Details")
        select_line = st.empty()
        st.subheader("Data Points")
        # Format the timestamp for display
        display_df = filtered_df.copy()
        display_df['timestamp'] = display_df['timestamp'].dt.strftime('%d %B %Y, %H:%M')

        st.dataframe(
            display_df[['id', 'device_name', 'timestamp', 'latitude', 'longitude']],
            hide_index=True,
            height=540
        )
    
    with col2:
        selected_id = select_line.selectbox(
            "Select Point ID",
            options=filtered_df['id'].tolist(),
            format_func=lambda x: f"ID: {x} ({filtered_df[filtered_df['id'] == x]['timestamp'].iloc[0].strftime('%d %B %Y %H:%M')})"
        )
        
        if selected_id:
            selected_row = filtered_df[filtered_df['id'] == selected_id].iloc[0]
            
            st.sidebar.write("Device:", selected_row['device_name'])
            st.sidebar.write("Date :", selected_row['timestamp'].strftime('%d %B %Y, %H:%M'))
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
                    st.error(f"Error plotting map: {str(e)}")
                

if __name__ == "__main__":
    main()