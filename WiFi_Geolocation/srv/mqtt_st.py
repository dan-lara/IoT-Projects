import streamlit as st
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do banco de dados PostgreSQL
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
# Função para conectar ao banco de dados PostgreSQL
@st.cache_resource
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            dbname=POSTGRES_DATABASE,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        return conn
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para buscar dados do banco de dados
@st.cache_data
def fetch_data():
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()

    try:
        query = "SELECT id, device_name, timestamp, latitude, longitude, wifi_networks FROM locations ORDER BY timestamp DESC"
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Erro ao buscar dados do banco de dados: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

# Título do App
st.title("Visualização de Dados IoT - Localizações e Redes WiFi")

# Carregar os dados
data = fetch_data()
# Verificar se há dados disponíveis
if data.empty:
    st.warning("Nenhum dado disponível no momento.")
else:
    st.subheader("Dados Recebidos")

    # Exibir os dados em formato de tabela
    st.dataframe(data)

    # Selecione um dispositivo para visualizar mais detalhes
    device_id = st.number_input("Insert a number",step=1)#st.selectbox("Selecione o dispositivo", data['device_name'].unique())

    # Filtrar os dados para o dispositivo selecionado
    filtered_data = data[data['id'] == device_id]

    # Exibir os detalhes
    st.subheader(f"Detalhes do dispositivo: {device_id}")
    # st.map(filtered_data[['latitude', 'longitude']])
    
    # Exibir os detalhes das redes WiFi em formato JSON
    st.subheader("Redes WiFi detectadas")
    wifi_details = filtered_data['wifi_networks'].iloc[0]
    st.json(wifi_details)
