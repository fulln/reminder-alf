"""
AIConfiguration data class for managing AI service settings.
"""
from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class AIConfiguration:
    """Configuration for AI services (OpenAI, DeepSeek, custom)."""

    provider: Literal["openai", "deepseek", "custom"]
    model: str
    api_key: str
    api_endpoint: str = "https://api.openai.com/v1"
    temperature: float = 0.7
    max_tokens: int = 131072
    timeout: int = 30
    organization_id: Optional[str] = None  # OpenAI-specific

    def validate(self) -> bool:
        """Validate configuration."""
        if self.provider not in ["openai", "deepseek", "custom"]:
            return False
        if not self.api_key:
            return False
        if not 0 <= self.temperature <= 2:
            return False
        if self.max_tokens < 1:
            return False
        if self.timeout < 1:
            return False
        return True

    def to_dict(self) -> dict:
        """Convert to dictionary (excluding sensitive data like API key)."""
        return {
            "provider": self.provider,
            "model": self.model,
            "api_endpoint": self.api_endpoint,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "timeout": self.timeout,
        }

    @classmethod
    def from_dict(cls, data: dict, api_key: str) -> "AIConfiguration":
        """Create from dictionary with API key from keyring."""
        provider = data["provider"]
        endpoint = data.get("api_endpoint", "https://api.openai.com/v1")
        
        if provider == "deepseek":
            if "api.openai.com" in endpoint:
                endpoint = "https://api.deepseek.com"
            elif endpoint.endswith("/v1"):
                endpoint = endpoint[:-3]

        return cls(
            provider=provider,
            model=data["model"],
            api_key=api_key,
            api_endpoint=endpoint,
            temperature=data.get("temperature", 0.7),
            max_tokens=data.get("max_tokens", 131072),
            timeout=data.get("timeout", 30),
            organization_id=data.get("organization_id"),
        )

    @classmethod
    def default_openai(cls, api_key: str) -> "AIConfiguration":
        """Create default OpenAI configuration."""
        return cls(
            provider="openai",
            model="gpt-4-turbo",
            api_key=api_key,
            api_endpoint="https://api.openai.com/v1",
        )

    @classmethod
    def default_deepseek(cls, api_key: str) -> "AIConfiguration":
        """Create default DeepSeek configuration."""
        return cls(
            provider="deepseek",
            model="deepseek-chat",
            api_key=api_key,
            api_endpoint="https://api.deepseek.com",
        )

