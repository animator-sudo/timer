import streamlit as st
import time
import base64
from streamlit_autorefresh import st_autorefresh

# Auto-Refresh alle 1 Sekunde, damit sich die Timer dynamisch aktualisieren
st_autorefresh(interval=1000, key="refresh")

# Seiteneinstellungen und Überschrift
st.set_page_config(page_title="Ilgen Lions Timer", layout="wide")
st.title("Ilgen Lions Timer")
st.write("Drücke 'Start', um den Timer zu starten, 'Pause', um anzuhalten, und 'Reset', um den Timer zurückzusetzen.")

# Hintergrundbild laden und als Base64 kodieren
with open("ilgen_lions.png", "rb") as f:
    img_data = f.read()
b64 = base64.b64encode(img_data).decode()

# CSS einbinden: Adaptiver Hintergrund mit transparenter Überlagerung; Timer-Boxen mit weißem Rahmen und runden Ecken; Button-Text schwarz
st.markdown(
    f"""
    <style>
    /* Hintergrundbild mit transparenter (0.1) schwarzer Überlagerung */
    .stApp {{
         background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), 
         url("data:image/png;base64,{b64}");
         background-size: cover;
         background-position: center;
    }}

    /* Jede Timer-Box als weißer Container mit weißem Rahmen und runden Ecken */
    .timer-box {{
         background-color: white;
         border: 2px solid white;
         padding: 10px;
         border-radius: 8px;
         text-align: center;
         margin-bottom: 10px;
    }}

    /* Button-Text explizit schwarz */
    .stButton button {{
         color: black !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Liste der Kindernamen – alphabetisch nach dem Anfangsbuchstaben sortiert
children_names = sorted([
    "Annabelle", "Charlotte", "Elena", "Ella", "Filippa",
    "Ida", "Luisa", "Meliah", "Noemi", "Uliana"
], key=lambda name: (name[0], name))

# Timer-Initialisierung (nur einmal in der Session)
if "timers" not in
