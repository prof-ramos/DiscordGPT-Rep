---
title: "Discord ChatGPT Bot"
description: "Bot Discord inteligente com múltiplos provedores de IA - OpenAI, Claude, Gemini, Grok e provedor gratuito"
type: docs
menu:
  main:
    weight: 10
---

{{< blocks/cover title="Discord ChatGPT Bot" image_anchor="center" height="min" color="primary" >}}

```
╔════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                        ║
║    ██████╗██╗  ██╗ █████╗ ████████╗ ██████╗ ██████╗ ████████╗    ██████╗  ██████╗ ████████╗  ║
║   ██╔════╝██║  ██║██╔══██╗╚══██╔══╝██╔════╝ ██╔══██╗╚══██╔══╝    ██╔══██╗██╔═══██╗╚══██╔══╝  ║
║   ██║     ███████║███████║   ██║   ██║  ███╗██████╔╝   ██║       ██████╔╝██║   ██║   ██║     ║
║   ██║     ██╔══██║██╔══██║   ██║   ██║   ██║██╔═══╝    ██║       ██╔══██╗██║   ██║   ██║     ║
║   ╚██████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║        ██║       ██████╔╝╚██████╔╝   ██║     ║
║    ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝        ╚═╝       ╚═════╝  ╚═════╝    ╚═╝     ║
║                                                                                        ║
║             Desenvolvido por Prof. Ramos • GitHub: prof-ramos/DiscordGPT              ║
╚════════════════════════════════════════════════════════════════════════════════════════╝
```

<p class="lead">
🤖 <strong>O bot Discord mais completo para IA conversacional</strong><br>
Múltiplos provedores, personalidades customizáveis e fallback automático
</p>

{{< blocks/link-down color="info" >}}

{{< /blocks/cover >}}

{{% blocks/lead color="white" %}}

## 🚀 Quick Start - 30 Segundos

Coloque seu bot funcionando em menos de 1 minuto:

```bash
# 1. Clone o repositório
git clone https://github.com/prof-ramos/DiscordGPT.git
cd DiscordGPT

# 2. Configure o ambiente
cp .env.example .env
# Adicione seu DISCORD_BOT_TOKEN no .env

# 3. Execute com Docker
docker compose up -d
```

{{< alert title="✨ Pronto!" color="success" >}}
Seu bot já está online! Use `/chat Olá` para testar.
{{< /alert >}}

{{% /blocks/lead %}}

{{% blocks/section color="primary" type="row" %}}

{{% blocks/feature icon="fas fa-robot" title="5 Provedores de IA" %}}
**OpenAI** • **Claude** • **Gemini** • **Grok** • **Gratuito**

Fallback automático entre provedores para máxima disponibilidade
{{% /blocks/feature %}}

{{% blocks/feature icon="fas fa-masks-theater" title="Sistema de Personalidades" %}}
**Standard** • **Creative** • **Technical** • **Casual**

Controle de acesso para personas jailbreak (apenas admins)
{{% /blocks/feature %}}

{{% blocks/feature icon="fas fa-images" title="Geração de Imagens" %}}
**DALL-E 3** • **Gemini** • **Fallbacks**

Integração nativa com múltiplos provedores de imagem
{{% /blocks/feature %}}

{{% /blocks/section %}}

{{% blocks/section color="white" %}}

## 🎯 Principais Funcionalidades

{{< cardpane >}}

{{< card header="**🎮 Comandos Slash**" >}}
- `/chat [mensagem]` - Conversar com IA
- `/provider` - Trocar provedor interativamente  
- `/draw [prompt]` - Gerar imagens
- `/switchpersona` - Trocar personalidade
- `/reset` - Limpar histórico
{{< /card >}}

{{< card header="**🔒 Segurança**" >}}
- Controle de acesso por ID de usuário
- Rate limiting automático
- Logging de ações sensíveis
- Container Docker hardening
- Fallback entre provedores
{{< /card >}}

{{< card header="**⚙️ Configuração**" >}}
- Deploy com Docker Compose
- Variáveis de ambiente simples
- Múltiplas opções de provedor
- Sistema de prompt customizável
- Logs estruturados
{{< /card >}}

{{< /cardpane >}}

{{% /blocks/section %}}

{{% blocks/section color="dark" type="row" %}}

{{% blocks/feature icon="fab fa-github" title="Código Aberto" url="https://github.com/prof-ramos/DiscordGPT" %}}
Totalmente open source com licença MIT
{{% /blocks/feature %}}

{{% blocks/feature icon="fas fa-heart" title="Comunidade" url="https://github.com/prof-ramos/DiscordGPT/discussions" %}}
Junte-se à nossa comunidade de desenvolvedores
{{% /blocks/feature %}}

{{% blocks/feature icon="fas fa-life-ring" title="Suporte" url="/getting-started/troubleshooting" %}}
Documentação completa e suporte ativo
{{% /blocks/feature %}}

{{% /blocks/section %}}

{{% blocks/section color="info" %}}

## 📊 Estatísticas do Projeto

{{< alert title="🎉 Marcos Importantes" color="success" >}}
- **72 testes** unitários passando
- **5 provedores** de IA integrados  
- **Suporte completo** a Docker
- **Documentação** em português
- **Deploy automático** GitHub Pages
{{< /alert >}}

### 🔥 Por que escolher o Discord ChatGPT Bot?

- **🚀 Setup rápido**: Funcional em menos de 1 minuto
- **🛡️ Confiável**: Sistema de fallback robusto
- **🎨 Personalizável**: Sistema de personalidades flexível
- **📈 Escalável**: Arquitetura modular e testada
- **🌐 Multi-idioma**: Suporte completo em português
- **🔒 Seguro**: Controles de acesso granulares

{{% /blocks/section %}}

{{% blocks/section color="white" %}}

## 🚦 Próximos Passos

{{< cardpane >}}

{{< card header="**1. 📥 Instalar**" >}}
[**Começar Agora →**](/getting-started/installation/)

Siga nosso guia de instalação passo a passo
{{< /card >}}

{{< card header="**2. ⚙️ Configurar**" >}}  
[**Configuração →**](/configuration/)

Configure provedores de IA e variáveis de ambiente
{{< /card >}}

{{< card header="**3. 🚀 Deploy**" >}}
[**Deploy →**](/deployment/)

Coloque seu bot em produção com Docker
{{< /card >}}

{{< /cardpane >}}

{{% /blocks/section %}}