"""Groq chat adapter. JSON syntax is requested; V2 validates the schema locally."""
import json
from urllib.request import Request, urlopen


def generate_groq(key, model, system, contents, schema=None):
    if schema:
        system += '\nReturn only a JSON object matching this schema: ' + json.dumps(schema)
    messages = [{'role': 'system', 'content': system}]
    if isinstance(contents, str):
        messages.append({'role': 'user', 'content': contents})
    else:
        messages.extend({'role': 'assistant' if turn.role == 'model' else 'user',
                         'content': '\n'.join(p.text for p in turn.parts if p.text)}
                        for turn in contents)
    body = {'model': model, 'messages': messages, 'temperature': 0.2,
            'max_completion_tokens': 2048}
    if schema:
        body['response_format'] = {'type': 'json_object'}
    request = Request('https://api.groq.com/openai/v1/chat/completions',
                      data=json.dumps(body).encode(), headers={
                          'Content-Type': 'application/json',
                          'Authorization': 'Bearer ' + key,
                          'User-Agent': 'AI-Escape-Room/1.0'}, method='POST')
    with urlopen(request, timeout=60) as response:
        result = json.load(response)
    choice = result['choices'][0]
    text = choice['message'].get('content')
    if choice.get('finish_reason') != 'stop' or not isinstance(text, str) or not text.strip():
        raise ValueError('Empty or incomplete model response')
    return text
