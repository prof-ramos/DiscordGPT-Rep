import pytest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_on_ready_sets_presence(monkeypatch):
    from src.aclient import DiscordClient
    c = DiscordClient()
    # Fake user and methods (override internal connection user)
    c._connection = SimpleNamespace(user=SimpleNamespace(id=1, __str__=lambda self='': 'bot'))
    c.tree.sync = AsyncMock(return_value=[1,2,3,4])
    c.change_presence = AsyncMock()
    await c.on_ready()
    c.tree.sync.assert_awaited()
    c.change_presence.assert_awaited()
