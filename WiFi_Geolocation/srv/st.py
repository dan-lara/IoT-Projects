import streamlit as st
import pandas as pd
import numpy as np
from localisateur import *
from trilateration import *
# from triangulateur import estimate_position
bdd = read_DB_csv_file('BDD.csv')
wifi = read_WiFi_json_file('wifi_data.json')
# print("WiFi JSON: \n", wifi)
location_df = fetch_locations(bdd, wifi)
# print("Location DataFrame: \n", location_df)

df = location_df[['Latitude', 'Longitude','RSSI']]
df.columns = ['lat', 'lon', 'accuracy']
df['color'] = "#FF0000"
df['accuracy'] = (-1*df['accuracy'].astype(float) - 40)/40
# print(df)


# position = estimate_position(location_df) #trilateration_2D(location_df)
position = [48.84506687, 2.35692861]
st.write("Position Estimée [Latitude, Longitude] :", position)
new_row = pd.DataFrame([{'lat': position[0], 'lon': position[1], 'accuracy': 2, 'color': '#0000FF'}])
df = pd.concat([df, new_row], ignore_index=True)
new_row = pd.DataFrame([{'lat': 48.845040, 'lon': 2.356970, 'accuracy': 0, 'color': '#00FF00'}])
df = pd.concat([df, new_row], ignore_index=True)
print(df)
st.map(df, latitude='lat', longitude='lon', size='accuracy', color='color', zoom=18, use_container_width=True)