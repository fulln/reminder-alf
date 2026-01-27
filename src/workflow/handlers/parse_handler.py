"""
Parse command handler for Alfred.
"""
from ..input_handler import ParsedInput
from ..feedback_builder import FeedbackBuilder
from ...services.parse_service import ParseService
from ...services.config_manager import ConfigManager
from ...services.eventkit_bridge import EventKitBridge
from ...utils.logger import get_logger

logger = get_logger(__name__)


def handle_parse_command(parsed_input: ParsedInput, feedback: FeedbackBuilder) -> FeedbackBuilder:
    """
    Handle parse commands to extract events and reminders.

    Args:
        parsed_input: Parsed user input
        feedback: Feedback builder for response

    Returns:
        Updated feedback builder
    """
    # Get configuration
    config_manager = ConfigManager()
    config = config_manager.get_configuration()

    if not config:
        return feedback.add_error(
            "Not Configured",
            "Please configure AI settings first",
            "Run 'rem config set <provider> <api_key>'"
        )

    # Get text to parse
    text = parsed_input.query
    if not text or not text.strip():
        return feedback.add_error(
            "No Input",
            "Please provide text to parse",
            "Example: rem 'meeting tomorrow at 2pm'"
        )

    # Show loading indicator
    feedback.add_loading("Parsing with AI...")

    try:
        # Parse with AI
        parse_service = ParseService(config)
        parse_result = parse_service.parse_input(text)

        if parse_result.errors:
            error_msg = "\n".join(parse_result.errors)
            from ...utils.notifier import send_notification
            send_notification("Reminder-Alf Parse Failed", error_msg)
            
            return feedback.clear().add_error(
                "Parse Failed",
                error_msg,
                "Try rephrasing your input"
            )

        if parse_result.is_empty():
            msg = "Could not identify calendar events or reminders."
            from ...utils.notifier import send_notification
            send_notification("Reminder-Alf", msg)
            
            return feedback.clear().add_warning(
                "No Items Found",
                msg + " Try being more specific (e.g., include dates/times)"
            )

        # Create items in system
        eventkit_bridge = EventKitBridge()
        events_created, reminders_created, errors = (
            parse_service.create_items_from_parse(parse_result, eventkit_bridge)
        )

        # Clear loading and show results
        feedback.clear()

        # Show created items
        for event in parse_result.calendar_events:
            start_time = event.start_date.strftime("%b %d, %I:%M %p")
            feedback.add_calendar_event(
                event.title,
                start_time,
                location=event.location
            )

        for reminder in parse_result.reminders:
            due_date = None
            if reminder.due_date:
                due_date = reminder.due_date.strftime("%b %d, %I:%M %p")
            feedback.add_reminder(
                reminder.title,
                due_date=due_date,
                priority=reminder.priority
            )

        # Add summary
        summary = f"✅ Created {events_created} events, {reminders_created} reminders"
        if parse_result.ambiguities:
            summary += f"\n⚠️ Ambiguities: {', '.join(parse_result.ambiguities[:2])}"

        feedback.add_info("Summary", summary)
        
        # Send notification
        from ...utils.notifier import send_notification
        send_notification("Reminder-Alf", summary)

        # Show errors if any
        if errors:
            error_msg = "\n".join(errors[:3])
            feedback.add_warning(
                "Some Items Failed",
                error_msg
            )
            # Notify about errors 
            send_notification("Reminder-Alf Warning", f"Some items failed: {error_msg}")

        return feedback

    except Exception as e:
        logger.error(f"Parse handler error: {e}", exc_info=True)
        # Notify about exception
        from ...utils.notifier import send_notification
        send_notification("Reminder-Alf Error", str(e))
        
        return feedback.clear().add_error(
            "Error",
            str(e),
            "Check logs for details"
        )
