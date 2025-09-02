import os
import asyncio
import aiohttp
from enum import Enum
from typing import List, Dict, Optional, Any
from dataclasses import dataclass

from src.log import logger

class ProviderType(Enum):
    """Available AI providers"""
    OPENAI = "OpenAI"
    CLAUDE = "Claude"
    GEMINI = "Gemini"
    GROK = "Grok"
    FREE = "Free"

class BaseProvider:
    """Base class for AI providers"""

    def __init__(self, provider_type: ProviderType):
        self.provider_type = provider_type
        self.is_available = False

    async def get_response(self, messages: list) -> str:
        """Get response from provider"""
        raise NotImplementedError("Subclasses must implement get_response")

    def check_availability(self) -> bool:
        """Check if provider is available"""
        raise NotImplementedError("Subclasses must implement check_availability")

@dataclass
class ModelInfo:
    """Information about an AI model"""
    name: str
    provider: ProviderType
    max_tokens: int
    cost_per_token: float = 0.0

class ProviderManager:
    """Manages AI providers and their configurations"""

    def __init__(self):
        self.current_provider = ProviderType.FREE
        self.models = {
            ProviderType.FREE: [
                ModelInfo("gpt-3.5-turbo", ProviderType.FREE, 4096, 0.0)
            ],
            ProviderType.OPENAI: [
                ModelInfo("gpt-3.5-turbo", ProviderType.OPENAI, 4096, 0.002),
                ModelInfo("gpt-4", ProviderType.OPENAI, 8192, 0.03),
                ModelInfo("gpt-4-turbo", ProviderType.OPENAI, 128000, 0.01)
            ],
            ProviderType.CLAUDE: [
                ModelInfo("claude-3-haiku", ProviderType.CLAUDE, 200000, 0.0025),
                ModelInfo("claude-3-sonnet", ProviderType.CLAUDE, 200000, 0.015),
                ModelInfo("claude-3-opus", ProviderType.CLAUDE, 200000, 0.075)
            ],
            ProviderType.GEMINI: [
                ModelInfo("gemini-pro", ProviderType.GEMINI, 32768, 0.0005),
                ModelInfo("gemini-pro-vision", ProviderType.GEMINI, 16384, 0.0025)
            ],
            ProviderType.GROK: [
                ModelInfo("grok-beta", ProviderType.GROK, 25000, 0.01)
            ]
        }

        self.current_model = self.models[ProviderType.FREE][0]

        # Initialize providers based on available keys
        self._initialize_providers()

        logger.info(f"Provider manager initialized with {self.current_provider.value}")

    def _initialize_providers(self):
        """Initialize available providers based on API keys"""
        available = [ProviderType.FREE]  # Free is always available

        if os.getenv("OPENAI_KEY"):
            available.append(ProviderType.OPENAI)

        if os.getenv("CLAUDE_KEY"):
            available.append(ProviderType.CLAUDE)

        if os.getenv("GEMINI_KEY"):
            available.append(ProviderType.GEMINI)

        if os.getenv("GROK_KEY"):
            available.append(ProviderType.GROK)

        self.available_providers = available
        logger.info(f"Available providers: {[p.value for p in available]}")

    def get_available_providers(self) -> List[ProviderType]:
        """Get list of available providers"""
        return self.available_providers

    def set_current_provider(self, provider: ProviderType) -> bool:
        """Set current provider"""
        if provider in self.available_providers:
            self.current_provider = provider
            # Set default model for provider
            if provider in self.models:
                self.current_model = self.models[provider][0]
            logger.info(f"Provider changed to: {provider.value}")
            return True
        return False

    def get_models_for_provider(self, provider: ProviderType) -> List[ModelInfo]:
        """Get available models for a provider"""
        return self.models.get(provider, [])

    def set_current_model(self, model_name: str) -> bool:
        """Set current model"""
        for model in self.models[self.current_provider]:
            if model.name == model_name:
                self.current_model = model
                logger.info(f"Model changed to: {model_name}")
                return True
        return False

    async def get_response(self, messages: List[Dict[str, str]]) -> str:
        """Get AI response from current provider"""
        try:
            if self.current_provider == ProviderType.FREE:
                return await self._get_free_response(messages)
            elif self.current_provider == ProviderType.OPENAI:
                return await self._get_openai_response(messages)
            elif self.current_provider == ProviderType.CLAUDE:
                return await self._get_claude_response(messages)
            elif self.current_provider == ProviderType.GEMINI:
                return await self._get_gemini_response(messages)
            elif self.current_provider == ProviderType.GROK:
                return await self._get_grok_response(messages)
            else:
                return "❌ Provedor não configurado."

        except Exception as e:
            logger.error(f"Error getting AI response: {e}")
            return "❌ Erro ao obter resposta da IA. Tente novamente."

    async def _get_free_response(self, messages: List[Dict[str, str]]) -> str:
        """Get response from free provider (g4f)"""
        try:
            import g4f
            from g4f.client import Client

            client = Client()

            # Convert messages format
            prompt = self._convert_messages_to_prompt(messages)

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error with free provider: {e}")
            return "❌ Erro no provedor gratuito. Verifique sua conexão."

    async def _get_openai_response(self, messages: List[Dict[str, str]]) -> str:
        """Get response from OpenAI"""
        try:
            import openai

            api_key = os.getenv("OPENAI_KEY")
            if not api_key:
                return "❌ Chave da OpenAI não configurada."

            client = openai.AsyncClient(api_key=api_key)

            response = await client.chat.completions.create(
                model=self.current_model.name,
                messages=messages,
                max_tokens=2000,
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error with OpenAI: {e}")
            return "❌ Erro ao conectar com OpenAI."

    async def _get_claude_response(self, messages: List[Dict[str, str]]) -> str:
        """Get response from Claude"""
        try:
            import anthropic

            api_key = os.getenv("CLAUDE_KEY")
            if not api_key:
                return "❌ Chave da Anthropic não configurada."

            client = anthropic.AsyncClient(api_key=api_key)

            # Convert format for Claude
            system_message = ""
            claude_messages = []

            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    claude_messages.append(msg)

            response = await client.messages.create(
                model=self.current_model.name,
                max_tokens=2000,
                system=system_message,
                messages=claude_messages
            )

            return response.content[0].text

        except Exception as e:
            logger.error(f"Error with Claude: {e}")
            return "❌ Erro ao conectar com Claude."

    async def _get_gemini_response(self, messages: List[Dict[str, str]]) -> str:
        """Get response from Gemini"""
        try:
            import google.generativeai as genai

            api_key = os.getenv("GEMINI_KEY")
            if not api_key:
                return "❌ Chave do Gemini não configurada."

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(self.current_model.name)

            # Convert messages to prompt
            prompt = self._convert_messages_to_prompt(messages)

            response = await model.generate_content_async(prompt)
            return response.text

        except Exception as e:
            logger.error(f"Error with Gemini: {e}")
            return "❌ Erro ao conectar com Gemini."

    async def _get_grok_response(self, messages: List[Dict[str, str]]) -> str:
        """Get response from Grok"""
        try:
            # Grok API implementation would go here
            # For now, fallback to free provider
            logger.warning("Grok provider not fully implemented, using free provider")
            return await self._get_free_response(messages)

        except Exception as e:
            logger.error(f"Error with Grok: {e}")
            return "❌ Erro ao conectar com Grok."

    def _convert_messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert messages to a single prompt string"""
        prompt_parts = []

        for message in messages:
            role = message["role"]
            content = message["content"]

            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")

        return "\n\n".join(prompt_parts)

    def get_provider_status(self) -> Dict[str, Any]:
        """Get status information about providers"""
        return {
            "current_provider": self.current_provider.value,
            "current_model": self.current_model.name,
            "available_providers": [p.value for p in self.available_providers],
            "models_count": len(self.models[self.current_provider])
        }