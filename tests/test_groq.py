import io
import json
from types import SimpleNamespace
from urllib.error import HTTPError
import pytest
from escape_room import groq_adapter, llm


def test_json_request(monkeypatch):
    def respond(request, timeout):
        body = json.loads(request.data)
        assert request.full_url == 'https://api.groq.com/openai/v1/chat/completions'
        assert body['response_format'] == {'type': 'json_object'}
        assert 'schema' in body['messages'][0]['content']
        assert body['messages'][1]['content'] == 'look'
        return io.BytesIO(b'{"choices":[{"finish_reason":"stop","message":{"content":"{}"}}]}')
    monkeypatch.setattr(groq_adapter, 'urlopen', respond)
    assert groq_adapter.generate_groq('fake', 'model', 'rules', 'look', {'type':'object'}) == '{}'


def test_v1_history(monkeypatch):
    def respond(request, timeout):
        messages = json.loads(request.data)['messages']
        assert [m['role'] for m in messages] == ['system', 'user', 'assistant']
        return io.BytesIO(b'{"choices":[{"finish_reason":"stop","message":{"content":"hello"}}]}')
    monkeypatch.setattr(groq_adapter, 'urlopen', respond)
    turns = [SimpleNamespace(role=r, parts=[SimpleNamespace(text='hi')]) for r in ['user','model']]
    assert groq_adapter.generate_groq('fake','model','rules',turns) == 'hello'


def test_truncated_response_rejected(monkeypatch):
    monkeypatch.setattr(groq_adapter, 'urlopen', lambda *a, **kw: io.BytesIO(
        b'{"choices":[{"finish_reason":"length","message":{"content":"partial"}}]}'))
    with pytest.raises(ValueError):
        groq_adapter.generate_groq('fake','model','rules','look')


def test_provider_isolation_and_safe_error(monkeypatch):
    monkeypatch.setenv('LLM_PROVIDER','groq')
    monkeypatch.setenv('GROQ_API_KEY','private-groq')
    monkeypatch.setenv('GROQ_MODEL','model')
    monkeypatch.setenv('GEMINI_API_KEY','private-google')
    def fail(key, *a):
        assert key == 'private-groq'
        raise HTTPError('url',429,'private-groq',{},None)
    monkeypatch.setattr(groq_adapter,'generate_groq',fail)
    with pytest.raises(llm.ModelUnavailable) as caught:
        llm.generate('rules','look')
    assert 'Groq' in str(caught.value) and '429' in str(caught.value)
    assert 'private' not in str(caught.value)
