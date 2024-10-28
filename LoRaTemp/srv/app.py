from sqlalchemy import create_engine
from dotenv import load_dotenv 
import streamlit as st
import pandas as pd
import os

load_dotenv()

POSTGRES_HOST = str(os.getenv('POSTGRES_HOST'))
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
BDD_PATH = os.getenv('BDD_PATH')

# Cache the database connection
def init_connection():
    try:
        conn_str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
        conn = create_engine(conn_str)
        return conn
    except Exception as e:
        st.error(f"Erreur de connexion à la base de données : {str(e)}")
        return None

# Cache the data fetching function
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_data():
    try:
        conn = init_connection()
        query = """
            SELECT id, device_name, timestamp, temperature, humidity
            FROM sensor_data
            ORDER BY timestamp
        """
        df = pd.read_sql(query, conn)
        # Convert timestamp to local timezone
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_convert('Europe/Paris')
        return df
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {str(e)}")
        return pd.DataFrame()

# Function to get unique device names
@st.cache_data
def get_device_names(df):
    return sorted(df['device_name'].unique())

# Function to get unique device names
@st.cache_data
def get_wifi_database():
    return pd.read_csv(BDD_PATH, delimiter=';', encoding='ISO-8859-1')

# Function to filter dataframe based on selections
def filter_dataframe(df, selected_devices, date_range, time_range):
    mask = (
        (df['device_name'].isin(selected_devices)) &
        (df['timestamp'].dt.date >= date_range[0]) &
        (df['timestamp'].dt.date <= date_range[1]) &
        (df['timestamp'].dt.time >= time_range[0]) &
        (df['timestamp'].dt.time <= time_range[1])
    )
    return df[mask]

def main():
    st.set_page_config(page_title="TP3 - Température/Humidité LoRa", page_icon=":thermometer:", layout="wide")
    LOGO_PATH = os.getenv('LOGO_PATH')
    ICON_PATH = os.getenv('ICON_PATH')
    st.logo(
        image=LOGO_PATH,
        icon_image=ICON_PATH,
        size="large"
    )
    st.title("Analyse des données du capteur DHT")
    
    # Fetch initial data
    try:
        df = fetch_data()
    except Exception as e:
        st.error(f"Erreur de connexion à la base de données : {str(e)}")
        return

    # Sidebar filters
    st.sidebar.header("Filtres")
    
    # Device selection
    device_names = get_device_names(df)
    selected_devices = st.sidebar.multiselect(
        "Sélectionnez les appareils",
        options=device_names,
        default=device_names
    )
    
    # Date range selection
    min_date = df['timestamp'].dt.date.min()
    max_date = df['timestamp'].dt.date.max()
    try:
        date_range = st.sidebar.date_input(
            "Sélectionnez la plage de dates",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        # Ensure date_range is a tuple of two dates
        if isinstance(date_range, tuple):
            start_date, end_date = date_range
        else:
            start_date = end_date = date_range
    except Exception as e:
        st.warning("Vous devez sélectionner une plage de dates")
        return
    try:
        # Time range selection
        min_time = df['timestamp'].dt.time.min()
        max_time = df['timestamp'].dt.time.max()
        time_range = st.sidebar.slider(
            "Sélectionnez la plage horaire",
            value=(min_time, max_time),
            format="HH:mm",
            min_value=min_time,
            max_value=max_time
        )
    except Exception as e:
        st.warning("Vouz devez sélectionner une plage horaire")
        return
    # Filter data based on selections
    filtered_df = filter_dataframe(df, selected_devices, (start_date, end_date), time_range)

    # Display filtered data
    col1, col2 = st.columns([5, 3])

    with col1:
        st.subheader("Graphique de température")
        st.line_chart(filtered_df.set_index('timestamp')[['temperature']], use_container_width=True)
        st.subheader("Graphique d'humidité")
        st.line_chart(filtered_df.set_index('timestamp')[['humidity']], use_container_width=True)

    with col2:
        st.subheader("Détails des points de données sélectionnés")
        display_df = filtered_df.copy()
        display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d, %H:%M')

        st.dataframe(
            display_df[['id', 'device_name', 'timestamp', 'temperature', 'humidity']],
            hide_index=True,
            height=540,
            use_container_width=True
        )

if __name__ == "__main__":
    main()