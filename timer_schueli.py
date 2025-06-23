import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=1000, key="refresh")

st.set_page_config(page_title="Ilgen Lions Timer", layout="wide")

# Mastertimer initialisieren
if "master_start_time" not in st.session_state:
    st.session_state.master_start_time = None

# Titel mit Mastertimer nebendran
st.markdown("""
    <style>
    .title-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .master-timer {
        font-size: 28px;
        font-weight: bold;
        color: lightgreen;
    }
    </style>
    """, unsafe_allow_html=True)

master_elapsed = 0.0
if st.session_state.master_start_time:
    master_elapsed = time.time() - st.session_state.master_start_time

def format_time(seconds):
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
    return f"{minutes:02d}:{sec:02d}"

st.markdown(
    f"""
    <div class="title-row">
        <h1>Ilgen Lions Timer</h1>
        <div class="master-timer">⏱ Master: {format_time(master_elapsed)}</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("Drücke 'S' zum Starten, 'P' zum Pausieren und 'R' zum Zurücksetzen.")

# CSS Styling
st.markdown("""
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
        font-size: 18px !important;
        padding: 6px 8px;
        border-radius: 8px;
        width: 100%;
        margin: 2px 0;
        min-width: 36px;
        height: 36px;
    }
    .name-time {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 18px;
        margin-bottom: 6px;
    }
    .rounds {
        font-size: 14px;
        margin-top: 6px;
    }
    .rounds span {
        margin-right: 6px;
    }
    </style>
    """, unsafe_allow_html=True)

# Layout der Kinder (Zeilen)
layout = [
    ["Charlotte", "Filippa", "Annabelle"],
    ["Noemi", "Ida", "Meliah"],
    ["Luisa", "Elena", "Ella"],
    ["Uliana"]
]

# Session-Initialisierung
if "timers" not in st.session_state:
    st.session_state.timers = []
    st.session_state.pending_start = set()
    st.session_state.group_start_time = None

# Timer-Daten initialisieren
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

timer_dict = {t["name"]: t for t in st.session_state.timers}

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

            # Name + Zeit
            time_str = format_time(timer["elapsed"])
            st.markdown(
                f'<div class="name-time">'
                f'<span style="color: {name_color}; font-weight: bold;">{name}</span>'
                f'<span>{time_str}</span></div>',
                unsafe_allow_html=True
            )

            # Buttons
            btn_cols = st.columns([1, 1, 1])
            with btn_cols[0]:
                if st.button("S", key=f"start_{name}"):
                    if not timer["running"]:
                        if name in st.session_state.pending_start:
                            st.session_state.pending_start.remove(name)
                        if st.session_state.group_start_time is None:
                            st.session_state.pending_start.add(name)
                            if len(st.session_state.pending_start) == 6:
                                st.session_state.group_start_time = time.time()
                                for n in st.session_state.pending_start:
                                    t = timer_dict[n]
                                    t["start_time"] = st.session_state.group_start_time
                                    t["running"] = True
                                st.session_state.pending_start.clear()
                                if st.session_state.master_start_time is None:
                                    st.session_state.master_start_time = st.session_state.group_start_time
                        else:
                            timer["start_time"] = time.time() - timer["elapsed"]
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
                    timer["start_time"] = None

            # Rundenzeiten unterhalb Buttons
            if timer["rounds"]:
                st.markdown('<div class="rounds">', unsafe_allow_html=True)
                for j, r in enumerate(timer["rounds"], 1):
                    st.markdown(f'<span>R{j}: {format_time(r)}</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
