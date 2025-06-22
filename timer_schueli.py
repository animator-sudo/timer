import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh

# Auto-Refresh alle 1 Sekunde
st_autorefresh(interval=1000, key="timer_refresh")

# Layout
st.set_page_config(layout="wide")
st.title("🕒 Kompakter 10-fach Kinder-Timer")

# Alphabetisch sortierte Kindernamen
kinder_namen = [
    "Annabelle", "Charlotte", "Elena", "Ella", "Filippa",
    "Ida", "Luisa", "Meliah", "Noemi", "Uliana"
]
kinder_namen.sort()

# Timer-Init
if "timers" not in st.session_state:
    st.session_state.timers = [
        {"name": name, "start_time": None, "elapsed": 0.0, "running": False}
        for name in kinder_namen
    ]

# Zeitformat
def format_time(seconds):
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
    return f"{minutes:02d}:{sec:02d}"

# 5 Timer pro Zeile
for row in range(2):
    timer_cols = st.columns(5)
    for i in range(5):
        idx = row * 5 + i
        timer = st.session_state.timers[idx]

        with timer_cols[i]:
            st.markdown(f"**{timer['name']}**")

            # Laufzeit aktualisieren
            if timer["running"]:
                timer["elapsed"] = time.time() - timer["start_time"]

            st.metric(label="Zeit", value=format_time(timer["elapsed"]))

            btn_cols = st.columns([1, 1, 1])
            with btn_cols[0]:
                if st.button("▶", key=f"start_{idx}"):
                    if not timer["running"]:
                        timer["start_time"] = time.time() - timer["elapsed"]
                        timer["running"] = True

            with btn_cols[1]:
                if st.button("⏸", key=f"pause_{idx}"):
                    if timer["running"]:
                        timer["elapsed"] = time.time() - timer["start_time"]
                        timer["running"] = False

            with btn_cols[2]:
                if st.button("⏹", key=f"stop_{idx}"):
                    timer["start_time"] = None
                    timer["elapsed"] = 0.0
                    timer["running"] = False

