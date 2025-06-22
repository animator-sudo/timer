import streamlit as st
import time
import base64
from streamlit_autorefresh import st_autorefresh

# Auto-Refresh alle 1 Sekunde, damit die Timer dynamisch aktualisiert werden
st_autorefresh(interval=1000, key="refresh")

# Seiteneinstellungen und Überschrift
st.set_page_config(page_title="Ilgen Lions Timer", layout="wide")
st.title("Ilgen Lions Timer")
st.write("Drücke 'Start', um den Timer zu starten, 'Pause', um anzuhalten und 'Reset', um den Timer zurückzusetzen.")

# Hintergrundbild laden und als Base64 kodieren
with open("ilgen_lions.png", "rb") as f:
    img_data = f.read()
b64 = base64.b64encode(img_data).decode()

# CSS einbinden: Adaptiver Hintergrund und Basis-Styling
st.markdown(
    f"""
    <style>
    /* Adaptiver Hintergrund mit leicht transparenter Überlagerung */
    .stApp {{
         background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), 
         url("data:image/png;base64,{b64}");
         background-size: cover;
         background-position: center;
    }}
    /* Basis-Styling für die Timer-Box */
    .timer-box {{
         padding: 10px;
         border-radius: 8px;
         text-align: center;
         margin-bottom: 10px;
    }}
    /* Button-Text bleibt schwarz */
    .stButton button {{
         color: black !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Kindernamen alphabetisch nach Anfangsbuchstaben sortieren
children_names = sorted(
