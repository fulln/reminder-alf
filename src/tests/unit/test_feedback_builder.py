"""
Tests for FeedbackBuilder.
"""
import pytest
import json
from src.workflow.feedback_builder import FeedbackBuilder, FeedbackItem


@pytest.fixture
def feedback_builder():
    return FeedbackBuilder()


class TestFeedbackItemBasics:
    """Test FeedbackItem creation and conversion."""

    def test_feedback_item_minimal(self):
        """Test creating minimal feedback item."""
        item = FeedbackItem(title="Test")
        assert item.title == "Test"
        assert item.subtitle == ""
        assert item.valid is True

    def test_feedback_item_to_dict(self):
        """Test converting feedback item to dict."""
        item = FeedbackItem(
            title="Test",
            subtitle="Details",
            arg="test_arg",
            valid=True
        )
        result = item.to_dict()
        assert result["title"] == "Test"
        assert result["subtitle"] == "Details"
        assert result["arg"] == "test_arg"
        assert result["valid"] is True


class TestFeedbackBuilderBasics:
    """Test FeedbackBuilder basics."""

    def test_builder_starts_empty(self, feedback_builder):
        """Test builder starts with no items."""
        assert len(feedback_builder.items) == 0

    def test_add_item(self, feedback_builder):
        """Test adding items."""
        item = FeedbackItem(title="Test")
        feedback_builder.add_item(item)
        assert len(feedback_builder.items) == 1
        assert feedback_builder.items[0].title == "Test"

    def test_builder_chaining(self, feedback_builder):
        """Test builder method chaining."""
        result = feedback_builder.add_item(
            FeedbackItem(title="Item 1")
        ).add_item(
            FeedbackItem(title="Item 2")
        )
        assert result is feedback_builder
        assert len(feedback_builder.items) == 2


class TestFeedbackBuilderMethods:
    """Test FeedbackBuilder convenience methods."""

    def test_add_error(self, feedback_builder):
        """Test adding error feedback."""
        feedback_builder.add_error("Test Error", "Error details")
        assert len(feedback_builder.items) == 1
        assert "❌" in feedback_builder.items[0].title
        assert feedback_builder.items[0].valid is False

    def test_add_error_with_suggestion(self, feedback_builder):
        """Test adding error with suggestion."""
        feedback_builder.add_error(
            "Test Error",
            "Error details",
            "Try this instead"
        )
        assert "💡" in feedback_builder.items[0].subtitle

    def test_add_warning(self, feedback_builder):
        """Test adding warning feedback."""
        feedback_builder.add_warning("Test Warning")
        assert "⚠️" in feedback_builder.items[0].title

    def test_add_info(self, feedback_builder):
        """Test adding info feedback."""
        feedback_builder.add_info("Test Info")
        assert "ℹ️" in feedback_builder.items[0].title

    def test_add_success(self, feedback_builder):
        """Test adding success feedback."""
        feedback_builder.add_success("Test Success")
        assert "✅" in feedback_builder.items[0].title
        assert feedback_builder.items[0].valid is True

    def test_add_calendar_event(self, feedback_builder):
        """Test adding calendar event."""
        feedback_builder.add_calendar_event(
            "Meeting",
            "2026-01-27 2:00 PM",
            location="Room 305"
        )
        assert len(feedback_builder.items) == 1
        assert "📅" in feedback_builder.items[0].subtitle
        assert "📍" in feedback_builder.items[0].subtitle

    def test_add_reminder(self, feedback_builder):
        """Test adding reminder."""
        feedback_builder.add_reminder(
            "Buy milk",
            priority=1
        )
        assert "📋" in feedback_builder.items[0].subtitle
        assert "🔵" in feedback_builder.items[0].subtitle

    def test_add_loading(self, feedback_builder):
        """Test adding loading indicator."""
        feedback_builder.add_loading("Parsing...")
        assert "⏳" in feedback_builder.items[0].title

    def test_add_progress(self, feedback_builder):
        """Test adding progress indicator."""
        feedback_builder.add_progress(5, 10, "Processing")
        assert "5/10" in feedback_builder.items[0].title
        assert "50%" in feedback_builder.items[0].subtitle


class TestFeedbackBuilderVariables:
    """Test workflow variables."""

    def test_set_variable(self, feedback_builder):
        """Test setting workflow variable."""
        feedback_builder.set_variable("key", "value")
        assert feedback_builder.variables["key"] == "value"

    def test_multiple_variables(self, feedback_builder):
        """Test setting multiple variables."""
        feedback_builder.set_variable("key1", "value1").set_variable(
            "key2", "value2"
        )
        assert len(feedback_builder.variables) == 2


class TestFeedbackBuilderJSON:
    """Test JSON output."""

    def test_to_json_empty(self, feedback_builder):
        """Test JSON output for empty builder."""
        json_str = feedback_builder.to_json()
        data = json.loads(json_str)
        assert data["items"] == []

    def test_to_json_with_items(self, feedback_builder):
        """Test JSON output with items."""
        feedback_builder.add_success("Test")
        json_str = feedback_builder.to_json()
        data = json.loads(json_str)
        assert len(data["items"]) == 1
        assert "✅" in data["items"][0]["title"]

    def test_to_json_with_variables(self, feedback_builder):
        """Test JSON output includes variables."""
        feedback_builder.set_variable("key", "value")
        json_str = feedback_builder.to_json()
        data = json.loads(json_str)
        assert data["variables"]["key"] == "value"

    def test_to_json_unicode(self, feedback_builder):
        """Test JSON output preserves unicode."""
        feedback_builder.add_success("测试事件")
        json_str = feedback_builder.to_json()
        assert "测试事件" in json_str


class TestFeedbackBuilderClear:
    """Test clearing builder."""

    def test_clear_items(self, feedback_builder):
        """Test clearing items."""
        feedback_builder.add_success("Test1").add_success("Test2")
        assert len(feedback_builder.items) == 2
        feedback_builder.clear()
        assert len(feedback_builder.items) == 0

    def test_clear_variables(self, feedback_builder):
        """Test clearing variables."""
        feedback_builder.set_variable("key", "value")
        assert len(feedback_builder.variables) == 1
        feedback_builder.clear()
        assert len(feedback_builder.variables) == 0
