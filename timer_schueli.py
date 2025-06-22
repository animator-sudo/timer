import streamlit as st
import time
import base64
from streamlit_autorefresh import st_autorefresh

# Auto-Refresh alle 1 Sekunde
st_autorefresh(interval=1000, key="timer_refresh")

# Layout festlegen
st.set_page_config(layout="wide")
st.title("🕒 Kompakter 10-fach Kinder-Timer")

# Hintergrundbild base64-kodieren
with open("ilgen_lions.png", "rb") as f:
    encoded = f.read()
b64 = base64.b64encode(encoded).decode()

# CSS für responsives Hintergrundbild
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{b64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    @media only screen and (max-width: 768px) {{
        .stApp {{
            background-size: contain;
            background-position: top center;
            background-attachment: scroll;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Alphabetisch sortierte Kindernamen
kinder_namen = [
    "Annabelle", "Charlotte", "Elena", "Ella", "Filippa",
    "Ida", "Luisa", "Meliah", "Noemi", "Uliana"
]
kinder_namen.sort()

# Timer-Initialisierung
if "timers" not in st.session_state:
    st.session_state.timers = [
        {"name": name, "start_time": None, "elapsed": 0.0, "running": False}
        for name in kinder_namen
    ]

# Funktion zur Formatierung der Zeit
def format_time(seconds):
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
