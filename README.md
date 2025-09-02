# Bot ChatGPT para Discord

> ### Crie seu próprio bot para Discord com múltiplos provedores de IA

---

> [!IMPORTANT]
>
> **Grande Refatoração (2025/07):**
> - **5 Provedores de IA**: Gratuito (g4f), OpenAI, Claude, Gemini, Grok
> - **Sem Autenticação por Cookies**: Removida a autenticação baseada em cookies para provedores gratuitos

### Chat

![image](https://user-images.githubusercontent.com/89479282/206497774-47d960cd-1aeb-4fba-9af5-1f9d6ff41f00.gif)

# Configuração

## Pré-requisitos

* **Python 3.9 ou superior**
* **Renomeie o arquivo `.env.example` para `.env`**
* Execute `pip3 install -r requirements.txt` para instalar as dependências necessárias
* Opcional: Chaves de API para provedores premium (OpenAI, Claude, Gemini, Grok)

---

## Passo 1: Crie um bot no Discord

1. Acesse https://discord.com/developers/applications e crie uma aplicação
2. Crie um bot dentro da aplicação
3. Obtenha o token nas configurações do bot

   ![image](https://user-images.githubusercontent.com/89479282/205949161-4b508c6d-19a7-49b6-b8ed-7525ddbef430.png)
4. Armazene o token no arquivo `.env` na variável `DISCORD_BOT_TOKEN`

   <img height="190" width="390" alt="image" src="https://user-images.githubusercontent.com/89479282/222661803-a7537ca7-88ae-4e66-9bec-384f3e83e6bd.png">

5. Ative o MESSAGE CONTENT INTENT

   ![image](https://user-images.githubusercontent.com/89479282/205949323-4354bd7d-9bb9-4f4b-a87e-deb9933a89b5.png)

6. Convide seu bot para o servidor usando o gerador de URL OAuth2

   ![image](https://user-images.githubusercontent.com/89479282/205949600-0c7ddb40-7e82-47a0-b59a-b089f929d177.png)

## Passo 2: Execute o bot no desktop

1. Abra um terminal ou prompt de comando
2. Navegue até o diretório onde você instalou o bot ChatGPT para Discord
3. Execute `python3 main.py` ou `python main.py` para iniciar o bot

---

## Passo 2: Execute o bot com Docker

1. Construa a imagem Docker e execute o container com `docker compose up -d`
2. Verifique se o bot está funcionando com `docker logs -t chatgpt-discord-bot`

   ### Pare o bot:

   * `docker ps` para ver a lista de serviços em execução
   * `docker stop <BOT CONTAINER ID>` para parar o bot em execução

### Boa conversa!

---

## Configuração de Provedores

### Provedor Gratuito (instável)

Modelo desatualizado, com capacidades próximas ao GPT-3.5 ou GPT-4

Nenhuma configuração necessária

### Provedores Premium (Opcional)

#### OpenAI

1. Obtenha sua chave de API em https://platform.openai.com/api-keys
2. Adicione ao `.env`: `OPENAI_KEY=sua_chave_api_aqui`

#### Claude (Anthropic)

1. Obtenha a chave de API em https://console.anthropic.com/
2. Adicione ao `.env`: `CLAUDE_KEY=sua_chave_api_aqui`

#### Gemini (Google)

1. Obtenha a chave de API em https://ai.google.dev/
2. Adicione ao `.env`: `GEMINI_KEY=sua_chave_api_aqui`

#### Grok (xAI)

1. Obtenha a chave de API em https://x.ai/api
2. Adicione ao `.env`: `GROK_KEY=sua_chave_api_aqui`

Use o comando `/provider` no Discord para alternar entre os provedores disponíveis

## Geração de Imagens

<img src="https://i.imgur.com/Eo1ZzKk.png" width="300" alt="image">

A geração de imagens agora está integrada ao sistema de provedores:

### OpenAI DALL-E 3

- Requer chave de API da OpenAI
- Geração de imagens de alta qualidade
- Use `/draw [prompt] openai`

### Google Gemini

- Requer chave de API do Gemini  
- Camada gratuita disponível
- Use `/draw [prompt] gemini`

### Opções de Fallback

- Se os provedores premium não estiverem disponíveis, o bot tentará usar alternativas gratuitas
- Os recursos de geração de imagens variam conforme a disponibilidade dos provedores

## Opcional: Configurar prompt do sistema

* Um prompt do sistema será acionado quando o bot for iniciado ou reiniciado
* Você pode configurá-lo modificando o conteúdo em `system_prompt.txt`
* Todo o texto no arquivo será enviado como prompt para o bot
* Receba a primeira mensagem do ChatGPT no seu canal do Discord!
* Nas configurações do Discord, ative o `modo desenvolvedor`

   1. Clique com o botão direito no canal onde deseja receber a mensagem, `Copiar ID`

        ![channel-id](https://user-images.githubusercontent.com/89479282/207697217-e03357b3-3b3d-44d0-b880-163217ed4a49.PNG)

   2. Cole no `.env` na variável `DISCORD_CHANNEL_ID`

## Opcional: Desativar logs

* Defina o valor de `LOGGING` no `.env` como False

## Comandos

### Comandos Principais

* `/chat [mensagem]` - Conversa com o provedor de IA atual
* `/provider` - Alterna entre provedores de IA (Gratuito, OpenAI, Claude, Gemini, Grok)
* `/draw [prompt] [modelo]` - Gera imagens com o provedor especificado
* `/reset` - Limpa o histórico da conversa
* `/help` - Exibe todos os comandos disponíveis

### Comandos de Persona

* `/switchpersona [persona]` - Alterna a personalidade da IA (somente administradores para jailbreaks)
   * `standard` - Assistente padrão e prestativo
   * `creative` - Respostas mais criativas e imaginativas  
   * `technical` - Respostas técnicas e precisas
   * `casual` - Tom casual e amigável
   * `jailbreak-v1` - Modo BYPASS (somente administradores)
   * `jailbreak-v2` - Modo SAM (somente administradores)
   * `jailbreak-v3` - Modo Developer Plus (somente administradores)

### Comportamento do Bot

* `/private` - Respostas do bot visíveis apenas para o usuário que enviou o comando
* `/public` - Respostas do bot visíveis para todos (padrão)
* `/replyall` - Bot responde a todas as mensagens no canal (alternar)

## Recursos de Segurança

### Acesso Restrito ao Jailbreak

Personas de jailbreak requerem privilégios de administrador para maior segurança:

1. Defina `ADMIN_USER_IDS` no `.env` com os IDs de usuários do Discord separados por vírgula
2. Apenas usuários administradores podem acessar personas de jailbreak
3. Usuários comuns veem apenas personas seguras em `/switchpersona`

> **Aviso**
> Personas de jailbreak podem gerar conteúdo que ignora as medidas normais de segurança da IA. Requer acesso de administrador.

### Segurança do Ambiente

- Nenhuma autenticação baseada em cookies (removida para maior confiabilidade)
- Gerenciamento seguro de chaves de API por meio de variáveis de ambiente
- Reforço de segurança no Docker com usuário não-root
- Sistema de arquivos somente leitura para segurança do container