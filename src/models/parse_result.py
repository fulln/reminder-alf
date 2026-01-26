"""
ParseResult data class for AI parsing output.
"""
from dataclasses import dataclass, field
from typing import Optional, List
from .calendar_event import CalendarEvent
from .reminder import Reminder


@dataclass
class ParseResult:
    """Result from AI parsing of natural language input."""

    calendar_events: List[CalendarEvent] = field(default_factory=list)
    reminders: List[Reminder] = field(default_factory=list)
    raw_text: str = ""
    confidence: float = 1.0
    ambiguities: List[str] = field(default_factory=list)
    raw_response: Optional[str] = None
    errors: List[str] = field(default_factory=list)

    def is_valid(self) -> bool:
        """Check if parse result is valid."""
        if self.errors:
            return False
        # At least one valid event or reminder
        for event in self.calendar_events:
            if event.validate():
                return True
        for reminder in self.reminders:
            if reminder.validate():
                return True
        return False

    def is_empty(self) -> bool:
        """Check if parsing found nothing."""
        return len(self.calendar_events) == 0 and len(self.reminders) == 0

    def total_items(self) -> int:
        """Count total parsed items."""
        return len(self.calendar_events) + len(self.reminders)

    def has_ambiguities(self) -> bool:
        """Check if user confirmation needed."""
        return len(self.ambiguities) > 0 or self.confidence < 0.7

    def to_dict(self) -> dict:
        """Convert to dictionary for logging/serialization."""
        return {
            "calendar_events": [e.to_dict() for e in self.calendar_events],
            "reminders": [r.to_dict() for r in self.reminders],
            "raw_text": self.raw_text,
            "confidence": self.confidence,
            "ambiguities": self.ambiguities,
            "raw_response": self.raw_response,
            "errors": self.errors,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ParseResult":
        """Create from dictionary."""
        return cls(
            calendar_events=[
                CalendarEvent.from_dict(e) for e in data.get("calendar_events", [])
            ],
            reminders=[Reminder.from_dict(r) for r in data.get("reminders", [])],
            raw_text=data.get("raw_text", ""),
            confidence=data.get("confidence", 1.0),
            ambiguities=data.get("ambiguities", []),
            raw_response=data.get("raw_response"),
            errors=data.get("errors", []),
        )

    @classmethod
    def error(cls, error_message: str, raw_text: str = "") -> "ParseResult":
        """Create error result."""
        return cls(raw_text=raw_text, confidence=0.0, errors=[error_message])
