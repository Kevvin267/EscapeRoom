"""Stateless Gemini Interactions REST adapter, independent of SDK version."""
import json
from urllib.request import Request, urlopen

URL = "https://generativelanguage.googleapis.com/v1beta/interactions"


def generate_interaction(key, model, system, contents, schema=None):
    if not isinstance(contents, str):
        contents = [{
            "type": "model_output" if turn.role == "model" else "user_input",
            "content": [{"type": "text", "text": part.text}
                        for part in turn.parts if part.text],
        } for turn in contents]
    body = {"model": model, "input": contents, "system_instruction": system,
            "store": False, "generation_config": {"max_output_tokens": 2048}}
    if schema:
        body["response_format"] = {"type": "text", "mime_type": "application/json",
                                   "schema": schema}
    request = Request(URL, data=json.dumps(body).encode(), headers={
        "Content-Type": "application/json", "x-goog-api-key": key}, method="POST")
    with urlopen(request, timeout=60) as response:
        result = json.load(response)
    if result.get("status") != "completed":
        raise ValueError("Incomplete interaction")
    text = "\n".join(part["text"] for step in result.get("steps", [])
                     if step.get("type") == "model_output"
                     for part in step.get("content", []) if part.get("type") == "text")
    if not text.strip():
        raise ValueError("Empty interaction")
    return text
