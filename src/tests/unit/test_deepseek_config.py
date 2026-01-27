
import pytest
from unittest.mock import Mock, patch
from src.workflow.handlers.config_handler import handle_config_command
from src.workflow.input_handler import ParsedInput
from src.workflow.feedback_builder import FeedbackBuilder

def test_deepseek_endpoint_configuration():
    """Test that setting deepseek provider sets the correct endpoint."""
    with patch('src.workflow.handlers.config_handler.ConfigManager') as mock_cm_cls:
        mock_cm = mock_cm_cls.return_value
        mock_cm.validate_credentials.return_value = (True, None)
        mock_cm.save_configuration.return_value = True

        parsed = ParsedInput(
            command="config",
            args=["set", "deepseek", "sk-test", "deepseek-chat"],
            raw_input="config set deepseek sk-test deepseek-chat"
        )
        feedback = FeedbackBuilder()

        handle_config_command(parsed, feedback)

        # Verify save_configuration was called
        assert mock_cm.save_configuration.called
        
        # Get the config object passed to save_configuration
        config = mock_cm.save_configuration.call_args[0][0]
        
        assert config.provider == "deepseek"
        assert config.api_endpoint == "https://api.deepseek.com"
