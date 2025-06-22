# Kindernamen nach Anfangsbuchstaben sortieren
kinder_namen = sorted([
    "Annabelle", "Charlotte", "Elena", "Ella", "Filippa",
    "Ida", "Luisa", "Meliah", "Noemi", "Uliana"
], key=lambda name: (name[0], name))

# Timer-Initialisierung
if "timers" not in st.session_state:
    st.session_state["timers"] = [
        {"name": name, "start_time": None, "elapsed": 0.0, "running": False}
        for name in kinder_namen
    ]

# Zeit formatieren
def format_time(seconds):
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
    return f"{minutes:02d}:{sec:02d}"

# Anzeige: 2 Zeilen à 5 Timer
for row in range(2):
    timer_cols = st.columns(5)
    for i in range(5):
        idx = row * 5 + i
        timer = st.session_state["timers"][idx]

        with timer_cols[i]:
            st.markdown('<div class="timer-box">', unsafe_allow_html=True)
            st.markdown(f"### {timer['name']}")
            if timer["running"]:
                timer["elapsed"] =
