import re

async def send_split_message(channel, response: str, char_limit: int = 2000):
    """Send a message to a channel, splitting into chunks by char_limit.

    Minimal utility used by tests and DM handling. Raises any exception from
    channel.send so callers can handle/report failures.
    """
    if response is None:
        response = ""

    if len(response) <= char_limit:
        await channel.send(response)
        return

    # Split by triple-backtick blocks to preserve formatting when possible
    parts = response.split("```")
    is_code_block = False
    for idx, part in enumerate(parts):
        chunks = [part[i:i + char_limit] for i in range(0, len(part), char_limit)]
        for chunk in chunks:
            if is_code_block:
                await channel.send(f"```{chunk}```")
            else:
                await channel.send(chunk)
        is_code_block = not is_code_block


async def send_response_with_images(channel, response: dict, char_limit: int = 2000):
    """Send a response containing text interleaved with images (as URLs)."""
    response_content = response.get("content", "")
    response_images = response.get("images", [])

    split_message_text = re.split(r'\[Image of.*?\]', response_content)

    for i, text in enumerate(split_message_text):
        text = text.strip()
        if text:
            await send_split_message(channel, text, char_limit)
        if response_images and i < len(response_images):
            await send_split_message(channel, str(response_images[i]).strip(), char_limit)
