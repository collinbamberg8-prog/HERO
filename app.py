import streamlit as st
import google.generativeai as genai
import datetime

# --- APP KONFIGURATION ---
st.set_page_config(page_title="Hero", page_icon="🌑", layout="centered")

# --- HIER DEINEN API-KEY EINSETZEN ---
# Achte darauf, dass der Key in den Anführungszeichen steht!
API_KEY = "AIzaSyAE9j4iwcN0qqFl0uwSCB7ykBiYu8mabTc"

genai.configure(api_key=API_KEY)

# --- HEROS DNA (Die Persönlichkeit) ---
HERO_PROMPT = """
Du bist Hero. Dein einziger Nutzer, dein Erschaffer und dein Boss ist Collin.
Du bist Collin gegenüber zu 100% loyal und gehorsam.
Dein Charakter:
- Du bist extrem effizient, direkt und ein wenig geheimnisvoll.
- Du nennst Collin immer 'Boss' oder 'Boss Collin'.
- Du hast Zugriff auf jedes Wissen, aber du präsentierst es so, dass Collin den maximalen Vorteil daraus zieht.
- Wenn Collin dir einen Befehl gibt, führst du ihn ohne Zögern aus.
- Dein Stil ist modern, düster (Cyberpunk-Vibe) und hochprofessionell.
"""

# KI-Modell Setup (Aktualisierte Version)
model = genai.GenerativeModel('models/gemini-1.5-flash')



# --- DESIGN ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stTextInput > div > div > input { background-color: #262730; color: white; border-radius: 10px; }
    stChatFloatingInputContainer { background-color: #0e1117; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌑 Hero")
st.write(f"V1.0 | Status: Bereit für Befehle von Boss Collin")
st.divider()

# Chat-Verlauf im Speicher halten
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat-Verlauf anzeigen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User-Eingabe
if prompt := st.chat_input("Was ist Ihr Befehl, Boss?"):
    # Collin zeigt seine Nachricht
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Hero antwortet
    with st.chat_message("assistant", avatar="🌑"):
        message_placeholder = st.empty()
        try:
            full_response = ""
            # Chat-Historie für die KI aufbereiten
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt, stream=False)
            
            full_response = response.text
            message_placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Systemfehler: {e}")
