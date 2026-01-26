"""
CommandRouter for routing workflow commands to handlers.
"""
from typing import Callable, Dict, Optional, Any
from .input_handler import ParsedInput
from .feedback_builder import FeedbackBuilder
from ..utils.logger import get_logger

logger = get_logger(__name__)


CommandHandler = Callable[[ParsedInput, FeedbackBuilder], FeedbackBuilder]


class CommandRouter:
    """Routes workflow commands to appropriate handlers."""

    def __init__(self):
        """Initialize CommandRouter."""
        self.handlers: Dict[str, CommandHandler] = {}
        self.default_handler: Optional[CommandHandler] = None

    def register(self, command: str, handler: CommandHandler) -> "CommandRouter":
        """
        Register command handler.

        Args:
            command: Command name
            handler: Handler function

        Returns:
            Self for chaining
        """
        self.handlers[command] = handler
        logger.debug(f"Registered handler for command: {command}")
        return self

    def register_default(self, handler: CommandHandler) -> "CommandRouter":
        """
        Register default handler for unknown commands.

        Args:
            handler: Default handler function

        Returns:
            Self for chaining
        """
        self.default_handler = handler
        logger.debug("Registered default handler")
        return self

    def route(self, parsed_input: ParsedInput) -> FeedbackBuilder:
        """
        Route command to appropriate handler.

        Args:
            parsed_input: Parsed input from InputHandler

        Returns:
            FeedbackBuilder with response
        """
        command = parsed_input.command.lower()
        feedback = FeedbackBuilder()

        # Check for registered handler
        if command in self.handlers:
            try:
                logger.info(f"Routing to handler: {command}")
                return self.handlers[command](parsed_input, feedback)
            except Exception as e:
                logger.error(f"Handler error for {command}: {e}", exc_info=True)
                return feedback.add_error(
                    "Command Failed",
                    str(e),
                    "Check logs for details"
                )

        # Try default handler
        if self.default_handler:
            try:
                logger.info(f"Routing to default handler: {command}")
                return self.default_handler(parsed_input, feedback)
            except Exception as e:
                logger.error(f"Default handler error: {e}", exc_info=True)
                return feedback.add_error(
                    "Command Failed",
                    str(e),
                    "Check logs for details"
                )

        # No handler found
        logger.warning(f"No handler found for command: {command}")
        return feedback.add_error(
            "Unknown Command",
            f"No handler registered for: {command}",
            "Type 'help' for available commands"
        )

    def has_handler(self, command: str) -> bool:
        """
        Check if command has registered handler.

        Args:
            command: Command name

        Returns:
            True if handler exists
        """
        return command.lower() in self.handlers

    def get_registered_commands(self) -> list[str]:
        """
        Get list of registered commands.

        Returns:
            List of command names
        """
        return list(self.handlers.keys())
