import pytest


def test_convert_messages_to_prompt():
    from src.providers import ProviderManager
    pm = ProviderManager()
    messages = [
        {"role": "system", "content": "S"},
        {"role": "user", "content": "U"},
        {"role": "assistant", "content": "A"},
    ]
    out = pm._convert_messages_to_prompt(messages)
    assert 'System: S' in out and 'User: U' in out and 'Assistant: A' in out


def test_get_provider_status_and_model_setter():
    from src.providers import ProviderManager
    pm = ProviderManager()
    status = pm.get_provider_status()
    assert set(['current_provider','current_model','available_providers','models_count']).issubset(status.keys())
    assert pm.set_current_model('non-existent') is False
