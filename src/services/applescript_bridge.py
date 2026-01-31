"""
AppleScript Bridge for macOS Calendar and Reminders integration.
Uses osascript to bypass EventKit permission issues.
"""
import subprocess
from typing import Optional, Tuple
from datetime import datetime
from ..models.calendar_event import CalendarEvent
from ..models.reminder import Reminder
from ..utils.logger import get_logger

logger = get_logger(__name__)


class AppleScriptBridge:
    """Wrapper for AppleScript to manage Calendar and Reminders."""

    def __init__(self):
        """Initialize AppleScript bridge."""
        self._default_calendar = None
        self._default_reminder_list = None

    def _run_applescript(self, script: str) -> Tuple[bool, str, str]:
        """
        Run AppleScript and return result.
        
        Returns:
            (success, stdout, stderr)
        """
        try:
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
        except subprocess.TimeoutExpired:
            return False, "", "AppleScript timeout"
        except Exception as e:
            return False, "", str(e)

    def get_calendars(self) -> list[str]:
        """Get list of calendar names."""
        script = 'tell application "Calendar" to get name of calendars'
        success, stdout, stderr = self._run_applescript(script)
        if success and stdout:
            return [name.strip() for name in stdout.split(", ")]
        return []

    def get_reminder_lists(self) -> list[str]:
        """Get list of reminder list names."""
        script = 'tell application "Reminders" to get name of lists'
        success, stdout, stderr = self._run_applescript(script)
        if success and stdout:
            return [name.strip() for name in stdout.split(", ")]
        return []

    def create_calendar_event(self, event: CalendarEvent) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Create calendar event using AppleScript.

        Args:
            event: CalendarEvent to create

        Returns:
            (success, event_id, error_message)
        """
        if not event.validate():
            return False, None, "Invalid event data"

        try:
            # Format dates for AppleScript
            start_str = self._format_date_for_applescript(event.start_date)
            end_str = self._format_date_for_applescript(event.end_date)
            
            # Escape title for AppleScript
            title = event.title.replace('"', '\\"')
            
            # Use default calendar or specified one
            calendar_name = event.calendar_name or "工作"
            
            # Build properties
            properties = f'summary:"{title}", start date:{start_str}, end date:{end_str}'
            
            if event.location:
                location = event.location.replace('"', '\\"')
                properties += f', location:"{location}"'
            
            if event.notes:
                notes = event.notes.replace('"', '\\"')
                properties += f', description:"{notes}"'
            
            script = f'''
tell application "Calendar"
    tell calendar "{calendar_name}"
        set newEvent to make new event with properties {{{properties}}}
        return id of newEvent
    end tell
end tell
'''
            success, stdout, stderr = self._run_applescript(script)
            
            if success:
                event_id = stdout.strip()
                logger.info(f"Created calendar event: {event.title} (ID: {event_id})")
                return True, event_id, None
            else:
                logger.error(f"Failed to create event: {stderr}")
                return False, None, stderr

        except Exception as e:
            logger.error(f"Exception creating calendar event: {e}")
            return False, None, str(e)

    def create_reminder(self, reminder: Reminder) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Create reminder using AppleScript.

        Args:
            reminder: Reminder to create

        Returns:
            (success, reminder_id, error_message)
        """
        if not reminder.validate():
            return False, None, "Invalid reminder data"

        try:
            # Escape title
            title = reminder.title.replace('"', '\\"')
            
            # Use default list or specified one
            list_name = reminder.list_name or "提醒"
            
            # Build properties
            properties = f'name:"{title}"'
            
            if reminder.due_date:
                due_str = self._format_date_for_applescript(reminder.due_date)
                properties += f', due date:{due_str}'
            
            if reminder.notes:
                notes = reminder.notes.replace('"', '\\"')
                properties += f', body:"{notes}"'
            
            script = f'''
tell application "Reminders"
    tell list "{list_name}"
        set newReminder to make new reminder with properties {{{properties}}}
        return id of newReminder
    end tell
end tell
'''
            success, stdout, stderr = self._run_applescript(script)
            
            if success:
                reminder_id = stdout.strip()
                logger.info(f"Created reminder: {reminder.title} (ID: {reminder_id})")
                return True, reminder_id, None
            else:
                logger.error(f"Failed to create reminder: {stderr}")
                return False, None, stderr

        except Exception as e:
            logger.error(f"Exception creating reminder: {e}")
            return False, None, str(e)

    def delete_calendar_event(self, event_id: str) -> Tuple[bool, Optional[str]]:
        """Delete calendar event by ID."""
        script = f'''
tell application "Calendar"
    set theEvents to every event of every calendar whose id is "{event_id}"
    repeat with eventList in theEvents
        repeat with theEvent in eventList
            delete theEvent
        end repeat
    end repeat
end tell
'''
        success, stdout, stderr = self._run_applescript(script)
        if success:
            logger.info(f"Deleted calendar event ID: {event_id}")
            return True, None
        return False, stderr

    def delete_reminder(self, reminder_id: str) -> Tuple[bool, Optional[str]]:
        """Delete reminder by ID."""
        script = f'''
tell application "Reminders"
    set theReminders to every reminder of every list whose id is "{reminder_id}"
    repeat with reminderList in theReminders
        repeat with theReminder in reminderList
            delete theReminder
        end repeat
    end repeat
end tell
'''
        success, stdout, stderr = self._run_applescript(script)
        if success:
            logger.info(f"Deleted reminder ID: {reminder_id}")
            return True, None
        return False, stderr

    def _format_date_for_applescript(self, dt: datetime) -> str:
        """Format datetime for AppleScript."""
        # AppleScript date format: date "2026-02-01 15:00:00"
        return f'date "{dt.strftime("%Y-%m-%d %H:%M:%S")}"'
