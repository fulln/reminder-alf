"""
Configuration workflow handler for Alfred.
"""
from ..input_handler import ParsedInput
from ..feedback_builder import FeedbackBuilder
from ...services.config_manager import ConfigManager
from ...models.ai_config import AIConfiguration
from ...utils.logger import get_logger

logger = get_logger(__name__)


def handle_config_command(parsed_input: ParsedInput, feedback: FeedbackBuilder) -> FeedbackBuilder:
    """
    Handle configuration commands.

    Args:
        parsed_input: Parsed user input
        feedback: Feedback builder for response

    Returns:
        Updated feedback builder
    """
    config_manager = ConfigManager()

    # Show current status
    if not parsed_input.args or parsed_input.args[0] == "status":
        if config_manager.is_configured():
            config = config_manager.get_configuration()
            if config:
                return feedback.add_success(
                    "✅ Configured",
                    f"Provider: {config.provider}\nModel: {config.model}"
                )
        return feedback.add_warning(
            "⚠️ Not Configured",
            "Run 'rem config set <provider> <api_key>' to configure"
        )

    # Set API key
    if parsed_input.args[0] == "set":
        if len(parsed_input.args) < 3:
            return feedback.add_error(
                "Missing Arguments",
                "Usage: ral config set <provider> <api_key> [model]",
                "Example: ral config set deepseek sk-... deepseek-chat"
            )

        provider = parsed_input.args[1]
        api_key = parsed_input.args[2]
        model = parsed_input.args[3] if len(parsed_input.args) > 3 else None

        # Set default model based on provider
        if not model:
            if provider == "openai":
                model = "gpt-4"
            elif provider == "deepseek":
                model = "deepseek-chat"
            else:
                model = "gpt-4"

        # Create configuration with correct endpoint
        config = AIConfiguration(
            provider=provider,
            model=model,
            api_key=api_key,
        )

        # Set correct endpoint based on provider
        if provider == "deepseek":
            config.api_endpoint = "https://api.deepseek.com/v1"
        elif provider == "openai":
            config.api_endpoint = "https://api.openai.com/v1"

        # Validate
        is_valid, error_msg = config_manager.validate_credentials(config)
        if not is_valid:
            return feedback.add_error(
                "Invalid Configuration",
                error_msg or "Configuration validation failed"
            )

        # Save
        if config_manager.save_configuration(config):
            return feedback.add_success(
                "Configuration Saved",
                f"Provider: {provider}\nModel: {model}"
            )
        else:
            return feedback.add_error(
                "Save Failed",
                "Could not save configuration"
            )

    # Delete API key
    if parsed_input.args[0] == "delete":
        provider = parsed_input.args[1] if len(parsed_input.args) > 1 else "openai"
        if config_manager.delete_api_key(provider):
            return feedback.add_success("Configuration Deleted")
        else:
            return feedback.add_warning("No configuration found to delete")

    # Invalid subcommand
    return feedback.add_error(
        "Unknown Config Command",
        f"Unknown command: {parsed_input.args[0]}",
        "Valid commands: status, set, delete"
    )
