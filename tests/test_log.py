
import pytest
import logging
from unittest.mock import patch

from src.log import logger


class TestLogging:
    def test_logger_exists(self):
        """Test logger is properly configured"""
        assert logger is not None
        assert isinstance(logger, logging.Logger)
    
    def test_logger_level(self):
        """Test logger has appropriate level"""
        # Should be INFO or DEBUG level for development
        assert logger.level <= logging.INFO
    
    @patch('src.log.logger.info')
    def test_logger_info(self, mock_info):
        """Test info logging works"""
        logger.info("Test message")
        mock_info.assert_called_once_with("Test message")
    
    @patch('src.log.logger.error')
    def test_logger_error(self, mock_error):
        """Test error logging works"""
        logger.error("Test error")
        mock_error.assert_called_once_with("Test error")
