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

# CSS einbinden: Adaptiver Hintergrund, Timer-Boxen, etc.
st.markdown(
    f"""
    <style>
    /* Adaptiver Hintergrund mit einer sehr dezenten, transparenten Überlagerung */
    .stApp {{
         background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), 
         url("data:image/png;base64,{b64}");
         background-size: cover;
         background-position: center;
    }}

    /* Jede Timer-Box als weißer Container mit weißem Rahmen */
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

# Kindernamen alphabetisch (nach dem Anfangsbuchstaben) sortieren
children_names = sorted([
    "Annabelle", "Charlotte", "Elena", "Ella", "Filippa",
    "Ida", "Luisa", "Meliah", "Noemi", "Uliana"
], key=lambda name: (name[0], name))

# Timer-Initialisierung (nur einmal in der Session)
if "timers" not in st.session_state:
    st.session_state.timers = [
        {"name": name, "elapsed": 0.0, "running": False, "start_time": None}
        for name in children_names
    ]

# Funktion zur Zeitformatierung im Format mm:ss
def format_time(seconds):
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
    return f"{minutes:02d}:{sec:02d}"

# Anzeige der Timer in 2 Reihen à 5 Spalten
for row in range(2):
    cols = st.columns(5)
    for i in range(5):
        idx = row * 5 + i
        timer = st.session_state.timers[idx]
        with cols[i]:
            # Aktualisiere die verstrichene Zeit, falls der Timer läuft
            if timer["running"]:
                timer["elapsed"] = time.time() - timer["start_time"]
            st.markdown('<div class="timer-box">', unsafe_allow_html=True)
            st.header(timer["name"])
            st.subheader(format_time(timer["elapsed"]))
            # Drei Steuerungsknöpfe in einer Zeile
            btn_cols = st.columns(3)
            with btn_cols[0]:
                if st.button("Start", key=f"start_{idx}"):
                    if not timer["running"]:
                        timer["start_time"] = time.time() - timer["elapsed"]
                        timer["running"] = True
            with btn_cols[1]:
                if st.button("Pause", key=f"pause_{idx}"):
                    if timer["running"]:
                        timer["elapsed"] = time.time() - timer["start_time"]
                        timer["running"] = False
            with btn_cols[2]:
                if st.button("Reset", key=f"reset_{idx}"):
                    timer["running"] = False
                    timer["elapsed"] = 0.0
            st.markdown("</div>", unsafe_allow_html=True)
