import streamlit as st
import time
import base64
from streamlit_autorefresh import st_autorefresh

# Auto-Refresh alle 1 Sekunde, damit Timer dynamisch aktualisiert werden
st_autorefresh(interval=1000, key="refresh")

# Seiteneinstellungen
st.set_page_config(page_title="Ilgen Lions Timer", layout="wide")
st.title("Ilgen Lions Timer")
st.write("Drücke 'Start', um den Timer zu starten, 'Pause', um anzuhalten und 'Reset', um den Timer zurückzusetzen.")

# Hintergrundbild laden und Base64 kodieren
with open("ilgen_lions.png", "rb") as f:
    img_data = f.read()
b64 = base64.b64encode(img_data).decode()

# CSS für iPad-Hochformat-Optimierung und Buttons
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{b64}");
        background-size: cover;
        background-position: center;
        color: white;
    }}
    .timer-box {{
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
        color: white;
    }}
    .stButton button {{
        background-color: #f0f0f0 !important;
        color: #000000 !important;
        font-weight: bold;
        font-size: 20px !important;
        padding: 14px 20px;
        border-radius: 10px;
        width: 100%;
    }}
    h1, h2, h3 {{
        font-size: 26px !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Kinder in gewünschter Reihenfolge auf 4 Zeilen
children_names = [
    "Charlotte", "Filippa", "Annabelle",        # Zeile 1
    "Noemi",                                    # Zeile 2
    "Luisa", "Elena", "Ella", "Ida", "Meliah",  # Zeile 3
    "Uliana"                                    # Zeile 4
]

# Timer initialisieren oder ergänzen
if "timers" not in st.session_state:
    st.session_state.timers = []

name_set = set(t["name"] for t in st.session_state.timers)
for name in children_names:
    if name not in name_set:
        st.session_state.timers.append({
            "name": name,
            "elapsed": 0.0,
            "running": False,
            "start_time": None,
            "rounds": []
        })
    else:
        for t in st.session_state.timers:
            if t["name"] == name and "rounds" not in t:
                t["rounds"] = []

def format_time(seconds):
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
    return f"{minutes:02d}:{sec:02d}"

def get_bg_color(elapsed, running):
    if not running:
        return "white"
    if elapsed < 60:
        return "white"
    elif elapsed < 120:
        return "yellow"
    elif elapsed < 180:
        return "orange"
    else:
        return "red"

# Layout mit festen 4 Zeilen
layout = [
    ["Charlotte", "Filippa", "Annabelle"],
    ["Noemi"],
    ["Luisa", "Elena", "Ella", "Ida", "Meliah"],
    ["Uliana"]
]

timer_dict = {t["name"]: t for t in st.session_state.timers}

for row in layout:
    cols = st.columns(len(row))
    for i, name in enumerate(row):
        timer = timer_dict[name]

        # Timer läuft: laufende Zeit berechnen
        if timer["running"]:
            timer["elapsed"] = time.time() - timer["start_time"]

        bg_color = get_bg_color(timer["elapsed"], timer["running"])

        with cols[i]:
            st.markdown(f'<div class="timer-box" style="background-color: {bg_color};">', unsafe_allow_html=True)
            st.header(timer["name"])
            st.subheader(format_time(timer["elapsed"]))

            btn_cols = st.columns(3)
            with btn_cols[0]:
                if st.button("Start", key=f"start_{name}"):
                    if not timer["running"]:
                        # Falls Zeit > 0, nicht neu starten, sondern weiterlaufen lassen
                        timer["start_time"] = time.time() - timer["elapsed"]
                        timer["running"] = True
            with btn_cols[1]:
                if st.button("Pause", key=f"pause_{name}"):
                    if timer["running"]:
                        timer["elapsed"] = time.time() - timer["start_time"]
                        timer["running"] = False
                        # Rundenzeit direkt speichern
                        timer["rounds"].append(timer["elapsed"])
            with btn_cols[2]:
                if st.button("Reset", key=f"reset_{name}"):
                    timer["running"] = False
                    timer["elapsed"] = 0.0
                    timer["rounds"] = []

            st.markdown("</div>", unsafe_allow_html=True)

            if timer["rounds"]:
                st.markdown("**Rundenzeiten:**")
                for j, r in enumerate(timer["rounds"], 1):
                    st.write(f"Runde {j}: {format_time(r)}")
