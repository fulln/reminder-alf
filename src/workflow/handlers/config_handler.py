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
                    f"Provider: {config.provider}\nModel: {config.model}\nTokens: {config.max_tokens}\nTimeout: {config.timeout}s"
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
        endpoint = parsed_input.args[4] if len(parsed_input.args) > 4 else None

        # Set default model based on provider
        if not model:
            if provider == "openai":
                model = "gpt-4"
            elif provider == "deepseek":
                model = "deepseek-chat"
            else:
                model = "gpt-4"

        # Determine endpoint
        if not endpoint:
            # If no explicit endpoint given
            if provider == "deepseek":
                endpoint = "https://api.deepseek.com"
            elif provider == "openai":
                endpoint = "https://api.openai.com/v1"
            elif provider == "custom":
                # For custom, try to preserve existing endpoint if available
                existing_config = config_manager.get_configuration()
                if existing_config:
                    endpoint = existing_config.api_endpoint
                else:
                    endpoint = "https://api.openai.com/v1"  # Fallback default
        
        # Create configuration
        config = AIConfiguration(
            provider=provider,
            model=model,
            api_key=api_key,
            api_endpoint=endpoint
        )

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

    # Set Endpoint URL
    if parsed_input.args[0] == "endpoint":
        if len(parsed_input.args) < 2:
            return feedback.add_error(
                "Missing Arguments",
                "Usage: ral config endpoint <url>",
                "Example: ral config endpoint https://api.deepseek.com"
            )
        
        url = parsed_input.args[1]
        config = config_manager.get_configuration()
        if config:
            config.api_endpoint = url
            if config_manager.save_configuration(config):
                return feedback.add_success("Endpoint Updated", f"URL: {url}")
        return feedback.add_error("Update Failed", "Could not save configuration")

    # Set Timeout
    if parsed_input.args[0] == "timeout":
        if len(parsed_input.args) < 2:
            return feedback.add_error(
                "Missing Arguments", 
                "Usage: ral config timeout <seconds>"
            )
            
        try:
            timeout = int(parsed_input.args[1])
            config = config_manager.get_configuration()
            if config:
                config.timeout = timeout
                if config_manager.save_configuration(config):
                    return feedback.add_success("Timeout Updated", f"Timeout: {timeout} seconds")
        except ValueError:
            return feedback.add_error("Invalid Value", "Timeout must be a number")
        return feedback.add_error("Update Failed", "Could not save configuration")

    # Set Max Tokens
    if parsed_input.args[0] in ["tokens", "max_tokens"]:
        if len(parsed_input.args) < 2:
            return feedback.add_error(
                "Missing Arguments", 
                "Usage: ral config tokens <number>"
            )
            
        try:
            tokens = int(parsed_input.args[1])
            config = config_manager.get_configuration()
            if config:
                config.max_tokens = tokens
                if config_manager.save_configuration(config):
                    return feedback.add_success("Tokens Updated", f"Max Tokens: {tokens}")
        except ValueError:
            return feedback.add_error("Invalid Value", "Tokens must be a number")
        return feedback.add_error("Update Failed", "Could not save configuration")

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
