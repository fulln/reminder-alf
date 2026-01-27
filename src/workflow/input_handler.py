"""
InputHandler for parsing Alfred workflow input.
"""
from dataclasses import dataclass
from typing import Optional, List
from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class ParsedInput:
    """Parsed Alfred input with command and arguments."""

    command: str
    args: List[str]
    raw_input: str

    @property
    def query(self) -> str:
        """Get full query text (all args joined)."""
        return " ".join(self.args)

    def get_arg(self, index: int, default: Optional[str] = None) -> Optional[str]:
        """
        Get argument at index.

        Args:
            index: Argument position (0-based)
            default: Default value if not found

        Returns:
            Argument value or default
        """
        if 0 <= index < len(self.args):
            return self.args[index]
        return default


class InputHandler:
    """Handles parsing of Alfred workflow input."""

    COMMAND_PREFIX = "ral"  # ral parse, ral config, ral delete, etc.

    def __init__(self):
        """Initialize InputHandler."""
        self.valid_commands = {
            "parse": "Parse natural language text",
            "config": "Manage AI configuration",
            "delete": "Delete tracked items",
            "list": "List tracked items",
            "clean": "Cleanup unexecuted tagged items",
            "help": "Show help",
        }

    def parse(self, raw_input: str) -> ParsedInput:
        """
        Parse Alfred input into command and arguments.

        Args:
            raw_input: Raw input from Alfred

        Returns:
            ParsedInput object
        """
        if not raw_input or not raw_input.strip():
            return ParsedInput(command="help", args=[], raw_input=raw_input)

        parts = raw_input.strip().split(maxsplit=1)

        # If input doesn't start with command, treat as parse command
        command = parts[0].lower()
        if command not in self.valid_commands:
            # Treat entire input as text to parse
            return ParsedInput(
                command="parse",
                args=[raw_input.strip()],
                raw_input=raw_input
            )

        # Extract arguments
        args = parts[1].split() if len(parts) > 1 else []

        logger.debug(f"Parsed input: command={command}, args={args}")

        return ParsedInput(
            command=command,
            args=args,
            raw_input=raw_input
        )

    def is_valid_command(self, command: str) -> bool:
        """
        Check if command is valid.

        Args:
            command: Command name

        Returns:
            True if valid
        """
        return command.lower() in self.valid_commands

    def get_command_help(self, command: Optional[str] = None) -> str:
        """
        Get help text for command.

        Args:
            command: Specific command or None for all

        Returns:
            Help text
        """
        if command and command in self.valid_commands:
            return f"{command}: {self.valid_commands[command]}"

        # Return all commands
        help_lines = ["Available commands:"]
        for cmd, desc in self.valid_commands.items():
            help_lines.append(f"  {cmd}: {desc}")

        return "\n".join(help_lines)
