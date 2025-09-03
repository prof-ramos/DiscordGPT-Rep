import os
from openai import AsyncOpenAI
from g4f.client import AsyncClient
from g4f.Provider import BingCreateImages, Gemini, OpenaiChat

# Initialize OpenAI client only if key is available
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_KEY")) if os.getenv("OPENAI_KEY") else None

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
    """Generate an image URL.

    - Uses OpenAI if enabled and configured; propagates errors to caller.
    - Uses g4f provider when OpenAI is disabled via OPENAI_ENABLED=False.
    """
    openai_enabled = os.getenv("OPENAI_ENABLED", "True").lower() not in {"false", "0", "no", "n"}

    if openai_enabled:
        if not openai_client:
            raise ValueError("OPENAI_KEY not configured for image generation")
        response = await openai_client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1792x1024",
            quality="auto",
            n=1,
        )
        return response.data[0].url

    # g4f fallback path
    image_provider = get_image_provider(model)
    g4f_client = AsyncClient(image_provider=image_provider)
    response = await g4f_client.images.generate(prompt=prompt)
    # Expect response.data[0].url from tests
    return response.data[0].url
