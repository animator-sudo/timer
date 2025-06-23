import streamlit as st
import time
import base64
from streamlit_autorefresh import st_autorefresh

# Auto-Refresh alle 1 Sekunde
st_autorefresh(interval=1000, key="refresh")

st.set_page_config(page_title="Ilgen Lions Timer", layout="wide")
st.title("Ilgen Lions Timer")
st.write("Drücke 'Start', um den Timer zu starten, 'Pause', um anzuhalten und 'Reset', um den Timer zurückzusetzen.")

# Hintergrundbild laden
with open("ilgen_lions.png", "rb") as f:
    img_data = f.read()
b64 = base64.b64encode(img_data).decode()

# CSS: kompakter, kleinere Schriften, engeres Layout, kleinere Buttons
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{b64}");
        background-size: cover;
        background-position: center;
        color: white;
        font-family: Arial, sans-serif;
    }}
    .timer-box {{
        padding: 10px 12px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 4px;
        color: white;
    }}
    .stButton button {{
        background-color: #f0f0f0 !important;
        color: #000000 !important;
        font-weight: bold;
        font-size: 16px !important;
        padding: 8px 10px;
        border-radius: 8px;
        width: 100%;
        margin: 2px 0;
    }}
    h1 {{
        font-size: 26px !important;
        margin-bottom: 8px;
    }}
    h2 {{
        font-size: 18px !important;
        margin: 2px 0 6px 0;
    }}
    h3 {{
        font-size: 16px !important;
        margin: 2px 0 6px 0;
    }}
    .row-container > div > div[role="listitem"] {{
        padding-bottom: 0px !important;
        margin-bottom: 0px !important;
    }}
    /* Reduziere den Abstand zwischen den Zeilen (Columns-Reihen) */
    .css-1lcbmhc.e1fqkh3o3 {{  /* Streamlit's class für column rows */
        margin-bottom: 2px !important;
    }}
    /* Rundenzeiten kleiner und kompakt */
    .round-time {{
        font-size: 14px;
        margin: 0 0 2px 0;
        padding: 0;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

children_names = [
    "Charlotte", "Filippa", "Annabelle",        # Zeile 1
    "Noemi",                                    # Zeile 2
    "Luisa", "Elena", "Ella", "Ida", "Meliah",  # Zeile 3
    "Uliana"                                    # Zeile 4
]

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

        if timer["running"]:
            timer["elapsed"] = time.time() - timer["start_time"]

        bg_color = get_bg_color(timer["elapsed"], timer["running"])

        with cols[i]:
            st.markdown(f'<div class="timer-box" style="background-color: {bg_color};">', unsafe_allow_html=True)
            st.header(timer["name"])
            st.subheader(format_time(timer["elapsed"]))

            btn_cols = st.columns([1,1,1])
            with btn_cols[0]:
                if st.button("Start", key=f"start_{name}"):
                    if not timer["running"]:
                        timer["start_time"] = time.time() - timer["elapsed"]
                        timer["running"] = True
            with btn_cols[1]:
                if st.button("Pause", key=f"pause_{name}"):
                    if timer["running"]:
                        timer["elapsed"] = time.time() - timer["start_time"]
                        timer["running"] = False
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
                    st.markdown(f'<p class="round-time">Runde {j}: {format_time(r)}</p>', unsafe_allow_html=True)
