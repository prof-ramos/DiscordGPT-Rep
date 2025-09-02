
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from typing import Optional

from src.aclient import DiscordClient
from src.log import logger
from src.art import get_random_art

def run_discord_bot():
    """Main function to run the Discord bot"""
    try:
        # Create and run the Discord client
        client = DiscordClient()
        
        # Display ASCII art
        print(get_random_art())
        
        # Run the bot
        logger.info("Starting Discord bot...")
        client.run_bot()
        
    except Exception as e:
        logger.error(f"Failed to start Discord bot: {e}")
        raise

class BotCommands(commands.Cog):
    """Discord bot commands"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="chat", description="Chat with AI")
    async def chat(self, interaction: discord.Interaction, message: str):
        """Chat command for AI interaction"""
        await interaction.response.defer(thinking=True)
        
        try:
            # Get the client instance
            client = self.bot
            if hasattr(client, 'handle_message'):
                response = await client.handle_message(message, interaction.user.id)
                await interaction.followup.send(response[:2000])
            else:
                await interaction.followup.send("❌ Bot não está configurado corretamente.")
                
        except Exception as e:
            logger.error(f"Error in chat command: {e}")
            await interaction.followup.send("❌ Erro ao processar mensagem.")
    
    @app_commands.command(name="reset", description="Reset conversation history")
    async def reset(self, interaction: discord.Interaction):
        """Reset conversation history"""
        try:
            # Reset logic would go here
            await interaction.response.send_message("🔄 Histórico de conversa resetado!")
            
        except Exception as e:
            logger.error(f"Error in reset command: {e}")
            await interaction.response.send_message("❌ Erro ao resetar conversa.")
    
    @app_commands.command(name="status", description="Check bot status")
    async def status(self, interaction: discord.Interaction):
        """Check bot status"""
        try:
            # Get basic status info
            embed = discord.Embed(
                title="🤖 Status do Bot",
                color=discord.Color.green()
            )
            embed.add_field(name="Status", value="✅ Online", inline=True)
            embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            logger.error(f"Error in status command: {e}")
            await interaction.response.send_message("❌ Erro ao verificar status.")

async def setup(bot):
    """Setup function for the cog"""
    await bot.add_cog(BotCommands(bot))
