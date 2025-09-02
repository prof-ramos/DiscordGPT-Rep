---
title: "Começar"
description: "Guia completo para configurar e executar seu Discord ChatGPT Bot"
weight: 20
---

# 🚀 Guia de Início Rápido

Bem-vindo ao Discord ChatGPT Bot! Este guia vai ajudá-lo a colocar seu bot funcionando em poucos minutos.

## 🎯 O que você vai aprender

{{< cardpane >}}

{{< card header="**📥 Instalação**" >}}
- Pré-requisitos do sistema
- Download e configuração inicial
- Instalação das dependências
{{< /card >}}

{{< card header="**🤖 Setup Discord**" >}}
- Criar aplicação Discord
- Configurar bot e permissões
- Obter token de acesso
{{< /card >}}

{{< card header="**🏃 Primeira Execução**" >}}
- Configurar variáveis de ambiente
- Executar o bot localmente
- Testar comandos básicos
{{< /card >}}

{{< /cardpane >}}

## ⚡ Quick Start - 3 Minutos

Para usuários experientes que querem começar imediatamente:

```bash
# 1. Clone e configure
git clone https://github.com/prof-ramos/DiscordGPT.git
cd DiscordGPT
cp .env.example .env

# 2. Adicione seu token Discord no .env
# DISCORD_BOT_TOKEN=seu_token_aqui

# 3. Execute
docker compose up -d
```

{{< alert title="🎉 Pronto!" color="success" >}}
Se você já tem experiência com Discord bots, isso deve funcionar imediatamente!
{{< /alert >}}

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter:

{{< tabpane >}}

{{% tab header="🐳 Docker (Recomendado)" %}}
- **Docker**: Versão 20.10 ou superior
- **Docker Compose**: Versão 2.0 ou superior
- **Git**: Para clonar o repositório

```bash
# Verificar versões
docker --version
docker compose version
git --version
```
{{% /tab %}}

{{% tab header="🐍 Python Nativo" %}}
- **Python**: 3.9 ou superior  
- **pip**: Gerenciador de pacotes Python
- **Git**: Para clonar o repositório

```bash
# Verificar versões
python --version  # ou python3 --version
pip --version     # ou pip3 --version
git --version
```
{{% /tab %}}

{{< /tabpane >}}

## 🎮 Próximos Passos

{{< cardpane >}}

{{< card header="**1. 📥 Instalação**" >}}
[**Instalar Agora →**](installation/)

Baixe e configure o Discord ChatGPT Bot
{{< /card >}}

{{< card header="**2. 🤖 Discord Setup**" >}}
[**Configurar Bot →**](discord-setup/)

Crie sua aplicação Discord e obtenha o token
{{< /card >}}

{{< card header="**3. 🏃 Primeira Execução**" >}}
[**Executar Bot →**](first-run/)

Execute seu bot pela primeira vez
{{< /card >}}

{{< /cardpane >}}

## 🆘 Precisa de Ajuda?

Se encontrar algum problema durante a instalação:

- 📖 Consulte nossa [**seção de troubleshooting**](troubleshooting/)
- 💬 Participe das [**discussões no GitHub**](https://github.com/prof-ramos/DiscordGPT/discussions)
- 🐛 [**Reporte bugs**](https://github.com/prof-ramos/DiscordGPT/issues) se necessário

{{< alert title="💡 Dica" color="info" >}}
**Primeira vez com Discord bots?** Não se preocupe! Nosso guia é feito para iniciantes e especialistas.
{{< /alert >}}