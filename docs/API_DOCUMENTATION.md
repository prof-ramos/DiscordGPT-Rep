
# 📚 Discord ChatGPT Bot - API Documentation

## Overview

The Discord ChatGPT Bot provides a comprehensive API for AI-powered conversations, image generation, and bot management through Discord slash commands and direct messages.

## Base Information

- **Bot Type**: Discord Application
- **Authentication**: Discord Bot Token
- **Response Format**: Discord Messages/Embeds
- **Rate Limiting**: Provider-dependent (see limits section)

---

## 🎮 Slash Commands API

### `/chat`

**Description**: Send a message to the AI and receive a response

**Parameters**:
- `mensagem` (string, required): The message to send to the AI

**Request Format**:
```
/chat <message>
```

**Response Format**:
- **Success**: AI-generated text response (max 2000 characters)
- **Error**: Error message with ❌ prefix

**Examples**:
```bash
# Basic conversation
/chat Hello, how are you?
# Returns: AI response based on current persona

# Technical question
/chat Explain machine learning in simple terms
# Returns: Detailed explanation from AI

# Creative request
/chat Write a poem about coding
# Returns: Creative poem (if using creative persona)
```

**Limitations**:
- Maximum message length: 2000 characters
- Response may be split if longer than Discord limit
- Subject to provider rate limits

---

### `/reset`

**Description**: Clear conversation history for the current user

**Parameters**: None

**Request Format**:
```
/reset
```

**Response Format**:
- **Success**: `🔄 Histórico de conversa limpo!`
- **Error**: `❌ Erro ao limpar conversa.`

**Example**:
```bash
/reset
# Returns: 🔄 Histórico de conversa limpo!
```

**Limitations**:
- Only clears history for the requesting user
- Cannot be undone

---

### `/persona`

**Description**: Change the AI's personality/behavior mode

**Parameters**:
- `nome` (string, required): Name of the persona to activate

**Request Format**:
```
/persona <persona_name>
```

**Available Personas**:
- `standard` - Default helpful assistant
- `creative` - Creative and imaginative responses
- `technical` - Technical and precise answers
- `casual` - Casual and friendly tone
- `jailbreak-v1` - BYPASS mode (admin only)
- `jailbreak-v2` - SAM mode (admin only)
- `jailbreak-v3` - Developer Mode (admin only)

**Response Format**:
- **Success**: `🎭 Persona alterada para: {persona_name}`
- **Error**: `❌ Persona inválida. Disponíveis: {available_list}`

**Examples**:
```bash
# Switch to creative mode
/persona creative
# Returns: 🎭 Persona alterada para: creative

# Invalid persona
/persona invalid
# Returns: ❌ Persona inválida. Disponíveis: standard, creative, technical, casual

# Admin-only persona (requires admin privileges)
/persona jailbreak-v1
# Returns: 🎭 Persona alterada para: jailbreak-v1 (if admin)
# Returns: ❌ Persona inválida (if not admin)
```

**Limitations**:
- Jailbreak personas require admin privileges
- Admin users defined in `ADMIN_USER_IDS` environment variable

---

### `/status`

**Description**: Display comprehensive bot status information

**Parameters**: None

**Request Format**:
```
/status
```

**Response Format**: Discord Embed with:
- Bot status (Online/Offline)
- Latency in milliseconds
- Current persona
- Current AI provider
- Available providers list

**Example**:
```bash
/status
```

**Response Structure**:
```json
{
  "embed": {
    "title": "🤖 Status do Bot",
    "color": "green",
    "fields": [
      {"name": "Status", "value": "✅ Online"},
      {"name": "Latency", "value": "45ms"},
      {"name": "Persona Atual", "value": "creative"},
      {"name": "Provedor Atual", "value": "openai"},
      {"name": "Provedores Disponíveis", "value": "free, openai, claude, gemini"}
    ]
  }
}
```

---

## 🔄 Provider Management API

### Provider Types

**Available Providers**:
- `FREE` - Free provider (always available)
- `OPENAI` - OpenAI GPT models
- `CLAUDE` - Anthropic Claude models  
- `GEMINI` - Google Gemini models
- `GROK` - xAI Grok models

### Provider Switching

**Method**: Interactive menu through provider manager
**Access**: Programmatic via `ProviderManager` class

**API Methods**:
```python
# Get current provider
provider = provider_manager.get_provider()

# Set provider
provider_manager.set_current_provider(ProviderType.OPENAI)

# Get available providers
providers = provider_manager.get_available_providers()

# Get all models
models = provider_manager.get_all_models()
```

---

## 💬 Direct Message API

### Message Handling

**Endpoint**: Direct Messages to Bot
**Authentication**: Discord User ID
**Format**: Plain text messages

**Request Format**:
```
Direct message to bot: "Your message here"
```

**Response Format**:
- AI response based on current persona and provider
- Automatic message splitting if response exceeds 2000 characters
- Error messages for failures

**Example**:
```
User DM: "What's the weather like?"
Bot Response: "I don't have access to real-time weather data, but I can help you with other questions!"
```

---

## 🔒 Authentication & Authorization

### Admin Authentication

**Method**: User ID verification
**Configuration**: `ADMIN_USER_IDS` environment variable

**Admin Privileges**:
- Access to jailbreak personas
- Future administrative features

**Verification Method**:
```python
def is_admin(user_id: int) -> bool:
    return user_id in self.admin_users
```

---

## ⚡ Rate Limiting

### Per-Provider Limits

| Provider | Requests/min | Tokens/min | Notes |
|----------|--------------|------------|-------|
| OpenAI   | 3,000        | 150,000    | Tier dependent |
| Claude   | 1,000        | 100,000    | API tier dependent |
| Gemini   | 15*          | 32,000*    | *Free tier limits |
| Grok     | 100          | 10,000     | Beta limits |
| Free     | Variable     | Variable   | Third-party dependent |

### Rate Limit Handling

**Behavior**: Automatic fallback to next available provider
**User Notification**: Transparent switching with status messages
**Retry Logic**: Built-in retry mechanism with exponential backoff

---

## 📊 Response Formats

### Standard Text Response

```json
{
  "type": "text",
  "content": "AI generated response text",
  "length": 1234,
  "provider": "openai",
  "model": "gpt-4o-mini"
}
```

### Error Response

```json
{
  "type": "error",
  "message": "❌ Error description",
  "error_code": "RATE_LIMIT|INVALID_KEY|NETWORK_ERROR",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

### Status Response (Embed)

```json
{
  "type": "embed",
  "title": "🤖 Status do Bot",
  "fields": [
    {"name": "Status", "value": "✅ Online", "inline": true},
    {"name": "Latency", "value": "45ms", "inline": true}
  ],
  "color": 65280
}
```

---

## 🚀 Usage Examples

### Basic Conversation Flow

```bash
# 1. Start conversation
/chat Hello, I'm learning Python

# 2. Continue conversation (maintains context)
/chat Can you show me a simple function example?

# 3. Switch persona for creative help
/persona creative

# 4. Ask for creative coding help
/chat Write a fun comment for a sorting function

# 5. Reset when done
/reset
```

### Error Handling Example

```bash
# If provider is down
/chat Hello
# Bot automatically tries fallback providers
# Response: "⏱️ Limite de requisições atingido. Tentando provedor alternativo..."
# Then provides response from working provider
```

### Admin Features Example

```bash
# Admin user accessing restricted persona
/persona jailbreak-v1
# Response: 🎭 Persona alterada para: jailbreak-v1

# Non-admin user trying same
/persona jailbreak-v1  
# Response: ❌ Persona inválida. Disponíveis: standard, creative, technical, casual
```

---

## 🔧 Configuration API

### Environment Variables

**Required**:
- `DISCORD_BOT_TOKEN` - Discord bot token

**Optional Provider Keys**:
- `OPENAI_KEY` - OpenAI API key
- `CLAUDE_KEY` - Anthropic API key  
- `GEMINI_KEY` - Google AI API key
- `GROK_KEY` - xAI API key

**Bot Configuration**:
- `ADMIN_USER_IDS` - Comma-separated admin user IDs
- `MAX_MESSAGE_LENGTH` - Maximum message length (default: 2000)
- `CONVERSATION_HISTORY_LIMIT` - Max conversation messages (default: 20)
- `TRIM_CONVERSATION_SIZE` - Messages kept after trimming (default: 8)

### Conversation Management

**API Methods**:
```python
# Get conversation history
history = client.conversation_histories.get(user_id, [])

# Add message to history
history.append({"role": "user", "content": message})

# Trim conversation if too long
if len(history) > limit:
    history = history[-trim_size:]
```

---

## 🛡️ Error Codes & Handling

### Error Types

| Code | Description | Action |
|------|-------------|--------|
| `RATE_LIMIT` | Provider rate limit exceeded | Auto-fallback to next provider |
| `INVALID_KEY` | Invalid API key | Skip provider, try next |
| `MODEL_NOT_FOUND` | Requested model unavailable | Use default model |
| `NETWORK_ERROR` | Connection/network issue | Retry with backoff |
| `PERMISSION_DENIED` | Insufficient permissions | Show permission error |

### Error Response Examples

```bash
# Rate limit error
❌ ⏱️ Limite de requisições atingido. Tentando provedor alternativo...

# Authentication error  
❌ 🔑 Erro de autenticação. Verificando configuração...

# Network error
❌ 🌐 Erro de conexão. Tentando novamente...

# Permission error
❌ Persona inválida. Disponíveis: standard, creative, technical, casual
```

---

## 📈 Monitoring & Metrics

### Health Check Endpoint

**Method**: Programmatic health check
**Returns**: Dictionary with system status

```python
async def health_check() -> Dict[str, bool]:
    return {
        "discord_connected": bot.is_ready(),
        "providers_available": len(provider_manager.get_available_providers()) > 0,
        "conversation_active": len(conversation_histories) > 0
    }
```

### Metrics Collected

- Command execution count
- Response time per provider
- Success/failure rates
- User activity patterns
- Provider usage distribution

---

## 🔄 Fallback System

### Provider Fallback Chain

1. **Primary Provider** (configured default)
2. **Secondary Providers** (other configured providers)
3. **Free Provider** (always available as last resort)

### Fallback Triggers

- Rate limit exceeded
- Invalid API key
- Network timeouts
- Model unavailable
- Service outages

### Fallback Behavior

```python
async def get_response_with_fallback(messages):
    providers = [primary, secondary, free]
    
    for provider in providers:
        try:
            return await provider.get_response(messages)
        except RateLimitError:
            continue
        except AuthError:
            continue
    
    raise AllProvidersFailedError()
```

---

## 📝 Logging & Audit

### Log Levels

- `INFO` - Normal operations
- `WARNING` - Non-critical issues  
- `ERROR` - Errors and failures
- `DEBUG` - Detailed debugging info

### Audit Events

- Slash command usage
- Persona changes (especially jailbreaks)
- Provider switches
- Rate limit hits
- Authentication failures

### Log Format

```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "level": "INFO",
  "user_id": "289558466551480320", 
  "command": "/chat",
  "provider": "openai",
  "response_time_ms": 1250,
  "success": true
}
```

---

## 🚀 Integration Examples

### Python Integration

```python
from src.aclient import DiscordClient
from src.providers import ProviderManager

# Initialize client
client = DiscordClient()

# Handle message programmatically
response = await client.handle_message("Hello!", user_id=12345)

# Switch provider
client.provider_manager.set_current_provider(ProviderType.CLAUDE)

# Change persona
client.set_persona("creative")
```

### Environment Setup

```bash
# .env file
DISCORD_BOT_TOKEN=your_bot_token_here
OPENAI_KEY=your_openai_key_here
CLAUDE_KEY=your_claude_key_here
ADMIN_USER_IDS=123456789,987654321
MAX_MESSAGE_LENGTH=2000
```

---

## 🔗 Related Documentation

- [Installation Guide](getting-started/installation.md)
- [Discord Setup](getting-started/discord-setup.md)
- [Provider Configuration](configuration/providers.md)
- [Features Overview](features/_index.md)

---

## ⚠️ Important Notes

1. **Token Security**: Never share your Discord bot token or API keys
2. **Rate Limits**: Respect provider rate limits to avoid service interruption
3. **Admin Access**: Jailbreak personas should only be given to trusted administrators
4. **Fallback**: Always ensure at least the free provider is available
5. **Updates**: API behavior may change with provider updates

---

*Last Updated: January 2025*
*Version: 2.0.0*
