"""
ParseService for orchestrating AI text parsing workflow.
"""
from dataclasses import dataclass
from typing import Optional
from ..models.parse_result import ParseResult
from ..models.ai_config import AIConfiguration
from ..services.ai_client import AIClient
from ..services.tracker_service import TrackerService
from ..models.tracker import CreatedItem
from ..utils.logger import get_logger
from datetime import datetime

logger = get_logger(__name__)


@dataclass
class ParseSession:
    """Session for a single parse operation."""

    session_id: str
    input_text: str
    parse_result: ParseResult
    created_items: list[CreatedItem]
    timestamp: datetime
    success: bool
    error_message: Optional[str] = None


class ParseService:
    """
    Service that orchestrates the parsing workflow.

    Coordinates AI parsing, EventKit integration, and item tracking.
    """

    def __init__(
        self,
        ai_config: AIConfiguration,
        tracker_service: Optional[TrackerService] = None
    ):
        """
        Initialize ParseService.

        Args:
            ai_config: AI configuration for API access
            tracker_service: Optional tracker service for persistence
        """
        self.ai_client = AIClient(ai_config)
        self.tracker_service = tracker_service or TrackerService()
        logger.info("ParseService initialized")

    def parse_input(self, text: str) -> ParseResult:
        """
        Parse user input text to extract events and reminders.

        Args:
            text: Natural language text from user

        Returns:
            ParseResult with extracted items
        """
        if not text or not text.strip():
            return ParseResult.error("No text provided", text)

        logger.info(f"Parsing input: {text[:50]}...")

        try:
            # Call AI client to parse
            result = self.ai_client.parse_text(text)

            if result.errors:
                logger.warning(f"Parse failed: {result.errors}")
                return result

            logger.info(
                f"Parse successful: {len(result.calendar_events)} events, "
                f"{len(result.reminders)} reminders"
            )

            return result

        except Exception as e:
            logger.error(f"Parse error: {e}")
            return ParseResult.error(f"Parse error: {str(e)}", text)

    def create_items_from_parse(
        self,
        parse_result: ParseResult,
        eventkit_bridge
    ) -> tuple[int, int, list[str]]:
        """
        Create calendar events and reminders from parse result.

        Args:
            parse_result: Result from parse_input
            eventkit_bridge: EventKitBridge for system integration

        Returns:
            (events_created, reminders_created, error_messages)
        """
        events_created = 0
        reminders_created = 0
        errors = []

        # Create calendar events
        for event in parse_result.calendar_events:
            try:
                success, event_id, error = eventkit_bridge.create_calendar_event(event)
                if success and event_id:
                    events_created += 1
                    # Track the created item
                    created_item = CreatedItem(
                        item_type="calendar_event",
                        item_id=event_id,
                        title=event.title,
                        created_at=datetime.now(),
                        calendar_or_list=event.calendar_name or "Default",
                        source_text=parse_result.raw_text,
                    )
                    self.tracker_service.track_created_item(created_item)
                    logger.info(f"Created calendar event: {event.title} (ID: {event_id})")
                else:
                    error_msg = error or "Unknown error"
                    errors.append(f"Event '{event.title}': {error_msg}")
                    logger.warning(f"Failed to create event: {event.title}")
            except Exception as e:
                errors.append(f"Event '{event.title}': {str(e)}")
                logger.error(f"Exception creating event: {e}")

        # Create reminders
        for reminder in parse_result.reminders:
            try:
                success, reminder_id, error = eventkit_bridge.create_reminder(reminder)
                if success and reminder_id:
                    reminders_created += 1
                    # Track the created item
                    created_item = CreatedItem(
                        item_type="reminder",
                        item_id=reminder_id,
                        title=reminder.title,
                        created_at=datetime.now(),
                        calendar_or_list=reminder.list_name or "Default",
                        source_text=parse_result.raw_text,
                    )
                    self.tracker_service.track_created_item(created_item)
                    logger.info(f"Created reminder: {reminder.title} (ID: {reminder_id})")
                else:
                    error_msg = error or "Unknown error"
                    errors.append(f"Reminder '{reminder.title}': {error_msg}")
                    logger.warning(f"Failed to create reminder: {reminder.title}")
            except Exception as e:
                errors.append(f"Reminder '{reminder.title}': {str(e)}")
                logger.error(f"Exception creating reminder: {e}")

        return events_created, reminders_created, errors

    def delete_tracked_item(self, item_id: str, eventkit_bridge) -> tuple[bool, Optional[str]]:
        """
        Delete a tracked item by ID.

        Args:
            item_id: ID of item to delete
            eventkit_bridge: EventKitBridge for system integration

        Returns:
            (success, error_message)
        """
        try:
            # Find tracked item
            all_items = self.tracker_service.get_all_tracked_items()
            tracked_item = None
            for item in all_items:
                if item.item_id == item_id:
                    tracked_item = item
                    break

            if not tracked_item:
                return False, f"Item not found: {item_id}"

            # Delete from system
            if tracked_item.item_type == "calendar_event":
                success, error = eventkit_bridge.delete_calendar_event(item_id)
            elif tracked_item.item_type == "reminder":
                success, error = eventkit_bridge.delete_reminder(item_id)
            else:
                return False, f"Unknown item type: {tracked_item.item_type}"

            if success:
                # Remove from tracker
                self.tracker_service.remove_tracked_item(item_id)
                logger.info(f"Deleted {tracked_item.item_type}: {tracked_item.title}")
                return True, None
            else:
                return False, error or "Unknown error"

        except Exception as e:
            logger.error(f"Exception deleting item: {e}")
            return False, str(e)

    def get_tracked_items(self, limit: Optional[int] = None) -> list[CreatedItem]:
        """
        Get tracked items.

        Args:
            limit: Optional limit on number of items

        Returns:
            List of created items
        """
        if limit:
            return self.tracker_service.get_recent_items(limit)
        return self.tracker_service.get_all_tracked_items()

    def cleanup_old_items(self, days: int = 7) -> int:
        """
        Clean up items older than specified days.

        Args:
            days: Age threshold in days

        Returns:
            Number of items removed
        """
        count = self.tracker_service.cleanup_old_items(days)
        logger.info(f"Cleaned up {count} items older than {days} days")
        return count
