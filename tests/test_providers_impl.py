import os
import types
import pytest
from unittest.mock import patch


@pytest.mark.asyncio
async def test_openai_response_success(monkeypatch):
    from src.providers import ProviderManager

    # Fake openai module
    mod = types.SimpleNamespace()
    async def create(**kwargs):
        return types.SimpleNamespace(choices=[types.SimpleNamespace(message=types.SimpleNamespace(content='OK'))])
    mod.AsyncClient = lambda api_key=None: types.SimpleNamespace(
        chat=types.SimpleNamespace(completions=types.SimpleNamespace(create=create))
    )

    with patch.dict(os.environ, {"OPENAI_KEY": "k"}, clear=False), \
         patch.dict('sys.modules', {'openai': mod}):
        pm = ProviderManager()
        out = await pm._get_openai_response([
            {"role":"user","content":"hi"}
        ])
        assert out == 'OK'


@pytest.mark.asyncio
async def test_openai_missing_key():
    from src.providers import ProviderManager
    with patch.dict(os.environ, {}, clear=True):
        pm = ProviderManager()
        out = await pm._get_openai_response([])
    assert 'OpenAI' in out or 'Openai' in out


@pytest.mark.asyncio
async def test_claude_response_success(monkeypatch):
    from src.providers import ProviderManager
    mod = types.SimpleNamespace()
    async def create(**kwargs):
        return types.SimpleNamespace(content=[types.SimpleNamespace(text='CLAUDE')])
    mod.AsyncClient = lambda api_key=None: types.SimpleNamespace(messages=types.SimpleNamespace(create=create))

    with patch.dict(os.environ, {"CLAUDE_KEY": "k"}, clear=False), \
         patch.dict('sys.modules', {'anthropic': mod}):
        pm = ProviderManager()
        out = await pm._get_claude_response([
            {"role":"system","content":"s"}, {"role":"user","content":"u"}
        ])
        assert out == 'CLAUDE'


@pytest.mark.asyncio
async def test_gemini_response_success(monkeypatch):
    from src.providers import ProviderManager

    # Fake google.generativeai
    class FakeModel:
        def __init__(self, name):
            self.name = name
        async def generate_content_async(self, prompt):
            return types.SimpleNamespace(text='GEMINI')
    fake_genai = types.SimpleNamespace(
        configure=lambda api_key=None: None,
        GenerativeModel=FakeModel
    )

    with patch.dict(os.environ, {"GEMINI_KEY": "k"}, clear=False), \
         patch.dict('sys.modules', {'google.generativeai': fake_genai}):
        pm = ProviderManager()
        out = await pm._get_gemini_response([
            {"role":"user","content":"u"}
        ])
        assert out == 'GEMINI'


@pytest.mark.asyncio
async def test_grok_fallback(monkeypatch):
    from src.providers import ProviderManager
    pm = ProviderManager()
    # ensure fallback path returns string
    out = await pm._get_grok_response([
        {"role":"user","content":"u"}
    ])
    assert isinstance(out, str)


@pytest.mark.asyncio
async def test_openai_response_exception(monkeypatch):
    from src.providers import ProviderManager
    # Fake openai raising exception
    class BadClient:
        class chat:
            class completions:
                @staticmethod
                async def create(**kwargs):
                    raise RuntimeError('boom')
    mod = types.SimpleNamespace(AsyncClient=lambda api_key=None: BadClient)
    with patch.dict(os.environ, {"OPENAI_KEY": "k"}, clear=True), \
         patch.dict('sys.modules', {'openai': mod}):
        pm = ProviderManager()
        out = await pm._get_openai_response([{"role":"user","content":"hi"}])
        assert 'Erro' in out or 'erro' in out
