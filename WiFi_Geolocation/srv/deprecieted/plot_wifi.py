import matplotlib.pyplot as plt
import pandas as pd
def calculate_distance_from_rssi(rssi, tx_power=-40, path_loss_exponent=3.0):
    return 10 ** ((tx_power - rssi) / (10 * path_loss_exponent))
def plot_wifi_triangulation(df, estimated_latitude, estimated_longitude, tx_power=-40):
    """
    Plota os pontos de acesso Wi-Fi e a localização estimada com base em um DataFrame.
    O raio dos círculos é calculado com base na fórmula de perda de percurso para o RSSI.

    Parâmetros:
        df (pd.DataFrame): DataFrame com as colunas 'ssid', 'latitude', 'longitude' e 'weight'.
        estimated_latitude (float): Latitude estimada do ponto desconhecido.
        estimated_longitude (float): Longitude estimada do ponto desconhecido.
        tx_power (float): Potência de transmissão em dBm dos pontos de acesso.
        
    Retorna:
        None: Gera um gráfico usando Matplotlib.
    """
    # Verificar se o DataFrame possui as colunas necessárias
    if not {'ssid', 'latitude', 'longitude', 'weight'}.issubset(df.columns):
        raise ValueError("O DataFrame deve conter as colunas: 'ssid', 'latitude', 'longitude', 'weight'")
    
    # Calcular o raio dos círculos usando a fórmula de perda de percurso
    df['distance'] = df['weight'].apply(lambda rssi: calculate_distance_from_rssi(rssi, tx_power=tx_power))
    
    # Criar a figura e o eixo
    plt.figure(figsize=(10, 10))
    
    # Plotar cada ponto de acesso como um círculo com raio proporcional à distância calculada
    for _, row in df.iterrows():
        # Plotar círculo com o raio calculado a partir do RSSI
        circle = plt.Circle((row['longitude'], row['latitude']), radius=row['distance'], color='r', fill=False, linestyle='--')
        plt.gca().add_patch(circle)
        
        # Adicionar o ponto central do ponto de acesso
        plt.scatter(row['longitude'], row['latitude'], label=f"{row['ssid']} ({row['latitude']:.4f}, {row['longitude']:.4f})")
        plt.text(row['longitude'], row['latitude'], f" {row['ssid']}", fontsize=10, verticalalignment='bottom')
    
    # Plotar a localização estimada
    plt.scatter(estimated_longitude, estimated_latitude, color='b', label=f"Estimated Location ({estimated_latitude:.4f}, {estimated_longitude:.4f})", zorder=5)
    plt.text(estimated_longitude, estimated_latitude, " Estimated", fontsize=12, verticalalignment='bottom', horizontalalignment='right')
    
    # Definir limites de visualização com base no alcance dos pontos de acesso
    margin = 0.01
    plt.xlim(df['longitude'].min() - margin, df['longitude'].max() + margin)
    plt.ylim(df['latitude'].min() - margin, df['latitude'].max() + margin)
    
    # Títulos e legendas
    plt.title("Wi-Fi Access Points Triangulation with Distance-Based Radius")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    
    # Mostrar o gráfico
    plt.show()

# Exemplo de uso com dados fictícios
data = {
    'ssid': ['AP1', 'AP2', 'AP3', 'AP4'],
    'latitude': [50.019, 48.846, 68.844, 48.843],
    'longitude': [2.356, 5.357, 9.355, 2.358],
    'weight': [0.01, 0.02, 0.015, 0.025]
}

# Criar DataFrame com os pontos de acesso
df_example = pd.DataFrame(data)

# Definir a localização estimada
estimated_lat = 48.8455
estimated_lon = 2.3565

# Plotar usando a função
plot_wifi_triangulation(df_example, estimated_lat, estimated_lon)
