"""
Tests for list and help handlers.
"""
import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from src.workflow.handlers.list_handler import handle_list_command
from src.workflow.handlers.help_handler import handle_help_command
from src.workflow.input_handler import ParsedInput
from src.workflow.feedback_builder import FeedbackBuilder


class TestListHandler:
    """Test list command handler."""

    def test_list_no_items(self):
        """Test list when no items tracked."""
        with patch('src.workflow.handlers.list_handler.TrackerService') as mock_ts:
            mock_ts.return_value.get_recent_items.return_value = []

            parsed = ParsedInput(
                command="list",
                args=[],
                raw_input="list"
            )
            feedback = FeedbackBuilder()

            result = handle_list_command(parsed, feedback)

            assert "No Items Tracked" in result.items[0].title

    def test_list_with_items(self):
        """Test list with tracked items."""
        with patch('src.workflow.handlers.list_handler.TrackerService') as mock_ts:
            mock_item = Mock()
            mock_item.title = "Test Event"
            mock_item.item_type = "calendar_event"
            mock_item.item_id = "event-123"
            mock_item.created_at = datetime(2026, 1, 27, 14, 0)
            mock_item.calendar_or_list = "Default"

            mock_ts.return_value.get_recent_items.return_value = [mock_item]

            parsed = ParsedInput(
                command="list",
                args=[],
                raw_input="list"
            )
            feedback = FeedbackBuilder()

            result = handle_list_command(parsed, feedback)

            # Should show items
            assert any("Test Event" in item.title for item in result.items)
            assert any("event-123" in item.subtitle for item in result.items)

    def test_list_with_custom_limit(self):
        """Test list with custom limit."""
        with patch('src.workflow.handlers.list_handler.TrackerService') as mock_ts:
            mock_ts.return_value.get_recent_items.return_value = []

            parsed = ParsedInput(
                command="list",
                args=["20"],
                raw_input="list 20"
            )
            feedback = FeedbackBuilder()

            result = handle_list_command(parsed, feedback)

            mock_ts.return_value.get_recent_items.assert_called_with(20)

    def test_list_shows_reminder_type(self):
        """Test list shows reminder items with correct icon."""
        with patch('src.workflow.handlers.list_handler.TrackerService') as mock_ts:
            mock_item = Mock()
            mock_item.title = "Buy milk"
            mock_item.item_type = "reminder"
            mock_item.item_id = "reminder-456"
            mock_item.created_at = datetime(2026, 1, 27, 14, 0)
            mock_item.calendar_or_list = "Inbox"

            mock_ts.return_value.get_recent_items.return_value = [mock_item]

            parsed = ParsedInput(
                command="list",
                args=[],
                raw_input="list"
            )
            feedback = FeedbackBuilder()

            result = handle_list_command(parsed, feedback)

            # Should show reminder item with 📋 icon
            assert any("📋" in item.subtitle for item in result.items)


class TestHelpHandler:
    """Test help command handler."""

    def test_help_shows_commands(self):
        """Test help shows available commands."""
        parsed = ParsedInput(
            command="help",
            args=[],
            raw_input="help"
        )
        feedback = FeedbackBuilder()

        result = handle_help_command(parsed, feedback)

        # Should have multiple items
        assert len(result.items) >= 5

    def test_help_shows_parse_command(self):
        """Test help includes parse command."""
        parsed = ParsedInput(
            command="help",
            args=[],
            raw_input="help"
        )
        feedback = FeedbackBuilder()

        result = handle_help_command(parsed, feedback)

        titles = [item.title for item in result.items]
        assert any("Parse" in title for title in titles)

    def test_help_shows_config_command(self):
        """Test help includes config command."""
        parsed = ParsedInput(
            command="help",
            args=[],
            raw_input="help"
        )
        feedback = FeedbackBuilder()

        result = handle_help_command(parsed, feedback)

        titles = [item.title for item in result.items]
        assert any("Configuration" in title or "Config" in title for title in titles)

    def test_help_shows_examples(self):
        """Test help includes usage examples."""
        parsed = ParsedInput(
            command="help",
            args=[],
            raw_input="help"
        )
        feedback = FeedbackBuilder()

        result = handle_help_command(parsed, feedback)

        # Should have examples section
        assert any("Examples" in item.title for item in result.items)
