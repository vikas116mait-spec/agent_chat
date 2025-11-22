You are an expert developer. Recreate this entire project exactly as described.

==============================================================
PROJECT: Local LLM Agent Chatbot (Fast + Tools + UI)
==============================================================

Build a complete project with this structure:

agent/
│
├── agent_app.py
│
├── controllers/
│   └── agent_controller.py
│
├── llm/
│   └── local_llm.py
│
├── tools/
│   ├── calculator.py
│   └── web_search.py
│
└── utils/
    └── json_parser.py


==============================================================
REQUIREMENTS
==============================================================

1. The agent must run on a **local LLM server** (Ollama compatible).
2. The agent must support 2 tools:
   - Calculator (safe AST evaluations)
   - DuckDuckGo web search
3. The agent must use a **custom controller** (NO LangChain).
4. The agent must:
   - detect math → use calculator
   - detect search queries → use web search
   - otherwise → respond with the LLM normally
5. The UI must be built in Streamlit:
   - Chat bubbles
   - Dark theme
   - Session history
   - Fast and responsive

6. The system must be fast:
   - Only ONE LLM call for normal chat
   - Immediate tool routing (no JSON necessary)
   - LLM used only to summarize tool outputs

7. Add JSON extraction utilities for safety.


==============================================================
FILE CONTENTS
==============================================================

----------------------------------------------
FILE: agent/agent_app.py
----------------------------------------------
import streamlit as st
from llm.local_llm import LocalLLM
from controllers.agent_controller import agent_controller

st.set_page_config(
    page_title="Agent Chatbot",
    page_icon="🤖",
    layout="centered",
)

st.markdown("""
<style>
.chat-bubble-user {
    background-color: #1f2937;
    color: white;
    padding: 12px 16px;
    border-radius: 12px;
    max-width: 80%;
    margin-bottom: 8px;
    align-self: flex-end;
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
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 Agent Chatbot")

if "history" not in st.session_state:
    st.session_state.history = []

llm = LocalLLM(
    model="llama3:8b-instruct-q4_K_M",
    base_url="http://10.10.110.25:11434"
)

for role, msg in st.session_state.history:
    if role == "user":
        st.markdown(f"<div class='chat-bubble-user'>🧑‍💻 {msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-bot'>🤖 {msg}</div>", unsafe_allow_html=True)

user_msg = st.chat_input("Type your message...")

if user_msg:
    st.session_state.history.append(("user", user_msg))
    st.markdown(f"<div class='chat-bubble-user'>🧑‍💻 {user_msg}</div>", unsafe_allow_html=True)

    with st.spinner("🤖 Thinking..."):
        reply, raw = agent_controller(user_msg, llm)

    st.session_state.history.append(("assistant", reply))
    st.markdown(f"<div class='chat-bubble-bot'>🤖 {reply}</div>", unsafe_allow_html=True)


----------------------------------------------
FILE: agent/controllers/agent_controller.py
----------------------------------------------
import re
from tools.calculator import calculator_tool
from tools.web_search import web_search_tool

def is_math(q):
    return bool(re.search(r"\d\s*[\+\-\*\/]\s*\d", q))

def is_search(q):
    return any(k in q.lower() for k in ["search", "find", "lookup", "google", "latest", "news"])

def agent_controller(user_input, llm):
    # Math tool
    if is_math(user_input):
        result = calculator_tool(user_input)["tool_result"]
        return f"🧮 Result: **{result}**", result

    # Web search
    if is_search(user_input):
        cleaned = user_input.replace("search", "").replace("find", "").strip()
        result = web_search_tool(cleaned)["tool_result"]
        summary_prompt = f"Summarize these results in clean bullet points:\n{result}"
        reply = llm(summary_prompt)
        return reply, result

    # Normal LLM chat
    prompt = f"You are a helpful assistant. Answer clearly:\n{user_input}"
    reply = llm(prompt)
    return reply, reply


----------------------------------------------
FILE: agent/tools/calculator.py
----------------------------------------------
import ast
import operator

ops = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

def eval_node(node):
    if isinstance(node, ast.Num):
        return node.n
    if isinstance(node, ast.BinOp):
        return ops[type(node.op)](eval_node(node.left), eval_node(node.right))
    raise ValueError("Invalid expression")

def calculator_tool(expr):
    tree = ast.parse(expr, mode="eval")
    value = eval_node(tree.body)
    return {"tool_result": value}


----------------------------------------------
FILE: agent/tools/web_search.py
----------------------------------------------
import requests
from bs4 import BeautifulSoup

def web_search_tool(query):
    url = "https://html.duckduckgo.com/html/"
    resp = requests.post(url, data={"q": query}, headers={"User-Agent": "Mozilla"})
    soup = BeautifulSoup(resp.text, "html.parser")

    results = []
    for a in soup.find_all("a", class_="result__a")[:3]:
        results.append(a.get_text())

    return {"tool_result": results}


----------------------------------------------
FILE: agent/llm/local_llm.py
----------------------------------------------
import requests
import json

class LocalLLM:
    def __init__(self, model, base_url):
        self.model = model
        self.url = f"{base_url}/api/generate"

    def __call__(self, prompt):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        r = requests.post(self.url, json=payload)
        data = r.json()
        return data.get("response", "")


----------------------------------------------
FILE: agent/utils/json_parser.py
----------------------------------------------
import json
import re

def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except:
        return None


==============================================================
README.md CONTENT
==============================================================

# 🚀 Agent Chatbot — Local LLM + Tools + Streamlit UI

A fast, modular AI Agent using:
- Local LLM (Ollama)
- Custom tool system
- Modern Streamlit UI
- Fast controller routing

## Features
- Calculator Tool
- Web Search Tool
- Natural Chat
- Dark UI with chat bubbles
- Modular code structure

## Run

