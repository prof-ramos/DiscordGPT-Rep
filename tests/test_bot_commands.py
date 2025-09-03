import pytest
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_setup_adds_cog():
    from src.bot import setup, BotCommands
    add_cog = AsyncMock()
    class FakeBot:
        async def add_cog(self, cog):
            await add_cog(cog)

    bot = FakeBot()
    await setup(bot)
    # Verifica que um Cog foi adicionado
    assert add_cog.await_count == 1
    assert isinstance(add_cog.await_args.args[0], BotCommands)
