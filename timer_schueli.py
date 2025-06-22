import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh

# Auto-Refresh alle 1 Sekunde, damit sich die Timer dynamisch aktualisieren
st_autorefresh(interval=1000, key="refresh")

# Seiteneinstellungen und Überschrift
st.set_page_config(page_title="Kinder-Timer", layout="wide")
st.title("Kompakter Kinder-Timer")
st.write("Drücke 'Start', um den Timer zu starten, 'Pause' zum Anhalten und 'Reset', um den Timer zurückzusetzen.")

# Liste der Kindernamen – alphabetisch nach dem Anfangsbuchstaben sortiert
children_names = sorted([
    "Annabelle", "Charlotte", "Elena", "Ella", "Filippa",
    "Ida", "Luisa", "Meliah", "Noemi", "Uliana"
], key=lambda name: (name[0], name))

# Timer-Initialisierung: Wir speichern jeden Timer in der Session, damit der Zustand erhalten bleibt.
if "timers" not in st.session_state:
    st.session_state.timers = [
        {"name": name, "elapsed": 0.0, "running": False, "start_time": None}
        for name in children_names
    ]

# Funktion zur Zeitformatierung (mm:ss)
def format_time(seconds):
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
    return f"{minutes:02d}:{sec:02d}"

# Anzeige der Timer in 2 Reihen à 5 Spalten
for row in range(2):
    cols = st.columns(5)
    for i, col in enumerate(cols):
        idx = row * 5 + i
        timer = st.session_state.timers[idx]
        with col:
            # Wenn der Timer läuft, aktualisiere die verstrichene Zeit
            if timer["running"]:
                timer["elapsed"] = time.time() - timer["start_time"]
                
            # Kindername und verstrichene Zeit anzeigen
            st.header(timer["name"])
            st.subheader(format_time(timer["elapsed"]))
            
            # Drei Buttons in einer Zeile
            btn_cols = st.columns(3)
            with btn_cols[0]:
                if st.button("Start", key=f"start_{idx}"):
                    if not timer["running"]:
                        # Timer startet und berücksichtigt bereits verstrichene Zeit
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
