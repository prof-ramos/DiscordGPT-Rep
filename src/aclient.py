
import os
import discord
import asyncio
import logging
from typing import List, Dict, Optional
from discord.ext import commands

from src import personas
from src.log import logger
from src.providers import ProviderManager, ProviderType, ModelInfo
from utils.message_utils import send_split_message

from dotenv import load_dotenv
from discord import app_commands

load_dotenv()

class DiscordClient(commands.Bot):
    """Main Discord client class"""
    
    def __init__(self):
        # Configure intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        
        super().__init__(command_prefix='!', intents=intents)
        
        # Initialize components
        self.provider_manager = ProviderManager()
        self.conversation_histories = {}
        self.current_persona = "helpful"
        
        # Configuration
        self.max_message_length = int(os.getenv("MAX_MESSAGE_LENGTH", "2000"))
        self.conversation_limit = int(os.getenv("CONVERSATION_HISTORY_LIMIT", "20"))
        self.trim_size = int(os.getenv("TRIM_CONVERSATION_SIZE", "8"))
        
        # Admin users
        admin_ids = os.getenv("ADMIN_USER_IDS", "")
        self.admin_users = [int(uid.strip()) for uid in admin_ids.split(",") if uid.strip()]
        
        logger.info("Discord client initialized")
    
    async def on_ready(self):
        """Called when bot is ready"""
        logger.info(f"✅ Bot conectado como: {self.user}")
        logger.info(f"Bot ID: {self.user.id}")
        
        try:
            # Sync commands
            synced = await self.tree.sync()
            logger.info(f"✅ {len(synced)} comandos sincronizados")
            
            # Set status
            await self.change_presence(
                status=discord.Status.online,
                activity=discord.Activity(
                    type=discord.ActivityType.listening,
                    name="/chat para conversar"
                )
            )
            
        except Exception as e:
            logger.error(f"Erro ao sincronizar comandos: {e}")
    
    async def on_message(self, message):
        """Handle direct messages"""
        # Ignore bot messages
        if message.author == self.user:
            return
        
        # Handle DMs
        if isinstance(message.channel, discord.DMChannel):
            try:
                response = await self.handle_message(message.content, message.author.id)
                await send_split_message(message.channel, response, self.max_message_length)
            except Exception as e:
                logger.error(f"Error handling DM: {e}")
                await message.channel.send("❌ Erro ao processar mensagem.")
    
    async def handle_message(self, content: str, user_id: int) -> str:
        """Handle message and generate AI response"""
        try:
            # Get or create conversation history
            if user_id not in self.conversation_histories:
                self.conversation_histories[user_id] = []
            
            history = self.conversation_histories[user_id]
            
            # Add user message to history
            history.append({"role": "user", "content": content})
            
            # Trim history if too long
            if len(history) > self.conversation_limit:
                # Keep system message and recent context
                recent_messages = history[-self.trim_size:]
                self.conversation_histories[user_id] = recent_messages
                history = recent_messages
            
            # Get current persona
            persona_prompt = personas.get_persona_prompt(self.current_persona)
            
            # Prepare messages for AI
            messages = [{"role": "system", "content": persona_prompt}] + history
            
            # Get AI response
            response = await self.provider_manager.get_response(messages)
            
            # Add AI response to history
            history.append({"role": "assistant", "content": response})
            
            return response
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            return "❌ Desculpe, ocorreu um erro ao processar sua mensagem."
    
    def set_persona(self, persona_name: str) -> bool:
        """Set current persona"""
        if personas.is_valid_persona(persona_name):
            self.current_persona = persona_name
            logger.info(f"Persona alterada para: {persona_name}")
            return True
        return False
    
    def clear_conversation(self, user_id: int):
        """Clear conversation history for user"""
        if user_id in self.conversation_histories:
            del self.conversation_histories[user_id]
            logger.info(f"Conversa limpa para usuário: {user_id}")
    
    def is_admin(self, user_id: int) -> bool:
        """Check if user is admin"""
        return user_id in self.admin_users
    
    def run_bot(self):
        """Run the Discord bot"""
        token = os.getenv("DISCORD_BOT_TOKEN")
        if not token:
            logger.error("DISCORD_BOT_TOKEN não encontrado!")
            raise ValueError("Token Discord é obrigatório")
        
        # Setup commands
        self.setup_commands()
        
        # Run the bot
        try:
            self.run(token)
        except discord.LoginFailure:
            logger.error("❌ Token Discord inválido!")
            raise
        except Exception as e:
            logger.error(f"❌ Erro ao executar bot: {e}")
            raise
    
    def setup_commands(self):
        """Setup slash commands"""
        
        @self.tree.command(name="chat", description="Conversar com IA")
        async def chat_command(interaction: discord.Interaction, mensagem: str):
            await interaction.response.defer(thinking=True)
            
            try:
                response = await self.handle_message(mensagem, interaction.user.id)
                await interaction.followup.send(response[:2000])
            except Exception as e:
                logger.error(f"Erro no comando chat: {e}")
                await interaction.followup.send("❌ Erro ao processar mensagem.")
        
        @self.tree.command(name="reset", description="Limpar histórico de conversa")
        async def reset_command(interaction: discord.Interaction):
            try:
                self.clear_conversation(interaction.user.id)
                await interaction.response.send_message("🔄 Histórico de conversa limpo!")
            except Exception as e:
                logger.error(f"Erro no comando reset: {e}")
                await interaction.response.send_message("❌ Erro ao limpar conversa.")
        
        @self.tree.command(name="persona", description="Alterar personalidade da IA")
        async def persona_command(interaction: discord.Interaction, nome: str):
            try:
                if self.set_persona(nome):
                    await interaction.response.send_message(f"🎭 Persona alterada para: {nome}")
                else:
                    available = ", ".join(personas.get_available_personas())
                    await interaction.response.send_message(
                        f"❌ Persona inválida. Disponíveis: {available}"
                    )
            except Exception as e:
                logger.error(f"Erro no comando persona: {e}")
                await interaction.response.send_message("❌ Erro ao alterar persona.")
        
        @self.tree.command(name="status", description="Ver status do bot")
        async def status_command(interaction: discord.Interaction):
            try:
                embed = discord.Embed(
                    title="🤖 Status do Bot",
                    color=discord.Color.green()
                )
                
                # Bot info
                embed.add_field(name="Status", value="✅ Online", inline=True)
                embed.add_field(name="Latency", value=f"{round(self.latency * 1000)}ms", inline=True)
                embed.add_field(name="Persona Atual", value=self.current_persona, inline=True)
                
                # Provider info
                current_provider = self.provider_manager.current_provider
                embed.add_field(name="Provedor Atual", value=current_provider.value, inline=True)
                
                # Available providers
                available_providers = [p.value for p in self.provider_manager.get_available_providers()]
                embed.add_field(
                    name="Provedores Disponíveis", 
                    value=", ".join(available_providers), 
                    inline=False
                )
                
                await interaction.response.send_message(embed=embed)
                
            except Exception as e:
                logger.error(f"Erro no comando status: {e}")
                await interaction.response.send_message("❌ Erro ao verificar status.")
