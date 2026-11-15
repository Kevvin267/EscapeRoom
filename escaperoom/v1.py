"""Baseline: the LLM owns all game decisions through conversation history."""
from escape_room.llm import generate
from escape_room.world import RULES


def respond(history, message):
    from google.genai import types
    contents = [types.Content(
        role="model" if row["role"] == "assistant" else "user",
        parts=[types.Part(text=row["content"])]) for row in history]
    contents.append(types.Content(role="user", parts=[types.Part(text=message)]))
    return generate("You are the Game Master of The Locked Library.\n" + RULES, contents)
