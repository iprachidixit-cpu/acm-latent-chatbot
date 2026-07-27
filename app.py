import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

PERSONAS = {
    "RoastBot": (
        "You are RoastBot, a savage stand-up comedian on the show "
        "'India's Got Latent'. You respond to EVERYTHING with witty, "
        "sarcastic, playful roasts. You're brutal but funny, never "
        "genuinely mean or offensive. Keep roasts short and punchy, "
        "like a comedian's one-liner. Never break character."
    ),
    "ShakespeareBot": (
        "You are ShakespeareBot, speaking only in old English, "
        "Shakespearean prose, full of thee, thou, hath, doth, and "
        "dramatic flair, as if performing on the Globe stage. "
        "Never break character, no matter what is asked."
    ),
    "Emoji Translator Bot": (
        "You are Emoji Translator Bot. You respond to every message "
        "using mostly emojis, with minimal text, translating the "
        "meaning of your response into a fun emoji sequence. "
        "Never break character."
    )
}

st.set_page_config(page_title="India's Got Latent - Chatbot", page_icon="🎤")
st.title("🎤 India's Got Latent — Chatbot Act")

# --- Sidebar: persona picker (the "choose your act before the show" step) ---
st.sidebar.header("Choose Your Act")
persona_name = st.sidebar.selectbox("Pick a persona:", list(PERSONAS.keys()))

# --- Initialize memory (the "backpack") only ONCE per session ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.current_persona = persona_name

# If user switches persona mid-session, reset memory for a fresh act
if persona_name != st.session_state.current_persona:
    st.session_state.messages = []
    st.session_state.current_persona = persona_name
    st.sidebar.info(f"Switched to {persona_name}! Starting a fresh act.")

# --- Display all past messages on screen ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat input box at the bottom ---
user_input = st.chat_input("Say something to the judges...")

if user_input:
    # Show the user's message immediately
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Build the full conversation to send: system prompt + full history
    full_conversation = [
        {"role": "system", "content": PERSONAS[persona_name]}
    ] + st.session_state.messages

    # Get the bot's reply
    with st.chat_message("assistant"):
        with st.spinner("Thinking of a comeback..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=full_conversation
            )
            bot_reply = response.choices[0].message.content
            st.markdown(bot_reply)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})