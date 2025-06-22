import streamlit as st
import time

# Page Setup
st.set_page_config(layout="wide")
st.title("🕒 Kompakter 10-fach Kinder-Timer")

# Timer-Init
if "timers" not in st.session_state:
    st.session_state.timers = [
        {"name": f"Kind {i+1}", "start_time": None, "elapsed": 0.0, "running": False}
        for i in range(10)
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
            st.markdown(f"🕒 {format_time(timer['elapsed'])}", help="Aktuelle Zeit")

            btn_cols = st.columns([1, 1, 1])
            with btn_cols[0]:
                if st.button("▶", key=f"start_{idx}"):
                    if not timer["running"]:
                        timer["start_time"] = time.time() - timer["elapsed"]
                        timer["running"] = True

            with btn_cols[1]:
