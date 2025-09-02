#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from src.bot import run_discord_bot
from src.log import logger

load_dotenv()

def validate_environment():
    """Validate required environment variables"""
    required_vars = ["DISCORD_BOT_TOKEN"]
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        elif var == "DISCORD_BOT_TOKEN":
            # Validate Discord token format
            if not value.startswith(('MTA', 'MTM', 'MTI', 'OTA', 'OTM', 'OTI')) or len(value) < 50:
                logger.error(f"Invalid Discord token format. Please check your DISCORD_BOT_TOKEN in .env")
                return False
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please check your .env file")
        return False
    
    providers = []
    if os.getenv("OPENAI_KEY"):
        providers.append("OpenAI")
    if os.getenv("CLAUDE_KEY"):
        providers.append("Claude")
    if os.getenv("GEMINI_KEY"):
        providers.append("Gemini")
    if os.getenv("GROK_KEY"):
        providers.append("Grok")
    
    providers.append("Free (always available)")
    
    logger.info(f"Available providers: {', '.join(providers)}")
    
    return True

def main():
    """Main entry point"""
    logger.info("Starting Discord AI Bot...")
    
    if not validate_environment():
        logger.error("❌ Environment validation failed. Bot cannot start.")
        return
    
    logger.info("✅ Environment validation passed")
    logger.info("Free provider configured - no authentication required")
    
    try:
        run_discord_bot()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Bot crashed: {e}")
        logger.error("Check your Discord token and bot permissions")
        raise

if __name__ == "__main__":
    main()
