import streamlit as st
import google.generativeai as genai

# --- CONFIG ---
st.set_page_config(page_title="Hero", page_icon="🌑")

# 1. HIER DEINEN KEY EINSETZEN
API_KEY = "DEIN_API_KEY_HIER"
genai.configure(api_key=API_KEY)

st.title("🌑 Hero")

# 2. DAS MODELL LADEN (Neue Schreibweise)
try:
    # Wir versuchen die stabilste Version
    model = genai.GenerativeModel('gemini-1.5-flash')
    
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
                # Direkter Aufruf ohne Umwege
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"KI-Fehler: {e}")
                st.info("Hinweis: Prüfe, ob dein API-Key im Google AI Studio aktiv ist.")

except Exception as e:
    st.error(f"System-Setup-Fehler: {e}")

