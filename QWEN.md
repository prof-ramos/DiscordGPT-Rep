# ChatGPT Discord Bot - Project Context

## Project Overview

This is a Discord bot that integrates with multiple AI providers, allowing users to chat with AI models and generate images directly within Discord. The bot is built with Python and supports both free and premium AI providers.

### Key Features

- **Multi-Provider Support**: Integrates with 5 AI providers:
  - **Free Provider**: Uses g4f (no API keys required)
  - **OpenAI**: GPT models and DALL-E image generation
  - **Claude**: Anthropic's Claude models
  - **Gemini**: Google's Gemini models and Imagen
  - **Grok**: xAI's Grok models
- **Discord Integration**: Full command support via slash commands and message handling
- **Persona System**: Switch between different AI personalities (including admin-only jailbreak personas)
- **Image Generation**: Create images using various providers
- **Conversation Management**: Maintains conversation history with trimming for context
- **Security Features**: Admin-only access for jailbreak personas and secure API key handling

## Setup and Configuration

### Prerequisites

- Python 3.9 or later
- Discord bot token
- Optional: API keys for premium providers (OpenAI, Claude, Gemini, Grok)

### Environment Configuration

1. Rename `.env.example` to `.env`
2. Configure your Discord bot token in `DISCORD_BOT_TOKEN`
3. Optionally add API keys for premium providers:
   - `OPENAI_KEY`
   - `CLAUDE_KEY`
   - `GEMINI_KEY`
   - `GROK_KEY`
4. Configure admin users with `ADMIN_USER_IDS` (comma-separated Discord user IDs)
5. Set default provider and model with `DEFAULT_PROVIDER` and `DEFAULT_MODEL`

### Running the Bot

Desktop:
```bash
python3 main.py
```

Docker:
```bash
docker compose up -d
```

## Development Information

### Project Structure

- `main.py`: Entry point with environment validation
- `src/bot.py`: Discord bot implementation with command handlers
- `src/aclient.py`: Discord client with AI provider integration
- `src/providers.py`: AI provider implementations and management
- `src/personas.py`: Personality system for different AI behaviors
- `system_prompt.txt`: Initial system prompt for the bot
- `requirements.txt`: Python dependencies

### Key Dependencies

- `discord.py`: Discord API integration
- `openai`: OpenAI API client
- `g4f`: Free AI provider integration
- `google-generativeai`: Google Gemini API client
- `anthropic`: Anthropic Claude API client
- `aiohttp`: HTTP client for API requests

### Provider Implementation

The bot uses a provider system that allows switching between different AI services:

1. **FreeProvider**: Uses g4f with verified working free models (Blackbox, Airforce, AIChatFree)
2. **OpenAIProvider**: Official OpenAI API with GPT models and DALL-E
3. **ClaudeProvider**: Anthropic Claude API
4. **GeminiProvider**: Google Gemini API with Imagen support
5. **GrokProvider**: xAI Grok API

Providers are managed by a `ProviderManager` that handles initialization and switching.

### Persona System

The bot supports different AI personalities:
- **Standard**: Default helpful assistant
- **Creative**: More imaginative responses
- **Technical**: Technical and precise responses
- **Casual**: Friendly and conversational tone
- **Jailbreak Personas** (admin-only):
  - jailbreak-v1 (BYPASS mode)
  - jailbreak-v2 (SAM mode)
  - jailbreak-v3 (Developer Mode Plus)

### Conversation Management

- Maintains conversation history in `conversation_history`
- Trims history when it exceeds `MAX_CONVERSATION_LENGTH` (default 20)
- Keeps recent context and system messages when trimming
- Resets history on persona switch or `/reset` command

### Security Features

- Admin-only access for jailbreak personas
- API keys stored in environment variables
- Input validation and sanitization
- Docker security with non-root user and read-only filesystem