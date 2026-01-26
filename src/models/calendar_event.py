"""
CalendarEvent data class for calendar events.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Literal


@dataclass
class CalendarEvent:
    """Represents a calendar event to be created in macOS Calendar."""

    title: str
    start_date: datetime
    end_date: datetime
    location: Optional[str] = None
    notes: Optional[str] = None
    calendar_name: Optional[str] = None
    all_day: bool = False
    url: Optional[str] = None

    # Recurrence
    recurrence_frequency: Optional[Literal["daily", "weekly", "monthly", "yearly"]] = None
    recurrence_interval: int = 1
    recurrence_end_date: Optional[datetime] = None

    # Alerts
    alert_minutes_before: Optional[int] = None

    def validate(self) -> bool:
        """Validate the event data."""
        if not self.title or not self.title.strip():
            return False
        if self.end_date <= self.start_date:
            return False
        if self.recurrence_frequency and self.recurrence_interval < 1:
            return False
        if self.alert_minutes_before is not None and self.alert_minutes_before < 0:
            return False
        return True

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "title": self.title,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "location": self.location,
            "notes": self.notes,
            "calendar_name": self.calendar_name,
            "all_day": self.all_day,
            "url": self.url,
            "recurrence_frequency": self.recurrence_frequency,
            "recurrence_interval": self.recurrence_interval,
            "recurrence_end_date": self.recurrence_end_date.isoformat()
            if self.recurrence_end_date
            else None,
            "alert_minutes_before": self.alert_minutes_before,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CalendarEvent":
        """Create from dictionary."""
        return cls(
            title=data["title"],
            start_date=datetime.fromisoformat(data["start_date"]),
            end_date=datetime.fromisoformat(data["end_date"]),
            location=data.get("location"),
            notes=data.get("notes"),
            calendar_name=data.get("calendar_name"),
            all_day=data.get("all_day", False),
            url=data.get("url"),
            recurrence_frequency=data.get("recurrence_frequency"),
            recurrence_interval=data.get("recurrence_interval", 1),
            recurrence_end_date=datetime.fromisoformat(data["recurrence_end_date"])
            if data.get("recurrence_end_date")
            else None,
            alert_minutes_before=data.get("alert_minutes_before"),
        )
