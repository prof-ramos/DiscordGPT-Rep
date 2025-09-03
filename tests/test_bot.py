import pytest
from unittest.mock import Mock, patch

from src.bot import run_discord_bot


class TestBotModule:
    @patch('src.bot.DiscordClient')
    def test_run_discord_bot_with_token(self, mock_client):
        """Bot runs when client.run_bot executes without error"""
        mock_instance = Mock()
        mock_client.return_value = mock_instance

        run_discord_bot()

        mock_client.assert_called_once()
        mock_instance.run_bot.assert_called_once()

    @patch('src.bot.DiscordClient')
    def test_run_discord_bot_no_token(self, mock_client):
        """Propagates ValueError from client.run_bot when token missing"""
        mock_instance = Mock()
        mock_instance.run_bot.side_effect = ValueError("Token Discord é obrigatório")
        mock_client.return_value = mock_instance

        with pytest.raises(ValueError, match="Token Discord é obrigatório"):
            run_discord_bot()

    @patch('src.bot.DiscordClient')
    def test_run_discord_bot_handles_exceptions(self, mock_client):
        """Propagates unexpected exceptions from client.run_bot"""
        mock_instance = Mock()
        mock_instance.run_bot.side_effect = Exception("Connection failed")
        mock_client.return_value = mock_instance

        with pytest.raises(Exception, match="Connection failed"):
            run_discord_bot()
