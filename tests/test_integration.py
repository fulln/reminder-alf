"""
Integration tests for end-to-end workflow.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from src.workflow.input_handler import InputHandler
from src.workflow.command_router import CommandRouter
from src.workflow.handlers import (
    handle_parse_command,
    handle_config_command,
    handle_delete_command,
    handle_list_command,
    handle_help_command,
)
from src.workflow.feedback_builder import FeedbackBuilder
from src.models.parse_result import ParseResult
from src.models.calendar_event import CalendarEvent
from src.models.reminder import Reminder


class TestWorkflowIntegration:
    """Integration tests for complete workflow."""

    def test_full_parse_workflow(self):
        """Test complete workflow: input parsing -> command routing -> handler execution."""
        # Step 1: Parse input
        input_handler = InputHandler()
        parsed = input_handler.parse("meeting tomorrow at 2pm")

        assert parsed.command == "parse"
        assert parsed.query == "meeting tomorrow at 2pm"

        # Step 2: Route command
        command_router = CommandRouter()
        command_router.register("parse", handle_parse_command)

        with patch('src.workflow.handlers.parse_handler.ConfigManager') as mock_cm:
            with patch('src.workflow.handlers.parse_handler.ParseService') as mock_ps:
                with patch('src.workflow.handlers.parse_handler.EventKitBridge'):

                    mock_config = Mock()
                    mock_cm.return_value.get_configuration.return_value = mock_config

                    parse_result = ParseResult(
                        calendar_events=[
                            CalendarEvent(
                                title="Meeting",
                                start_date=datetime(2026, 1, 28, 14, 0),
                                end_date=datetime(2026, 1, 28, 15, 0)
                            )
                        ],
                        reminders=[],
                        raw_text="meeting tomorrow at 2pm"
                    )
                    mock_ps.return_value.parse_input.return_value = parse_result
                    mock_ps.return_value.create_items_from_parse.return_value = (1, 0, [])

                    feedback = FeedbackBuilder()
                    result = command_router.route(parsed)

                    # Should have created event
                    assert len(result.items) > 0

    def test_config_workflow(self):
        """Test configuration workflow."""
        input_handler = InputHandler()
        parsed = input_handler.parse("config status")

        assert parsed.command == "config"

        with patch('src.workflow.handlers.config_handler.ConfigManager') as mock_cm:
            mock_config = Mock()
            mock_config.provider = "openai"
            mock_config.model = "gpt-4"

            mock_cm.return_value.is_configured.return_value = True
            mock_cm.return_value.get_configuration.return_value = mock_config

            feedback = FeedbackBuilder()
            result = handle_config_command(parsed, feedback)

            assert "✅" in result.items[0].title

    def test_delete_workflow(self):
        """Test delete workflow."""
        input_handler = InputHandler()
        parsed = input_handler.parse("delete event-123")

        assert parsed.command == "delete"
        assert parsed.args[0] == "event-123"

        with patch('src.workflow.handlers.delete_handler.EventKitBridge'):
            with patch('src.workflow.handlers.delete_handler.ParseService') as mock_ps:

                mock_ps.return_value.delete_tracked_item.return_value = (True, None)

                feedback = FeedbackBuilder()
                result = handle_delete_command(parsed, feedback)

                assert "✅" in result.items[0].title

    def test_list_workflow(self):
        """Test list workflow."""
        input_handler = InputHandler()
        parsed = input_handler.parse("list 5")

        assert parsed.command == "list"

        with patch('src.workflow.handlers.list_handler.TrackerService') as mock_ts:
            mock_item = Mock()
            mock_item.title = "Test Event"
            mock_item.item_type = "calendar_event"
            mock_item.item_id = "event-123"
            mock_item.created_at = datetime.now()
            mock_item.calendar_or_list = "Default"

            mock_ts.return_value.get_recent_items.return_value = [mock_item]

            feedback = FeedbackBuilder()
            result = handle_list_command(parsed, feedback)

            # Should show items
            assert any("Test Event" in item.title for item in result.items)

    def test_help_workflow(self):
        """Test help command."""
        input_handler = InputHandler()
        parsed = input_handler.parse("help")

        assert parsed.command == "help"

        feedback = FeedbackBuilder()
        result = handle_help_command(parsed, feedback)

        # Should show help items
        assert len(result.items) > 0
        assert any("help" in item.title.lower() for item in result.items)

    def test_unknown_command_defaults_to_parse(self):
        """Test that unknown commands default to parse."""
        input_handler = InputHandler()
        parsed = input_handler.parse("arbitrary text here")

        assert parsed.command == "parse"
        assert parsed.query == "arbitrary text here"

    def test_chinese_input_workflow(self):
        """Test Chinese language input."""
        input_handler = InputHandler()
        parsed = input_handler.parse("明天下午3点开会")

        assert parsed.command == "parse"
        assert "明天下午3点开会" in parsed.raw_input

    def test_command_with_arguments(self):
        """Test command with multiple arguments."""
        input_handler = InputHandler()
        parsed = input_handler.parse("config set openai sk-test gpt-4")

        assert parsed.command == "config"
        assert parsed.args[0] == "set"
        assert parsed.args[1] == "openai"
        assert "sk-test" in parsed.args[2]

    def test_delete_old_with_days(self):
        """Test delete old command with custom days."""
        input_handler = InputHandler()
        parsed = input_handler.parse("delete old 30")

        assert parsed.command == "delete"
        assert parsed.args[0] == "old"
        assert parsed.args[1] == "30"


class TestCommandRouterIntegration:
    """Integration tests for command router."""

    def test_router_executes_multiple_commands(self):
        """Test router can handle multiple command types."""
        router = CommandRouter()

        command_results = []

        def mock_handler1(pi, fb):
            command_results.append("handler1")
            return fb.add_success("Handler 1")

        def mock_handler2(pi, fb):
            command_results.append("handler2")
            return fb.add_success("Handler 2")

        router.register("cmd1", mock_handler1)
        router.register("cmd2", mock_handler2)

        from src.workflow.input_handler import ParsedInput

        result1 = router.route(ParsedInput(command="cmd1", args=[], raw_input="cmd1"))
        result2 = router.route(ParsedInput(command="cmd2", args=[], raw_input="cmd2"))

        assert "Handler 1" in result1.items[0].title
        assert "Handler 2" in result2.items[0].title
        assert len(command_results) == 2


class TestErrorHandling:
    """Integration tests for error handling."""

    def test_missing_configuration_error(self):
        """Test handling of missing configuration."""
        with patch('src.workflow.handlers.parse_handler.ConfigManager') as mock_cm:
            mock_cm.return_value.get_configuration.return_value = None

            from src.workflow.input_handler import ParsedInput
            parsed = ParsedInput(command="parse", args=["test"], raw_input="parse test")
            feedback = FeedbackBuilder()

            result = handle_parse_command(parsed, feedback)

            assert result.items[0].valid is False
            assert "Not Configured" in result.items[0].title

    def test_invalid_command_error(self):
        """Test handling of invalid commands."""
        input_handler = InputHandler()
        parsed = input_handler.parse("nonexistent_command")

        router = CommandRouter()
        # Don't register any handlers, so it will use default
        router.register_default(handle_help_command)

        result = router.route(parsed)

        # Should still return valid feedback (help)
        assert len(result.items) > 0

    def test_handler_exception_caught(self):
        """Test that exceptions in handlers are caught gracefully."""
        router = CommandRouter()

        def failing_handler(pi, fb):
            raise RuntimeError("Intentional test error")

        router.register("fail", failing_handler)

        from src.workflow.input_handler import ParsedInput
        parsed = ParsedInput(command="fail", args=[], raw_input="fail")

        result = router.route(parsed)

        # Should have error feedback
        assert result.items[0].valid is False
        assert "Command Failed" in result.items[0].title
