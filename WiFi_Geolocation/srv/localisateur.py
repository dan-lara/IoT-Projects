import pandas as pd
import json

def read_DB_csv_file(csv_file):
    # Load CSV file and parse into a pandas DataFrame
    # Charger le fichier CSV et l'analyser dans un DataFrame pandas
    csv_file = 'BDD.csv'
    df = pd.read_csv(csv_file, delimiter=';', encoding='ISO-8859-1')
    df = df.dropna()
    return df

def read_WiFi_json_file(json_file):
    # Define the structure of the JSON output
    # Définir la structure de sortie JSON
    with open(json_file, 'r') as f:
        wifi_data = json.load(f)
    wifi_networks = []

    # Iterate through each row in the DataFrame and create a JSON-like structure
    # Itérer à travers chaque ligne du DataFrame pour créer une structure JSON
    for element in wifi_data.get("Networks", []):
        network = {
            'MAC': element.get('MAC'),
            'SSID': element.get('SSID'),
            'RSSI': element.get('RSSI'),
        }
        wifi_networks.append(network)
    
    wifi_json = json.dumps(wifi_networks, indent=4)
    return wifi_json

def fetch_locations(df, wifi_json):
    # Load the JSON data into a DataFrame
    # Charger les données JSON dans un DataFrame

    wifi_df = pd.read_json(wifi_json)
    
    # Merge the WiFi DataFrame with the location DataFrame based on the MAC address
    # Fusionner le DataFrame WiFi avec le DataFrame de localisation en fonction de l'adresse MAC
    df.columns = ['MAC', 'SSID', 'RSSI', 'Latitude', 'Longitude', 'Altitude', 'Acuracy', 'Type']
    merged_df = pd.merge(wifi_df, df, on='MAC', how='inner')
    print(merged_df.size)
    if merged_df.empty or merged_df.size < 30:
        return search_api()
    merged_df.rename(columns={'SSID_x': 'SSID', 'RSSI_x': 'RSSI'}, inplace=True)
    merged_df.drop(['SSID_y', 'RSSI_y', 'Type'], axis=1, inplace=True)
    merged_df[['Latitude', 'Longitude', 'Altitude', 'Acuracy']] = merged_df[['Latitude', 'Longitude', 'Altitude', 'Acuracy']].astype(float)
    merged_df['RSSI'] = merged_df['RSSI'].astype(int)
    return merged_df

def search_api():
    # Placeholder for API call to fetch location data
    # Placeholder pour l'appel API pour obtenir les données de localisation
    return None

# bdd = read_DB_csv_file('BDD.csv')
# wifi = read_WiFi_json_file('wifi_data.json')
# location_df = fetch_locations(bdd, wifi)
# print("Location DataFrame: \n", location_df)
