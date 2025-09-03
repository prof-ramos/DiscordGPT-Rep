
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
import discord

from src.aclient import DiscordClient


class TestErrorHandling:
    @pytest.mark.asyncio
    async def test_handle_message_provider_error(self):
        """Test handling provider API errors"""
        client = DiscordClient()
        
        with patch.object(client.provider_manager, 'get_response', 
                         side_effect=Exception("API Error")):
            
            response = await client.handle_message("Hello", 12345)
            assert "erro" in response.lower()
    
    @pytest.mark.asyncio
    async def test_handle_message_timeout(self):
        """Test handling provider timeouts"""
        client = DiscordClient()
        
        with patch.object(client.provider_manager, 'get_response', 
                         side_effect=asyncio.TimeoutError()):
            
            response = await client.handle_message("Hello", 12345)
            assert "erro" in response.lower()
    
    @pytest.mark.asyncio
    async def test_on_message_dm_error(self):
        """Test DM handling errors"""
        client = DiscordClient()
        
        mock_message = Mock()
        mock_message.author = Mock()
        mock_message.author.id = 12345
        mock_message.content = "Test"
        mock_message.channel = Mock(spec=discord.DMChannel)
        mock_message.channel.send = AsyncMock(side_effect=Exception("Send failed"))
        
        # Should not raise exception
        with patch.object(client, 'handle_message', new=AsyncMock(return_value="Response")):
            await client.on_message(mock_message)
    
    def test_set_persona_invalid(self):
        """Test setting invalid persona"""
        client = DiscordClient()
        
        result = client.set_persona("nonexistent_persona")
        assert result is False
        # Should keep current persona
        assert client.current_persona == "helpful"
    
    def test_clear_conversation_nonexistent_user(self):
        """Test clearing conversation for user without history"""
        client = DiscordClient()
        
        # Should not raise error
        client.clear_conversation(99999)
        assert 99999 not in client.conversation_histories
