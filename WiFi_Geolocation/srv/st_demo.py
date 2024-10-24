import folium
import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
from localisateur import *
from trilateration import *
# from triangulateur import estimate_position
bdd = read_DB_csv_file('BDD.csv')
wifi = read_WiFi_json_file('wifi_data.json')
location_df = fetch_locations(bdd, wifi)
print("-"*30)
df = location_df[['SSID', 'RSSI', 'Latitude', 'Longitude','RSSI']]
df.columns = ['ssid', 'rssi', 'lat', 'lon', 'accuracy']
df['color'] = 'red'#"#FF0000"
df['accuracy'] = (-1*df['accuracy'].astype(float) - 40)/40
# print(df)

from triangulateur import estimate_position
position = estimate_position(location_df)[0:2]
st.write("Position Estimée [Latitude, Longitude] :", position)
new_row = pd.DataFrame([{'ssid':"This Device", 'rssi':-30, 'lat': position[0], 'lon': position[1], 'accuracy': 1, 'color': 'green'}])#'#0000FF'
df = pd.concat([df, new_row], ignore_index=True)
# new_row = pd.DataFrame([{'ssid':"Correct Place", 'rssi':-30, 'lat': 48.845243, 'lon': 2.356881, 'accuracy': 1, 'color': 'green'}])#'#00FF00'
# df = pd.concat([df, new_row], ignore_index=True)
print(df)
# print(df)
# st.map(df, latitude='lat', longitude='lon', size='accuracy', color='color', zoom=18, use_container_width=True)

# import folium
# from streamlit_folium import st_folium
# map = folium.Map(location=[48.845278, 2.3568355], zoom_start=18)
# for i in range(df.shape[0]):
#     folium.CircleMarker(location=[df.iloc[i]['lat'], df.iloc[i]['lon']],
#                         radius=df.iloc[i]['accuracy']*10,
#                         color=df.iloc[i]['color'],
#                         fill=True).add_to(map)
# st_folium(map)
def plot_map(selected_index, texture):
    # Récupérer les coordonnées et autres informations pour le point sélectionné
    lat = df.iloc[selected_index]['lat']
    lon = df.iloc[selected_index]['lon']
    accuracy = df.iloc[selected_index]['accuracy']
    color = df.iloc[selected_index]['color']
    ssid = df.iloc[selected_index]['ssid']
    rssi = df.iloc[selected_index]['rssi']
    
    # Vérifier le type de texture et créer la carte
    # Créer la carte
    map = folium.Map(location=[lat, lon], zoom_start=18)

    # Ajouter des cercles pour chaque point avec SSID et RSSI
    for i in range(df.shape[0]):
        if df.iloc[i]['color'] == 'green':
            folium.Marker(
                location=[df.iloc[i]['lat'], df.iloc[i]['lon']],
                popup=f"Position Estimée<br>Latitude: {df.iloc[i]['lat']}<br>Longitude: {df.iloc[i]['lon']}",
                icon=folium.Icon(color=df.iloc[i]['color'])
            ).add_to(map)
        else:
            folium.Marker(
                location=[df.iloc[i]['lat'], df.iloc[i]['lon']],
                popup=f"{df.iloc[i]['ssid']}<br>RSSI: {df.iloc[i]['rssi']}",
                icon=folium.Icon(color=df.iloc[i]['color'])
            ).add_to(map)

    # Affichage de la carte
    st_folium(map, width=800)


st.title("Map Visualization")
texture = st.selectbox("Select map texture", ["OpenStreetMap", "Stamen Terrain", "Stamen Toner", "CartoDB Positron", "CartoDB Dark Matter"])

# Affichage de la liste des lignes pour la sélection
selected_index = st.selectbox("Select data point", range(df.shape[0]), format_func=lambda x: f"Lat: {df.iloc[x]['lat']}, Lon: {df.iloc[x]['lon']}")
plot_map(selected_index, texture)

# Si aucune ligne n'est sélectionnée, afficher la dernière par défaut
if selected_index is None:
    plot_map(df.shape[0] - 1)  # Dernière ligne par défaut


