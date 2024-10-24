import json
import pandas as pd
import numpy as np

# Carregar dados do JSON (modifique o caminho se necessário)
json_file = 'wifi_data.json'

# Carregar o conteúdo do JSON
with open(json_file, 'r') as file:
    data = json.load(file)

# Função para filtrar e organizar os pontos de acesso
def parse_wifi_data(json_data):
    """
    Extrai e organiza os pontos de acesso do JSON.
    
    Parâmetros:
        json_data (dict): Conteúdo do JSON com pontos de acesso Wi-Fi.
        
    Retorna:
        pd.DataFrame: DataFrame com as colunas 'ssid', 'mac', 'latitude', 'longitude', 'signal_strength'.
    """
    wifi_points = []
    
    # Iterar pelos resultados e extrair informações necessárias
    for entry in json_data.get('results', []):
        # print(entry)
        wifi_points.append({
            "ssid": entry.get('ssid'),
            "mac": entry.get('netid'),
            "latitude": entry.get('trilat'),
            "longitude": entry.get('trilong'),
            "signal_strength": entry.get('qos')  # Neste exemplo, 'qos' é usado como força do sinal
        })
    
    # Criar um DataFrame para fácil manipulação
    wifi_df = pd.DataFrame(wifi_points)
    
    # Filtrar apenas pontos com coordenadas válidas
    wifi_df = wifi_df.dropna(subset=['latitude', 'longitude'])
    
    return wifi_df

# Função de triangulação ponderada
def triangulate_location(wifi_df):
    """
    Calcula a localização estimada usando a triangulação ponderada dos pontos de acesso.
    
    Parâmetros:
        wifi_df (pd.DataFrame): DataFrame com 'latitude', 'longitude' e 'signal_strength'.
        
    Retorna:
        dict: Dicionário com 'estimated_latitude' e 'estimated_longitude'.
    """
    # Verificar se há pontos de acesso suficientes
    if wifi_df.empty or len(wifi_df) < 3:
        return {"error": "Insufficient data for triangulation"}

    # Calcular peso baseado na força do sinal (quanto maior, mais forte)
    wifi_df['weight'] = wifi_df['signal_strength'].apply(lambda x: 1 / (x + 1e-9) if x != 0 else 1)
    
    # Calcular latitude e longitude ponderadas
    weighted_lat = np.average(wifi_df['latitude'], weights=wifi_df['weight'])
    weighted_lon = np.average(wifi_df['longitude'], weights=wifi_df['weight'])
    
    return {"estimated_latitude": weighted_lat, "estimated_longitude": weighted_lon}, wifi_df

# Processar os dados e calcular a localização
wifi_df = parse_wifi_data(data)
estimated_location, new_df = triangulate_location(wifi_df)
print(wifi_df)


# Exibir o resultado
print("Estimated Location:", estimated_location)
from WiFi_Geolocation.srv.deprecieted.plot_wifi import plot_wifi_triangulation
plot_wifi_triangulation(new_df, estimated_location['estimated_latitude'], estimated_location['estimated_longitude'])