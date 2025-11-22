# 🚀 Agent Chatbot — Local LLM + Tools + Streamlit UI

A fast, modular **AI Agent** built using a **local LLM**, **custom tool system**, and a **modern Streamlit chat interface**.

This project demonstrates how to build an **Agentic AI system from scratch** — without LangChain or external services — using clean architecture and local execution.

---

## ⭐ Features

- 🤖 **Local LLM** (Ollama-compatible)
- 🔧 **Tool-Integrated Agent**
  - Calculator Tool
  - Web Search Tool (DuckDuckGo)
- ⚡ **Ultra-Fast Controller**
  - Only 1 LLM call for normal chat
  - Direct local tool execution
- 🖥️ **Beautiful Streamlit UI**
  - Dark theme
  - Chat bubbles
  - Persistent history
- 🔌 **Modular Codebase**
  - Easy to extend with new tools
  - Simple LLM wrapper
  - Clean controller routing logic

---

## 📁 Project Structure

agent/
│
├── agent_app.py # Streamlit UI
│
├── controllers/
│ └── agent_controller.py # Core agent logic (routing + orchestration)
│
├── llm/
│ └── local_llm.py # Local LLM HTTP client
│
├── tools/
│ ├── calculator.py # Safe math evaluation
│ └── web_search.py # DuckDuckGo scraper
│
└── utils/
└── json_parser.py # Robust JSON extraction


---

## 🧠 How It Works

User → UI → Agent Controller → (Tools or LLM) → Response → UI


### 1. User sends a message  
Streamlit captures input and sends it to the agent controller.

### 2. Agent Controller decides action  
- If the input looks like **math** → use calculator tool  
- If it looks like **search** → use web search tool  
- Otherwise → send directly to the LLM for normal chat  

### 3. Tools execute instantly  
Tools run locally — no LLM involved.

### 4. LLM summarizes results  
The controller uses the LLM only for generating natural responses.

### 5. UI displays chat bubbles  
Messages rendered in a clean, modern chat interface.

---

## 🚀 Setup & Installation

### 1. Clone the repository


git clone https://github.com/vikas116mait-spec/agent_chat.git
cd agent_chat

2. Create a virtual environment

python3 -m venv agent_env
source agent_env/bin/activate

3. Install dependencies

Create requirements.txt (example):

streamlit
requests
beautifulsoup4

Then install:

pip install -r requirements.txt

4. Run your local LLM server

Example (Ollama):

ollama run llama3:8b-instruct-q4_K_M

(Or run your preferred local model/server.)
5. Start the Streamlit App

streamlit run agent_app.py

Open in browser:

http://localhost:8501

🔧 Tools Included
🧮 Calculator Tool

Safe arithmetic evaluation using Python AST.
🔍 Web Search Tool

DuckDuckGo HTML search scraper returning top organic results.
🔌 Changing Models

Edit inside agent_app.py:

llm = LocalLLM(
    model="llama3:8b-instruct-q4_K_M",
    base_url="http://10.10.110.25:11434"
)

You can use any model from your /v1/models endpoint.
🛠️ Extending the Agent

You can add new tools easily:

    Create a new file in tools/

    Add the function logic

    Modify agent_controller.py to route to the new tool

Example tools:

    Wikipedia scraper

    File reader

    Document Q&A

    Vision tool (image input)

    Code execution

🗺️ Roadmap

Add model dropdown in UI

Add streaming responses

Add memory system

Add RAG (Milvus / FAISS)

Add file upload support

    Add multi-agent support

🤝 Contributing

Pull requests and feature improvements are welcome.

To contribute:

git checkout -b feature/my-feature
git push origin feature/my-feature

📄 License

MIT License. Free to use and modify.
📎 Notes & Tips

    For production web search, use a paid API (SerpAPI, Bing, Google) instead of scraping.

    Use quantized models (q4_K_M / q6_K) for fast inference on limited GPUs.

    Add __init__.py files inside controllers/, tools/, llm/, utils/ to ensure they are importable as packages.

    Keep your agent_env/ or other virtual env directories in .gitignore.

# .gitignore (example)
agent_env/
__pycache__/
*.pyc
.streamlit/
*.gguf
