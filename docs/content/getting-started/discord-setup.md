---
title: "Configuração do Discord"
description: "Como criar e configurar seu bot Discord"
weight: 20
---

# 🤖 Configuração do Bot Discord

Para usar o Discord ChatGPT Bot, você precisa criar uma aplicação Discord e obter um token de bot.

## 📋 Passo a Passo

### 1. Criar Aplicação Discord

1. Acesse o [**Discord Developer Portal**](https://discord.com/developers/applications)
2. Clique em **"New Application"**
3. Digite um nome para seu bot (ex: "ChatGPT Bot")
4. Clique em **"Create"**

{{< alert title="💡 Dica" color="info" >}}
Escolha um nome único e descritivo para seu bot. Este nome será visível para outros usuários.
{{< /alert >}}

### 2. Configurar o Bot

1. No menu lateral, clique em **"Bot"**
2. Clique em **"Add Bot"** → **"Yes, do it!"**
3. Configure as seguintes opções:

{{< tabpane >}}

{{% tab header="🔧 Configurações Básicas" %}}

**Username**: Nome que aparecerá no Discord
- Escolha algo como "ChatGPT", "AI Assistant", etc.

**Icon**: Avatar do seu bot
- Faça upload de uma imagem 512x512px
- Opcional, mas recomendado para aparência profissional

{{% /tab %}}

{{% tab header="🔒 Permissões de Bot" %}}

**Configurações importantes**:
- ✅ **PUBLIC BOT**: Ativo (outros podem convidar)
- ❌ **REQUIRES OAUTH2 CODE GRANT**: Desativo
- ✅ **MESSAGE CONTENT INTENT**: **MUITO IMPORTANTE!**
- ✅ **SERVER MEMBERS INTENT**: Recomendado
- ❌ **PRESENCE INTENT**: Opcional

{{< alert title="⚠️ Atenção" color="warning" >}}
**MESSAGE CONTENT INTENT** deve estar ATIVO ou o bot não funcionará!
{{< /alert >}}

{{% /tab %}}

{{< /tabpane >}}

### 3. Obter Token do Bot

1. Na seção **"Token"**, clique em **"Reset Token"**
2. Clique em **"Yes, do it!"**  
3. Copie o token que aparece
4. **⚠️ GUARDE EM SEGURANÇA!**

{{< alert title="🔐 Segurança" color="danger" >}}
**NUNCA compartilhe seu token!** Ele dá acesso total ao seu bot. Se vazar, reset imediatamente.
{{< /alert >}}

### 4. Configurar OAuth2

1. No menu lateral, clique em **"OAuth2"** → **"URL Generator"**
2. Em **"Scopes"**, selecione:
   - ✅ **bot**
   - ✅ **applications.commands**

3. Em **"Bot Permissions"**, selecione:

{{< tabpane >}}

{{% tab header="🔧 Permissões Essenciais" %}}
```
✅ Send Messages              # Enviar mensagens
✅ Use Slash Commands         # Usar comandos /
✅ Read Message History       # Ler histórico
✅ Embed Links               # Links incorporados
✅ Attach Files              # Anexar arquivos
✅ Add Reactions             # Adicionar reações
```
{{% /tab %}}

{{% tab header="📋 Lista Completa" %}}
```
General Permissions:
✅ Read Messages/View Channels
✅ Send Messages
✅ Send Messages in Threads
✅ Create Public Threads
✅ Create Private Threads
✅ Embed Links
✅ Attach Files
✅ Read Message History
✅ Add Reactions
✅ Use Slash Commands
✅ Use Application Commands

Advanced Permissions (Opcional):
□ Manage Messages           # Para comandos de moderação
□ Manage Threads           # Para gerenciar threads
□ Connect                  # Para comandos de voz (futuro)
□ Speak                    # Para comandos de voz (futuro)
```
{{% /tab %}}

{{< /tabpane >}}

4. Copie a **URL gerada** na parte inferior

### 5. Convidar Bot para Servidor

1. Use a URL copiada acima
2. Selecione o servidor onde quer adicionar o bot
3. Clique em **"Authorize"**
4. Complete o captcha se necessário

{{< alert title="✅ Sucesso!" color="success" >}}
Seu bot agora está no servidor! Você deve vê-lo offline na lista de membros.
{{< /alert >}}

## 🔧 Configurar Token no Bot

### Método 1: Arquivo .env (Recomendado)

```bash
# Edite o arquivo .env
nano .env  # ou use seu editor favorito

# Adicione seu token:
DISCORD_BOT_TOKEN=SEU_TOKEN_AQUI_SEM_ASPAS
```

### Método 2: Variável de Ambiente

```bash
# Linux/Mac
export DISCORD_BOT_TOKEN="seu_token_aqui"

# Windows (PowerShell)
$env:DISCORD_BOT_TOKEN="seu_token_aqui"

# Windows (CMD)
set DISCORD_BOT_TOKEN=seu_token_aqui
```

### Método 3: Docker Compose

```yaml
# docker-compose.yml
services:
  discord-bot:
    # ... outras configurações
    environment:
      - DISCORD_BOT_TOKEN=seu_token_aqui
```

## ✅ Testar Configuração

Execute seu bot e verifique os logs:

{{< tabpane >}}

{{% tab header="🐳 Docker" %}}
```bash
# Iniciar bot
docker compose up -d

# Ver logs
docker logs chatgpt-discord-bot

# Logs de sucesso devem mostrar:
# ✅ "Bot conectado como: SeuBot#1234"
# ✅ "Comandos sincronizados"
```
{{% /tab %}}

{{% tab header="🐍 Python" %}}
```bash
# Executar bot
python main.py

# Logs de sucesso devem mostrar:
# ✅ "Bot conectado como: SeuBot#1234"
# ✅ "Comandos sincronizados"
# ✅ "Bot is now running!"
```
{{% /tab %}}

{{< /tabpane >}}

## 🎮 Testar Comandos

No Discord, digite:

```
/chat Olá, como você está?
```

Se o bot responder, está funcionando perfeitamente! 🎉

## ⚠️ Problemas Comuns

### Bot Aparece Offline

**Possíveis causas:**
- Token incorreto ou inválido
- MESSAGE CONTENT INTENT desabilitado
- Permissões insuficientes

**Solução:**
```bash
# Verificar logs
docker logs chatgpt-discord-bot

# Procurar por erros como:
# "Improper token has been passed"
# "Missing permissions"
```

### Comandos Não Aparecem

**Causa:** Bot sem permissão de slash commands

**Solução:**
1. Remover bot do servidor
2. Usar nova URL OAuth2 com `applications.commands`
3. Re-adicionar bot com permissões corretas

### "Missing Access" Error

**Causa:** Bot não tem permissões no canal

**Solução:**
```
1. Configurações do servidor
2. Roles → @SeuBot
3. Permissões → Send Messages ✅
```

## 🎯 Próximo Passo

{{< alert title="🤖 Bot Configurado!" color="success" >}}
Seu bot Discord está configurado! Agora vamos executá-lo pela primeira vez.
{{< /alert >}}

[**➡️ Primeira Execução**](../first-run/) - Execute e teste seu bot