import os
import pytest
from unittest.mock import patch


class TestMainValidation:
    @patch('src.log.logger')
    def test_missing_token(self, mock_logger):
        from importlib import reload
        import main as main_mod
        with patch('dotenv.load_dotenv', lambda *a, **k: None), \
             patch.dict(os.environ, {}, clear=True):
            reload(main_mod)
            ok = main_mod.validate_environment()
            assert ok is False
            assert any('Missing required environment variables' in c[0][0] for c in mock_logger.error.call_args_list)

    @patch('src.log.logger')
    def test_invalid_token_format(self, mock_logger):
        from importlib import reload
        import main as main_mod
        with patch.dict(os.environ, {"DISCORD_BOT_TOKEN": "abc123"}, clear=True):
            reload(main_mod)
            ok = main_mod.validate_environment()
            assert ok is False
            assert any('Invalid Discord token format' in c[0][0] for c in mock_logger.error.call_args_list)

    @patch('src.log.logger')
    def test_valid_env_and_providers(self, mock_logger):
        from importlib import reload
        import main as main_mod
        token = 'MTM' + 'x'*60
        env = {
            'DISCORD_BOT_TOKEN': token,
            'OPENAI_KEY': 'k1',
            'CLAUDE_KEY': 'k2',
            'GEMINI_KEY': 'k3',
        }
        with patch.dict(os.environ, env, clear=True):
            reload(main_mod)
            ok = main_mod.validate_environment()
            assert ok is True
