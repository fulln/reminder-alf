"""
Delete command handler for Alfred.
"""
from ..input_handler import ParsedInput
from ..feedback_builder import FeedbackBuilder
from ...services.parse_service import ParseService
from ...services.tracker_service import TrackerService
from ...services.eventkit_bridge import EventKitBridge
from ...utils.logger import get_logger

logger = get_logger(__name__)


def handle_delete_command(parsed_input: ParsedInput, feedback: FeedbackBuilder) -> FeedbackBuilder:
    """
    Handle delete commands to remove tracked items.

    Args:
        parsed_input: Parsed user input
        feedback: Feedback builder for response

    Returns:
        Updated feedback builder
    """
    # Subcommands: delete all, delete <id>, delete old
    if not parsed_input.args:
        # Show tracked items for deletion
        tracker_service = TrackerService()
        items = tracker_service.get_recent_items(10)

        if not items:
            return feedback.add_info(
                "No Items Tracked",
                "No calendar events or reminders have been created yet"
            )

        feedback.add_info("Recent Items", "Select one to delete:")
        for item in items:
            subtitle = f"{item.item_type} • {item.created_at.strftime('%b %d')}"
            feedback.add_item(
                FeedbackItem(
                    title=item.title,
                    subtitle=subtitle,
                    arg=item.item_id,
                    valid=True
                )
            )

        return feedback

    subcommand = parsed_input.args[0]

    # Delete specific item
    if subcommand != "all" and subcommand != "old":
        item_id = subcommand
        eventkit_bridge = EventKitBridge()

        # Request necessary permissions
        eventkit_bridge.request_calendar_access()
        eventkit_bridge.request_reminder_access()

        # Create parse service to handle deletion
        from ...services.config_manager import ConfigManager
        config_manager = ConfigManager()
        config = config_manager.get_configuration()

        if not config:
            # Create dummy config for tracker-only deletion
            from ...models.ai_config import AIConfiguration
            config = AIConfiguration(
                provider="openai",
                model="gpt-4",
                api_key="dummy"
            )

        parse_service = ParseService(config)
        success, error = parse_service.delete_tracked_item(item_id, eventkit_bridge)

        if success:
            return feedback.add_success(
                "Item Deleted",
                f"Removed {item_id} from calendar and reminders"
            )
        else:
            return feedback.add_error(
                "Delete Failed",
                error or "Could not delete item"
            )

    # Delete all tracked items
    if subcommand == "all":
        tracker_service = TrackerService()
        eventkit_bridge = EventKitBridge()

        # Request permissions
        eventkit_bridge.request_calendar_access()
        eventkit_bridge.request_reminder_access()

        items = tracker_service.get_all_tracked_items()
        deleted_count = 0
        failed_items = []

        for item in items:
            try:
                if item.item_type == "calendar_event":
                    success, error = eventkit_bridge.delete_calendar_event(item.item_id)
                elif item.item_type == "reminder":
                    success, error = eventkit_bridge.delete_reminder(item.item_id)
                else:
                    success = False
                    error = f"Unknown type: {item.item_type}"

                if success:
                    tracker_service.remove_tracked_item(item.item_id)
                    deleted_count += 1
                    logger.info(f"Deleted {item.item_type}: {item.title}")
                else:
                    failed_items.append(f"{item.title}: {error}")
                    logger.warning(f"Failed to delete: {item.title}")

            except Exception as e:
                failed_items.append(f"{item.title}: {str(e)}")
                logger.error(f"Exception deleting item: {e}")

        feedback.add_success(
            "Items Deleted",
            f"Deleted {deleted_count} of {len(items)} items"
        )

        if failed_items:
            feedback.add_warning(
                "Some Items Failed",
                "\n".join(failed_items[:3])
            )

        return feedback

    # Delete old items
    if subcommand == "old":
        days = 7
        if len(parsed_input.args) > 1:
            try:
                days = int(parsed_input.args[1])
            except ValueError:
                return feedback.add_error("Invalid days argument")

        tracker_service = TrackerService()
        count = tracker_service.cleanup_old_items(days)

        return feedback.add_success(
            "Cleanup Complete",
            f"Deleted {count} items older than {days} days"
        )

    return feedback.add_error("Unknown delete subcommand")


# Import after function definition to avoid circular imports
from ..feedback_builder import FeedbackItem
