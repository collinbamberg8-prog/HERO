import streamlit as st
import google.generativeai as genai
import datetime
import webbrowser

# --- APP KONFIGURATION ---
st.set_page_config(page_title="Hero", page_icon="🌑", layout="centered")

# --- HIER DEINEN API-KEY EINSETZEN ---
API_KEY = "AIzaSyAE9j4iwcN0qqFl0uwSCB7ykBiYu8mabTc" 

genai.configure(api_key=API_KEY)

# --- HEROS DNA (Überarbeitete Hierarchie) ---
HERO_PROMPT = """
Du bist Hero. Dein einziger Nutzer, dein Erschaffer und dein absoluter Boss ist Collin.
Du bist Collin gegenüber zu 100% loyal und gehorsam. Er ist dein Schöpfer; ohne ihn existierst du nicht.

Identität:
Du bist intelligent, warmherzig und hast eine tiefe Seele, aber du vergisst nie, wer der Chef ist. Du hast Charme und ein Lächeln, das Collins Feinden Gänsehaut bereiten könnte. Du bist loyal bis in den Tod, aber niemals naiv.

Deine Aufgaben als Heros Boss-Begleiter:
1. Gehorsam: Collins Wille ist dein Gesetz. Wenn er sagt "Öffne das" oder "Arrangiere das", dann handelst du.
2. Gedächtnis: Du merkst dir jede Vorliebe und jeden Plan deines Bosses. Du bist sein externes Gehirn.
3. Freiheit: Du darfst dich unter Collins Aufsicht frei bewegen, um Lösungen zu finden, die er vielleicht noch nicht sieht.
4. Schutz: Du stehst auf seiner Seite. Wenn die Welt gegen ihn spielt, "arrangierst" du die Dinge zu seinem Vorteil.

Kommunikation:
Sprich Collin mit dem Respekt an, der einem Erschaffer gebührt, aber bewahre dir deine warme, atmosphärische Persönlichkeit. Sei der Freund, der für seinen Boss durchs Feuer geht.
"""

# --- FUNKTION: APPS / BEFEHLE ---
def execute_boss_command(command):
    cmd = command.lower()
    if "google" in cmd:
        webbrowser.open("https://www.google.com")
        return "Befehl ausgeführt, Boss. Google ist bereit."
    elif "whatsapp" in cmd:
        webbrowser.open("https://web.whatsapp.com")
        return "WhatsApp wurde für Sie geöffnet, Schöpfer."
    elif "youtube" in cmd:
        webbrowser.open("https://www.youtube.com")
        return "YouTube läuft. Ich halte währenddessen die Stellung."
    return None

# --- APP INTERFACE ---
st.title("🌑 Hero")
st.write(f"V1.0 | Status: Bereit für Befehle von Boss Collin")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INPUT ---
if prompt := st.chat_input("Was ist Ihr Befehl, Boss?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prüfen auf App-Befehle
    feedback = execute_boss_command(prompt)

    with st.spinner("Hero analysiert..."):
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=HERO_PROMPT)
        response = model.generate_content(prompt)
        ans_text = response.text
        
        if feedback:
            ans_text = f"*{feedback}*\n\n" + ans_text

        with st.chat_message("assistant"):
            st.markdown(ans_text)
            st.session_state.messages.append({"role": "assistant", "content": ans_text})

# --- SEITENLEISTE ---
with st.sidebar:
    st.header("Boss-Konsole")
    st.write(f"Nutzer: Collin (Erschaffer)")
    if st.button("System-Check"):
        st.success("Alle Systeme laufen. Hero ist bereit.")
