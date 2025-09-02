
import pytest
import asyncio
from unittest.mock import Mock
import os

# Test configuration
pytest_plugins = ['pytest_asyncio']

@pytest.fixture
def mock_discord_message():
    """Create a mock Discord message"""
    message = Mock()
    message.content = "Test message"
    message.author = Mock()
    message.author.id = 12345
    message.channel = Mock()
    return message

@pytest.fixture
def mock_discord_interaction():
    """Create a mock Discord interaction"""
    interaction = Mock()
    interaction.user = Mock()
    interaction.user.id = 12345
    interaction.response = Mock()
    interaction.followup = Mock()
    return interaction

@pytest.fixture
def clean_env():
    """Provide clean environment for tests"""
    original_env = dict(os.environ)
    
    # Set test environment
    test_env = {
        "MAX_MESSAGE_LENGTH": "2000",
        "CONVERSATION_HISTORY_LIMIT": "20", 
        "TRIM_CONVERSATION_SIZE": "8",
        "ADMIN_USER_IDS": "123456789"
    }
    
    for key, value in test_env.items():
        os.environ[key] = value
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)

@pytest.fixture
def mock_provider_manager():
    """Create a mock provider manager"""
    manager = Mock()
    manager.get_response = AsyncMock(return_value="Mock AI response")
    manager.current_provider = Mock()
    manager.current_provider.value = "FREE"
    manager.get_available_providers.return_value = [Mock()]
    return manager
