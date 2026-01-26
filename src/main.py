#!/usr/bin/env python3
"""
Alfred workflow entry point for AI-powered calendar and reminder management.
"""
import sys
import json
from workflow import Workflow3
from .workflow.input_handler import InputHandler
from .workflow.command_router import CommandRouter
from .workflow.handlers import (
    handle_config_command,
    handle_parse_command,
    handle_delete_command,
    handle_list_command,
    handle_help_command,
)
from .utils.logger import get_logger

logger = get_logger(__name__)


def main(wf: Workflow3) -> None:
    """
    Main workflow entry point.

    Args:
        wf: Alfred workflow instance
    """
    try:
        # Get user input from Alfred
        query = wf.args[0] if wf.args else ""

        # Parse input
        input_handler = InputHandler()
        parsed_input = input_handler.parse(query)

        # Route to command handler
        command_router = CommandRouter()
        command_router.register("parse", handle_parse_command)
        command_router.register("config", handle_config_command)
        command_router.register("delete", handle_delete_command)
        command_router.register("list", handle_list_command)
        command_router.register("help", handle_help_command)

        # Add default handler for help
        command_router.register_default(handle_help_command)

        # Execute command
        feedback = command_router.route(parsed_input)

        # Convert feedback to Alfred JSON and send
        feedback_json = json.loads(feedback.to_json())
        for item in feedback_json.get("items", []):
            wf.add_item(
                title=item.get("title", ""),
                subtitle=item.get("subtitle", ""),
                arg=item.get("arg"),
                valid=item.get("valid", False),
                icon=item.get("icon", {}).get("path"),
                autocomplete=item.get("autocomplete"),
                uid=item.get("uid"),
            )

        # Add workflow variables
        for key, value in feedback_json.get("variables", {}).items():
            wf.setvar(key, value)

        wf.send_feedback()

    except Exception as e:
        logger.error(f"Main error: {e}", exc_info=True)
        wf.add_item(
            title="Error",
            subtitle=str(e),
            valid=False
        )
        wf.send_feedback()


if __name__ == "__main__":
    wf = Workflow3()
    sys.exit(wf.run(main))
