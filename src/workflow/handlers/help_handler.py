"""
Help command handler for Alfred.
"""
from ..input_handler import ParsedInput
from ..feedback_builder import FeedbackBuilder, FeedbackItem


def handle_help_command(parsed_input: ParsedInput, feedback: FeedbackBuilder) -> FeedbackBuilder:
    """
    Handle help commands.

    Args:
        parsed_input: Parsed user input
        feedback: Feedback builder for response

    Returns:
        Updated feedback builder
    """
    feedback.add_info(
        "Reminder-Alf Help",
        "AI-powered calendar and reminder management for Alfred"
    )

    feedback.add_item(
        FeedbackItem(
            title="Parse Natural Language",
            subtitle="rem Meeting tomorrow at 2pm",
            valid=False
        )
    )

    feedback.add_item(
        FeedbackItem(
            title="Configuration",
            subtitle="rem config set openai sk-YOUR_KEY [model]",
            valid=False
        )
    )

    feedback.add_item(
        FeedbackItem(
            title="List Items",
            subtitle="rem list [limit]",
            valid=False
        )
    )

    feedback.add_item(
        FeedbackItem(
            title="Delete Items",
            subtitle="rem delete [id|all|old DAYS]",
            valid=False
        )
    )

    feedback.add_info(
        "Examples",
        "Parse: 'Lunch with Sarah at noon' or '明天下午3点开会'\n"
        "Config: 'rem config status'\n"
        "List: 'rem list 20'\n"
        "Delete: 'rem delete all'"
    )

    return feedback
