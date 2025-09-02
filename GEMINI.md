# GEMINI.md

## Project Overview

This project is a Discord bot that integrates with multiple AI providers to offer chat and image generation functionalities. The bot is built with Python and the `discord.py` library. It supports various AI backends, including OpenAI, Claude, Gemini, and Grok, as well as a free provider.

The project is structured with a `src` directory containing the main application logic, a `tests` directory for unit tests, and configuration files for Docker and other tools. The bot's entry point is `main.py`, which validates the environment variables and starts the bot. The core bot logic, including command handling, is located in `src/bot.py`.

## Building and Running

### Prerequisites

*   Python 3.9+
*   Docker (optional)

### With Python

1.  **Install dependencies:**
    ```bash
    pip3 install -r requirements.txt
    ```
2.  **Configure environment:**
    *   Rename `.env.example` to `.env`.
    *   Add your Discord bot token and any premium AI provider API keys to the `.env` file.
3.  **Run the bot:**
    ```bash
    python3 main.py
    ```

### With Docker

1.  **Build and run the container:**
    ```bash
    docker compose up -d
    ```
2.  **Check the logs:**
    ```bash
    docker logs -t chatgpt-discord-bot
    ```
3.  **Stop the bot:**
    ```bash
    docker stop <BOT CONTAINER ID>
    ```

### Testing

The project uses `pytest` for testing. The tests are located in the `tests` directory.

*   **Run all tests:**
    ```bash
    pytest
    ```

## Development Conventions

*   **Code Style:** The code follows standard Python conventions (PEP 8).
*   **Dependencies:** Project dependencies are managed in the `requirements.txt` file.
*   **Configuration:** The bot is configured through environment variables, which are documented in `.env.example`.
*   **Logging:** The project uses a custom logger configured in `src/log.py`.
*   **Testing:** Tests are written using `pytest` and `pytest-asyncio`. Test files are located in the `tests` directory and follow the `test_*.py` naming convention.
*   **Modularity:** The code is organized into modules within the `src` directory, promoting separation of concerns.
