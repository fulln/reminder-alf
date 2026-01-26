"""
Tests for CommandRouter.
"""
import pytest
from src.workflow.command_router import CommandRouter
from src.workflow.input_handler import ParsedInput
from src.workflow.feedback_builder import FeedbackBuilder


@pytest.fixture
def command_router():
    return CommandRouter()


class TestCommandRouterBasics:
    """Test CommandRouter basics."""

    def test_router_starts_empty(self, command_router):
        """Test router starts with no handlers."""
        assert len(command_router.handlers) == 0

    def test_register_handler(self, command_router):
        """Test registering command handler."""

        def handler(parsed_input, feedback):
            return feedback.add_success("Handled")

        command_router.register("test", handler)
        assert command_router.has_handler("test")

    def test_register_multiple_handlers(self, command_router):
        """Test registering multiple handlers."""

        def handler(parsed_input, feedback):
            return feedback

        command_router.register("cmd1", handler)
        command_router.register("cmd2", handler)
        assert len(command_router.handlers) == 2

    def test_has_handler(self, command_router):
        """Test checking for handler."""

        def handler(parsed_input, feedback):
            return feedback

        command_router.register("test", handler)
        assert command_router.has_handler("test")
        assert not command_router.has_handler("missing")


class TestCommandRouterChaining:
    """Test method chaining."""

    def test_register_chaining(self, command_router):
        """Test register returns self for chaining."""

        def handler(parsed_input, feedback):
            return feedback

        result = command_router.register("cmd1", handler).register("cmd2", handler)
        assert result is command_router
        assert len(command_router.handlers) == 2

    def test_register_default_chaining(self, command_router):
        """Test register_default returns self."""

        def handler(parsed_input, feedback):
            return feedback

        result = command_router.register_default(handler)
        assert result is command_router


class TestCommandRouterRouting:
    """Test command routing."""

    def test_route_to_registered_handler(self, command_router):
        """Test routing to registered handler."""

        def handler(parsed_input, feedback):
            return feedback.add_success("Handled")

        command_router.register("test", handler)

        parsed = ParsedInput(command="test", args=["arg1"], raw_input="test arg1")
        result = command_router.route(parsed)

        assert len(result.items) == 1
        assert "✅" in result.items[0].title

    def test_route_case_insensitive(self, command_router):
        """Test routing is case-insensitive."""

        def handler(parsed_input, feedback):
            return feedback.add_success("Handled")

        command_router.register("test", handler)

        parsed = ParsedInput(command="TEST", args=[], raw_input="TEST")
        result = command_router.route(parsed)

        assert len(result.items) == 1

    def test_route_to_default_handler(self, command_router):
        """Test routing to default handler."""

        def default_handler(parsed_input, feedback):
            return feedback.add_info("Default handler")

        command_router.register_default(default_handler)

        parsed = ParsedInput(command="unknown", args=[], raw_input="unknown")
        result = command_router.route(parsed)

        assert "Default handler" in result.items[0].title

    def test_route_no_handler(self, command_router):
        """Test routing with no handler returns error."""
        parsed = ParsedInput(command="unknown", args=[], raw_input="unknown")
        result = command_router.route(parsed)

        assert result.items[0].valid is False
        assert "Unknown Command" in result.items[0].title

    def test_route_handler_exception(self, command_router):
        """Test handler exception is caught."""

        def failing_handler(parsed_input, feedback):
            raise ValueError("Test error")

        command_router.register("fail", failing_handler)

        parsed = ParsedInput(command="fail", args=[], raw_input="fail")
        result = command_router.route(parsed)

        assert result.items[0].valid is False
        assert "Command Failed" in result.items[0].title


class TestCommandRouterListing:
    """Test listing registered commands."""

    def test_get_registered_commands(self, command_router):
        """Test getting list of registered commands."""

        def handler(parsed_input, feedback):
            return feedback

        command_router.register("cmd1", handler)
        command_router.register("cmd2", handler)

        commands = command_router.get_registered_commands()
        assert "cmd1" in commands
        assert "cmd2" in commands
