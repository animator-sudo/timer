import streamlit as st
import time
import base64
from streamlit_autorefresh import st_autorefresh

# Auto-Refresh alle 1 Sekunde (damit die Timer aktualisiert werden)
st_autorefresh(interval=1000, key="timer_refresh")

# Layout & Titel setzen
st.set_page_config(layout="wide")
st.title("🕒 Kompakter 10-fach Kinder-Timer (nach Anfangsbuchstaben gruppiert)")

# Hintergrundbild laden und als Base64 kodieren
with open("ilgen_lions.png", "rb") as f:
    encoded = f.read()
b64 = base64.b64encode(encoded).decode()

# CSS einbinden – sorgt für den Hintergrund, Stil und Weißfärbung des Texts
st.markdown(
    f'''
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
                          url("data:image/png;base64,{b64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white;
    }}

    @media only screen and (max-width: 768px) {{
        .stApp {{
            background-size: contain;
            background-position: top center;
            background-attachment: scroll;
        }}
    }}

    h1, h2, h3, h4, h5, h6, .stMetric, .stButton, .stMarkdown {{
        color: white !important;
    }}

    .timer-box {{
        background-color: rgba(0, 0, 0, 0.6);
        padding: 1em;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
        margin-bottom: 10px;
    }}
    </style>
    ''',
    unsafe_allow_html=True
)

# Kindernamen alphabetisch nach dem Anfangsbuchstaben sortieren
kinder_namen = sorted([
    "Annabelle", "Charlotte", "Elena", "Ella", "Filippa",
    "Ida", "Luisa", "Meliah", "Noemi", "Uliana"
], key=lambda name: (name[0], name))

# Timer-Initialisierung in der Session (nur einmal beim ersten Start)
if "timers" not in st.session_state:
    st.session_state["timers"] = [
        {"name": name, "start_time": None, "elapsed": 0.0, "running": False}
        for name in kinder_namen
    ]

# Funktion, um die verstrichene Zeit im Format mm:ss anzuzeigen
def format_time(seconds):
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
    return f"{minutes:02d}:{sec:02d}"

# Anzeige: 2 Zeilen mit je 5 Timer-Boxen
for row in range(2):
    timer_cols = st.columns(5)
    for i in range(5):
        idx = row * 5 + i
        timer = st.session_state["timers"][idx]
        with timer_cols[i]:
            # Timer-Box: Hier wird der Name und die verstrichene Zeit angezeigt.
            st.markdown('<div class="timer-box">', unsafe_allow_html=True)
            st.markdown(f"<h3>{timer['name']}</h3>", unsafe_allow_html=True)
            if timer["running"]:
                timer["elapsed"] = time.time() - timer["start_time"]
            st.metric(label="Zeit", value=format_time(timer["elapsed"]))
            st.markdown("</div>", unsafe_allow_html=True)

            # Steuerungsknöpfe in einer Zeile unter der Timer-Box
            btn_cols = st.columns(3)
            with btn_cols[0]:
                if st.button("▶", key=f"start_{idx}"):
                    if not timer["running"]:
                        # Falls der Timer gestartet wird, berücksichtige bereits verstrichene Zeit
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
