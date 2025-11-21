import json

def extract_json(text):
    try:
        start = text.find("{")
        end = text.rfind("}")
        return json.loads(text[start:end+1])
    except:
        return None
