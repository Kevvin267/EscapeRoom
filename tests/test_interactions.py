import io
import json
from types import SimpleNamespace
from urllib.error import HTTPError
import pytest
from escape_room import interactions, llm


def test_structured_request_and_response(monkeypatch):
    def fake_open(request, timeout):
        body = json.loads(request.data)
        assert body['store'] is False
        assert body['response_format']['schema'] == {'type': 'object'}
        assert timeout == 60
        return io.BytesIO(json.dumps({'status': 'completed', 'steps': [
            {'type': 'thought', 'content': [{'type': 'text', 'text': 'hidden'}]},
            {'type': 'model_output', 'content': [{'type': 'text', 'text': '{}'}]}
        ]}).encode())
    monkeypatch.setattr(interactions, 'urlopen', fake_open)
    assert interactions.generate_interaction('fake', 'model', 'rules', 'look',
                                             {'type': 'object'}) == '{}'


def test_history_conversion(monkeypatch):
    def fake_open(request, timeout):
        turns = json.loads(request.data)['input']
        assert [t['type'] for t in turns] == ['user_input', 'model_output']
        return io.BytesIO(b'{"status":"completed","steps":[{"type":"model_output","content":[{"type":"text","text":"hello"}]}]}')
    monkeypatch.setattr(interactions, 'urlopen', fake_open)
    turns = [SimpleNamespace(role=r, parts=[SimpleNamespace(text='hi')])
             for r in ['user', 'model']]
    assert interactions.generate_interaction('fake', 'model', 'rules', turns) == 'hello'


@pytest.mark.parametrize('payload', [{'status': 'failed'}, {'status': 'completed', 'steps': []}])
def test_no_empty_success(monkeypatch, payload):
    monkeypatch.setattr(interactions, 'urlopen', lambda *a, **kw: io.BytesIO(json.dumps(payload).encode()))
    with pytest.raises(ValueError):
        interactions.generate_interaction('fake', 'model', 'rules', 'look')


def test_safe_service_error(monkeypatch):
    monkeypatch.setenv('GEMINI_API_KEY', 'secret-test-value')
    monkeypatch.setenv('GEMINI_MODEL', 'model')
    monkeypatch.setenv('GEMINI_TRANSPORT', 'interactions')
    def fail(*a, **kw):
        raise HTTPError('url', 503, 'secret-test-value', {}, None)
    monkeypatch.setattr(interactions, 'urlopen', fail)
    with pytest.raises(llm.ModelUnavailable) as result:
        llm.generate('rules', 'look')
    assert '503' in str(result.value)
    assert 'secret-test-value' not in str(result.value)
