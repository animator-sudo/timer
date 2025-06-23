import streamlit as st
import time
import base64
from streamlit_autorefresh import st_autorefresh

# Auto-Refresh alle 1 Sekunde
st_autorefresh(interval=1000, key="refresh")

# Seiteneinstellungen und Titel
st.set_page_config(page_title="Ilgen Lions Timer", layout="wide")
st.title("Ilgen Lions Timer")
st.write("Drücke 'Start', um den Timer zu starten, 'Pause', um anzuhalten und 'Reset', um den Timer zurückzusetzen.")

# Hintergrundbild als Base64
with open("ilgen_lions.png", "rb") as f:
    img_data = f.read()
b64 = base64.b64encode(img_data).decode()

# CSS Styling
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
         padding: 16px;
         border-radius: 12px;
         text-align: center;
         margin-bottom: 16px;
