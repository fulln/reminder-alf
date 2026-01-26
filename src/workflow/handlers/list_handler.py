"""
List command handler for Alfred.
"""
from ..input_handler import ParsedInput
from ..feedback_builder import FeedbackBuilder, FeedbackItem
from ...services.tracker_service import TrackerService
from ...utils.logger import get_logger

logger = get_logger(__name__)


def handle_list_command(parsed_input: ParsedInput, feedback: FeedbackBuilder) -> FeedbackBuilder:
    """
    Handle list commands to show tracked items.

    Args:
        parsed_input: Parsed user input
        feedback: Feedback builder for response

    Returns:
        Updated feedback builder
    """
    tracker_service = TrackerService()

    # Get limit from args
    limit = 10
    if parsed_input.args and parsed_input.args[0].isdigit():
        limit = int(parsed_input.args[0])

    items = tracker_service.get_recent_items(limit)

    if not items:
        return feedback.add_info(
            "No Items Tracked",
            "No calendar events or reminders have been created yet"
        )

    feedback.add_info(
        "Recent Created Items",
        f"Showing {len(items)} most recent items"
    )

    for item in items:
        # Format created date
        created_date = item.created_at.strftime("%b %d, %I:%M %p")

        # Create type icon
        type_icon = "📅" if item.item_type == "calendar_event" else "📋"
        type_label = "Calendar Event" if item.item_type == "calendar_event" else "Reminder"

        # Build subtitle with details
        subtitle = f"{type_icon} {type_label} • {created_date}\nID: {item.item_id}"
        if item.calendar_or_list:
            subtitle += f" • {item.calendar_or_list}"

        feedback.add_item(
            FeedbackItem(
                title=item.title,
                subtitle=subtitle,
                arg=item.item_id,
                valid=False,  # Not directly executable
            )
        )

    return feedback
