import os
from g4f.client import AsyncClient
from g4f.Provider import BingCreateImages, Gemini, OpenaiChat
from src.log import logger

def get_image_provider(provider_name: str):
    providers = {
        "Gemini": Gemini,
        "openai": OpenaiChat,
        "BingCreateImages": BingCreateImages,
    }
    return providers.get(provider_name, BingCreateImages)

def get_random_art() -> str:
    """Returns ASCII art for bot startup"""
    art = """
╔════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                        ║
║   ██████╗██╗  ██╗ █████╗ ████████╗ ██████╗ ██████╗ ████████╗    ██████╗  ██████╗ ████████╗   ║
║  ██╔════╝██║  ██║██╔══██╗╚══██╔══╝██╔════╝ ██╔══██╗╚══██╔══╝    ██╔══██╗██╔═══██╗╚══██╔══╝   ║
║  ██║     ███████║███████║   ██║   ██║  ███╗██████╔╝   ██║       ██████╔╝██║   ██║   ██║      ║
║  ██║     ██╔══██║██╔══██║   ██║   ██║   ██║██╔═══╝    ██║       ██╔══██╗██║   ██║   ██║      ║
║  ╚██████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║        ██║       ██████╔╝╚██████╔╝   ██║      ║
║   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝        ╚═╝       ╚═════╝  ╚═════╝    ╚═╝      ║
║                                                                                        ║
║             Desenvolvido por Prof. Ramos • GitHub: prof-ramos/DiscordGPT              ║
╚════════════════════════════════════════════════════════════════════════════════════════╝
    """
    return art

async def draw(model: str, prompt: str) -> str:
    """Generate an image URL using either OpenAI (if configured) or g4f fallback.

    - Avoids importing or initializing OpenAI client at module import time.
    - Provides clear logging when falling back due to missing configuration.
    """
    openai_enabled = os.getenv("OPENAI_ENABLED", "True").lower() in {"1", "true", "yes", "y"}
    api_key = os.getenv("OPENAI_KEY") or os.getenv("OPENAI_API_KEY")

    # Use OpenAI if explicitly enabled and api key present
    if openai_enabled and api_key:
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=api_key)
            response = await client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                size="1792x1024",
                quality="auto",
                n=1,
            )
            return response.data[0].url
        except Exception as e:
            logger.warning(f"OpenAI image generation failed, falling back to g4f: {e}")

    # Fallback path using g4f
    if not api_key:
        logger.info("OPENAI_KEY not set; using free image provider fallback")
    image_provider = get_image_provider(model)
    g4f_client = AsyncClient(image_provider=image_provider)
    response = await g4f_client.images.generate(prompt=prompt)
    return getattr(response, "data", [{"url": getattr(response, "url", "")}])[0].get("url") or getattr(response, "url", "")

