import os
import logging
import logging.handlers
from pathlib import Path


class CustomFormatter(logging.Formatter):
    LEVEL_COLORS = [
        (logging.DEBUG, '\x1b[40;1m'),
        (logging.INFO, '\x1b[34;1m'),
        (logging.WARNING, '\x1b[33;1m'),
        (logging.ERROR, '\x1b[31m'),
        (logging.CRITICAL, '\x1b[41m'),
    ]
    FORMATS = {
        level: logging.Formatter(
            f'\x1b[30;1m%(asctime)s\x1b[0m {color}%(levelname)-8s\x1b[0m \x1b[35m%(name)s\x1b[0m -> %(message)s',
            '%Y-%m-%d %H:%M:%S'
        )
        for level, color in LEVEL_COLORS
    }


    def format(self, record):
        formatter = self.FORMATS.get(record.levelno)
        if formatter is None:
            formatter = self.FORMATS[logging.DEBUG]

        # Override the traceback to always print in red
        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f'\x1b[31m{text}\x1b[0m'

        output = formatter.format(record)
        # Remove the cache layer
        record.exc_text = None
        return output


def setup_logger(module_name: str) -> logging.Logger:
    """Configure and return a module-specific logger.

    Behavior:
    - Always logs to console with colors.
    - Logs to a rotating file by default (can be disabled with LOG_TO_FILE=False).
    - Respects LOG_LEVEL, LOG_DIR, LOG_FILE env vars.
    - Falls back to /tmp when LOG_DIR is not writable.
    """
    # Create/reuse a named logger per top-level library
    library, _, _ = module_name.partition('.py')
    logger = logging.getLogger(library)

    # Avoid duplicate handlers if called multiple times
    if getattr(logger, "_configured", False):
        return logger

    # Levels and flags
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    level = logging.getLevelName(log_level)
    logger.setLevel(level if isinstance(level, int) else logging.INFO)

    # Console handler (always on)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logger.level)
    console_handler.setFormatter(CustomFormatter())
    logger.addHandler(console_handler)

    # File handler (default on, can be disabled)
    to_file = os.getenv("LOG_TO_FILE", os.getenv("LOGGING", "True")).lower() in {"1", "true", "yes", "y"}

    if to_file:
        # Determine directory and ensure it exists
        desired_dir = os.getenv("LOG_DIR")
        if desired_dir:
            log_dir = Path(desired_dir)
        else:
            # Prefer project ./logs if writable, else /tmp
            project_logs = Path.cwd() / "logs"
            tmp_dir = Path("/tmp") if Path("/tmp").exists() else Path.cwd()
            log_dir = project_logs if (project_logs.exists() or project_logs.parent.exists()) else tmp_dir

        try:
            log_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            # Fallback to /tmp or CWD if mkdir fails
            fallback = Path("/tmp") if Path("/tmp").exists() else Path.cwd()
            log_dir = fallback

        log_name = os.getenv("LOG_FILE", "chatgpt_discord_bot.log")
        log_path = log_dir / log_name

        try:
            file_handler = logging.handlers.RotatingFileHandler(
                filename=str(log_path),
                encoding='utf-8',
                maxBytes=32 * 1024 * 1024,
                backupCount=2,
            )
            file_handler.setFormatter(CustomFormatter())
            file_handler.setLevel(logger.level)
            logger.addHandler(file_handler)
        except (OSError, IOError) as e:
            logger.warning(f"Could not create log file at {log_path}: {e}. Using console logging only.")

    # Mark configured to prevent duplicate handlers
    logger._configured = True  # type: ignore[attr-defined]
    return logger

logger = setup_logger(__name__)
