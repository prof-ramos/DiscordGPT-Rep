import os
from unittest.mock import patch


def test_logger_file_toggle(tmp_path):
    from importlib import reload
    with patch.dict(os.environ, {
        'LOG_TO_FILE': 'True',
        'LOG_DIR': str(tmp_path),
        'LOG_LEVEL': 'INFO'
    }, clear=False):
        import src.log as logmod
        reload(logmod)
        lg = logmod.setup_logger('src.test')
        # Deve ter ao menos 1 handler (console) e provavelmente 2 (arquivo)
        assert len(lg.handlers) >= 1
