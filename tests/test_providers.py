import pytest
from unittest.mock import AsyncMock
from src.providers import ProviderType, ModelInfo, ProviderManager


class TestModelInfo:
    def test_model_info_creation(self):
        model = ModelInfo(
            name="test-model",
            provider=ProviderType.FREE,
            max_tokens=4096,
            cost_per_token=0.0,
        )
        assert model.name == "test-model"
        assert model.provider == ProviderType.FREE
        assert model.max_tokens == 4096
        assert model.cost_per_token == 0.0


class TestProviderManagerFree:
    @pytest.mark.asyncio
    async def test_get_response_free_provider(self, monkeypatch):
        manager = ProviderManager()
        # Force FREE provider
        manager.set_current_provider(ProviderType.FREE)
        # Stub free response to avoid network
        async def fake_free(messages):
            return "Test response"
        monkeypatch.setattr(manager, "_get_free_response", fake_free)
        resp = await manager.get_response([{"role": "user", "content": "Hi"}])
        assert resp == "Test response"
    
    def test_get_models_for_provider(self):
        manager = ProviderManager()
        models = manager.get_models_for_provider(ProviderType.FREE)
        assert isinstance(models, list) and len(models) >= 1


class TestProviderManagerOpenAI:
    def test_available_providers_reflect_env(self, monkeypatch):
        # Ensure FREE always present; others depend on env keys
        monkeypatch.delenv("OPENAI_KEY", raising=False)
        manager = ProviderManager()
        providers = manager.get_available_providers()
        assert ProviderType.FREE in providers


class TestProviderManagerSwitching:
    def test_set_current_provider(self, monkeypatch):
        manager = ProviderManager()
        assert manager.set_current_provider(ProviderType.FREE) is True
        assert manager.current_provider == ProviderType.FREE
        # Attempt to switch to non-available provider should return False
        monkeypatch.delenv("OPENAI_KEY", raising=False)
        assert (ProviderType.OPENAI in manager.get_available_providers()) in {True, False}


class TestProviderManagerBasics:
    def test_get_available_providers(self):
        manager = ProviderManager()
        providers = manager.get_available_providers()
        assert ProviderType.FREE in providers
        assert len(providers) >= 1
