"""
Reminder data class for reminders/tasks.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Literal


@dataclass
class Reminder:
    """Represents a reminder/task to be created in macOS Reminders."""

    title: str
    notes: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Literal[0, 1, 2, 3] = 0  # 0=None, 1=Low, 2=Medium, 3=High
    list_name: Optional[str] = None
    url: Optional[str] = None

    # Recurrence
    recurrence_frequency: Optional[Literal["daily", "weekly", "monthly", "yearly"]] = None
    recurrence_interval: int = 1
    recurrence_end_date: Optional[datetime] = None

    def validate(self) -> bool:
        """Validate the reminder data."""
        if not self.title or not self.title.strip():
            return False
        if self.priority not in [0, 1, 2, 3]:
            return False
        if self.recurrence_frequency and self.recurrence_interval < 1:
            return False
        return True

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "title": self.title,
            "notes": self.notes,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "priority": self.priority,
            "list_name": self.list_name,
            "url": self.url,
            "recurrence_frequency": self.recurrence_frequency,
            "recurrence_interval": self.recurrence_interval,
            "recurrence_end_date": self.recurrence_end_date.isoformat()
            if self.recurrence_end_date
            else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Reminder":
        """Create from dictionary."""
        return cls(
            title=data["title"],
            notes=data.get("notes"),
            due_date=datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None,
            priority=data.get("priority", 0),
            list_name=data.get("list_name"),
            url=data.get("url"),
            recurrence_frequency=data.get("recurrence_frequency"),
            recurrence_interval=data.get("recurrence_interval", 1),
            recurrence_end_date=datetime.fromisoformat(data["recurrence_end_date"])
            if data.get("recurrence_end_date")
            else None,
        )
