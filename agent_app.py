import streamlit as st
from llm.local_llm import LocalLLM
from controllers.agent_controller import agent_controller

# ------------------------------------------
# PAGE CONFIG
# ------------------------------------------
st.set_page_config(
    page_title="Agent Chatbot",
    page_icon="🤖",
    layout="centered",
)

# ------------------------------------------
# CUSTOM CSS FOR BEAUTIFUL UI
# ------------------------------------------
st.markdown("""
<style>

body {
    background-color: #0d0f17;
}

.chat-bubble-user {
    background-color: #1f2937;
    color: white;
    padding: 12px 16px;
    border-radius: 12px;
    max-width: 80%;
    margin-bottom: 8px;
    align-self: flex-end;
    box-shadow: 0 0 4px rgba(255,255,255,0.1);
}

.chat-bubble-bot {
    background-color: #111827;
    color: #f3f4f6;
    padding: 12px 16px;
    border-radius: 12px;
    max-width: 80%;
    margin-bottom: 8px;
    align-self: flex-start;
    border-left: 4px solid #10b981;
    box-shadow: 0 0 6px rgba(0,255,180,0.15);
}

.tool-message {
    background-color: #0e1b24;
    color: #a7f3d0;
    padding: 10px;
    border-radius: 8px;
    font-size: 13px;
    margin: 6px 0;
    border-left: 3px solid #34d399;
}

.stChatMessage > div {
    padding: 0px !important;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------
# TITLE HEADER
# ------------------------------------------
st.markdown("<h1 style='text-align: center; color: #e5e7eb;'>🤖 Agent Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af; margin-top: -10px; margin-bottom: 25px;'>Smart Agent • Calculator • Web Search • Natural Chat</p>", unsafe_allow_html=True)

# ------------------------------------------
# SETUP SESSION HISTORY
# ------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ------------------------------------------
# CONNECT TO LOCAL MODEL
# ------------------------------------------
llm = LocalLLM(
    model="llama3:8b-instruct-q4_K_M",
    base_url="http://10.10.110.25:11434"
)

# ------------------------------------------
# RENDER CHAT HISTORY BEAUTIFULLY
# ------------------------------------------
for role, msg in st.session_state.history:
    if role == "user":
        st.markdown(f"<div class='chat-bubble-user'>🧑‍💻 {msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-bot'>🤖 {msg}</div>", unsafe_allow_html=True)

# ------------------------------------------
# USER INPUT BOX
# ------------------------------------------
user_input = st.chat_input("Type your message...")

# ------------------------------------------
# MAIN CHAT LOGIC
# ------------------------------------------
if user_input:
    # Add user bubble
    st.session_state.history.append(("user", user_input))
    st.markdown(f"<div class='chat-bubble-user'>🧑‍💻 {user_input}</div>", unsafe_allow_html=True)

    with st.spinner("🤖 Thinking..."):
        reply, raw = agent_controller(user_input, llm)

    # Add bot bubble
    st.session_state.history.append(("assistant", reply))
    st.markdown(f"<div class='chat-bubble-bot'>🤖 {reply}</div>", unsafe_allow_html=True)
