
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
import time

from src.aclient import DiscordClient
from src.providers import ProviderManager, ProviderType


class TestPerformance:
    @pytest.mark.asyncio
    async def test_conversation_memory_management(self):
        """Test memory usage with large conversation histories"""
        client = DiscordClient()
        user_id = 12345
        
        # Mock provider to return quickly
        with patch.object(client.provider_manager, 'get_response', 
                         new=AsyncMock(return_value="Quick response")):
            
            # Add many messages to test trimming
            for i in range(50):
                await client.handle_message(f"Message {i}", user_id)
            
            # Should be trimmed to trim_size (8)
            assert len(client.conversation_histories[user_id]) <= client.trim_size * 2
    
    @pytest.mark.asyncio
    async def test_concurrent_message_handling(self):
        """Test handling multiple concurrent messages"""
        client = DiscordClient()
        
        with patch.object(client.provider_manager, 'get_response', 
                         new=AsyncMock(return_value="Concurrent response")):
            
            # Create multiple concurrent tasks
            tasks = []
            for i in range(10):
                task = client.handle_message(f"Message {i}", i)
                tasks.append(task)
            
            # All should complete successfully
            responses = await asyncio.gather(*tasks)
            assert len(responses) == 10
            assert all(r == "Concurrent response" for r in responses)
    
    def test_provider_switching_performance(self):
        """Test performance of provider switching"""
        manager = ProviderManager()
        
        start_time = time.time()
        
        # Switch providers multiple times
        for _ in range(100):
            manager.set_current_provider(ProviderType.FREE)
        
        end_time = time.time()
        
        # Should be very fast (under 0.1 seconds)
        assert end_time - start_time < 0.1
