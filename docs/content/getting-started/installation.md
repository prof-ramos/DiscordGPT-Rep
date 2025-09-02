---
title: "Instalação"
description: "Como instalar e configurar o Discord ChatGPT Bot"
weight: 10
---

# 📥 Instalação do Discord ChatGPT Bot

Este guia vai te ajudar a instalar o Discord ChatGPT Bot no seu sistema.

## 🎯 Métodos de Instalação

{{< tabpane >}}

{{% tab header="🐳 Docker (Recomendado)" %}}

### Por que Docker?
- ✅ **Mais fácil**: Sem problemas de dependências
- ✅ **Mais rápido**: Setup em 30 segundos
- ✅ **Mais seguro**: Isolamento de containers
- ✅ **Mais confiável**: Ambiente consistente

### Instalação com Docker

```bash
# 1. Clone o repositório
git clone https://github.com/prof-ramos/DiscordGPT.git
cd DiscordGPT

# 2. Copie o arquivo de ambiente
cp .env.example .env

# 3. Execute com Docker
docker compose up -d
```

### Verificar se está funcionando

```bash
# Ver logs do container
docker logs chatgpt-discord-bot

# Ver containers rodando
docker ps
```

{{< alert title="🎉 Sucesso!" color="success" >}}
Se você viu logs de conexão, o bot está funcionando! Agora configure o token Discord.
{{< /alert >}}

{{% /tab %}}

{{% tab header="🐍 Python Nativo" %}}

### Pré-requisitos
- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)

### Instalação Nativa

```bash
# 1. Clone o repositório  
git clone https://github.com/prof-ramos/DiscordGPT.git
cd DiscordGPT

# 2. Crie ambiente virtual
python -m venv venv

# 3. Ative o ambiente virtual
# No Linux/Mac:
source venv/bin/activate
# No Windows:
# venv\Scripts\activate

# 4. Instale dependências
pip install -r requirements.txt

# 5. Copie arquivo de ambiente
cp .env.example .env

# 6. Execute o bot
python main.py
```

### Usando UV (Mais Rápido)

```bash
# 1. Instale UV (se não tiver)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clone repositório
git clone https://github.com/prof-ramos/DiscordGPT.git
cd DiscordGPT

# 3. Criar ambiente virtual
uv venv --python python3.11

# 4. Ativar ambiente
source .venv/bin/activate

# 5. Instalar dependências
uv pip install -r requirements.txt

# 6. Configurar ambiente
cp .env.example .env

# 7. Executar bot
python main.py
```

{{% /tab %}}

{{% tab header="📦 Git Submodule" %}}

### Para Projetos Existentes

Se você já tem um projeto e quer adicionar o bot como submodule:

```bash
# 1. Adicionar como submodule
git submodule add https://github.com/prof-ramos/DiscordGPT.git discord-bot

# 2. Inicializar submodule
git submodule init
git submodule update

# 3. Entrar no diretório
cd discord-bot

# 4. Seguir instalação Docker ou Python
docker compose up -d
```

{{% /tab %}}

{{< /tabpane >}}

## 🔧 Dependências do Sistema

### Dependências Python (se não usar Docker)

O bot usa as seguintes bibliotecas principais:

```text
discord.py==2.4.0         # Integração Discord
openai==1.66.2            # API OpenAI
anthropic==0.42.0         # API Claude
google-generativeai==0.8.3 # API Gemini
g4f==0.3.2.9             # Provedor gratuito
pytest==8.3.4            # Testes
```

### Verificar Instalação

Execute este comando para verificar se tudo está funcionando:

```bash
# Se usando Docker
docker exec chatgpt-discord-bot python -c "import discord; print('✅ Discord.py OK')"

# Se usando Python nativo
python -c "import discord; print('✅ Discord.py OK')"
python -c "import openai; print('✅ OpenAI OK')"
python -c "import anthropic; print('✅ Anthropic OK')"
```

## 📁 Estrutura do Projeto

Após a instalação, sua estrutura de arquivos deve estar assim:

```
DiscordGPT/
├── 📂 src/                    # Código fonte principal
│   ├── 🐍 aclient.py         # Cliente Discord
│   ├── 🐍 bot.py             # Comandos slash
│   ├── 🐍 providers.py       # Provedores de IA
│   ├── 🐍 personas.py        # Sistema de personalidades
│   └── 🎨 art.py             # Arte ASCII
├── 📂 utils/                  # Utilitários
│   └── 🐍 message_utils.py   # Funções de mensagem
├── 📂 tests/                  # Testes unitários
├── 🐳 docker-compose.yml     # Configuração Docker
├── 🐳 Dockerfile             # Imagem Docker
├── ⚙️ .env.example           # Exemplo de variáveis
├── 📋 requirements.txt       # Dependências Python
└── 🐍 main.py               # Ponto de entrada
```

## ⚠️ Problemas Comuns

### "ModuleNotFoundError: No module named 'discord'"

```bash
# Solução: Instalar dependências
pip install -r requirements.txt

# Ou com UV:
uv pip install -r requirements.txt
```

### "Permission denied" (Linux/Mac)

```bash
# Solução: Dar permissões corretas
chmod +x main.py
```

### "Docker command not found"

```bash
# Instalar Docker no Ubuntu/Debian:
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# No Mac: Baixar Docker Desktop
# No Windows: Baixar Docker Desktop
```

## 🎯 Próximo Passo

{{< alert title="✅ Instalação Concluída!" color="success" >}}
Agora você precisa configurar seu bot Discord para obter o token de acesso.
{{< /alert >}}

[**➡️ Configurar Discord Bot**](../discord-setup/) - Criar aplicação e obter token