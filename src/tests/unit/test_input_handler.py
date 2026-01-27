"""
Tests for InputHandler.
"""
import pytest
from src.workflow.input_handler import InputHandler, ParsedInput


@pytest.fixture
def input_handler():
    return InputHandler()


class TestInputHandlerBasics:
    """Test basic input handling."""

    def test_parse_empty_input(self, input_handler):
        """Test parsing empty input defaults to help."""
        result = input_handler.parse("")
        assert result.command == "help"
        assert result.args == []

    def test_parse_whitespace_input(self, input_handler):
        """Test parsing whitespace-only input defaults to help."""
        result = input_handler.parse("   ")
        assert result.command == "help"
        assert result.args == []

    def test_parse_unknown_command_as_parse_text(self, input_handler):
        """Test unknown command is treated as parse text."""
        result = input_handler.parse("meeting tomorrow at 2pm")
        assert result.command == "parse"
        assert result.args == ["meeting tomorrow at 2pm"]

    def test_parse_valid_command(self, input_handler):
        """Test parsing valid command."""
        result = input_handler.parse("config openai")
        assert result.command == "config"
        assert result.args == ["openai"]

    def test_parse_command_case_insensitive(self, input_handler):
        """Test command parsing is case-insensitive."""
        result = input_handler.parse("CONFIG openai")
        assert result.command == "config"

    def test_parse_multiple_arguments(self, input_handler):
        """Test parsing multiple arguments."""
        result = input_handler.parse("delete item1 item2 item3")
        assert result.command == "delete"
        assert result.args == ["item1", "item2", "item3"]


class TestInputHandlerProperties:
    """Test ParsedInput properties."""

    def test_query_single_arg(self, input_handler):
        """Test query property with single argument."""
        result = input_handler.parse("parse meeting tomorrow")
        assert result.query == "meeting tomorrow"

    def test_query_multiple_args(self, input_handler):
        """Test query property with multiple arguments."""
        result = input_handler.parse("parse hello world test")
        assert result.query == "hello world test"

    def test_get_arg_valid_index(self, input_handler):
        """Test getting argument at valid index."""
        result = input_handler.parse("parse hello world test")
        assert result.get_arg(0) == "hello"
        assert result.get_arg(1) == "world"
        assert result.get_arg(2) == "test"

    def test_get_arg_invalid_index(self, input_handler):
        """Test getting argument at invalid index returns default."""
        result = input_handler.parse("parse hello")
        assert result.get_arg(5) is None
        assert result.get_arg(5, "default") == "default"

    def test_raw_input_preserved(self, input_handler):
        """Test raw input is preserved."""
        raw = "parse test input with spaces"
        result = input_handler.parse(raw)
        assert result.raw_input == raw


class TestCommandValidation:
    """Test command validation."""

    def test_is_valid_command_true(self, input_handler):
        """Test valid command returns True."""
        assert input_handler.is_valid_command("parse")
        assert input_handler.is_valid_command("config")
        assert input_handler.is_valid_command("delete")

    def test_is_valid_command_false(self, input_handler):
        """Test invalid command returns False."""
        assert not input_handler.is_valid_command("invalid")
        assert not input_handler.is_valid_command("unknown")

    def test_is_valid_command_case_insensitive(self, input_handler):
        """Test command validation is case-insensitive."""
        assert input_handler.is_valid_command("PARSE")
        assert input_handler.is_valid_command("Config")


class TestHelpText:
    """Test help text generation."""

    def test_get_help_all_commands(self, input_handler):
        """Test getting help for all commands."""
        help_text = input_handler.get_command_help()
        assert "parse" in help_text
        assert "config" in help_text
        assert "delete" in help_text

    def test_get_help_specific_command(self, input_handler):
        """Test getting help for specific command."""
        help_text = input_handler.get_command_help("parse")
        assert "parse" in help_text
