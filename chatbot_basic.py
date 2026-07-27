import os
from dotenv import load_dotenv
from groq import Groq

# Load the secret key from our .env file into the program
load_dotenv()

# Create a "client" - this is our connector to talk to Groq's AI
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# This list will hold our whole conversation so the AI can "remember"
conversation_history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

print("Chatbot is ready! Type 'quit' to exit.\n")

while True:
    # Ask the user to type something
    user_input = input("You: ")

    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    # Add the user's message to our memory list
    conversation_history.append({"role": "user", "content": user_input})

    # Send the WHOLE conversation history to Groq, so it has context
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversation_history
    )

    # Extract just the text reply from the response
    bot_reply = response.choices[0].message.content

    # Show it to the user
    print(f"Bot: {bot_reply}\n")

    # Add the bot's reply to memory too, so it remembers what IT said
    conversation_history.append({"role": "assistant", "content": bot_reply})