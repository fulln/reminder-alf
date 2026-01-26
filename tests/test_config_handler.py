"""
Tests for config handler.
"""
import pytest
from unittest.mock import Mock, patch
from src.workflow.handlers.config_handler import handle_config_command
from src.workflow.input_handler import ParsedInput
from src.workflow.feedback_builder import FeedbackBuilder


class TestConfigHandlerStatus:
    """Test config status command."""

    def test_status_not_configured(self):
        """Test status when not configured."""
        with patch('src.workflow.handlers.config_handler.ConfigManager') as mock_cm:
            mock_cm.return_value.is_configured.return_value = False

            parsed = ParsedInput(
                command="config",
                args=[],
                raw_input="config"
            )
            feedback = FeedbackBuilder()

            result = handle_config_command(parsed, feedback)

            assert "Not Configured" in result.items[0].title

    def test_status_configured(self):
        """Test status when configured."""
        with patch('src.workflow.handlers.config_handler.ConfigManager') as mock_cm:
            mock_config = Mock()
            mock_config.provider = "openai"
            mock_config.model = "gpt-4"

            mock_cm.return_value.is_configured.return_value = True
            mock_cm.return_value.get_configuration.return_value = mock_config

            parsed = ParsedInput(
                command="config",
                args=["status"],
                raw_input="config status"
            )
            feedback = FeedbackBuilder()

            result = handle_config_command(parsed, feedback)

            assert "✅" in result.items[0].title


class TestConfigHandlerSet:
    """Test config set command."""

    def test_set_missing_args(self):
        """Test set with missing arguments."""
        with patch('src.workflow.handlers.config_handler.ConfigManager'):
            parsed = ParsedInput(
                command="config",
                args=["set", "openai"],
                raw_input="config set openai"
            )
            feedback = FeedbackBuilder()

            result = handle_config_command(parsed, feedback)

            assert result.items[0].valid is False
            assert "Missing Arguments" in result.items[0].title

    def test_set_invalid_config(self):
        """Test set with invalid configuration."""
        with patch('src.workflow.handlers.config_handler.ConfigManager') as mock_cm:
            mock_cm.return_value.validate_credentials.return_value = (
                False,
                "Invalid API key"
            )

            parsed = ParsedInput(
                command="config",
                args=["set", "openai", "invalid-key"],
                raw_input="config set openai invalid-key"
            )
            feedback = FeedbackBuilder()

            result = handle_config_command(parsed, feedback)

            assert "Invalid Configuration" in result.items[0].title

    def test_set_successful(self):
        """Test successful config set."""
        with patch('src.workflow.handlers.config_handler.ConfigManager') as mock_cm:
            mock_cm.return_value.validate_credentials.return_value = (True, None)
            mock_cm.return_value.save_configuration.return_value = True

            parsed = ParsedInput(
                command="config",
                args=["set", "openai", "sk-valid-key", "gpt-4"],
                raw_input="config set openai sk-valid-key gpt-4"
            )
            feedback = FeedbackBuilder()

            result = handle_config_command(parsed, feedback)

            assert "✅" in result.items[0].title


class TestConfigHandlerDelete:
    """Test config delete command."""

    def test_delete_successful(self):
        """Test successful config deletion."""
        with patch('src.workflow.handlers.config_handler.ConfigManager') as mock_cm:
            mock_cm.return_value.delete_api_key.return_value = True

            parsed = ParsedInput(
                command="config",
                args=["delete"],
                raw_input="config delete"
            )
            feedback = FeedbackBuilder()

            result = handle_config_command(parsed, feedback)

            assert "✅" in result.items[0].title

    def test_delete_not_found(self):
        """Test delete when no config exists."""
        with patch('src.workflow.handlers.config_handler.ConfigManager') as mock_cm:
            mock_cm.return_value.delete_api_key.return_value = False

            parsed = ParsedInput(
                command="config",
                args=["delete"],
                raw_input="config delete"
            )
            feedback = FeedbackBuilder()

            result = handle_config_command(parsed, feedback)

            assert "⚠️" in result.items[0].title
