---
title: "Primeira Execução"
description: "Execute seu Discord ChatGPT Bot pela primeira vez"
weight: 30
---

# 🏃 Primeira Execução do Bot

Agora que você tem o bot instalado e configurado, vamos executá-lo pela primeira vez!

## 🚀 Execução Rápida

{{< tabpane >}}

{{% tab header="🐳 Docker" %}}
```bash
# 1. Navegar para diretório do bot
cd DiscordGPT

# 2. Executar em background
docker compose up -d

# 3. Ver logs em tempo real
docker logs -f chatgpt-discord-bot
```

**Logs de sucesso:**
```
✅ Environment validation passed
✅ Provider initialized: FREE
✅ Bot connected as: SeuBot#1234  
✅ Commands synchronized
✅ Bot is now running!
```
{{% /tab %}}

{{% tab header="🐍 Python" %}}
```bash
# 1. Ativar ambiente virtual
source venv/bin/activate
# ou: source .venv/bin/activate

# 2. Executar bot
python main.py

# 3. Ver logs
# (aparecem diretamente no terminal)
```

**Logs de sucesso:**
```
✅ Environment validation passed
✅ Provider initialized: FREE
✅ Bot connected as: SeuBot#1234
✅ Commands synchronized  
✅ Bot is now running!
```
{{% /tab %}}

{{< /tabpane >}}

{{< alert title="🎉 Primeiro Sucesso!" color="success" >}}
Se você viu os logs acima, seu bot está **online e funcionando**!
{{< /alert >}}

## 🎮 Primeiros Comandos

### Teste Básico

No Discord, digite:

```
/chat Olá! Como você está hoje?
```

**Resposta esperada:** O bot deve responder com uma mensagem amigável usando o provedor gratuito.

### Comandos Essenciais

{{< tabpane >}}

{{% tab header="💬 Comandos de Chat" %}}
```bash
# Conversa básica
/chat Explique o que é inteligência artificial

# Ver provedores disponíveis  
/provider

# Resetar conversa
/reset

# Ajuda
/help
```
{{% /tab %}}

{{% tab header="🎭 Comandos de Personalidade" %}}
```bash
# Ver personalidades disponíveis
/switchpersona

# Trocar para personalidade técnica
/switchpersona technical

# Trocar para personalidade criativa
/switchpersona creative
```
{{% /tab %}}

{{% tab header="🖼️ Comandos de Imagem" %}}
```bash
# Gerar imagem (requer provedor premium)
/draw Um gato fofo usando óculos de sol

# Verificar se funciona
/chat Você consegue gerar imagens?
```
{{% /tab %}}

{{< /tabpane >}}

## 📊 Status do Sistema

### Ver Status dos Provedores

O bot inicializa com diferentes provedores baseado nas suas configurações:

```bash
# Ver logs de inicialização
docker logs chatgpt-discord-bot | grep "Provider"

# Resultado típico:
# ✅ Provider initialized: FREE
# ⚠️  Provider not available: OPENAI (missing API key)
# ⚠️  Provider not available: CLAUDE (missing API key)
```

### Comandos de Diagnóstico

```bash
# Ver informações do sistema
/chat Quais provedores você tem disponível?

# Testar funcionalidade
/chat Teste de conectividade - responda com OK se funcionar
```

## ⚙️ Configurações Iniciais

### Configurar Canal de Sistema (Opcional)

Para receber mensagens de sistema:

1. **Obter ID do canal:**
   - Ativar "Modo Desenvolvedor" no Discord
   - Clicar direito no canal → "Copiar ID"

2. **Configurar no .env:**
   ```bash
   DISCORD_CHANNEL_ID=1177294119186485338
   ```

3. **Reiniciar bot:**
   ```bash
   docker compose restart
   ```

### Configurar Administradores

Para usar personalidades jailbreak:

```bash
# Adicionar no .env
ADMIN_USER_IDS=289558466551480320,311385521360

# Obter seu ID Discord:
# 1. Modo Desenvolvedor ON
# 2. Clicar direito em seu nome → "Copiar ID"
```

## 🔧 Monitoramento

### Comandos Úteis

{{< tabpane >}}

{{% tab header="🐳 Docker" %}}
```bash
# Ver status dos containers
docker ps

# Ver logs em tempo real
docker logs -f chatgpt-discord-bot

# Ver recursos utilizados
docker stats chatgpt-discord-bot

# Reiniciar bot
docker compose restart

# Parar bot
docker compose down
```
{{% /tab %}}

{{% tab header="🐍 Python" %}}
```bash
# Ver processos Python
ps aux | grep python

# Matar processo se necessário
pkill -f main.py

# Executar em background
nohup python main.py &

# Ver logs de background
tail -f nohup.out
```
{{% /tab %}}

{{< /tabpane >}}

### Logs Importantes

**🔍 Procurar por:**
- `✅ Bot is now running!` - Bot iniciado com sucesso
- `❌ Error:` - Erros que precisam correção
- `⚠️ Warning:` - Avisos importantes
- `📊 Provider fallback` - Mudança automática de provedor

## 🚨 Problemas na Primeira Execução

### Bot Não Conecta

{{< alert title="🔍 Diagnóstico" color="info" >}}
```bash
# Ver logs completos
docker logs chatgpt-discord-bot

# Procurar por:
# "Improper token" → Token Discord inválido
# "Missing intent" → MESSAGE CONTENT INTENT desabilitado  
# "Missing permissions" → Permissões insuficientes
```
{{< /alert >}}

### Comandos Não Aparecem

**Causa mais comum:** Permissões OAuth2 incorretas

**Solução:**
1. Remover bot do servidor
2. Gerar nova URL OAuth2 com `applications.commands` 
3. Re-adicionar bot

### Respostas Estranhas

**Causa:** Provedor gratuito pode ser instável

**Soluções:**
- Configure uma API key premium (OpenAI, Claude, etc.)
- Use `/provider` para trocar provedor
- Aguarde alguns minutos e tente novamente

## 🎯 Próximos Passos

{{< alert title="🎉 Bot Funcionando!" color="success" >}}
Parabéns! Seu Discord ChatGPT Bot está rodando. Agora você pode:
{{< /alert >}}

{{< cardpane >}}

{{< card header="**⚙️ Configurar Provedores**" >}}
[**Adicionar APIs →**](/configuration/providers/)

Configure OpenAI, Claude, Gemini para melhor qualidade
{{< /card >}}

{{< card header="**🚀 Fazer Deploy**" >}}
[**Deploy em Produção →**](/deployment/)

Coloque seu bot online 24/7
{{< /card >}}

{{< card header="**🔧 Personalizar**" >}}
[**Ver Todas as Funcionalidades →**](/features/)

Explore comandos avançados e personalidades
{{< /card >}}

{{< /cardpane >}}

## 📋 Checklist de Sucesso

- [ ] Bot aparece online no Discord
- [ ] `/chat` responde corretamente  
- [ ] `/provider` mostra provedores disponíveis
- [ ] `/help` lista todos os comandos
- [ ] Logs não mostram erros críticos
- [ ] Bot responde em até 30 segundos

{{< alert title="✅ Tudo OK?" color="success" >}}
Se todos os itens estão marcados, seu bot está funcionando perfeitamente!
{{< /alert >}}