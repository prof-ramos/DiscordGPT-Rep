
import pytest
from unittest.mock import Mock, patch, AsyncMock
import os

from src.bot import run_discord_bot


class TestBotModule:
    @patch('src.bot.DiscordClient')
    @patch('src.bot.os.getenv')
    def test_run_discord_bot_with_token(self, mock_getenv, mock_client):
        """Test bot runs when token is available"""
        mock_getenv.return_value = "test_token"
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        
        run_discord_bot()
        
        mock_client.assert_called_once()
        mock_instance.run_bot.assert_called_once()
    
    @patch('src.bot.os.getenv')
    def test_run_discord_bot_no_token(self, mock_getenv):
        """Test bot fails gracefully without token"""
        mock_getenv.return_value = None
        
        with pytest.raises(ValueError, match="Token Discord é obrigatório"):
            run_discord_bot()
    
    @patch('src.bot.DiscordClient')
    @patch('src.bot.os.getenv')
    def test_run_discord_bot_handles_exceptions(self, mock_getenv, mock_client):
        """Test bot handles runtime exceptions"""
        mock_getenv.return_value = "test_token"
        mock_instance = Mock()
        mock_instance.run_bot.side_effect = Exception("Connection failed")
        mock_client.return_value = mock_instance
        
        with pytest.raises(Exception, match="Connection failed"):
            run_discord_bot()
