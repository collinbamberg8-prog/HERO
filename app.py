import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Hero AI", page_icon="🌑")
st.title("🌑 Hero")

# PASTE YOUR NEW KEY HERE
API_KEY = "AIzaSyAtV2u3HCQeyg_WAcdbLiNDm1vZBV2Li10" 
genai.configure(api_key=API_KEY)

# --- 2. MODEL INITIALIZATION ---
try:
    # Auto-detect available models for your key
    available_models = [m.name for m in genai.list_models()]
    
    # Selection logic: Flash 1.5 -> Pro -> fallback
    if 'models/gemini-1.5-flash' in available_models:
        selected_model = 'models/gemini-1.5-flash'
    elif 'models/gemini-pro' in available_models:
        selected_model = 'models/gemini-pro'
    else:
        selected_model = available_models[0]
    
    model = genai.GenerativeModel(model_name=selected_model)
    st.caption(f"System Status: Online ({selected_model})")
except Exception as e:
    st.error(f"Initialization Error: {e}")

# --- 3. CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Waiting for your command, Boss..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(
                prompt,
                generation_config={"candidate_count": 1}
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"AI Error: {e}")





