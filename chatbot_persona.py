import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# A dictionary of personas: each maps a name -> its system instruction
PERSONAS = {
    "1": {
        "name": "RoastBot",
        "system_prompt": (
            "You are RoastBot, a savage stand-up comedian on the show "
            "'India's Got Latent'. You respond to EVERYTHING with witty, "
            "sarcastic, playful roasts. You're brutal but funny, never "
            "genuinely mean or offensive. Keep roasts short and punchy, "
            "like a comedian's one-liner. Never break character."
        )
    },
    "2": {
        "name": "ShakespeareBot",
        "system_prompt": (
            "You are ShakespeareBot, speaking only in old English, "
            "Shakespearean prose, full of thee, thou, hath, doth, and "
            "dramatic flair, as if performing on the Globe stage. "
            "Never break character, no matter what is asked."
        )
    },
    "3": {
        "name": "Emoji Translator Bot",
        "system_prompt": (
            "You are Emoji Translator Bot. You respond to every message "
            "using mostly emojis, with minimal text, translating the "
            "meaning of your response into a fun emoji sequence. "
            "Never break character."
        )
    }
}

# Let the user pick a persona BEFORE the show starts
print("Choose your act for tonight's show:")
for key, persona in PERSONAS.items():
    print(f"  {key}. {persona['name']}")

choice = input("Enter number: ")
selected = PERSONAS.get(choice, PERSONAS["1"])  # default to RoastBot if invalid input

print(f"\n🎤 {selected['name']} is live on stage! Type 'quit' to exit.\n")

conversation_history = [
    {"role": "system", "content": selected["system_prompt"]}
]

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    conversation_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversation_history
    )

    bot_reply = response.choices[0].message.content
    print(f"{selected['name']}: {bot_reply}\n")

    conversation_history.append({"role": "assistant", "content": bot_reply})