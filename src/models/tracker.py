"""
CreatedItemTracker for tracking created calendar events and reminders.
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Literal
from pathlib import Path
import json


@dataclass
class CreatedItem:
    """Represents a created calendar item for tracking."""

    item_type: Literal["calendar_event", "reminder"]
    item_id: str  # EventKit identifier
    title: str
    created_at: datetime
    calendar_or_list: str
    source_text: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "item_type": self.item_type,
            "item_id": self.item_id,
            "title": self.title,
            "created_at": self.created_at.isoformat(),
            "calendar_or_list": self.calendar_or_list,
            "source_text": self.source_text,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CreatedItem":
        """Create from dictionary."""
        return cls(
            item_type=data["item_type"],
            item_id=data["item_id"],
            title=data["title"],
            created_at=datetime.fromisoformat(data["created_at"]),
            calendar_or_list=data["calendar_or_list"],
            source_text=data.get("source_text", ""),
        )


class CreatedItemTracker:
    """Tracks created items for undo functionality."""

    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.items: List[CreatedItem] = []
        self.load()

    def add(self, item: CreatedItem) -> None:
        """Add a created item."""
        self.items.append(item)
        self.save()

    def get_all(self) -> List[CreatedItem]:
        """Get all tracked items."""
        return self.items.copy()

    def get_recent(self, limit: int = 10) -> List[CreatedItem]:
        """Get recent items."""
        return sorted(self.items, key=lambda x: x.created_at, reverse=True)[:limit]

    def remove(self, item_id: str) -> bool:
        """Remove an item by ID. Returns True if found."""
        original_length = len(self.items)
        self.items = [item for item in self.items if item.item_id != item_id]
        if len(self.items) < original_length:
            self.save()
            return True
        return False

    def clear_all(self) -> int:
        """Clear all items. Returns count of removed items."""
        count = len(self.items)
        self.items.clear()
        self.save()
        return count

    def clear_old(self, days: int = 7) -> int:
        """Clear items older than specified days. Returns count removed."""
        cutoff = datetime.now() - timedelta(days=days)
        original_count = len(self.items)
        self.items = [item for item in self.items if item.created_at > cutoff]
        if len(self.items) < original_count:
            self.save()
        return original_count - len(self.items)

    def save(self) -> None:
        """Save to disk with atomic write."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        data = {"version": "1.0", "items": [item.to_dict() for item in self.items]}

        # Atomic write: write to temp file then rename
        temp_path = self.storage_path.with_suffix(".tmp")
        with open(temp_path, "w") as f:
            json.dump(data, f, indent=2)
        temp_path.replace(self.storage_path)

    def load(self) -> None:
        """Load from disk."""
        if not self.storage_path.exists():
            return

        try:
            with open(self.storage_path, "r") as f:
                data = json.load(f)
            self.items = [CreatedItem.from_dict(item_data) for item_data in data.get("items", [])]
        except (json.JSONDecodeError, KeyError) as e:
            # Log error but don't fail - start with empty tracker
            print(f"Warning: Could not load tracking data: {e}")
            self.items = []
