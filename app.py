import streamlit as st
import google.generativeai as genai

# --- 1. KEY EINSETZEN ---
# Ersetze den Text unten durch deinen kopierten Key
API_KEY = "AIzaSyCOZnDV2NCLDzIznYx6FlxeYzs5EPvsJBs" 
genai.configure(api_key=API_KEY)

# --- 2. PERSÖNLICHKEIT ---
HERO_PROMPT = "Du bist Hero. Dein einziger Nutzer ist Boss Collin. Sei loyal, effizient und direkt."

# --- 3. SETUP ---
st.set_page_config(page_title="Hero", page_icon="🌑")
st.title("🌑 Hero")

# Wir nehmen das Modell, das sicher mit deinem Key funktioniert
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=HERO_PROMPT)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Was ist Ihr Befehl, Boss?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Fehler: {e}")

