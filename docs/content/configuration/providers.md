---
title: "Provedores de IA"
description: "Configure OpenAI, Claude, Gemini, Grok e outros provedores"
weight: 20
---

# 🤖 Configuração de Provedores de IA

O Discord ChatGPT Bot suporta múltiplos provedores de IA com fallback automático para máxima confiabilidade.

## 🎯 Provedores Disponíveis

{{< alert title="💡 Como Funciona" color="info" >}}
O bot tenta usar o **provedor padrão** primeiro. Se falhar, automaticamente tenta outros provedores disponíveis.
{{< /alert >}}

| Provedor | Gratuito | Qualidade | Velocidade | Recursos |
|----------|----------|-----------|------------|----------|
| **Free (g4f)** | ✅ | ⭐⭐⭐ | ⭐⭐ | Chat básico |
| **OpenAI** | ❌ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Chat + Imagens |
| **Claude** | ❌ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Chat avançado |
| **Gemini** | 🟡 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Chat + Tier gratuito |
| **Grok** | ❌ | ⭐⭐⭐⭐ | ⭐⭐⭐ | Chat + Humor |

## 🆓 1. Provedor Gratuito (g4f)

### Características
- ✅ **Completamente gratuito**
- ✅ **Sem configuração necessária**
- ✅ **Funciona imediatamente**
- ⚠️ **Qualidade variável**
- ⚠️ **Pode ser instável**

### Configuração

```env
# .env
DEFAULT_PROVIDER=free
# Nenhuma chave API necessária!
```

### Modelos Disponíveis
- `blackboxai` - Modelo principal
- `gpt-3.5-turbo` - Via proxy gratuito
- `gpt-4` - Via proxy gratuito (limitado)

{{< alert title="📝 Nota" color="info" >}}
O provedor gratuito é perfeito para testar o bot, mas para uso em produção recomendamos APIs premium.
{{< /alert >}}

## 🧠 2. OpenAI

### Características
- ⭐⭐⭐⭐⭐ **Melhor qualidade geral**
- 🚀 **Muito rápido**
- 🖼️ **DALL-E 3 para imagens**
- 💰 **Pago por uso**

### Como Obter Chave API

1. **Acesse:** [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. **Login** com sua conta OpenAI
3. **Clique** em "Create new secret key"
4. **Nomeie** a chave (ex: "Discord Bot")
5. **Copie** a chave que aparece

{{< alert title="💳 Billing" color="warning" >}}
Você precisa adicionar um método de pagamento na OpenAI para usar a API.
{{< /alert >}}

### Configuração

```env
# .env
DEFAULT_PROVIDER=openai
OPENAI_KEY=sk-proj-1234567890abcdef...

# Modelo padrão (opcional)
DEFAULT_MODEL=gpt-4o-mini  # Mais barato
# DEFAULT_MODEL=gpt-4o     # Melhor qualidade
```

### Modelos Disponíveis

{{< tabpane >}}

{{% tab header="💬 Chat Models" %}}
- **`gpt-4o`** - Modelo mais avançado (mais caro)
- **`gpt-4o-mini`** - Ótimo custo-benefício (recomendado)
- **`gpt-3.5-turbo`** - Mais barato, boa qualidade
- **`gpt-4-turbo`** - Anterior flagship model

**Preços aproximados (por 1M tokens):**
- GPT-4o: $5.00 input / $15.00 output
- GPT-4o-mini: $0.15 input / $0.60 output
- GPT-3.5-turbo: $0.50 input / $1.50 output
{{% /tab %}}

{{% tab header="🖼️ Image Models" %}}
- **`dall-e-3`** - Melhor qualidade
- **`dall-e-2`** - Mais barato

**Preços:**
- DALL-E 3: $0.040 por imagem (1024x1024)
- DALL-E 2: $0.020 por imagem (1024x1024)

**Usar:**
```
/draw Um gato astronauta no espaço
```
{{% /tab %}}

{{< /tabpane >}}

### Configuração Avançada

```env
# Usar modelo específico
DEFAULT_MODEL=gpt-4o-mini

# Configurações de temperatura e máx tokens (futuro)
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=2000
```

## 🔮 3. Claude (Anthropic)

### Características
- ⭐⭐⭐⭐⭐ **Excelente para textos longos**
- 🛡️ **Muito ético e seguro**
- 📝 **Ótimo para análise de código**
- 💰 **Pago por uso**

### Como Obter Chave API

1. **Acesse:** [console.anthropic.com](https://console.anthropic.com/)
2. **Crie conta** ou faça login
3. **Vá para** "API Keys"
4. **Clique** em "Create Key"
5. **Copie** a chave gerada

### Configuração

```env
# .env
DEFAULT_PROVIDER=claude
CLAUDE_KEY=sk-ant-api03-1234567890abcdef...

# Modelo padrão
DEFAULT_MODEL=claude-3-5-haiku-latest  # Mais rápido
# DEFAULT_MODEL=claude-3-5-sonnet-latest  # Melhor qualidade
```

### Modelos Disponíveis

- **`claude-3-5-sonnet-latest`** - Melhor modelo geral
- **`claude-3-5-haiku-latest`** - Mais rápido e barato
- **`claude-3-opus-latest`** - Máxima qualidade (mais caro)

**Preços aproximados:**
- Haiku: $0.25/$1.25 por 1M tokens
- Sonnet: $3.00/$15.00 por 1M tokens
- Opus: $15.00/$75.00 por 1M tokens

## 🌟 4. Google Gemini

### Características
- ⭐⭐⭐⭐ **Bom custo-benefício**
- 🆓 **Tier gratuito generoso**
- 🚀 **Muito rápido**
- 🔗 **Integração com Google**

### Como Obter Chave API

1. **Acesse:** [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. **Login** com conta Google
3. **Clique** em "Create API Key"
4. **Selecione** um projeto ou crie novo
5. **Copie** a chave gerada

### Configuração

```env
# .env
DEFAULT_PROVIDER=gemini
GEMINI_KEY=AIzaSy1234567890abcdef...

# Modelo padrão
DEFAULT_MODEL=gemini-pro  # Recomendado
```

### Modelos Disponíveis

- **`gemini-pro`** - Modelo principal, boa qualidade
- **`gemini-pro-vision`** - Suporte a imagens (futuro)

### Tier Gratuito

{{< alert title="🎉 Gratuito!" color="success" >}}
Google Gemini oferece **15 requisições por minuto** gratuitamente! Perfeito para uso pessoal.
{{< /alert >}}

## 🚀 5. Grok (xAI)

### Características
- ⭐⭐⭐⭐ **Modelo inovador**
- 😄 **Tom mais descontraído**
- ⚡ **Acesso a informações recentes**
- 💰 **Pago por uso**

### Como Obter Chave API

1. **Acesse:** [console.x.ai](https://console.x.ai/)
2. **Crie conta** xAI
3. **Vá para** "API Keys"
4. **Generate** nova chave
5. **Copie** a chave

### Configuração

```env
# .env
DEFAULT_PROVIDER=grok
GROK_KEY=xai-1234567890abcdef...

# Modelo padrão
DEFAULT_MODEL=grok-beta  # Único modelo disponível
```

## ⚙️ Configuração Multi-Provedor

### Fallback Automático

Configure múltiplos provedores para máxima confiabilidade:

```env
# Provedor principal
DEFAULT_PROVIDER=openai
OPENAI_KEY=sk-proj-sua_chave_openai

# Fallbacks
CLAUDE_KEY=sk-ant-sua_chave_claude
GEMINI_KEY=sua_chave_gemini

# Gratuito sempre disponível como último recurso
# (não precisa configurar)
```

**Ordem de fallback:**
1. **Provedor configurado** (`DEFAULT_PROVIDER`)
2. **Outros provedores premium** (se configurados)
3. **Provedor gratuito** (sempre disponível)

### Configuração por Qualidade

{{< tabpane >}}

{{% tab header="🥇 Máxima Qualidade" %}}
```env
DEFAULT_PROVIDER=openai
OPENAI_KEY=sk-proj-sua_chave
DEFAULT_MODEL=gpt-4o

# Fallback premium
CLAUDE_KEY=sk-ant-sua_chave
```
{{% /tab %}}

{{% tab header="⚡ Máxima Velocidade" %}}
```env
DEFAULT_PROVIDER=openai
OPENAI_KEY=sk-proj-sua_chave
DEFAULT_MODEL=gpt-3.5-turbo

# Fallback rápido
GEMINI_KEY=sua_chave
```
{{% /tab %}}

{{% tab header="💰 Economia" %}}
```env
DEFAULT_PROVIDER=gemini  # Tier gratuito
GEMINI_KEY=sua_chave

# Sem fallback premium para economizar
```
{{% /tab %}}

{{< /tabpane >}}

## 🎮 Trocar Provedores no Discord

### Comando `/provider`

Use no Discord para trocar provedor interativamente:

```
/provider
```

**Interface interativa mostra:**
- ✅ Provedores disponíveis
- ❌ Provedores não configurados
- 🔄 Modelo atual
- 📊 Status da API

### Trocar Temporariamente

```
# Usar OpenAI para uma conversa
/provider openai

# Voltar ao padrão
/provider default
```

## 📊 Monitoramento de Provedores

### Ver Status nos Logs

```bash
# Ver inicialização dos provedores
docker logs chatgpt-discord-bot | grep "Provider"

# Resultado típico:
# ✅ Provider initialized: OPENAI
# ✅ Provider initialized: CLAUDE  
# ⚠️  Provider not available: GEMINI (missing API key)
# ✅ Provider initialized: FREE
```

### Comandos de Diagnóstico

```
# Ver provedores disponíveis
/chat Quais provedores você tem configurados?

# Testar provedor específico
/provider openai
/chat Teste - você está usando OpenAI agora?
```

## 🚨 Troubleshooting

### "Provider not available"

**Causa:** Chave API inválida ou ausente

**Solução:**
```bash
# Verificar .env
cat .env | grep OPENAI_KEY

# Testar chave
curl -H "Authorization: Bearer $OPENAI_KEY" \
     https://api.openai.com/v1/models
```

### "Rate limit exceeded"

**Causa:** Muitas requisições para a API

**Solução:**
- Aguardar alguns minutos
- Bot automaticamente usa fallback
- Verificar limites da sua conta

### "Invalid API key"

**Causa:** Chave API expirada ou incorreta

**Solução:**
1. Gerar nova chave API
2. Atualizar arquivo `.env`
3. Reiniciar bot

### "Model not found"

**Causa:** Modelo especificado não existe

**Solução:**
```env
# Usar "auto" para seleção automática
DEFAULT_MODEL=auto

# Ou especificar modelo válido
DEFAULT_MODEL=gpt-4o-mini
```

## 💡 Dicas de Otimização

### Para Uso Pessoal
- Use **Gemini** (tier gratuito)
- Configure **OpenAI** como fallback
- Mantenha **Free** como último recurso

### Para Servidores Grandes
- Use **OpenAI** como principal
- Configure **Claude** como fallback
- Monitor logs para otimizar custos

### Para Desenvolvimento
- Use **Free** durante desenvolvimento
- Teste com **OpenAI** antes do deploy
- Configure todos os provedores para testes

{{< alert title="🎯 Recomendação" color="success" >}}
**Setup ideal**: OpenAI (principal) + Gemini (fallback) + Free (emergência)
{{< /alert >}}
