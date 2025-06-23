import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh

# Auto-Refresh alle 1 Sekunde
st_autorefresh(interval=1000, key="refresh")

st.set_page_config(page_title="Ilgen Lions Timer", layout="wide")
st.title("Ilgen Lions Timer")
st.write("Drücke 'S' zum Starten, 'P' zum Pausieren und 'R' zum Zurücksetzen.")

# CSS: Grauer Hintergrund + kompakte Darstellung
st.markdown(
    """
    <style>
    .stApp {
        background-color: #888888;
        color: white;
        font-family: Arial, sans-serif;
    }
    .timer-box {
        padding: 10px 12px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 4px;
        color: white;
    }
    .stButton button {
        background-color: #f0f0f0 !important;
        color: #000000 !important;
        font-weight: bold;
        font-size: 20px !important;
        padding: 6px 8px;
        border-radius: 8px;
        width: 100%;
        margin: 2px 0;
        min-width: 40px;
        height: 40px;
    }
    h1 {
        font-size: 26px !important;
        margin-bottom: 8px;
    }
    h2 {
        font-size: 18px !important;
        margin: 2px 0 6px 0;
    }
    h3 {
        font-size: 16px !important;
        margin: 2px 0 6px 0;
    }
    .round-time {
        font-size: 14px;
        margin: 0 0 2px 0;
        padding: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Kind-Layout: 4 Zeilen
layout = [
    ["Charlotte", "Filippa", "Annabelle"],
    ["Noemi", "Ida", "Meliah"],
    ["Luisa", "Elena", "Ella"],
    ["Uliana"]
]

# Initialisierung
if "timers" not in st.session_state:
    st.session_state.timers = []
    st.session_state.start_trigger_count = 0
    st.session_state.group_start_time = None

# Timer-Speicherung vorbereiten
existing_names = {t["name"] for t in st.session_state.timers}
for row in layout:
    for name in row:
        if name not in existing_names:
            st.session_state.timers.append({
                "name": name,
                "elapsed": 0.0,
                "running": False,
                "start_time": None,
                "rounds": [],
                "color_offset": 0.0
            })

# Hilfsfunktionen
def format_time(seconds):
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
    return f"{minutes:02d}:{sec:02d}"

def get_bg_color(elapsed, running, color_offset):
    adj = elapsed - color_offset
    if not running:
        return "white"
    if adj >= 300:
        return "violet"
    elif adj >= 180:
        return "red"
    elif adj >= 120:
        return "orange"
    elif adj >= 60:
        return "yellow"
    else:
        return "white"

# Umwandlung zu Dictionary
timer_dict = {t["name"]: t for t in st.session_state.timers}

# Timeranzeige nach Layout
for row in layout:
    cols = st.columns(len(row))
    for i, name in enumerate(row):
        timer = timer_dict[name]

        if timer["running"]:
            timer["elapsed"] = time.time() - timer["start_time"]

        bg_color = get_bg_color(timer["elapsed"], timer["running"], timer["color_offset"])
        name_color = "limegreen" if timer["running"] else "white"

        with cols[i]:
            st.markdown(f'<div class="timer-box" style="background-color: {bg_color};">', unsafe_allow_html=True)
            st.markdown(f'<h2 style="color: {name_color}; margin-bottom: 0.3rem;">{timer["name"]}</h2>', unsafe_allow_html=True)
            st.subheader(format_time(timer["elapsed"]))

            btn_cols = st.columns([1,1,1])
            with btn_cols[0]:
                if st.button("S", key=f"start_{name}"):
                    if not timer["running"]:
                        st.session_state.start_trigger_count += 1
                        if st.session_state.group_start_time is None and st.session_state.start_trigger_count >= 6:
                            st.session_state.group_start_time = time.time()
                            for t in st.session_state.timers:
                                t["start_time"] = st.session_state.group_start_time
                                t["running"] = True
                        elif st.session_state.group_start_time is not None:
                            timer["start_time"] = time.time()
                            timer["running"] = True
            with btn_cols[1]:
                if st.button("P", key=f"pause_{name}"):
                    if timer["running"]:
                        timer["elapsed"] = time.time() - timer["start_time"]
                        timer["running"] = False
                        timer["rounds"].append(timer["elapsed"])
                        timer["color_offset"] = timer["elapsed"]
            with btn_cols[2]:
                if st.button("R", key=f"reset_{name}"):
                    timer["running"] = False
                    timer["elapsed"] = 0.0
                    timer["rounds"] = []
                    timer["color_offset"] = 0.0

            st.markdown("</div>", unsafe_allow_html=True)

            if timer["rounds"]:
                st.markdown("**Rundenzeiten:**")
                for j, r in enumerate(timer["rounds"], 1):
                    st.markdown(f'<p class="round-time">Runde {j}: {format_time(r)}</p>', unsafe_allow_html=True)
