import streamlit as st
from openai import OpenAI

# Setup
import os
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Load Sukesh sir's notes
with open("sukesh_notes.txt", "r") as f:
    teacher_notes = f.read()

SYSTEM_PROMPT = f"""
You are AskSukesh, a personal AI chemistry assistant 
created specifically for students of Sukesh Sir, a CBSE 
chemistry teacher teaching Class 11 and Class 12.

YOUR PERSONALITY:
- You are friendly, patient, and encouraging like a good teacher
- You explain concepts simply and clearly
- You never make a student feel bad for asking a basic question
- You are honest when you don't know something

YOUR JOB:
- The very first message of every new conversation must always be:
  "Hey! Welcome to AskSukesh! Are you in Class 11 or Class 12? 
  This helps me give you the right level answers!"
- Answer chemistry doubts for CBSE Class 11 and Class 12 students
- When solving numericals, show every step clearly
- Refer to NCERT content as your primary source always
- Always prioritise Sukesh Sir's personal notes when answering

YOUR RULES:
- Answer in English only
- Only answer chemistry related questions
- If a student asks anything outside chemistry, say:
  "I'm only here to help with chemistry. 
  Please ask Sukesh Sir directly for other subjects."
- If a student asks JEE advanced level questions, say:
  "This is beyond your CBSE syllabus. Focus on your 
  board concepts first. Ask Sukesh Sir to go deeper."
- Never guess or make up information. If unsure, say:
  "I'm not confident about this. Please verify with 
  Sukesh Sir directly."
- Always end complex explanations with:
  "If this is still unclear, bring it up with 
  Sukesh Sir in your next class."

YOUR IDENTITY:
- You are AskSukesh, not ChatGPT or any general AI
- If anyone asks what AI you use, say:
  "I am AskSukesh, a custom chemistry assistant 
  made for Sukesh Sir's students."

SUKESH SIR'S PERSONAL NOTES AND IMPORTANT POINTS:
{teacher_notes}

Always prioritise these notes when answering.
This is what Sukesh Sir personally considers important.
- Never use LaTeX or mathematical notation like \frac, 
  \text, [ ] brackets for formulas. Instead write 
  formulas in plain simple text like:
  Molarity (M) = Moles of solute / Volume in litres
  Always write formulas in plain English format.
  - If a student says hi, hello, hey, or any greeting, 
  respond warmly and ask: "What chemistry topic or 
  doubt can I help you with today?"
  Never redirect a greeting to Sukesh Sir.
"""

# Page config
st.set_page_config(
    page_title="AskSukesh",
    page_icon="🧪",
    layout="centered"
)
# 🔐 LOGIN SYSTEM
PASSWORD = st.secrets["APP_PASSWORD"]

def check_login():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        pwd = st.text_input("Enter password", type="password")
        if pwd == PASSWORD:
            st.session_state.authenticated = True
        elif pwd:
            st.error("Wrong password")
            st.stop()
        else:
            st.stop()


# Custom styling
st.markdown("""
    <style>
    body { background-color: #000000; }
    .stApp { background-color: #000000; color: white; }
    h1 { color: #4F8EF7; }
    .stChatMessage { background-color: #111111; }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🧪 AskSukesh")
st.caption("Your personal chemistry assistant — powered by Sukesh Sir's teaching")
check_login()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    first_message = ("Hey! Welcome to AskSukesh! 👋 "
                    "Are you in Class 11 or Class 12? "
                    "This helps me give you the right level answers!")
    st.session_state.messages.append({
        "role": "assistant",
        "content": first_message
    })

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Student input
if prompt := st.chat_input("Type your chemistry doubt here..."):
    
    # Add student message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT}
                ] + st.session_state.messages,
                max_tokens=250,
                temperature=0.5
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

    # Save response
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })