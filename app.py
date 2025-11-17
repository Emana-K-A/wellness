import os
import gradio as gr 
from groq import Groq

# Initialize the Groq client securely
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# System instruction
def initialize_messages():
    return [{
        "role": "system",
        "content": """You are a supportive listener who provides
        motivational, non-medical emotional guidance. You help the user
        reduce stress, stay positive, and find simple coping strategies."""
    }]

messages_prmt = initialize_messages()

# Chat function
def customLLMBot(user_input, history):
    global messages_prmt

    messages_prmt.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        messages=messages_prmt,
        model="llama-3.3-70b-versatile",
    )

    LLM_reply = response.choices[0].message.content
    messages_prmt.append({"role": "assistant", "content": LLM_reply})

    return LLM_reply

# Gradio interface
iface = gr.ChatInterface(
    fn=customLLMBot,
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(placeholder="Share what's on your mind"),
    title="Wellness Companion",
    description="A gentle, non-medical emotional support chatbot to help you relax and stay positive.",
    theme="soft",
    examples=[
        "I feel stressed",
        "I am not motivated today",
        "I need some positivity"
    ]
)

# Launch the app
iface.launch()
