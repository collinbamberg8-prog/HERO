import streamlit as st
import google.generativeai as genai

# --- 1. SETUP ---
st.set_page_config(page_title="Hero", page_icon="🌑")
st.title("🌑 Hero")

# HIER DEINEN KEY EINSETZEN
API_KEY = "AIzaSy..." # Dein Key aus dem AI Studio
genai.configure(api_key=API_KEY)

# --- 2. MODELL-SUCHE ---
try:
    # Wir suchen automatisch, was dein Key erlaubt
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # Priorität: Flash 1.5 -> Pro -> Erstes verfügbares
    if 'models/gemini-1.5-flash' in models:
        m_name = 'gemini-1.5-flash'
    elif 'models/gemini-pro' in models:
        m_name = 'gemini-pro'
    else:
        m_name = models[0].replace('models/', '')
    
    model = genai.GenerativeModel(m_name)
    st.write(f"V1.0 | Status: Bereit ({m_name})")
except Exception as e:
    st.error(f"Setup-Fehler: {e}")

# --- 3. CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

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
            st.error(f"KI-Fehler: {e}")

