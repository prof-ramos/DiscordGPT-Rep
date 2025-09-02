---
title: "API Reference"
description: "Referência completa da API do Discord ChatGPT Bot"
weight: 50
---

# 📚 Referência da API

Documentação completa de todos os comandos, eventos e APIs do Discord ChatGPT Bot.

## 🎮 Comandos Slash

### `/chat`
**Descrição:** Conversar com a IA  
**Parâmetros:**
- `message` (obrigatório): Mensagem para enviar à IA

**Exemplo:**
```
/chat Explique machine learning em termos simples
```

**Resposta:** Resposta da IA usando o provedor configurado

---

### `/provider`
**Descrição:** Gerenciar provedores de IA  
**Parâmetros:** Nenhum

**Funcionalidade:**
- Exibe menu interativo
- Lista provedores disponíveis  
- Permite troca de provedor
- Mostra status atual

---

### `/draw`
**Descrição:** Gerar imagens com IA  
**Parâmetros:**
- `prompt` (obrigatório): Descrição da imagem
- `model` (opcional): Provedor específico

**Exemplos:**
```
/draw Um gato astronauta
/draw Paisagem futurista openai
```

---

### `/switchpersona`
**Descrição:** Trocar personalidade da IA  
**Parâmetros:**
- `persona` (obrigatório): Nome da personalidade

**Personas Disponíveis:**
- `standard` - Assistente padrão
- `creative` - Criativo e imaginativo  
- `technical` - Técnico e preciso
- `casual` - Descontraído e amigável
- `jailbreak-v1` - BYPASS (admin only)
- `jailbreak-v2` - SAM (admin only)
- `jailbreak-v3` - Developer Mode (admin only)

---

### `/reset`
**Descrição:** Limpar histórico de conversa  
**Parâmetros:** Nenhum

**Efeito:** Remove todo o contexto da conversa atual

---

### `/help`
**Descrição:** Exibir ajuda e lista de comandos  
**Parâmetros:** Nenhum

---

### `/private`
**Descrição:** Ativar respostas privadas  
**Parâmetros:** Nenhum

**Efeito:** Bot responde apenas para você (ephemeral)

---

### `/public`
**Descrição:** Ativar respostas públicas  
**Parâmetros:** Nenhum

**Efeito:** Bot responde publicamente no canal

---

### `/replyall`
**Descrição:** Toggle modo reply all  
**Parâmetros:** Nenhum

**Efeito:** Bot responde a todas as mensagens do canal

## 🔧 API dos Provedores

### Estrutura Base

```python
class BaseProvider:
    async def chat_completion(self, messages: List[Dict], model: str) -> str
    async def generate_image(self, prompt: str, model: str = None) -> str
    def get_available_models(self) -> List[ModelInfo]
    def supports_image_generation(self) -> bool
```

### ProviderManager

```python
class ProviderManager:
    def __init__(self)
    def get_provider(self, provider_type: ProviderType = None) -> BaseProvider
    def set_current_provider(self, provider_type: ProviderType)
    def get_available_providers(self) -> List[ProviderType]
    def get_all_models(self) -> Dict[ProviderType, List[ModelInfo]]
```

## 📡 Eventos Discord

### `on_ready`
Disparado quando o bot conecta com sucesso.

**Ações realizadas:**
- Sincronização de comandos slash
- Envio de prompt do sistema
- Inicialização do processamento de mensagens

### `on_message`  
Disparado para cada mensagem no servidor.

**Processamento:**
- Ignora mensagens do próprio bot
- Verifica modo reply all
- Processa mensagens em fila

## 🔄 Sistema de Fallback

### Ordem de Tentativas

1. **Provedor Padrão** (`DEFAULT_PROVIDER`)
2. **Provedores Premium** (se configurados)
3. **Provedor Gratuito** (sempre disponível)

### Códigos de Erro

| Código | Descrição | Ação |
|--------|-----------|-------|
| `RATE_LIMIT` | Limite de rate excedido | Tenta próximo provedor |
| `INVALID_KEY` | Chave API inválida | Pula provedor |
| `MODEL_NOT_FOUND` | Modelo inexistente | Usa modelo padrão |
| `NETWORK_ERROR` | Erro de conexão | Retry após delay |

## 📊 Rate Limiting

### Limites por Provedor

| Provedor | Requests/min | Tokens/min |
|----------|--------------|------------|
| OpenAI | 3,000 | 150,000 |
| Claude | 1,000 | 100,000 |
| Gemini | 15* | 32,000* |
| Grok | 100 | 10,000 |
| Free | Variável | Variável |

*Tier gratuito

### Sistema de Filas

```python
# Processamento sequencial
queue = asyncio.Queue()
await queue.put(message)
```

## 🔒 Sistema de Autenticação

### Verificação de Admin

```python
def is_admin(user_id: str) -> bool:
    admin_ids = os.getenv("ADMIN_USER_IDS", "").split(",")
    return str(user_id) in admin_ids
```

### Controle de Acesso Personas

```python
def get_available_personas(user_id: str = None) -> List[str]:
    personas = ["standard", "creative", "technical", "casual"]
    
    if user_id and is_admin(user_id):
        personas.extend(["jailbreak-v1", "jailbreak-v2", "jailbreak-v3"])
    
    return personas
```

## 📝 Logs e Auditoria

### Estrutura de Logs

```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "level": "INFO",
  "user_id": "289558466551480320",
  "command": "/switchpersona",
  "parameters": {"persona": "jailbreak-v1"},
  "provider": "openai",
  "model": "gpt-4o-mini"
}
```

### Eventos Auditados

- Uso de personas jailbreak
- Mudanças de provedor
- Erros de API
- Rate limiting
- Falhas de autenticação

## 🛡️ Tratamento de Erros

### Hierarquia de Exceções

```python
class BotException(Exception):
    """Base exception"""

class ProviderException(BotException):
    """Provider-related errors"""

class RateLimitException(ProviderException):
    """Rate limiting errors"""

class AuthenticationException(BotException):
    """Authentication errors"""
```

### Respostas de Erro

```python
error_responses = {
    "rate_limit": "⏱️ Limite de requisições atingido. Tentando provedor alternativo...",
    "invalid_key": "🔑 Erro de autenticação. Verificando configuração...",
    "network_error": "🌐 Erro de conexão. Tentando novamente...",
    "model_error": "🤖 Modelo indisponível. Usando alternativo..."
}
```

## 📈 Métricas e Monitoring

### Métricas Coletadas

- Número de comandos executados
- Tempo de resposta por provedor
- Taxa de sucesso/falha
- Uso por usuário/canal
- Distribuição de modelos

### Health Checks

```python
async def health_check() -> Dict[str, bool]:
    return {
        "discord_connected": bot.is_ready(),
        "providers_available": len(provider_manager.get_available_providers()) > 0,
        "database_connected": True,  # Se aplicável
    }
```

## 🔧 Configuração Avançada

### Variables de Ambiente API

```env
# Rate limiting
MAX_REQUESTS_PER_MINUTE=60
MAX_CONCURRENT_REQUESTS=5

# Timeouts
PROVIDER_TIMEOUT=30
DISCORD_TIMEOUT=15

# Retries
MAX_RETRIES=3
RETRY_DELAY=1
```

### Configuração de Logging

```env
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_FILE=/var/log/discord-bot.log
```

{{< alert title="📚 Documentação Técnica" color="info" >}}
Esta API reference cobre os aspectos principais. Para implementação detalhada, consulte o código fonte no [GitHub](https://github.com/prof-ramos/DiscordGPT).
{{< /alert >}}