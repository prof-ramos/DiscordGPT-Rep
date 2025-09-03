import os
import pytest
from unittest.mock import patch


class TestAdminPanel:
    def test_env_load_and_save(self, tmp_path, monkeypatch):
        # Stub streamlit before import
        import importlib
        monkeypatch.setitem(os.sys.modules, 'streamlit', __import__('types').SimpleNamespace(**{
            'set_page_config': lambda **kwargs: None,
            'markdown': lambda *a, **k: None,
            'sidebar': __import__('types').SimpleNamespace(__enter__=lambda s: s, __exit__=lambda *a: False),
            'selectbox': lambda *a, **k: '📊 Dashboard',
            'image': lambda *a, **k: None,
        }))
        ap = importlib.import_module('admin_panel')
        panel = ap.AdminPanel()
        # Redirect config file
        panel.config_file = tmp_path / '.env'
        panel.config = {'A': '1', 'B': '2'}
        panel._save_config()
        # New instance loads same file
        panel2 = ap.AdminPanel()
        panel2.config_file = tmp_path / '.env'
        panel2._load_config()
        assert panel2.config['A'] == '1'
        assert panel2.config['B'] == '2'

    def test_get_system_stats(self, monkeypatch):
        import importlib
        monkeypatch.setitem(os.sys.modules, 'streamlit', __import__('types').SimpleNamespace(
            set_page_config=lambda **k: None,
            markdown=lambda *a, **k: None,
        ))
        ap = importlib.import_module('admin_panel')
        panel = ap.AdminPanel()
        stats = panel._get_system_stats()
        assert set(['cpu_percent', 'memory_percent', 'disk_percent', 'uptime']).issubset(stats.keys())
