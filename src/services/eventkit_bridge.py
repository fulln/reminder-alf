"""
EventKit Bridge for macOS Calendar and Reminders integration.
"""
from typing import Optional, Tuple, List
from datetime import datetime
import EventKit
from ..models.calendar_event import CalendarEvent
from ..models.reminder import Reminder
from ..utils.logger import get_logger

logger = get_logger(__name__)


class EventKitBridge:
    """Wrapper for macOS EventKit framework to manage Calendar and Reminders."""

    def __init__(self):
        """Initialize EventKit store."""
        self.event_store = EventKit.EKEventStore.alloc().init()
        self._calendar_authorized = False
        self._reminder_authorized = False

    def request_calendar_access(self) -> bool:
        """
        Request access to Calendar.

        Returns:
            True if access granted
        """
        if self._calendar_authorized:
            return True

        # Check current authorization status
        status = EventKit.EKEventStore.authorizationStatusForEntityType_(
            EventKit.EKEntityTypeEvent
        )

        if status == EventKit.EKAuthorizationStatusAuthorized:
            self._calendar_authorized = True
            return True

        # Request access (this will show system dialog)
        granted = [False]

        def completion_handler(granted_param, error):
            granted[0] = granted_param
            if error:
                logger.error(f"Calendar access error: {error}")

        self.event_store.requestAccessToEntityType_completion_(
            EventKit.EKEntityTypeEvent, completion_handler
        )

        # In real workflow, this would be async, but for simplicity return current status
        self._calendar_authorized = granted[0]
        return granted[0]

    def request_reminder_access(self) -> bool:
        """
        Request access to Reminders.

        Returns:
            True if access granted
        """
        if self._reminder_authorized:
            return True

        status = EventKit.EKEventStore.authorizationStatusForEntityType_(
            EventKit.EKEntityTypeReminder
        )

        if status == EventKit.EKAuthorizationStatusAuthorized:
            self._reminder_authorized = True
            return True

        granted = [False]

        def completion_handler(granted_param, error):
            granted[0] = granted_param
            if error:
                logger.error(f"Reminder access error: {error}")

        self.event_store.requestAccessToEntityType_completion_(
            EventKit.EKEntityTypeReminder, completion_handler
        )

        self._reminder_authorized = granted[0]
        return granted[0]

    def get_default_calendar(self) -> Optional[EventKit.EKCalendar]:
        """Get user's default calendar."""
        return self.event_store.defaultCalendarForNewEvents()

    def get_default_reminder_list(self) -> Optional[EventKit.EKCalendar]:
        """Get user's default reminder list."""
        return self.event_store.defaultCalendarForNewReminders()

    def create_calendar_event(self, event: CalendarEvent) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Create calendar event in macOS Calendar.

        Args:
            event: CalendarEvent to create

        Returns:
            (success, event_id, error_message)
        """
        if not self.request_calendar_access():
            return False, None, "Calendar access denied. Grant permission in System Settings."

        if not event.validate():
            return False, None, "Invalid event data"

        try:
            # Create EKEvent
            ek_event = EventKit.EKEvent.eventWithEventStore_(self.event_store)
            ek_event.setTitle_(event.title)
            ek_event.setStartDate_(event.start_date)
            ek_event.setEndDate_(event.end_date)

            if event.location:
                ek_event.setLocation_(event.location)

            if event.notes:
                ek_event.setNotes_(event.notes)

            # Add tag for easy filtering/deletion
            try:
                # categories expect an array of strings
                ek_event.addCategory_("Reminder-Alf")
            except Exception:
                pass

            ek_event.setAllDay_(event.all_day)

            if event.url:
                from Foundation import NSURL
                ek_event.setURL_(NSURL.URLWithString_(event.url))

            # Set calendar
            if event.calendar_name:
                # Find calendar by name
                calendar = self._find_calendar_by_name(event.calendar_name)
                if calendar:
                    ek_event.setCalendar_(calendar)
                else:
                    logger.warning(f"Calendar '{event.calendar_name}' not found, using default")
                    ek_event.setCalendar_(self.get_default_calendar())
            else:
                ek_event.setCalendar_(self.get_default_calendar())

            # Add alarm if specified
            if event.alert_minutes_before:
                alarm = EventKit.EKAlarm.alarmWithRelativeOffset_(
                    -event.alert_minutes_before * 60
                )
                ek_event.addAlarm_(alarm)

            # Save event
            error = None
            success = self.event_store.saveEvent_span_error_(
                ek_event, EventKit.EKSpanThisEvent, error
            )

            if success:
                event_id = ek_event.eventIdentifier()
                logger.info(f"Created calendar event: {event.title} (ID: {event_id})")
                return True, event_id, None
            else:
                error_msg = str(error) if error else "Unknown error"
                logger.error(f"Failed to create event: {error_msg}")
                return False, None, error_msg

        except Exception as e:
            logger.error(f"Exception creating calendar event: {e}")
            return False, None, str(e)

    def create_reminder(self, reminder: Reminder) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Create reminder in macOS Reminders.

        Args:
            reminder: Reminder to create

        Returns:
            (success, reminder_id, error_message)
        """
        if not self.request_reminder_access():
            return False, None, "Reminders access denied. Grant permission in System Settings."

        if not reminder.validate():
            return False, None, "Invalid reminder data"

        try:
            # Create EKReminder
            ek_reminder = EventKit.EKReminder.reminderWithEventStore_(self.event_store)
            ek_reminder.setTitle_(reminder.title)

            if reminder.notes:
                ek_reminder.setNotes_(reminder.notes)

            # Set due date
            if reminder.due_date:
                from Foundation import NSCalendar, NSDateComponents
                calendar = NSCalendar.currentCalendar()
                components = calendar.components_fromDate_(
                    EventKit.NSCalendarUnitYear
                    | EventKit.NSCalendarUnitMonth
                    | EventKit.NSCalendarUnitDay
                    | EventKit.NSCalendarUnitHour
                    | EventKit.NSCalendarUnitMinute,
                    reminder.due_date,
                )
                ek_reminder.setDueDateComponents_(components)

            # Add tag for easy filtering/deletion
            try:
                ek_reminder.addCategory_("Reminder-Alf")
            except Exception:
                pass

            # Set priority (0-3 maps to EKReminderPriority)
            ek_reminder.setPriority_(reminder.priority)

            if reminder.url:
                from Foundation import NSURL
                ek_reminder.setURL_(NSURL.URLWithString_(reminder.url))

            # Set reminder list
            if reminder.list_name:
                reminder_list = self._find_reminder_list_by_name(reminder.list_name)
                if reminder_list:
                    ek_reminder.setCalendar_(reminder_list)
                else:
                    logger.warning(f"List '{reminder.list_name}' not found, using default")
                    ek_reminder.setCalendar_(self.get_default_reminder_list())
            else:
                ek_reminder.setCalendar_(self.get_default_reminder_list())

            # Save reminder
            error = None
            success = self.event_store.saveReminder_commit_error_(ek_reminder, True, error)

            if success:
                reminder_id = ek_reminder.calendarItemIdentifier()
                logger.info(f"Created reminder: {reminder.title} (ID: {reminder_id})")
                return True, reminder_id, None
            else:
                error_msg = str(error) if error else "Unknown error"
                logger.error(f"Failed to create reminder: {error_msg}")
                return False, None, error_msg

        except Exception as e:
            logger.error(f"Exception creating reminder: {e}")
            return False, None, str(e)

    def delete_calendar_event(self, event_id: str) -> Tuple[bool, Optional[str]]:
        """
        Delete calendar event by ID.

        Args:
            event_id: EventKit event identifier

        Returns:
            (success, error_message)
        """
        if not self.request_calendar_access():
            return False, "Calendar access denied"

        try:
            event = self.event_store.eventWithIdentifier_(event_id)
            if not event:
                return False, "Event not found"

            error = None
            success = self.event_store.removeEvent_span_error_(
                event, EventKit.EKSpanThisEvent, error
            )

            if success:
                logger.info(f"Deleted calendar event ID: {event_id}")
                return True, None
            else:
                error_msg = str(error) if error else "Unknown error"
                return False, error_msg

        except Exception as e:
            logger.error(f"Exception deleting event: {e}")
            return False, str(e)

    def delete_reminder(self, reminder_id: str) -> Tuple[bool, Optional[str]]:
        """
        Delete reminder by ID.

        Args:
            reminder_id: EventKit reminder identifier

        Returns:
            (success, error_message)
        """
        if not self.request_reminder_access():
            return False, "Reminders access denied"

        try:
            reminder = self.event_store.calendarItemWithIdentifier_(reminder_id)
            if not reminder:
                return False, "Reminder not found"

            error = None
            success = self.event_store.removeReminder_commit_error_(reminder, True, error)

            if success:
                logger.info(f"Deleted reminder ID: {reminder_id}")
                return True, None
            else:
                error_msg = str(error) if error else "Unknown error"
                return False, error_msg

        except Exception as e:
            logger.error(f"Exception deleting reminder: {e}")
            return False, str(e)

    def _find_calendar_by_name(self, name: str) -> Optional[EventKit.EKCalendar]:
        """Find calendar by name."""
        calendars = self.event_store.calendarsForEntityType_(EventKit.EKEntityTypeEvent)
        for calendar in calendars:
            if calendar.title() == name:
                return calendar
        return None

    def _find_reminder_list_by_name(self, name: str) -> Optional[EventKit.EKCalendar]:
        """Find reminder list by name."""
        lists = self.event_store.calendarsForEntityType_(EventKit.EKEntityTypeReminder)
        for reminder_list in lists:
            if reminder_list.title() == name:
                return reminder_list
        return None

    def cleanup_tagged_items(self, dry_run: bool = False) -> Tuple[int, int, List[str]]:
        """
        Cleanup "unexecuted" items tagged with 'Reminder-Alf'.
        
        Args:
            dry_run: If True, only count items without deleting.
            
        Returns:
            (deleted_events_count, deleted_reminders_count, item_titles)
        """
        deleted_events = 0
        deleted_reminders = 0
        titles = []
        now = datetime.now()

        # 1. Cleanup Future Events
        if self.request_calendar_access():
            # Search from now to 1 year in the future
            from Foundation import NSDate
            start_date = NSDate.date()
            end_date = NSDate.dateWithTimeIntervalSinceNow_(365 * 24 * 60 * 60)
            
            predicate = self.event_store.predicateForEventsWithStartDate_endDate_calendars_(
                start_date, end_date, None
            )
            events = self.event_store.eventsMatchingPredicate_(predicate)
            
            for event in events:
                # Check categories
                cats = event.categories()
                if cats and "Reminder-Alf" in cats:
                    titles.append(f"[Event] {event.title()}")
                    if not dry_run:
                        error = None
                        self.event_store.removeEvent_span_error_(
                            event, EventKit.EKSpanThisEvent, error
                        )
                    deleted_events += 1

        # 2. Cleanup Incomplete Reminders
        if self.request_reminder_access():
            import threading
            reminders_done = threading.Event()
            found_reminders = []

            def reminders_completion(reminders):
                if reminders:
                    for r in reminders:
                        # Check categories and incomplete status
                        # Note: EKReminder.isCompleted() or completed()
                        if not r.isCompleted():
                            cats = r.categories()
                            if cats and "Reminder-Alf" in cats:
                                found_reminders.append(r)
                reminders_done.set()

            calendars = self.event_store.calendarsForEntityType_(EventKit.EKEntityTypeReminder)
            reminders_predicate = self.event_store.predicateForRemindersInCalendars_(calendars)
            
            # This call is async
            self.event_store.fetchRemindersMatchingPredicate_completion_(
                reminders_predicate, reminders_completion
            )
            
            # Wait for completion (max 10s)
            reminders_done.wait(timeout=10)
            
            for reminder in found_reminders:
                titles.append(f"[Reminder] {reminder.title()}")
                if not dry_run:
                    error = None
                    # REMEMBER: saveReminder_commit_error_ or removeReminder_commit_error_
                    self.event_store.removeReminder_commit_error_(reminder, True, error)
                deleted_reminders += 1
            
        return deleted_events, deleted_reminders, titles
