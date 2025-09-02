import os

from openai import AsyncOpenAI
from g4f.client import AsyncClient
from g4f.Provider import BingCreateImages, Gemini, OpenaiChat

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_KEY"))

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
    if os.getenv("OPENAI_ENABLED") == "False":
        image_provider = get_image_provider(model)
        g4f_client = AsyncClient(image_provider=image_provider)
        response = await g4f_client.images.generate(prompt=prompt)
    else:
        response = await openai_client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1792x1024",
            quality="auto",
            n=1,
        )
    return response.data[0].url


