# Phase 1: Data Model

## Overview
This document defines the core data structures used in the AI Calendar Reminder workflow.

## Core Data Structures

### CalendarEvent

Represents a calendar event to be created in macOS Calendar.

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Literal

@dataclass
class CalendarEvent:
    """Represents a calendar event."""
    
    title: str
    start_date: datetime
    end_date: datetime
    location: Optional[str] = None
    notes: Optional[str] = None
    calendar_name: Optional[str] = None
    all_day: bool = False
    url: Optional[str] = None
    
    # Recurrence
    recurrence_frequency: Optional[Literal['daily', 'weekly', 'monthly', 'yearly']] = None
    recurrence_interval: int = 1
    recurrence_end_date: Optional[datetime] = None
    
    # Alerts
    alert_minutes_before: Optional[int] = None
    
    def validate(self) -> bool:
        """Validate the event data."""
        if not self.title:
            return False
        if self.end_date <= self.start_date:
            return False
        if self.recurrence_frequency and self.recurrence_interval < 1:
            return False
        return True
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'title': self.title,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'location': self.location,
            'notes': self.notes,
            'calendar_name': self.calendar_name,
            'all_day': self.all_day,
            'url': self.url,
            'recurrence_frequency': self.recurrence_frequency,
            'recurrence_interval': self.recurrence_interval,
            'recurrence_end_date': self.recurrence_end_date.isoformat() if self.recurrence_end_date else None,
            'alert_minutes_before': self.alert_minutes_before,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CalendarEvent':
        """Create from dictionary."""
        return cls(
            title=data['title'],
            start_date=datetime.fromisoformat(data['start_date']),
            end_date=datetime.fromisoformat(data['end_date']),
            location=data.get('location'),
            notes=data.get('notes'),
            calendar_name=data.get('calendar_name'),
            all_day=data.get('all_day', False),
            url=data.get('url'),
            recurrence_frequency=data.get('recurrence_frequency'),
            recurrence_interval=data.get('recurrence_interval', 1),
            recurrence_end_date=datetime.fromisoformat(data['recurrence_end_date']) if data.get('recurrence_end_date') else None,
            alert_minutes_before=data.get('alert_minutes_before'),
        )
```

**Field Descriptions**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | str | Yes | Event title/summary |
| `start_date` | datetime | Yes | Event start time |
| `end_date` | datetime | Yes | Event end time |
| `location` | str | No | Physical or virtual location |
| `notes` | str | No | Additional details |
| `calendar_name` | str | No | Target calendar (default if not specified) |
| `all_day` | bool | No | All-day event flag |
| `url` | str | No | Associated URL |
| `recurrence_frequency` | str | No | How often to repeat |
| `recurrence_interval` | int | No | Repeat every N periods |
| `recurrence_end_date` | datetime | No | When to stop repeating |
| `alert_minutes_before` | int | No | Alert time in minutes before event |

**Examples**:

```python
# Simple event
event = CalendarEvent(
    title="Team Meeting",
    start_date=datetime(2024, 1, 15, 14, 0),
    end_date=datetime(2024, 1, 15, 15, 0),
    location="Conference Room A"
)

# All-day event
event = CalendarEvent(
    title="Company Holiday",
    start_date=datetime(2024, 12, 25, 0, 0),
    end_date=datetime(2024, 12, 26, 0, 0),
    all_day=True
)

# Recurring event
event = CalendarEvent(
    title="Weekly Standup",
    start_date=datetime(2024, 1, 15, 9, 0),
    end_date=datetime(2024, 1, 15, 9, 30),
    recurrence_frequency='weekly',
    recurrence_interval=1,
    alert_minutes_before=15
)
```

### Reminder

Represents a reminder to be created in macOS Reminders.

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Literal

@dataclass
class Reminder:
    """Represents a reminder item."""
    
    title: str
    notes: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Literal[0, 1, 2, 3] = 0  # 0=None, 1=Low, 2=Medium, 3=High
    list_name: Optional[str] = None
    url: Optional[str] = None
    
    # Recurrence (similar to events)
    recurrence_frequency: Optional[Literal['daily', 'weekly', 'monthly', 'yearly']] = None
    recurrence_interval: int = 1
    recurrence_end_date: Optional[datetime] = None
    
    def validate(self) -> bool:
        """Validate the reminder data."""
        if not self.title:
            return False
        if self.priority not in [0, 1, 2, 3]:
            return False
        if self.recurrence_frequency and self.recurrence_interval < 1:
            return False
        return True
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'title': self.title,
            'notes': self.notes,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'priority': self.priority,
            'list_name': self.list_name,
            'url': self.url,
            'recurrence_frequency': self.recurrence_frequency,
            'recurrence_interval': self.recurrence_interval,
            'recurrence_end_date': self.recurrence_end_date.isoformat() if self.recurrence_end_date else None,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Reminder':
        """Create from dictionary."""
        return cls(
            title=data['title'],
            notes=data.get('notes'),
            due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None,
            priority=data.get('priority', 0),
            list_name=data.get('list_name'),
            url=data.get('url'),
            recurrence_frequency=data.get('recurrence_frequency'),
            recurrence_interval=data.get('recurrence_interval', 1),
            recurrence_end_date=datetime.fromisoformat(data['recurrence_end_date']) if data.get('recurrence_end_date') else None,
        )
```

**Field Descriptions**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | str | Yes | Reminder title |
| `notes` | str | No | Additional details |
| `due_date` | datetime | No | When reminder is due |
| `priority` | int | No | Priority level (0-3) |
| `list_name` | str | No | Target reminder list |
| `url` | str | No | Associated URL |
| `recurrence_frequency` | str | No | How often to repeat |
| `recurrence_interval` | int | No | Repeat every N periods |
| `recurrence_end_date` | datetime | No | When to stop repeating |

**Priority Levels**:
- `0`: None (default)
- `1`: Low (!)
- `2`: Medium (!!)
- `3`: High (!!!)

**Examples**:

```python
# Simple reminder
reminder = Reminder(
    title="Buy groceries",
    due_date=datetime(2024, 1, 15, 18, 0),
    priority=2
)

# Reminder without due date
reminder = Reminder(
    title="Read documentation",
    notes="EventKit framework docs",
    priority=1
)

# Recurring reminder
reminder = Reminder(
    title="Water plants",
    recurrence_frequency='weekly',
    recurrence_interval=1,
    priority=2
)
```

### AIConfiguration

Configuration for AI service settings.

```python
from dataclasses import dataclass
from typing import Literal, Optional

@dataclass
class AIConfiguration:
    """Configuration for AI services."""
    
    provider: Literal['openai', 'anthropic', 'gemini']
    model: str
    api_key: str
    temperature: float = 0.7
    max_tokens: int = 1024
    timeout: int = 30
    
    # Provider-specific settings
    organization_id: Optional[str] = None  # OpenAI
    
    def validate(self) -> bool:
        """Validate configuration."""
        if self.provider not in ['openai', 'anthropic', 'gemini']:
            return False
        if not self.api_key:
            return False
        if not 0 <= self.temperature <= 2:
            return False
        if self.max_tokens < 1:
            return False
        return True
    
    def to_dict(self) -> dict:
        """Convert to dictionary (excluding sensitive data)."""
        return {
            'provider': self.provider,
            'model': self.model,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'timeout': self.timeout,
        }
    
    @classmethod
    def from_dict(cls, data: dict, api_key: str) -> 'AIConfiguration':
        """Create from dictionary with API key from keyring."""
        return cls(
            provider=data['provider'],
            model=data['model'],
            api_key=api_key,
            temperature=data.get('temperature', 0.7),
            max_tokens=data.get('max_tokens', 1024),
            timeout=data.get('timeout', 30),
            organization_id=data.get('organization_id'),
        )
```

**Default Configurations**:

```python
# OpenAI
openai_config = AIConfiguration(
    provider='openai',
    model='gpt-4-turbo',
    api_key='sk-...',
    temperature=0.7,
    max_tokens=1024
)

# Anthropic
anthropic_config = AIConfiguration(
    provider='anthropic',
    model='claude-3-sonnet-20240229',
    api_key='sk-ant-...',
    temperature=0.7,
    max_tokens=1024
)

# Gemini
gemini_config = AIConfiguration(
    provider='gemini',
    model='gemini-pro',
    api_key='AI...',
    temperature=0.7,
    max_tokens=1024
)
```

### ParseResult

Result from AI parsing of natural language input.

```python
from dataclasses import dataclass
from typing import Optional, Literal, List

@dataclass
class ParseResult:
    """Result from parsing natural language input."""
    
    item_type: Literal['event', 'reminder']
    event: Optional[CalendarEvent] = None
    reminder: Optional[Reminder] = None
    confidence: float = 1.0
    raw_response: Optional[str] = None
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
    
    def is_valid(self) -> bool:
        """Check if parse result is valid."""
        if self.errors:
            return False
        if self.item_type == 'event':
            return self.event is not None and self.event.validate()
        elif self.item_type == 'reminder':
            return self.reminder is not None and self.reminder.validate()
        return False
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'item_type': self.item_type,
            'event': self.event.to_dict() if self.event else None,
            'reminder': self.reminder.to_dict() if self.reminder else None,
            'confidence': self.confidence,
            'raw_response': self.raw_response,
            'errors': self.errors,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ParseResult':
        """Create from dictionary."""
        return cls(
            item_type=data['item_type'],
            event=CalendarEvent.from_dict(data['event']) if data.get('event') else None,
            reminder=Reminder.from_dict(data['reminder']) if data.get('reminder') else None,
            confidence=data.get('confidence', 1.0),
            raw_response=data.get('raw_response'),
            errors=data.get('errors', []),
        )
```

**Examples**:

```python
# Successful event parse
result = ParseResult(
    item_type='event',
    event=CalendarEvent(
        title="Team Meeting",
        start_date=datetime(2024, 1, 15, 14, 0),
        end_date=datetime(2024, 1, 15, 15, 0)
    ),
    confidence=0.95
)

# Successful reminder parse
result = ParseResult(
    item_type='reminder',
    reminder=Reminder(
        title="Buy groceries",
        due_date=datetime(2024, 1, 15, 18, 0),
        priority=2
    ),
    confidence=0.90
)

# Failed parse
result = ParseResult(
    item_type='event',
    event=None,
    confidence=0.3,
    errors=["Could not determine event time"]
)
```

### CreatedItemTracker

Tracks created events and reminders for undo functionality.

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List, Literal
import json
from pathlib import Path

@dataclass
class CreatedItem:
    """Represents a created calendar item."""
    
    item_type: Literal['event', 'reminder']
    item_id: str  # EventKit identifier
    title: str
    created_at: datetime
    calendar_or_list: str
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'item_type': self.item_type,
            'item_id': self.item_id,
            'title': self.title,
            'created_at': self.created_at.isoformat(),
            'calendar_or_list': self.calendar_or_list,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CreatedItem':
        """Create from dictionary."""
        return cls(
            item_type=data['item_type'],
            item_id=data['item_id'],
            title=data['title'],
            created_at=datetime.fromisoformat(data['created_at']),
            calendar_or_list=data['calendar_or_list'],
        )

class CreatedItemTracker:
    """Tracks created items for undo functionality."""
    
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.items: List[CreatedItem] = []
        self.load()
    
    def add(self, item: CreatedItem):
        """Add a created item."""
        self.items.append(item)
        self.save()
    
    def get_recent(self, limit: int = 10) -> List[CreatedItem]:
        """Get recent items."""
        return sorted(
            self.items,
            key=lambda x: x.created_at,
            reverse=True
        )[:limit]
    
    def remove(self, item_id: str) -> bool:
        """Remove an item by ID."""
        original_length = len(self.items)
        self.items = [item for item in self.items if item.item_id != item_id]
        if len(self.items) < original_length:
            self.save()
            return True
        return False
    
    def clear_old(self, days: int = 7):
        """Clear items older than specified days."""
        cutoff = datetime.now() - timedelta(days=days)
        self.items = [
            item for item in self.items
            if item.created_at > cutoff
        ]
        self.save()
    
    def save(self):
        """Save to disk."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            'items': [item.to_dict() for item in self.items]
        }
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load(self):
        """Load from disk."""
        if not self.storage_path.exists():
            return
        
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
            self.items = [
                CreatedItem.from_dict(item_data)
                for item_data in data.get('items', [])
            ]
        except Exception as e:
            # Log error but don't fail
            self.items = []
```

**Usage Example**:

```python
from pathlib import Path

# Initialize tracker
tracker = CreatedItemTracker(
    Path.home() / 'Library/Application Support/Alfred/Workflow Data/com.example.reminder-alf/created_items.json'
)

# Add created event
tracker.add(CreatedItem(
    item_type='event',
    item_id='ABC123',
    title='Team Meeting',
    created_at=datetime.now(),
    calendar_or_list='Work'
))

# Get recent items
recent = tracker.get_recent(limit=5)

# Remove item
tracker.remove('ABC123')

# Clean up old items
tracker.clear_old(days=7)
```

## Data Flow

```
User Input (Natural Language)
    ↓
AI Service (OpenAI/Anthropic/Gemini)
    ↓
ParseResult (validated)
    ↓
CalendarEvent OR Reminder
    ↓
EventKit (macOS)
    ↓
CreatedItem (tracking)
```

## Validation Rules

### CalendarEvent Validation
1. Title must not be empty
2. End date must be after start date
3. If recurring, interval must be >= 1
4. If all-day, times should be midnight
5. Alert minutes must be positive if set

### Reminder Validation
1. Title must not be empty
2. Priority must be 0-3
3. If recurring, interval must be >= 1
4. Due date must be in future (optional)

### ParseResult Validation
1. Must have either event or reminder (not both)
2. Item type must match which field is set
3. The event/reminder must pass its own validation
4. Confidence should be 0.0-1.0

## Error Handling

All data classes should handle errors gracefully:

```python
try:
    event = CalendarEvent.from_dict(data)
    if not event.validate():
        # Handle validation error
        pass
except KeyError as e:
    # Handle missing required field
    pass
except ValueError as e:
    # Handle invalid value
    pass
```

## JSON Schema Reference

See `contracts/` directory for:
- `ai-response.json`: Expected AI response format
- `alfred-feedback.json`: Alfred XML feedback format

## Future Extensions (Phase 2+)

Potential additions to data model:
- Attendees for events
- Subtasks for reminders
- Custom fields
- Tags/categories
- Geofencing for location-based reminders
- Time zone handling for events
- Attachments

## References

- [EventKit Framework Documentation](https://developer.apple.com/documentation/eventkit)
- [Python dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [JSON Schema](https://json-schema.org/)
