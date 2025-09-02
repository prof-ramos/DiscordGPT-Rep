
import pytest
from unittest.mock import Mock, patch, AsyncMock
import os

from src.aclient import DiscordClient
from src.providers import ProviderManager, ProviderType


class TestIntegration:
    def test_client_initialization(self):
        """Test Discord client initializes properly"""
        with patch.dict(os.environ, {
            "MAX_MESSAGE_LENGTH": "2000",
            "CONVERSATION_HISTORY_LIMIT": "20",
            "TRIM_CONVERSATION_SIZE": "8",
            "ADMIN_USER_IDS": "123456789"
        }):
            client = DiscordClient()
            
            assert client.provider_manager is not None
            assert isinstance(client.conversation_histories, dict)
            assert client.max_message_length == 2000
            assert client.conversation_limit == 20
            assert client.trim_size == 8
            assert 123456789 in client.admin_users
    
    @pytest.mark.asyncio
    async def test_message_handling_flow(self):
        """Test complete message handling flow"""
        client = DiscordClient()
        
        # Mock provider response
        with patch.object(client.provider_manager, 'get_response', 
                         new=AsyncMock(return_value="Test AI response")):
            
            response = await client.handle_message("Hello", 12345)
            
            assert response == "Test AI response"
            assert 12345 in client.conversation_histories
            assert len(client.conversation_histories[12345]) == 2  # user + assistant
    
    def test_persona_provider_integration(self):
        """Test persona and provider work together"""
        client = DiscordClient()
        
        # Test persona change
        success = client.set_persona("creative")
        assert success is True
        assert client.current_persona == "creative"
        
        # Test invalid persona
        success = client.set_persona("invalid_persona")
        assert success is False
    
    def test_admin_permissions(self):
        """Test admin permission system"""
        with patch.dict(os.environ, {"ADMIN_USER_IDS": "123,456"}):
            client = DiscordClient()
            
            assert client.is_admin(123) is True
            assert client.is_admin(456) is True
            assert client.is_admin(789) is False
