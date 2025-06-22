import streamlit as st
import time

# Initialisiere den Session State
if "timers" not in st.session_state:
    st.session_state.timers = [
        {"name": f"Kind {i+1}", "start_time": None, "elapsed": 0.0, "running": False}
        for i in range(10)
    ]

st.set_page_config(layout="wide")
st.title("🕒 Kinder-Timer (10-fach kompakt)")

def format_time(seconds):
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
    return f"{minutes:02d}:{sec:02d}"

# 5 Timer pro Zeile (2 Zeilen)
for row in range(2):
    cols = st.columns(5)
    for i in range(5):
        idx = row * 5 + i
        timer = st.session_state.timers[idx]

        with cols[i]:
            st.markdown(f"**{timer['name']}**")
            
            c1, c2, c3 = st.colum
import streamlit as st
import time

# Initialisiere den Session State (nur beim ersten Laden)
if "timers" not in st.session_state:
    st.session_state.timers = [
        {"name": f"Kind {i+1}", "start_time": None, "elapsed": 0.0, "running": False}
        for i in range(10)
    ]

st.title("🕒 Kinder-Timer (10-fach)")

# Funktion zum Zeitformat
def format_time(seconds):
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
    return f"{minutes:02d}:{sec:02d}"

# Schleife über die 10 Timer
for idx, timer in enumerate(st.session_state.timers):
    st.subheader(timer["name"])

    cols = st.columns([1, 1, 1, 3])
    with cols[0]:
        if st.button(f"▶️ Start {idx}", key=f"start_{idx}"):
            if not timer["running"]:
                timer["start_time"] = time.time() - timer["elapsed"]
                timer["running"] = True

    with cols[1]:
        if st.button(f"⏸ Pause {idx}", key=f"pause_{idx}"):
            if timer["running"]:
                timer["elapsed"] = time.time() - timer["start_time"]
                timer["running"] = False

    with cols[2]:
        if st.button(f"⏹ Stopp {idx}", key=f"stop_{idx}"):
            timer["start_time"] = None
            timer["elapsed"] = 0.0
            timer["running"] = False

    # Anzeige der Zeit (automatisch aktualisiert)
    if timer["running"]:
        timer["elapsed"] = time.time() - timer["start_time"]
        st.write(f"⏱ Zeit: **{format_time(timer['elapsed'])}**")
        st.experimental_rerun()  # automatische Aktualisierung
    else:
        st.write(f"⏱ Zeit: **{format_time(timer['elapsed'])}**")

    st.divider()
