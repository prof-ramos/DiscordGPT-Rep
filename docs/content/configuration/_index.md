---
title: "Configuração"
description: "Configure o Discord ChatGPT Bot para suas necessidades"
weight: 30
---

# ⚙️ Configuração do Bot

Configure o Discord ChatGPT Bot de acordo com suas necessidades específicas.

## 🎯 O que você pode configurar

{{< cardpane >}}

{{< card header="**🌍 Variáveis de Ambiente**" >}}
- Token Discord e configurações básicas
- Comportamento do bot e logging
- IDs de canais e administradores
{{< /card >}}

{{< card header="**🤖 Provedores de IA**" >}}
- OpenAI (GPT-3.5, GPT-4, DALL-E)
- Claude (Anthropic)
- Google Gemini
- xAI Grok
{{< /card >}}

{{< card header="**🔒 Segurança**" >}}
- Controle de acesso por usuário
- Personas jailbreak restritas
- Rate limiting e logs de auditoria
{{< /card >}}

{{< /cardpane >}}

## ⚡ Configuração Rápida

### Configuração Mínima (.env)

```env
# ✅ OBRIGATÓRIO
DISCORD_BOT_TOKEN=seu_token_discord_aqui

# ✅ RECOMENDADO
DEFAULT_PROVIDER=openai
OPENAI_KEY=sk-proj-sua_chave_openai_aqui
ADMIN_USER_IDS=seu_discord_id_aqui

# ✅ OPCIONAL
LOGGING=True
MAX_CONVERSATION_LENGTH=20
```

### Configuração Completa (.env)

```env
# === DISCORD ===
DISCORD_BOT_TOKEN=MTM5NzIwMzQ5ODg0MzUwODgzNw.exemplo
DISCORD_CHANNEL_ID=1177294119186485338
REPLYING_ALL_DISCORD_CHANNEL_ID=1177294119186485338

# === COMPORTAMENTO ===
LOGGING=True
REPLYING_ALL=False
DEFAULT_PROVIDER=openai
DEFAULT_MODEL=auto

# === ADMINISTRAÇÃO ===
ADMIN_USER_IDS=289558466551480320,311385521360
MAX_CONVERSATION_LENGTH=20
CONVERSATION_TRIM_SIZE=8

# === PROVEDORES DE IA ===
OPENAI_KEY=sk-proj-exemplo
CLAUDE_KEY=sk-ant-exemplo
GEMINI_KEY=exemplo
GROK_KEY=xai-exemplo
```

## 📋 Guias Detalhados

{{< cardpane >}}

{{< card header="**🌍 Variáveis de Ambiente**" >}}
[**Configurar .env →**](environment/)

Todas as variáveis disponíveis e seus valores
{{< /card >}}

{{< card header="**🤖 Provedores de IA**" >}}
[**Configurar APIs →**](providers/)

Como obter e configurar chaves API
{{< /card >}}

{{< card header="**🔒 Segurança**" >}}
[**Configurar Segurança →**](security/)

Controle de acesso e auditoria
{{< /card >}}

{{< card header="**🐳 Docker**" >}}
[**Configurar Docker →**](docker/)

Configurações avançadas de container
{{< /card >}}

{{< /cardpane >}}

## 🔧 Configurações por Categoria

### 🤖 Provedores Disponíveis

{{< tabpane >}}

{{% tab header="🆓 Gratuito" %}}
**Provedor**: `free` (g4f)
- ✅ **Sem API key necessária**
- ✅ **Funciona imediatamente**
- ⚠️ **Qualidade variável**
- ⚠️ **Pode ser instável**

```env
DEFAULT_PROVIDER=free
# Nenhuma configuração adicional necessária
```
{{% /tab %}}

{{% tab header="🧠 OpenAI" %}}
**Provedor**: `openai`
- ✅ **Melhor qualidade**
- ✅ **GPT-4, DALL-E 3**
- ✅ **Muito estável**
- 💰 **Pago**

```env
DEFAULT_PROVIDER=openai
OPENAI_KEY=sk-proj-sua_chave_aqui
```

[**Obter chave API →**](https://platform.openai.com/api-keys)
{{% /tab %}}

{{% tab header="🔮 Claude" %}}
**Provedor**: `claude`
- ✅ **Excelente para textos longos**
- ✅ **Muito ético e seguro**
- ✅ **Boa análise de código**
- 💰 **Pago**

```env
DEFAULT_PROVIDER=claude
CLAUDE_KEY=sk-ant-sua_chave_aqui
```

[**Obter chave API →**](https://console.anthropic.com/)
{{% /tab %}}

{{% tab header="🌟 Gemini" %}}
**Provedor**: `gemini`
- ✅ **Bom custo-benefício**
- ✅ **Integração com Google**
- ✅ **Tier gratuito disponível**
- 💰 **Freemium**

```env
DEFAULT_PROVIDER=gemini
GEMINI_KEY=sua_chave_aqui
```

[**Obter chave API →**](https://aistudio.google.com/app/apikey)
{{% /tab %}}

{{< /tabpane >}}

### 🎭 Sistema de Personalidades

{{< tabpane >}}

{{% tab header="👤 Padrão (Todos)" %}}
Disponível para todos os usuários:

- **`standard`** - Assistente útil padrão
- **`creative`** - Respostas criativas e imaginativas
- **`technical`** - Respostas técnicas e precisas  
- **`casual`** - Tom casual e amigável

```env
# Não precisa configurar nada especial
```
{{% /tab %}}

{{% tab header="🔓 Jailbreak (Admins)" %}}
**⚠️ Apenas para administradores:**

- **`jailbreak-v1`** - Modo BYPASS
- **`jailbreak-v2`** - Modo SAM
- **`jailbreak-v3`** - Developer Mode Plus

```env
# Configurar administradores
ADMIN_USER_IDS=289558466551480320,311385521360

# Como obter seu Discord ID:
# 1. Modo Desenvolvedor ON no Discord
# 2. Clicar direito em seu nome → "Copiar ID"
```

{{< alert title="⚠️ Aviso" color="warning" >}}
Personas jailbreak podem gerar conteúdo que bypass medidas de segurança da IA. Use com responsabilidade.
{{< /alert >}}

{{% /tab %}}

{{< /tabpane >}}

## 🚀 Configurações de Performance

### Otimizar para Velocidade

```env
# Provedor mais rápido
DEFAULT_PROVIDER=openai
DEFAULT_MODEL=gpt-3.5-turbo

# Histórico menor
MAX_CONVERSATION_LENGTH=10
CONVERSATION_TRIM_SIZE=5

# Logs mínimos
LOGGING=False
```

### Otimizar para Qualidade

```env
# Melhor provedor
DEFAULT_PROVIDER=openai
DEFAULT_MODEL=gpt-4

# Histórico maior
MAX_CONVERSATION_LENGTH=30
CONVERSATION_TRIM_SIZE=15

# Logs completos
LOGGING=True
```

### Otimizar para Custo

```env
# Provedor gratuito
DEFAULT_PROVIDER=free

# Ou usar Gemini (tier gratuito)
DEFAULT_PROVIDER=gemini
GEMINI_KEY=sua_chave_gratuita

# Histórico padrão
MAX_CONVERSATION_LENGTH=20
```

## 🔍 Validação de Configuração

### Teste Rápido

Execute este comando para validar sua configuração:

```bash
# Com Docker
docker exec chatgpt-discord-bot python -c "
import os
print('✅ DISCORD_BOT_TOKEN:', '✅ OK' if os.getenv('DISCORD_BOT_TOKEN') else '❌ MISSING')
print('✅ DEFAULT_PROVIDER:', os.getenv('DEFAULT_PROVIDER', 'free'))
print('✅ OPENAI_KEY:', '✅ OK' if os.getenv('OPENAI_KEY') else '❌ NOT SET')
"

# Com Python nativo
python -c "
import os
print('✅ DISCORD_BOT_TOKEN:', '✅ OK' if os.getenv('DISCORD_BOT_TOKEN') else '❌ MISSING')
print('✅ DEFAULT_PROVIDER:', os.getenv('DEFAULT_PROVIDER', 'free'))
print('✅ OPENAI_KEY:', '✅ OK' if os.getenv('OPENAI_KEY') else '❌ NOT SET')
"
```

### Logs de Inicialização

Procure por estas mensagens nos logs:

```
✅ Environment validation passed
✅ Provider initialized: OPENAI
✅ Admin users configured: ['289558466551480320']
✅ Bot is now running!
```

## 🆘 Problemas Comuns

### "Missing DISCORD_BOT_TOKEN"

```bash
# Verificar se .env existe
ls -la .env

# Verificar conteúdo
cat .env | grep DISCORD_BOT_TOKEN

# Se vazio, configure:
echo "DISCORD_BOT_TOKEN=seu_token_aqui" >> .env
```

### "Provider not available"

```bash
# Verificar chaves API no .env
cat .env | grep -E "(OPENAI|CLAUDE|GEMINI|GROK)_KEY"

# Adicionar chave ausente:
echo "OPENAI_KEY=sk-proj-sua_chave" >> .env
```

### "Jailbreak persona not available"

```bash
# Verificar configuração de admin
cat .env | grep ADMIN_USER_IDS

# Adicionar seu ID:
echo "ADMIN_USER_IDS=seu_discord_id_aqui" >> .env
```

## 🎯 Próximos Passos

{{< alert title="⚙️ Configuração Básica Pronta!" color="success" >}}
Com essas configurações, seu bot já funciona bem. Para configurações avançadas:
{{< /alert >}}

{{< cardpane >}}

{{< card header="**🌍 Variáveis Avançadas**" >}}
[**Ver Todas →**](environment/)

Lista completa de variáveis de ambiente
{{< /card >}}

{{< card header="**🤖 Configurar APIs**" >}}
[**Obter Chaves →**](providers/)

Guias para cada provedor de IA
{{< /card >}}

{{< card header="**🔒 Segurança Avançada**" >}}
[**Configurar →**](security/)

Rate limiting, auditoria e controles
{{< /card >}}

{{< /cardpane >}}