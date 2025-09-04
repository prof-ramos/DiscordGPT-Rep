import pytest
from unittest.mock import Mock, patch, AsyncMock
import os
from src.art import get_random_art, draw


class TestArtModule:
    """Test cases for the art module"""

    def test_get_random_art(self):
        """Test that get_random_art returns ASCII art"""
        art = get_random_art()

        # Should contain ASCII art
        assert isinstance(art, str)
        assert len(art) > 100  # Should be substantial ASCII art

        # Should contain expected text
        assert "DiscordGPT" in art
        assert "Prof. Ramos" in art

    @pytest.mark.asyncio
    async def test_draw_with_openai_enabled(self):
        """Test image drawing with OpenAI enabled"""
        with patch.dict(os.environ, {
            "OPENAI_ENABLED": "True",
            "OPENAI_KEY": "test-key"
        }):
            mock_response = Mock()
            mock_response.data = [Mock()]
            mock_response.data[0].url = "https://example.com/image.png"

            # Patch the module-level openai_client object directly
            with patch('src.art.openai_client') as mock_client:
                mock_client.images.generate = AsyncMock(return_value=mock_response)
                result = await draw("openai", "A beautiful sunset")

                assert result == "https://example.com/image.png"

    @pytest.mark.asyncio
    async def test_draw_with_g4f_provider(self):
        """Test image drawing with g4f provider"""
        with patch.dict(os.environ, {
            "OPENAI_ENABLED": "False"
        }):
            mock_response = Mock()
            mock_response.data = [Mock()]
            mock_response.data[0].url = "https://example.com/g4f-image.png"

            with patch('src.art.AsyncClient') as mock_client_class:
                mock_client = Mock()
                mock_client.images.generate = AsyncMock(return_value=mock_response)
                mock_client_class.return_value = mock_client

                result = await draw("Gemini", "A beautiful sunset")

                assert result == "https://example.com/g4f-image.png"

    def test_get_image_provider(self):
        """Test provider selection"""
        from src.art import get_image_provider

        # Test known providers
        assert get_image_provider("Gemini") is not None
        assert get_image_provider("openai") is not None

        # Test unknown provider (should return default)
        assert get_image_provider("unknown") is not None

    @pytest.mark.asyncio
    async def test_draw_error_handling(self):
        """Test error handling in draw function"""
        with patch.dict(os.environ, {
            "OPENAI_ENABLED": "True",
            "OPENAI_KEY": "test-key"
        }):
            with patch('src.art.openai_client') as mock_client:
                mock_client.images.generate = AsyncMock(side_effect=Exception("API Error"))
                with pytest.raises(Exception):
                    await draw("openai", "Test prompt")
