import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Hero AI", page_icon="🌑")
st.title("🌑 Hero")

# ENTER YOUR API KEY HERE
API_KEY = "PASTE_YOUR_AIZA_KEY_HERE" 
genai.configure(api_key=API_KEY)

# --- 2. MODEL INITIALIZATION ---
try:
    # Check for available models to ensure we use a valid path
    available_models = [m.name for m in genai.list_models()]
    
    # We use the full 'models/' prefix to avoid the v1beta 404 error
    if 'models/gemini-1.5-flash' in available_models:
        selected_model = 'models/gemini-1.5-flash'
    else:
        selected_model = 'models/gemini-pro'
    
    model = genai.GenerativeModel(model_name=selected_model)
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
            # Using stable generation config to prevent crashes
            response = model.generate_content(
                prompt,
                generation_config={"candidate_count": 1}
            )
            st.markdown(response.text)
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"AI Error: {e}")
            st.info("Note: If you see a 404, please wait 1 minute for the API key to sync.")




