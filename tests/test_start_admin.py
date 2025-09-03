import os
import pytest
from unittest.mock import patch, Mock


class TestStartAdmin:
    def test_check_requirements_ok(self, monkeypatch):
        import importlib
        monkeypatch.setitem(os.sys.modules, 'streamlit', Mock())
        monkeypatch.setitem(os.sys.modules, 'psutil', Mock())
        monkeypatch.setitem(os.sys.modules, 'pandas', Mock())
        sa = importlib.import_module('start_admin')
        assert sa.check_requirements() is True

    def test_check_requirements_missing(self, monkeypatch):
        import importlib
        import builtins
        sa = importlib.import_module('start_admin')
        real_import = builtins.__import__
        def fake_import(name, *a, **k):
            if name in ('streamlit', 'psutil', 'pandas'):
                raise ImportError('missing')
            return real_import(name, *a, **k)
        with patch('builtins.__import__', side_effect=fake_import):
            assert sa.check_requirements() is False

    def test_check_bot_config(self, tmp_path, monkeypatch):
        import importlib
        sa = importlib.import_module('start_admin')
        monkeypatch.chdir(tmp_path)
        # No .env
        assert sa.check_bot_config() is False
        # With .env and token
        (tmp_path / '.env').write_text('DISCORD_BOT_TOKEN=abc12345678901234567890')
        assert sa.check_bot_config() is True

    def test_start_admin_panel_spawns(self, tmp_path, monkeypatch):
        import importlib
        sa = importlib.import_module('start_admin')
        monkeypatch.chdir(tmp_path)
        (tmp_path / 'admin_panel.py').write_text('print("ok")')
        with patch('start_admin.subprocess.Popen') as mock_popen, \
             patch('start_admin.webbrowser.open') as mock_open, \
             patch('start_admin.time.sleep') as mock_sleep:
            proc = Mock()
            proc.wait = Mock(side_effect=KeyboardInterrupt)
            mock_popen.return_value = proc
            assert sa.start_admin_panel() is True
