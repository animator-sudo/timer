import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Ilgen Lions Timer", layout="wide")
st_autorefresh(interval=1000, key="refresh")

st.markdown("""
    <style>
    .stApp {
        background-color: #333333;
        color: white;
    }
    .timer-box {
        padding: 8px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 0px;
        font-size: 16px;
    }
    .stButton button {
        color: black !important;
        font-size: 14px !important;
        padding: 4px 8px !important;
    }
    .round-time {
        font-size: 13px;
        margin: 2px 0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Ilgen Lions Timer")

# Mastertimer
if "master_start_time" not in st.session_state:
    st.session_state.master_start_time = None
if "master_running" not in st.session_state:
    st.session_state.master_running = False

def format_time(seconds):
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
    return f"{minutes:02d}:{sec:02d}"

def get_color(elapsed):
    if elapsed < 120:
        return "lightgreen"
    elif elapsed < 240:
        return "green"
    elif elapsed < 360:
        return "yellow"
    elif elapsed < 480:
        return "orange"
    elif elapsed < 600:
        return "violet"
    elif elapsed < 720:
        return "red"
    else:
        return "black"

# Kinder in definierter Anordnung
children_names = [
    "Charlotte", "Filippa", "Annabelle",      # oberste Reihe
    "Noemi",                                   # zweite Reihe
    "Ida", "Meliah", "Luisa", "Elena", "Ella", # dritte Reihe
    "Uliana"                                   # unterste Reihe
]

# Initialisierung
if "timers" not in st.session_state:
    st.session_state.timers = [{
        "name": name,
        "elapsed": 0.0,
        "running": False,
        "start_time": None,
        "rounds": []
    } for name in children_names]

# Mastertimer Logik
active_timers = [t for t in st.session_state.timers if t["running"]]
if len(active_timers) >= 6 and not st.session_state.master_running:
    st.session_state.master_start_time = time.time()
    st.session_state.master_running = True

if st.session_state.master_running:
    master_elapsed = time.time() - st.session_state.master_start_time
    st.subheader(f"⏱️ Mastertimer: {format_time(master_elapsed)}")
else:
    st.subheader("⏱️ Mastertimer: --:--")

# Anzeige in Zeilen
rows = [
    ["Charlotte", "Filippa", "Annabelle"],
    ["Noemi"],
    ["Ida", "Meliah", "Luisa", "Elena", "Ella"],
    ["Uliana"]
]

for row in rows:
    cols = st.columns(len(row))
    for i, name in enumerate(row):
        timer = next(t for t in st.session_state.timers if t["name"] == name)

        if timer["running"]:
            timer["elapsed"] = time.time() - timer["start_time"]

        color = get_color(timer["elapsed"])
        name_color = color  # Name hat gleiche Farbe wie Balken

        with cols[i]:
            st.markdown(f'<div class="timer-box" style="background-color: {color};">', unsafe_allow_html=True)
            st.markdown(f"<h4 style='margin-bottom:4px;color:{name_color}'>{timer['name']}</h4>", unsafe_allow_html=True)
            st.markdown(f"<h5 style='margin-top:0px'>{format_time(timer['elapsed'])}</h5>", unsafe_allow_html=True)

            # Rundenzeiten
            if timer["rounds"]:
                for idx, r in enumerate(timer["rounds"], 1):
                    st.markdown(f"<div class='round-time'>R{idx}: {format_time(r)}</div>", unsafe_allow_html=True)

            btn_cols = st.columns(3)
            with btn_cols[0]:
                if st.button("S", key=f"start_{name}"):
                    if not timer["running"]:
                        timer["start_time"] = time.time() - timer["elapsed"]
                        timer["running"] = True
            with btn_cols[1]:
                if st.button("P", key=f"pause_{name}"):
                    if timer["running"]:
                        timer["elapsed"] = time.time() - timer["start_time"]
                        timer["rounds"].append(timer["elapsed"])
                        timer["running"] = False
            with btn_cols[2]:
                if st.button("R", key=f"reset_{name}"):
                    timer["elapsed"] = 0.0
                    timer["running"] = False
                    timer["start_time"] = None
                    timer["rounds"] = []
            st.markdown("</div>", unsafe_allow_html=True)
