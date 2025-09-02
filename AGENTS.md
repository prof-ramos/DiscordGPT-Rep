# Repository Guidelines

## Project Structure & Module Organization
- `src/`: Core bot modules — `bot.py` (Discord logic), `providers.py` (LLM adapters), `aclient.py` (async HTTP/LLM client), `personas.py` (prompt/persona registry), `log.py` (logging).
- `main.py`: CLI entry to run the Discord bot.
- `start_admin.py`: Streamlit admin panel (local dashboard).
- `tests/`: Pytest unit/integration tests (`test_*.py`).
- `docs/`: User/developer documentation.
- `utils/`, `auto_login/`: Optional helpers (local use only).
- Assets & prompts: `.env` (from `.env.example`), `system_prompt.txt`.

## Build, Test, and Development Commands
- Install deps: `pip install -r requirements.txt`.
- Run bot: `python main.py`.
- Run admin (opens http://localhost:8501): `python start_admin.py`.
- Docker dev: `docker compose up -d`; logs: `docker logs -t chatgpt-discord-bot`.
- Tests (all): `pytest -v`.
- Tests (fast filter): `pytest -m "unit and not slow"`.

## Coding Style & Naming Conventions
- Python, PEP 8, 4-space indents; prefer type hints where practical.
- Names: modules/functions `snake_case`; classes `PascalCase`; constants `UPPER_SNAKE_CASE`.
- Logging: use `from src.log import logger`; avoid `print` in runtime code.
- Provider integrations must stay small and isolated in `src/providers.py`; do not leak provider-specific details across modules.

## Testing Guidelines
- Frameworks: `pytest`, `pytest-asyncio` (asyncio_mode=auto).
- Marks available: `unit`, `integration`, `slow` (see `pytest.ini`).
- Naming: files `tests/test_*.py`, classes `Test*`, functions `test_*`.
- Write fast, deterministic unit tests; mark external/variable behavior as `integration` or `slow`.

## Commit & Pull Request Guidelines
- Commits: concise, present tense; include scope when helpful (e.g., "providers: add Grok model list").
- PRs must include: purpose/summary, linked issues (e.g., `Closes #123`), screenshots/logs for UX-facing changes (bot replies/admin panel), tests for new logic (note any skipped/marked), and docs updates when flags/commands/behavior change.

## Security & Configuration
- Never commit secrets. Copy `.env.example` to `.env`; set `DISCORD_BOT_TOKEN`, optional `OPENAI_KEY`, `CLAUDE_KEY`, `GEMINI_KEY`, `GROK_KEY`, `ADMIN_USER_IDS`.
- Jailbreak personas are admin-only; validate `ADMIN_USER_IDS` before enabling.
- Prefer Docker for isolation; review `Dockerfile` and `docker-compose.yml` before deploy.
