import streamlit as st
import time
import base64
from streamlit_autorefresh import st_autorefresh

# Auto-Refresh alle 1 Sekunde
st_autorefresh(interval=1000, key="timer_refresh")

# Layout & Titel
st.set_page_config(layout="wide")
st.title("🕒 Kompakter 10-fach Kinder-Timer (nach Anfangsbuchstaben gruppiert)")

# Hintergrundbild einlesen & codieren
with open("ilgen_lions.png", "rb") as f:
    encoded = f.read()
b64 = base64.b64encode(encoded).decode()

# CSS einbinden
st.markdown(
    f'''
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
                          url("data:image/png;base64,{b64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;

