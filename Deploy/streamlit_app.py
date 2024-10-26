import streamlit as st
st.logo("images/poly_logo.jpeg", icon_image="images/logo.jpeg")
# try:
#     from WiFi_Geolocation.srv.app import geoloc_main as geoloc_app  # Certifique-se de que 'app.py' possui uma função 'run'
# except Exception as e:
#     st.error("Módulo WiFi_Geolocation não encontrado. Verifique o caminho e a estrutura.")
#     print(e)
# tp2 = st.Page(geoloc_app, title="Geolocation")

# try:
#     from LoRaTemp.srv.app import temp_hum_main as temp_app  # Certifique-se de que 'app.py' possui uma função 'run'
# except Exception as e:
#     st.error("Módulo WiFi_Geolocation não encontrado. Verifique o caminho e a estrutura.")
#     print(e)
# tp3 = st.Page(temp_app, title="Temperature")
tp2 = st.Page(
    "pages/geo.py",
    title="Request 1",
    icon=":material/help:",
)
tp3 = st.Page(
    "pages/temp.py",
    title="Request 2",
    icon=":material/help:",
)
pg = st.navigation([tp2, tp3]
)
st.set_page_config(page_title="Data manager", page_icon=":shark:", layout="wide")
pg.run()
