"""
Tests for delete handler.
"""
import pytest
from unittest.mock import Mock, patch
from src.workflow.handlers.delete_handler import handle_delete_command
from src.workflow.input_handler import ParsedInput
from src.workflow.feedback_builder import FeedbackBuilder


class TestDeleteHandlerList:
    """Test listing items for deletion."""

    def test_list_no_items(self):
        """Test listing when no items tracked."""
        with patch('src.workflow.handlers.delete_handler.TrackerService') as mock_ts:
            mock_ts.return_value.get_recent_items.return_value = []

            parsed = ParsedInput(
                command="delete",
                args=[],
                raw_input="delete"
            )
            feedback = FeedbackBuilder()

            result = handle_delete_command(parsed, feedback)

            assert "No Items Tracked" in result.items[0].title

    def test_list_with_items(self):
        """Test listing tracked items."""
        with patch('src.workflow.handlers.delete_handler.TrackerService') as mock_ts:
            mock_item = Mock()
            mock_item.title = "Test Event"
            mock_item.item_type = "calendar_event"
            mock_item.item_id = "event-123"
            mock_item.created_at = Mock()
            mock_item.created_at.strftime = Mock(return_value="Jan 27")

            mock_ts.return_value.get_recent_items.return_value = [mock_item]

            parsed = ParsedInput(
                command="delete",
                args=[],
                raw_input="delete"
            )
            feedback = FeedbackBuilder()

            result = handle_delete_command(parsed, feedback)

            # Should show items to delete
            assert len(result.items) >= 2


class TestDeleteHandlerSingle:
    """Test deleting single items."""

    def test_delete_specific_item(self):
        """Test deleting specific item by ID."""
        with patch('src.workflow.handlers.delete_handler.EventKitBridge') as mock_eb:
            with patch('src.workflow.handlers.delete_handler.ParseService') as mock_ps:

                mock_ps.return_value.delete_tracked_item.return_value = (
                    True,
                    None
                )

                parsed = ParsedInput(
                    command="delete",
                    args=["event-123"],
                    raw_input="delete event-123"
                )
                feedback = FeedbackBuilder()

                result = handle_delete_command(parsed, feedback)

                assert "✅" in result.items[0].title
                assert "Item Deleted" in result.items[0].title

    def test_delete_item_not_found(self):
        """Test deleting non-existent item."""
        with patch('src.workflow.handlers.delete_handler.EventKitBridge'):
            with patch('src.workflow.handlers.delete_handler.ParseService') as mock_ps:

                mock_ps.return_value.delete_tracked_item.return_value = (
                    False,
                    "Item not found"
                )

                parsed = ParsedInput(
                    command="delete",
                    args=["missing-123"],
                    raw_input="delete missing-123"
                )
                feedback = FeedbackBuilder()

                result = handle_delete_command(parsed, feedback)

                assert result.items[0].valid is False


class TestDeleteHandlerAll:
    """Test deleting all items."""

    def test_delete_all_items(self):
        """Test deleting all tracked items."""
        with patch('src.workflow.handlers.delete_handler.TrackerService') as mock_ts:
            with patch('src.workflow.handlers.delete_handler.EventKitBridge') as mock_eb:

                mock_item = Mock()
                mock_item.item_id = "event-123"
                mock_item.item_type = "calendar_event"
                mock_item.title = "Test Event"

                mock_ts.return_value.get_all_tracked_items.return_value = [mock_item]
                mock_eb.return_value.delete_calendar_event.return_value = (True, None)

                parsed = ParsedInput(
                    command="delete",
                    args=["all"],
                    raw_input="delete all"
                )
                feedback = FeedbackBuilder()

                result = handle_delete_command(parsed, feedback)

                assert "✅" in result.items[0].title
                assert "Deleted" in result.items[0].title

    def test_delete_all_with_failures(self):
        """Test delete all with some failures."""
        with patch('src.workflow.handlers.delete_handler.TrackerService') as mock_ts:
            with patch('src.workflow.handlers.delete_handler.EventKitBridge') as mock_eb:

                mock_item1 = Mock()
                mock_item1.item_id = "event-123"
                mock_item1.item_type = "calendar_event"
                mock_item1.title = "Event 1"

                mock_item2 = Mock()
                mock_item2.item_id = "reminder-456"
                mock_item2.item_type = "reminder"
                mock_item2.title = "Reminder 1"

                mock_ts.return_value.get_all_tracked_items.return_value = [
                    mock_item1,
                    mock_item2
                ]
                mock_eb.return_value.delete_calendar_event.return_value = (True, None)
                mock_eb.return_value.delete_reminder.return_value = (False, "Permission denied")

                parsed = ParsedInput(
                    command="delete",
                    args=["all"],
                    raw_input="delete all"
                )
                feedback = FeedbackBuilder()

                result = handle_delete_command(parsed, feedback)

                # Should show success and warning
                titles = [item.title for item in result.items]
                assert any("Items Deleted" in title for title in titles)
                assert any("Failed" in title for title in titles)


class TestDeleteHandlerOld:
    """Test deleting old items."""

    def test_delete_old_default_days(self):
        """Test deleting items older than default 7 days."""
        with patch('src.workflow.handlers.delete_handler.TrackerService') as mock_ts:
            mock_ts.return_value.cleanup_old_items.return_value = 5

            parsed = ParsedInput(
                command="delete",
                args=["old"],
                raw_input="delete old"
            )
            feedback = FeedbackBuilder()

            result = handle_delete_command(parsed, feedback)

            assert "✅" in result.items[0].title
            mock_ts.return_value.cleanup_old_items.assert_called_with(7)

    def test_delete_old_custom_days(self):
        """Test deleting items older than custom days."""
        with patch('src.workflow.handlers.delete_handler.TrackerService') as mock_ts:
            mock_ts.return_value.cleanup_old_items.return_value = 3

            parsed = ParsedInput(
                command="delete",
                args=["old", "30"],
                raw_input="delete old 30"
            )
            feedback = FeedbackBuilder()

            result = handle_delete_command(parsed, feedback)

            assert "✅" in result.items[0].title
            mock_ts.return_value.cleanup_old_items.assert_called_with(30)
