import requests
from bs4 import BeautifulSoup

def web_search_tool(query):
    try:
        url = "https://html.duckduckgo.com/html/"
        res = requests.post(url, data={"q": query}, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        results = []
        for r in soup.select(".result__snippet")[:3]:
            results.append(r.get_text(strip=True))

        return {"tool_result": results}
    except Exception as e:
        return {"tool_result": f"Search error: {e}"}
