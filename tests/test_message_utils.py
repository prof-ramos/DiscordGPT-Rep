
import pytest
from unittest.mock import Mock, AsyncMock

from utils.message_utils import send_split_message


class TestMessageUtils:
    @pytest.mark.asyncio
    async def test_send_split_message_short(self):
        """Test sending message within limit"""
        mock_channel = Mock()
        mock_channel.send = AsyncMock()
        
        message = "Short message"
        await send_split_message(mock_channel, message, 2000)
        
        mock_channel.send.assert_called_once_with("Short message")
    
    @pytest.mark.asyncio
    async def test_send_split_message_long(self):
        """Test splitting long messages"""
        mock_channel = Mock()
        mock_channel.send = AsyncMock()
        
        # Create a message longer than the limit
        message = "A" * 2100
        await send_split_message(mock_channel, message, 2000)
        
        # Should be called twice (split message)
        assert mock_channel.send.call_count == 2
    
    @pytest.mark.asyncio
    async def test_send_split_message_empty(self):
        """Test handling empty message"""
        mock_channel = Mock()
        mock_channel.send = AsyncMock()
        
        await send_split_message(mock_channel, "", 2000)
        
        mock_channel.send.assert_called_once_with("")
    
    @pytest.mark.asyncio
    async def test_send_split_message_exception(self):
        """Test handling send failures"""
        mock_channel = Mock()
        mock_channel.send = AsyncMock(side_effect=Exception("Send failed"))
        
        with pytest.raises(Exception, match="Send failed"):
            await send_split_message(mock_channel, "test", 2000)
