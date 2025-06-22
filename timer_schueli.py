import streamlit as st
import time
import base64
from streamlit_autorefresh import st_autorefresh

# Auto-Refresh alle 1 Sekunde
st_autorefresh(interval=1000, key="timer_refresh")

# Layout & Titel
st.set_page_config(layout="wide")
st.title("🕒 Kompakter 10-fach Kinder-Timer (nach Anfangsbuchstaben gruppiert)")

# Hintergrundbild laden & base64-kodieren
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
        color: white;
    }}

    @media only screen and (max-width: 768px) {{
        .stApp {{
            background-size: contain;
            background-position: top center;
            background-attachment: scroll;
        }}
    }}

    h1, h2, h3, h4, h5, h6, .stMetric, .stButton, .stMarkdown {{
        color: white !important;
    }}

    .timer-box {{
        background-color: rgba(0, 0, 0, 0.6);
        padding: 1em;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
        margin-bottom: 10px;
    }}
    </style>
    ''',
    unsafe_allow_html=True
)

# Kindernamen nach Anfangsbuchstaben sortieren
kinder_namen = sorted([
    "Annabelle", "Charlotte", "Elena", "Ella", "Filippa",
    "Ida", "Luisa", "Meliah", "Noemi", "Uliana"
], key=lambda name: (name[0], name))

# Timer-Initialisierung
if "timers" not in st.session_state:
    st.session_state["timers"] = [
        {"name": name, "start_time": None, "elapsed": 0.0, "running": False}
        for name in kinder_namen
    ]

# Zeit formatieren (mm:ss)
def format_time(seconds):
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
    return f"{minutes:02d}:{sec:02d}"

# Anzeige: 2 Reihen à 5 Timer
for row in range(2):
    timer_cols = st.columns(5)
