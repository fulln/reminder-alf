"""
Tests for ParseService.
"""
import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
from src.services.parse_service import ParseService
from src.models.ai_config import AIConfiguration
from src.models.parse_result import ParseResult
from src.models.calendar_event import CalendarEvent
from src.models.reminder import Reminder


@pytest.fixture
def mock_ai_config():
    return AIConfiguration(
        provider="openai",
        model="gpt-4",
        api_key="test-key"
    )


@pytest.fixture
def mock_eventkit_bridge():
    bridge = Mock()
    bridge.create_calendar_event.return_value = (True, "event-123", None)
    bridge.create_reminder.return_value = (True, "reminder-123", None)
    bridge.delete_calendar_event.return_value = (True, None)
    bridge.delete_reminder.return_value = (True, None)
    return bridge


@pytest.fixture
def parse_service(mock_ai_config):
    with patch('src.services.parse_service.AIClient'):
        with patch('src.services.parse_service.TrackerService'):
            return ParseService(mock_ai_config)


class TestParseServiceBasics:
    """Test ParseService initialization and basics."""

    def test_parse_service_init(self, mock_ai_config):
        """Test service initialization."""
        with patch('src.services.parse_service.AIClient'):
            with patch('src.services.parse_service.TrackerService'):
                service = ParseService(mock_ai_config)
                assert service is not None

    def test_parse_empty_input(self, parse_service):
        """Test parsing empty input."""
        result = parse_service.parse_input("")
        assert len(result.errors) > 0

    def test_parse_whitespace_input(self, parse_service):
        """Test parsing whitespace input."""
        result = parse_service.parse_input("   ")
        assert len(result.errors) > 0


class TestParseServiceParsing:
    """Test parsing functionality."""

    def test_parse_valid_input(self, parse_service):
        """Test parsing valid input."""
        # Mock AI client response
        parse_service.ai_client.parse_text = Mock(
            return_value=ParseResult(
                calendar_events=[
                    CalendarEvent(
                        title="Test Event",
                        start_date=datetime(2026, 1, 27, 14, 0),
                        end_date=datetime(2026, 1, 27, 15, 0)
                    )
                ],
                reminders=[],
                raw_text="meeting tomorrow at 2pm"
            )
        )

        result = parse_service.parse_input("meeting tomorrow at 2pm")
        assert len(result.errors) == 0
        assert len(result.calendar_events) == 1

    def test_parse_error_handling(self, parse_service):
        """Test error handling in parsing."""
        parse_service.ai_client.parse_text = Mock(
            return_value=ParseResult.error("API Error", "test input")
        )

        result = parse_service.parse_input("test")
        assert len(result.errors) > 0


class TestCreateItems:
    """Test item creation from parse results."""

    def test_create_calendar_event(self, parse_service, mock_eventkit_bridge):
        """Test creating calendar event."""
        parse_result = ParseResult(
            calendar_events=[
                CalendarEvent(
                    title="Test Event",
                    start_date=datetime(2026, 1, 27, 14, 0),
                    end_date=datetime(2026, 1, 27, 15, 0)
                )
            ],
            reminders=[],
            raw_text="test"
        )

        events, reminders, errors = parse_service.create_items_from_parse(
            parse_result,
            mock_eventkit_bridge
        )

        assert events == 1
        assert reminders == 0
        assert len(errors) == 0
        mock_eventkit_bridge.create_calendar_event.assert_called_once()

    def test_create_reminder(self, parse_service, mock_eventkit_bridge):
        """Test creating reminder."""
        parse_result = ParseResult(
            calendar_events=[],
            reminders=[
                Reminder(
                    title="Test Reminder",
                    priority=2
                )
            ],
            raw_text="test"
        )

        events, reminders, errors = parse_service.create_items_from_parse(
            parse_result,
            mock_eventkit_bridge
        )

        assert events == 0
        assert reminders == 1
        assert len(errors) == 0
        mock_eventkit_bridge.create_reminder.assert_called_once()

    def test_create_mixed_items(self, parse_service, mock_eventkit_bridge):
        """Test creating mixed events and reminders."""
        parse_result = ParseResult(
            calendar_events=[
                CalendarEvent(
                    title="Event",
                    start_date=datetime(2026, 1, 27, 14, 0),
                    end_date=datetime(2026, 1, 27, 15, 0)
                )
            ],
            reminders=[
                Reminder(title="Reminder")
            ],
            raw_text="test"
        )

        events, reminders, errors = parse_service.create_items_from_parse(
            parse_result,
            mock_eventkit_bridge
        )

        assert events == 1
        assert reminders == 1
        assert len(errors) == 0

    def test_create_failure_handling(self, parse_service, mock_eventkit_bridge):
        """Test handling creation failures."""
        mock_eventkit_bridge.create_calendar_event.return_value = (
            False,
            None,
            "Permission denied"
        )

        parse_result = ParseResult(
            calendar_events=[
                CalendarEvent(
                    title="Event",
                    start_date=datetime(2026, 1, 27, 14, 0),
                    end_date=datetime(2026, 1, 27, 15, 0)
                )
            ],
            reminders=[],
            raw_text="test"
        )

        events, reminders, errors = parse_service.create_items_from_parse(
            parse_result,
            mock_eventkit_bridge
        )

        assert events == 0
        assert len(errors) == 1


class TestDeleteItem:
    """Test item deletion."""

    def test_delete_calendar_event(self, parse_service, mock_eventkit_bridge):
        """Test deleting calendar event."""
        # Mock tracker service
        mock_item = Mock()
        mock_item.item_id = "event-123"
        mock_item.item_type = "calendar_event"

        parse_service.tracker_service.get_all_tracked_items = Mock(
            return_value=[mock_item]
        )
        parse_service.tracker_service.remove_tracked_item = Mock()

        success, error = parse_service.delete_tracked_item(
            "event-123",
            mock_eventkit_bridge
        )

        assert success is True
        assert error is None
        mock_eventkit_bridge.delete_calendar_event.assert_called_once()

    def test_delete_item_not_found(self, parse_service, mock_eventkit_bridge):
        """Test deleting non-existent item."""
        parse_service.tracker_service.get_all_tracked_items = Mock(
            return_value=[]
        )

        success, error = parse_service.delete_tracked_item(
            "missing-123",
            mock_eventkit_bridge
        )

        assert success is False
        assert "not found" in error.lower()


class TestTrackedItems:
    """Test retrieving tracked items."""

    def test_get_all_items(self, parse_service):
        """Test getting all tracked items."""
        mock_items = [Mock(), Mock()]
        parse_service.tracker_service.get_all_tracked_items = Mock(
            return_value=mock_items
        )

        items = parse_service.get_tracked_items()
        assert len(items) == 2

    def test_get_recent_items(self, parse_service):
        """Test getting recent tracked items."""
        mock_items = [Mock()]
        parse_service.tracker_service.get_recent_items = Mock(
            return_value=mock_items
        )

        items = parse_service.get_tracked_items(limit=10)
        assert len(items) == 1
        parse_service.tracker_service.get_recent_items.assert_called_with(10)
