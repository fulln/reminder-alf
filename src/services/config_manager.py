"""
ConfigManager for handling AI configuration and credentials.
"""
import os
import json
from pathlib import Path
from typing import Optional
import keyring
from ..models.ai_config import AIConfiguration
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ConfigManager:
    """Manages AI configuration and secure credential storage."""

    SERVICE_NAME = "reminder-alf"
    KEY_API_KEY = "api_key"

    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize ConfigManager.

        Args:
            config_dir: Directory for config files (defaults to ~/.config/reminder-alf)
        """
        if config_dir is None:
            # Use user config directory
            config_dir = Path.home() / ".config" / "reminder-alf"
        self.config_dir = config_dir
        self.config_file = config_dir / "config.json"
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def get_api_key(self, provider: str = "openai") -> Optional[str]:
        """
        Retrieve API key from keychain.

        Args:
            provider: Provider name (openai, anthropic, custom)

        Returns:
            API key or None if not found
        """
        try:
            key = keyring.get_password(self.SERVICE_NAME, f"{provider}_{self.KEY_API_KEY}")
            return key
        except Exception as e:
            logger.error(f"Failed to retrieve API key from keychain: {e}")
            return None

    def set_api_key(self, api_key: str, provider: str = "openai") -> bool:
        """
        Store API key securely in keychain.

        Args:
            api_key: API key to store
            provider: Provider name

        Returns:
            True if successful
        """
        try:
            keyring.set_password(self.SERVICE_NAME, f"{provider}_{self.KEY_API_KEY}", api_key)
            logger.info(f"API key stored successfully for {provider}")
            return True
        except Exception as e:
            logger.error(f"Failed to store API key in keychain: {e}")
            return False

    def delete_api_key(self, provider: str = "openai") -> bool:
        """
        Delete API key from keychain.

        Args:
            provider: Provider name

        Returns:
            True if successful
        """
        try:
            keyring.delete_password(self.SERVICE_NAME, f"{provider}_{self.KEY_API_KEY}")
            return True
        except keyring.errors.PasswordDeleteError:
            return False
        except Exception as e:
            logger.error(f"Failed to delete API key: {e}")
            return False

    def get_configuration(self) -> Optional[AIConfiguration]:
        """
        Load AI configuration from file and keychain.

        Returns:
            AIConfiguration or None if not configured
        """
        if not self.config_file.exists():
            return None

        try:
            with open(self.config_file, "r") as f:
                config_data = json.load(f)

            provider = config_data.get("provider", "openai")
            api_key = self.get_api_key(provider)

            if not api_key:
                logger.warning(f"No API key found for {provider}")
                return None

            return AIConfiguration.from_dict(config_data, api_key)
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            return None

    def save_configuration(self, config: AIConfiguration) -> bool:
        """
        Save AI configuration to file and keychain.

        Args:
            config: AIConfiguration to save

        Returns:
            True if successful
        """
        try:
            # Save API key to keychain
            if not self.set_api_key(config.api_key, config.provider):
                return False

            # Save config to file (without API key)
            config_data = config.to_dict()
            with open(self.config_file, "w") as f:
                json.dump(config_data, f, indent=2)

            logger.info("Configuration saved successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            return False

    def get_endpoint_url(self, provider: str = "openai") -> str:
        """
        Get API endpoint URL from environment variable or default.

        Args:
            provider: Provider name

        Returns:
            API endpoint URL
        """
        env_key = f"REMINDER_ALF_{provider.upper()}_ENDPOINT"

        # 默认端点
        defaults = {
            "openai": "https://api.openai.com/v1",
            "deepseek": "https://api.deepseek.com/v1",
        }

        return os.environ.get(env_key, defaults.get(provider, "https://api.openai.com/v1"))

    def set_endpoint_url(self, url: str, provider: str = "openai") -> bool:
        """
        Set API endpoint URL in configuration.

        Args:
            url: Endpoint URL
            provider: Provider name

        Returns:
            True if successful
        """
        try:
            config = self.get_configuration()
            if config:
                config.api_endpoint = url
                return self.save_configuration(config)
            return False
        except Exception as e:
            logger.error(f"Failed to set endpoint URL: {e}")
            return False

    def validate_credentials(self, config: AIConfiguration) -> tuple[bool, Optional[str]]:
        """
        Validate credentials by making a test API call.

        Args:
            config: Configuration to validate

        Returns:
            (is_valid, error_message)
        """
        # TODO: Implement actual API validation call
        # For now, just check basic validity
        if not config.validate():
            return False, "Invalid configuration"

        if not config.api_key:
            return False, "API key is missing"

        return True, None

    def is_configured(self) -> bool:
        """Check if workflow is configured."""
        config = self.get_configuration()
        return config is not None and config.validate()
