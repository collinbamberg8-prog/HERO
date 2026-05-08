import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Hero AI", page_icon="🌑")
st.title("🌑 Hero")

# ENTER YOUR API KEY HERE
API_KEY = "AIzaSyCOZnDV2NCLDzIznYx6FlxeYzs5EPvsJBs" 
genai.configure(api_key=API_KEY)

# --- 2. MODEL INITIALIZATION ---
try:
    # Check for available models to avoid 404 errors
    available_models = [m.name for m in genai.list_models()]
    if 'models/gemini-1.5-flash' in available_models:
        selected_model = 'gemini-1.5-flash'
    else:
        selected_model = 'gemini-pro'
    
    model = genai.GenerativeModel(selected_model)
    st.caption(f"System Status: Online ({selected_model})")
except Exception as e:
    st.error(f"Initialization Error: {e}")

# --- 3. CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Waiting for your command, Boss..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Assistant Response
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"AI Error: {e}")



