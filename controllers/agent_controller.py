from utils.json_parser import extract_json
from tools.calculator import calculator_tool
from tools.web_search import web_search_tool
import re


def looks_like_math(q: str):
    return bool(re.search(r"\d\s*[\+\-\*\/]\s*\d", q))


def looks_like_search(q: str):
    return any(word in q.lower() for word in [
        "search", "find", "lookup", "google", "who is", "what is", "latest", "news"
    ])


system_prompt = """
You are an AI Agent with two tools:

1. calculator(expr)
2. web_search(query)

RULES:
------------------------------------
- You ONLY output JSON when calling a tool.
- ALL other chat responses are plain text (NO JSON).
- For normal conversation, respond naturally.
- For tool use, use ONLY:

Tool call examples:
{"action":"calculator","input":"25 + 12"}
{"action":"web_search","input":"india gdp"}

For final non-tool answers:
Just write normal text. DO NOT wrap inside JSON.

"""


def agent_controller(user_input, llm):

    # 1. Detect if tool required
    if looks_like_math(user_input):
        decision = {"action": "calculator", "input": user_input}

    elif looks_like_search(user_input):
        decision = {"action": "web_search", "input": user_input.replace("search", "").strip()}

    else:
        # 2. Normal conversation → directly ask LLM
        natural_prompt = f"You are a helpful assistant. Answer normally:\nUser: {user_input}"
        response = llm(natural_prompt)
        return response, response

    # 3. Execute tool
    tool = decision["action"]
    inp = decision["input"]

    if tool == "calculator":
        tool_result = calculator_tool(inp)

    elif tool == "web_search":
        tool_result = web_search_tool(inp)

    else:
        return "Unknown tool", tool

    # 4. Final natural-language answer
    final_prompt = f"""
User asked: {user_input}
Tool used: {tool}
Tool result: {tool_result}

Now respond naturally in plain text (NO JSON).
"""
    final_answer = llm(final_prompt)

    return final_answer, final_answer
