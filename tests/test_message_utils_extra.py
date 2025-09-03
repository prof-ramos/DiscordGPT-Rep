import pytest
from unittest.mock import AsyncMock, Mock


@pytest.mark.asyncio
async def test_split_exact_boundary():
    from utils.message_utils import send_split_message
    channel = Mock()
    channel.send = AsyncMock()
    text = 'A' * 2000
    await send_split_message(channel, text, 2000)
    channel.send.assert_awaited_once_with(text)


@pytest.mark.asyncio
async def test_split_code_blocks_uneven():
    from utils.message_utils import send_split_message
    channel = Mock()
    channel.send = AsyncMock()
    text = "Here```CODE_START" + ("X" * 2100)
    await send_split_message(channel, text, 1000)
    # Should have sent multiple chunks
    assert channel.send.await_count >= 3


@pytest.mark.asyncio
async def test_split_multiple_blocks():
    from utils.message_utils import send_split_message
    channel = Mock()
    channel.send = AsyncMock()
    text = "pre```code1```mid```code2```post"
    await send_split_message(channel, text, 10)
    # Several chunks expected
    assert channel.send.await_count >= 3
