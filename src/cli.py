#!/usr/bin/env python3
"""
CLI entry point for Reminder-Alf.
Provides command-line interface for AI-powered calendar and reminder management.
"""
import sys
import json
import argparse
from typing import Optional


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for CLI."""
    parser = argparse.ArgumentParser(
        prog="ral",
        description="AI-powered calendar and reminder management",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Parse command (default - natural language input)
    parse_parser = subparsers.add_parser("parse", help="Parse natural language input")
    parse_parser.add_argument("text", nargs="+", help="Natural language text to parse")
    
    # Config command
    config_parser = subparsers.add_parser("config", help="Configuration management")
    config_subparsers = config_parser.add_subparsers(dest="config_action")
    
    # config status
    config_subparsers.add_parser("status", help="Show configuration status")
    
    # config set
    config_set = config_subparsers.add_parser("set", help="Set AI provider configuration")
    config_set.add_argument("provider", choices=["openai", "deepseek", "anthropic", "custom"])
    config_set.add_argument("api_key", help="API key")
    config_set.add_argument("model", nargs="?", default=None, help="Model name (optional)")
    
    # config delete
    config_subparsers.add_parser("delete", help="Delete configuration")
    
    # config endpoint
    config_endpoint = config_subparsers.add_parser("endpoint", help="Set custom endpoint URL")
    config_endpoint.add_argument("url", help="Endpoint URL")
    
    # config timeout
    config_timeout = config_subparsers.add_parser("timeout", help="Set request timeout")
    config_timeout.add_argument("seconds", type=int, help="Timeout in seconds")
    
    # config tokens
    config_tokens = config_subparsers.add_parser("tokens", help="Set max tokens")
    config_tokens.add_argument("count", type=int, help="Max tokens")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List recent items")
    list_parser.add_argument("count", nargs="?", type=int, default=10, help="Number of items")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete items")
    delete_parser.add_argument("target", nargs="?", help="Item ID, 'all', or 'old N'")
    delete_parser.add_argument("days", nargs="?", type=int, help="Days for 'old' command")
    
    # Help command
    subparsers.add_parser("help", help="Show help")
    
    # Version
    parser.add_argument("--version", action="version", version="%(prog)s 1.3.0")
    
    # JSON output format (for Raycast integration)
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    
    return parser


def output_result(result: dict, as_json: bool = False) -> None:
    """Output result to stdout."""
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # Human-readable output
        if result.get("success"):
            print(f"✅ {result.get('message', 'Success')}")
            if result.get("items"):
                for item in result["items"]:
                    print(f"  - {item.get('title', '')}: {item.get('subtitle', '')}")
        else:
            print(f"❌ {result.get('error', 'Unknown error')}")


def handle_parse(args, as_json: bool) -> dict:
    """Handle parse command."""
    from .services.config_manager import ConfigManager
    from .services.parse_service import ParseService
    from .services.applescript_bridge import AppleScriptBridge
    
    text = " ".join(args.text)
    
    config_manager = ConfigManager()
    config = config_manager.get_configuration()
    
    if not config:
        return {"success": False, "error": "Not configured. Run: ral config set <provider> <api_key>"}
    
    try:
        parse_service = ParseService(config)
        result = parse_service.parse_input(text)
        
        if result.errors:
            return {"success": False, "error": result.errors[0]}
        
        # Create items in system using AppleScript
        bridge = AppleScriptBridge()
        events_created, reminders_created, errors = parse_service.create_items_from_parse(
            result, bridge
        )
        
        items = []
        for event in result.calendar_events:
            items.append({
                "type": "calendar_event",
                "title": event.title,
                "subtitle": f"📅 {event.start_date}"
            })
        for reminder in result.reminders:
            items.append({
                "type": "reminder", 
                "title": reminder.title,
                "subtitle": f"📋 Due: {reminder.due_date}" if reminder.due_date else "📋 No due date"
            })
        
        return {
            "success": True,
            "message": f"Created {events_created} events and {reminders_created} reminders",
            "items": items,
            "errors": errors
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def handle_config(args, as_json: bool) -> dict:
    """Handle config command."""
    from .services.config_manager import ConfigManager
    from .models.ai_config import AIConfiguration
    
    config_manager = ConfigManager()
    
    if args.config_action == "status":
        config = config_manager.get_configuration()
        if config:
            return {
                "success": True,
                "message": "Configuration found",
                "config": {
                    "provider": config.provider,
                    "model": config.model,
                    "endpoint": config.api_endpoint
                }
            }
        return {"success": False, "error": "Not configured"}
    
    elif args.config_action == "set":
        model_defaults = {
            "openai": "gpt-4-turbo",
            "deepseek": "deepseek-chat",
            "anthropic": "claude-3-sonnet-20240229",
            "custom": "gpt-3.5-turbo"
        }
        model = args.model or model_defaults.get(args.provider, "gpt-4")
        
        config = AIConfiguration(
            provider=args.provider,
            api_key=args.api_key,
            model=model
        )
        
        if config_manager.save_configuration(config):
            return {"success": True, "message": f"Configuration saved for {args.provider}"}
        return {"success": False, "error": "Failed to save configuration"}
    
    elif args.config_action == "delete":
        config = config_manager.get_configuration()
        if config:
            config_manager.delete_api_key(config.provider)
            return {"success": True, "message": "Configuration deleted"}
        return {"success": False, "error": "No configuration to delete"}
    
    elif args.config_action == "endpoint":
        if config_manager.set_endpoint_url(args.url):
            return {"success": True, "message": f"Endpoint set to {args.url}"}
        return {"success": False, "error": "Failed to set endpoint"}
    
    return {"success": False, "error": "Unknown config action"}


def handle_list(args, as_json: bool) -> dict:
    """Handle list command."""
    from .services.tracker_service import TrackerService
    
    tracker = TrackerService()
    items = tracker.get_recent_items(args.count)
    
    return {
        "success": True,
        "message": f"Found {len(items)} items",
        "items": [
            {
                "id": item.item_id,
                "type": item.item_type,
                "title": item.title,
                "created_at": item.created_at.isoformat()
            }
            for item in items
        ]
    }


def handle_delete(args, as_json: bool) -> dict:
    """Handle delete command."""
    from .services.tracker_service import TrackerService
    from .services.config_manager import ConfigManager
    from .services.parse_service import ParseService
    from .services.eventkit_bridge import EventKitBridge
    
    tracker = TrackerService()
    
    if not args.target:
        # Show list of items to delete
        items = tracker.get_recent_items(10)
        return {
            "success": True,
            "message": "Select an item to delete",
            "items": [
                {"id": item.item_id, "title": item.title, "type": item.item_type}
                for item in items
            ]
        }
    
    if args.target == "all":
        count = len(tracker.get_all_tracked_items())
        tracker.clear_all()
        return {"success": True, "message": f"Deleted {count} items"}
    
    if args.target == "old":
        days = args.days or 7
        count = tracker.cleanup_old_items(days)
        return {"success": True, "message": f"Deleted {count} items older than {days} days"}
    
    # Delete specific item
    config_manager = ConfigManager()
    config = config_manager.get_configuration()
    
    if config:
        parse_service = ParseService(config)
        eventkit_bridge = EventKitBridge()
        success, error = parse_service.delete_tracked_item(args.target, eventkit_bridge)
        
        if success:
            return {"success": True, "message": f"Deleted item {args.target}"}
        return {"success": False, "error": error or "Failed to delete item"}
    
    return {"success": False, "error": "Not configured"}


def handle_help(args, as_json: bool) -> dict:
    """Handle help command."""
    help_text = """
Reminder-Alf - AI-powered calendar and reminder management

Commands:
  ral <text>                    Parse natural language and create events/reminders
  ral config status             Show configuration status
  ral config set <provider> <key> [model]   Set AI provider
  ral config delete             Delete configuration
  ral config endpoint <url>     Set custom API endpoint
  ral list [count]              List recent items (default: 10)
  ral delete                    Show items to delete
  ral delete <id>               Delete specific item
  ral delete all                Delete all tracked items
  ral delete old [days]         Delete items older than N days (default: 7)
  ral help                      Show this help

Providers: openai, deepseek, anthropic, custom

Examples:
  ral Meeting tomorrow at 2pm
  ral 明天下午3点开会
  ral config set openai sk-xxx gpt-4
  ral config set deepseek sk-xxx deepseek-chat
"""
    return {"success": True, "message": help_text.strip()}


def main() -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    as_json = getattr(args, "json", False)
    
    # Handle commands
    if args.command == "parse":
        result = handle_parse(args, as_json)
    elif args.command == "config":
        result = handle_config(args, as_json)
    elif args.command == "list":
        result = handle_list(args, as_json)
    elif args.command == "delete":
        result = handle_delete(args, as_json)
    elif args.command == "help" or args.command is None:
        result = handle_help(args, as_json)
    else:
        # Treat as natural language input
        args.text = [args.command] + sys.argv[2:]
        result = handle_parse(args, as_json)
    
    output_result(result, as_json)
    return 0 if result.get("success") else 1


if __name__ == "__main__":
    sys.exit(main())
