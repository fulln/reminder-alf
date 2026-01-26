"""
FeedbackBuilder for creating Alfred JSON feedback.
"""
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
import json
from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class FeedbackItem:
    """Alfred feedback item."""

    title: str
    subtitle: str = ""
    arg: Optional[str] = None
    valid: bool = True
    icon: Optional[str] = None
    autocomplete: Optional[str] = None
    uid: Optional[str] = None
    type_: Optional[str] = None  # "default" or "file" or "file:skipcheck"
    mods: Dict[str, Any] = field(default_factory=dict)
    text: Dict[str, str] = field(default_factory=dict)
    quicklookurl: Optional[str] = None
    variables: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to Alfred JSON format.

        Returns:
            Dictionary for JSON serialization
        """
        result: Dict[str, Any] = {
            "title": self.title,
            "subtitle": self.subtitle,
            "valid": self.valid,
        }

        if self.arg is not None:
            result["arg"] = self.arg

        if self.icon:
            result["icon"] = {"path": self.icon}

        if self.autocomplete:
            result["autocomplete"] = self.autocomplete

        if self.uid:
            result["uid"] = self.uid

        if self.type_:
            result["type"] = self.type_

        if self.mods:
            result["mods"] = self.mods

        if self.text:
            result["text"] = self.text

        if self.quicklookurl:
            result["quicklookurl"] = self.quicklookurl

        if self.variables:
            result["variables"] = self.variables

        return result


class FeedbackBuilder:
    """Builder for Alfred workflow feedback."""

    # Icon constants (using system icons)
    ICON_ERROR = "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertStopIcon.icns"
    ICON_WARNING = "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertCautionIcon.icns"
    ICON_INFO = "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/ToolbarInfo.icns"
    ICON_SUCCESS = "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/ToolbarInfo.icns"
    ICON_CALENDAR = "/System/Applications/Calendar.app/Contents/Resources/App.icns"
    ICON_REMINDERS = "/System/Applications/Reminders.app/Contents/Resources/App.icns"
    ICON_GEAR = "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/ToolbarAdvanced.icns"
    ICON_DELETE = "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/TrashIcon.icns"

    def __init__(self):
        """Initialize FeedbackBuilder."""
        self.items: List[FeedbackItem] = []
        self.variables: Dict[str, str] = {}

    def add_item(self, item: FeedbackItem) -> "FeedbackBuilder":
        """
        Add feedback item.

        Args:
            item: FeedbackItem to add

        Returns:
            Self for chaining
        """
        self.items.append(item)
        return self

    def add_error(
        self,
        title: str,
        subtitle: str = "",
        suggestion: Optional[str] = None
    ) -> "FeedbackBuilder":
        """
        Add error feedback item.

        Args:
            title: Error title
            subtitle: Error details
            suggestion: Optional suggestion for user

        Returns:
            Self for chaining
        """
        full_subtitle = subtitle
        if suggestion:
            full_subtitle = f"{subtitle}\n💡 {suggestion}" if subtitle else f"💡 {suggestion}"

        item = FeedbackItem(
            title=f"❌ {title}",
            subtitle=full_subtitle,
            valid=False,
            icon=self.ICON_ERROR,
        )
        self.items.append(item)
        return self

    def add_warning(self, title: str, subtitle: str = "") -> "FeedbackBuilder":
        """
        Add warning feedback item.

        Args:
            title: Warning title
            subtitle: Warning details

        Returns:
            Self for chaining
        """
        item = FeedbackItem(
            title=f"⚠️ {title}",
            subtitle=subtitle,
            valid=False,
            icon=self.ICON_WARNING,
        )
        self.items.append(item)
        return self

    def add_info(self, title: str, subtitle: str = "") -> "FeedbackBuilder":
        """
        Add info feedback item.

        Args:
            title: Info title
            subtitle: Info details

        Returns:
            Self for chaining
        """
        item = FeedbackItem(
            title=f"ℹ️ {title}",
            subtitle=subtitle,
            valid=False,
            icon=self.ICON_INFO,
        )
        self.items.append(item)
        return self

    def add_success(
        self,
        title: str,
        subtitle: str = "",
        arg: Optional[str] = None
    ) -> "FeedbackBuilder":
        """
        Add success feedback item.

        Args:
            title: Success title
            subtitle: Success details
            arg: Optional argument to pass

        Returns:
            Self for chaining
        """
        item = FeedbackItem(
            title=f"✅ {title}",
            subtitle=subtitle,
            arg=arg,
            valid=True,
            icon=self.ICON_SUCCESS,
        )
        self.items.append(item)
        return self

    def add_calendar_event(
        self,
        title: str,
        start_time: str,
        location: Optional[str] = None,
        arg: Optional[str] = None
    ) -> "FeedbackBuilder":
        """
        Add calendar event feedback item.

        Args:
            title: Event title
            start_time: Event start time
            location: Event location
            arg: Argument to pass

        Returns:
            Self for chaining
        """
        subtitle = f"📅 {start_time}"
        if location:
            subtitle += f" | 📍 {location}"

        item = FeedbackItem(
            title=title,
            subtitle=subtitle,
            arg=arg,
            valid=True,
            icon=self.ICON_CALENDAR,
        )
        self.items.append(item)
        return self

    def add_reminder(
        self,
        title: str,
        due_date: Optional[str] = None,
        priority: int = 0,
        arg: Optional[str] = None
    ) -> "FeedbackBuilder":
        """
        Add reminder feedback item.

        Args:
            title: Reminder title
            due_date: Due date string
            priority: Priority level (0-3)
            arg: Argument to pass

        Returns:
            Self for chaining
        """
        priority_icons = {0: "", 1: "🔵", 2: "🟡", 3: "🔴"}
        priority_icon = priority_icons.get(priority, "")

        subtitle = "📋 Reminder"
        if due_date:
            subtitle += f" | Due: {due_date}"
        if priority_icon:
            subtitle = f"{priority_icon} {subtitle}"

        item = FeedbackItem(
            title=title,
            subtitle=subtitle,
            arg=arg,
            valid=True,
            icon=self.ICON_REMINDERS,
        )
        self.items.append(item)
        return self

    def add_loading(self, message: str = "Processing...") -> "FeedbackBuilder":
        """
        Add loading indicator.

        Args:
            message: Loading message

        Returns:
            Self for chaining
        """
        item = FeedbackItem(
            title=f"⏳ {message}",
            subtitle="Please wait...",
            valid=False,
            icon=self.ICON_INFO,
        )
        self.items.append(item)
        return self

    def add_progress(
        self,
        current: int,
        total: int,
        message: str = "Processing"
    ) -> "FeedbackBuilder":
        """
        Add progress indicator.

        Args:
            current: Current progress
            total: Total items
            message: Progress message

        Returns:
            Self for chaining
        """
        percentage = int((current / total) * 100) if total > 0 else 0
        progress_bar = self._create_progress_bar(percentage)

        item = FeedbackItem(
            title=f"{message} ({current}/{total})",
            subtitle=f"{progress_bar} {percentage}%",
            valid=False,
            icon=self.ICON_INFO,
        )
        self.items.append(item)
        return self

    def _create_progress_bar(self, percentage: int, width: int = 20) -> str:
        """
        Create text progress bar.

        Args:
            percentage: Progress percentage (0-100)
            width: Bar width in characters

        Returns:
            Progress bar string
        """
        filled = int((percentage / 100) * width)
        bar = "█" * filled + "░" * (width - filled)
        return bar

    def set_variable(self, key: str, value: str) -> "FeedbackBuilder":
        """
        Set workflow variable.

        Args:
            key: Variable name
            value: Variable value

        Returns:
            Self for chaining
        """
        self.variables[key] = value
        return self

    def to_json(self) -> str:
        """
        Convert to Alfred JSON format.

        Returns:
            JSON string
        """
        result: Dict[str, Any] = {
            "items": [item.to_dict() for item in self.items]
        }

        if self.variables:
            result["variables"] = self.variables

        return json.dumps(result, ensure_ascii=False, indent=2)

    def clear(self) -> "FeedbackBuilder":
        """
        Clear all items and variables.

        Returns:
            Self for chaining
        """
        self.items.clear()
        self.variables.clear()
        return self
