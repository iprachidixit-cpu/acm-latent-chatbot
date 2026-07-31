import os
import random
import time
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

AVATARS = {
    "RoastBot": "🔥",
    "ShakespeareBot": "🎭",
    "Emoji Translator Bot": "😂"
}

INTROS = {
    "RoastBot": "🔥 *The mic is hot. Say something — I dare you.*",
    "ShakespeareBot": "🎭 *Pray, speaker, what dost thou wish to discuss?*",
    "Emoji Translator Bot": "😂 *type anything... i'll emoji-fy it 🔥💯*"
}

st.set_page_config(page_title="India's Got Latent - Chatbot", page_icon="🎤")

# Custom background gradient via CSS injection
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0E1117 0%, #1a1a2e 100%);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎤 India's Got Latent — Chatbot Act")

# --- Sidebar: persona picker ---
st.sidebar.header("Choose Your Act")
persona_name = st.sidebar.selectbox("Pick a persona:", list(PERSONAS.keys()))

# --- Initialize memory only once per session ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.current_persona = persona_name

# Reset memory when persona changes mid-session
if persona_name != st.session_state.current_persona:
    st.session_state.messages = []
    st.session_state.current_persona = persona_name
    st.sidebar.info(f"Switched to {persona_name}! Starting a fresh act.")

# Themed intro caption
st.caption(INTROS[persona_name])

# --- Display chat history ---
for msg in st.session_state.messages:
    avatar = AVATARS[persona_name] if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# --- Chat input ---
user_input = st.chat_input("Say something to the judges...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    full_conversation = [
        {"role": "system", "content": PERSONAS[persona_name]}
    ] + st.session_state.messages

    with st.chat_message("assistant", avatar=AVATARS[persona_name]):
        with st.spinner("Thinking of a comeback..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=full_conversation
            )
            bot_reply = response.choices[0].message.content

        # Typewriter effect: reveal the reply letter by letter
        placeholder = st.empty()
        displayed = ""
        for char in bot_reply:
            displayed += char
            placeholder.markdown(displayed + "▌")  # cursor-like blinker at the end
            time.sleep(0.015)
        placeholder.markdown(displayed)  # final clean version, no cursor

        # Celebratory flourish - now 70% chance
        if random.random() < 0.5:
            st.balloons()

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})