"""
Tests for parse handler.
"""
import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from src.workflow.handlers.parse_handler import handle_parse_command
from src.workflow.input_handler import ParsedInput
from src.workflow.feedback_builder import FeedbackBuilder
from src.models.parse_result import ParseResult
from src.models.calendar_event import CalendarEvent
from src.models.reminder import Reminder


class TestParseHandlerBasics:
    """Test parse handler basics."""

    def test_handler_no_config(self):
        """Test handler when not configured."""
        with patch('src.workflow.handlers.parse_handler.ConfigManager') as mock_cm:
            mock_cm.return_value.get_configuration.return_value = None

            parsed = ParsedInput(
                command="parse",
                args=["meeting"],
                raw_input="parse meeting"
            )
            feedback = FeedbackBuilder()

            result = handle_parse_command(parsed, feedback)

            assert result.items[0].valid is False
            assert "Not Configured" in result.items[0].title

    def test_handler_no_input(self):
        """Test handler with no input text."""
        with patch('src.workflow.handlers.parse_handler.ConfigManager') as mock_cm:
            mock_config = Mock()
            mock_cm.return_value.get_configuration.return_value = mock_config

            parsed = ParsedInput(
                command="parse",
                args=[],
                raw_input="parse"
            )
            feedback = FeedbackBuilder()

            result = handle_parse_command(parsed, feedback)

            assert result.items[0].valid is False
            assert "No Input" in result.items[0].title


class TestParseHandlerSuccess:
    """Test successful parse operations."""

    def test_parse_successful(self):
        """Test successful parsing and creation."""
        with patch('src.workflow.handlers.parse_handler.ConfigManager') as mock_cm:
            with patch('src.workflow.handlers.parse_handler.ParseService') as mock_ps:
                with patch('src.workflow.handlers.parse_handler.EventKitBridge') as mock_eb:

                    # Setup mocks
                    mock_config = Mock()
                    mock_cm.return_value.get_configuration.return_value = mock_config

                    parse_result = ParseResult(
                        calendar_events=[
                            CalendarEvent(
                                title="Meeting",
                                start_date=datetime(2026, 1, 27, 14, 0),
                                end_date=datetime(2026, 1, 27, 15, 0)
                            )
                        ],
                        reminders=[],
                        raw_text="meeting tomorrow at 2pm"
                    )
                    mock_ps.return_value.parse_input.return_value = parse_result
                    mock_ps.return_value.create_items_from_parse.return_value = (1, 0, [])

                    parsed = ParsedInput(
                        command="parse",
                        args=["meeting tomorrow"],
                        raw_input="parse meeting tomorrow"
                    )
                    feedback = FeedbackBuilder()

                    result = handle_parse_command(parsed, feedback)

                    # Should have created event feedback
                    titles = [item.title for item in result.items]
                    assert any("Meeting" in title for title in titles)

    def test_parse_with_ambiguities(self):
        """Test parse result with ambiguities."""
        with patch('src.workflow.handlers.parse_handler.ConfigManager') as mock_cm:
            with patch('src.workflow.handlers.parse_handler.ParseService') as mock_ps:
                with patch('src.workflow.handlers.parse_handler.EventKitBridge'):

                    mock_config = Mock()
                    mock_cm.return_value.get_configuration.return_value = mock_config

                    parse_result = ParseResult(
                        calendar_events=[],
                        reminders=[],
                        raw_text="meeting",
                        ambiguities=["Time not specified"]
                    )
                    mock_ps.return_value.parse_input.return_value = parse_result
                    mock_ps.return_value.create_items_from_parse.return_value = (0, 0, [])

                    parsed = ParsedInput(
                        command="parse",
                        args=["meeting"],
                        raw_input="parse meeting"
                    )
                    feedback = FeedbackBuilder()

                    result = handle_parse_command(parsed, feedback)

                    # Should show warning about empty result
                    assert any("no items" in item.title.lower() for item in result.items)


class TestParseHandlerErrors:
    """Test error handling."""

    def test_parse_error(self):
        """Test parse error handling."""
        with patch('src.workflow.handlers.parse_handler.ConfigManager') as mock_cm:
            with patch('src.workflow.handlers.parse_handler.ParseService') as mock_ps:

                mock_config = Mock()
                mock_cm.return_value.get_configuration.return_value = mock_config

                parse_result = ParseResult.error("Parse failed", "test input")
                mock_ps.return_value.parse_input.return_value = parse_result

                parsed = ParsedInput(
                    command="parse",
                    args=["test"],
                    raw_input="parse test"
                )
                feedback = FeedbackBuilder()

                result = handle_parse_command(parsed, feedback)

                assert result.items[0].valid is False
                assert "Parse Failed" in result.items[0].title
