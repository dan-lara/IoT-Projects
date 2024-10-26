import streamlit as st

st.set_page_config(page_title="Data manager", page_icon=":shark:", layout="wide")

st.title("Data manager")
st.logo("images/poly_logo.png", icon_image="images/logo.png")

tp2 = st.Page(
    "pages/geo.py",
    title="Geolocation",
    icon=":world:",
)
tp3 = st.Page(
    "pages/temp.py",
    title="Temperature",
    icon=":material/help:",
)
def login():
    st.sidebar.title("Data manager")
    st.header("Log in")
    st.write("This application is a data manager for the IoT devices.")

pg = st.navigation([st.Page(login),tp2, tp3])

pg.run()