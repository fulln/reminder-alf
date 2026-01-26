# Phase 0: Technology Research

## Overview
This document captures the research findings for technologies used in the AI Calendar Reminder Alfred workflow.

## Core Technologies

### Python 3.11
- **Purpose**: Primary programming language
- **Version Requirement**: 3.11+
- **Key Features Used**:
  - Type hints and annotations
  - Dataclasses for structured data
  - Pattern matching (match/case)
  - Exception groups
  - Better error messages

**Installation on macOS**:
```bash
brew install python@3.11
```

**Verification**:
```bash
python3.11 --version
```

### PyObjC
- **Purpose**: Bridge between Python and macOS system frameworks
- **Version**: Latest stable (9.x+)
- **Key Frameworks Used**:
  - `EventKit`: Calendar and Reminders access
  - `Foundation`: Date/time handling, notifications

**Installation**:
```bash
pip install pyobjc-framework-EventKit
pip install pyobjc-framework-Foundation
```

**Key Classes**:
- `EKEventStore`: Central access point for calendar/reminder data
- `EKCalendar`: Represents a calendar
- `EKEvent`: Represents a calendar event
- `EKReminder`: Represents a reminder item
- `EKRecurrenceRule`: For recurring events/reminders

**Permission Handling**:
```python
from EventKit import EKEventStore, EKEntityTypeEvent, EKEntityTypeReminder

store = EKEventStore.alloc().init()

# Request calendar access
store.requestAccessToEntityType_completion_(
    EKEntityTypeEvent,
    lambda granted, error: handle_calendar_access(granted, error)
)

# Request reminders access
store.requestAccessToEntityType_completion_(
    EKEntityTypeReminder,
    lambda granted, error: handle_reminders_access(granted, error)
)
```

### alfred-workflow
- **Purpose**: Simplifies Alfred workflow development
- **Repository**: https://github.com/deanishe/alfred-workflow
- **Version**: 1.40+

**Installation**:
```bash
pip install alfred-workflow
```

**Key Features**:
- XML feedback generation
- Settings management
- Caching
- Background jobs
- Keychain access
- Update checking

**Basic Usage**:
```python
from workflow import Workflow3

wf = Workflow3()

# Add items to feedback
wf.add_item(
    title='Event Title',
    subtitle='Event details',
    arg='event_data',
    valid=True,
    icon='calendar.png'
)

# Send feedback to Alfred
wf.send_feedback()
```

**Settings Storage**:
```python
# Save settings
wf.settings['api_key'] = 'secret_key'
wf.settings['model'] = 'gpt-4'

# Load settings
api_key = wf.settings.get('api_key')
```

**Caching**:
```python
# Cache data with expiration
wf.cached_data('cache_key', data_func, max_age=3600)

# Clear cache
wf.clear_cache()
```

## AI Client Libraries

### OpenAI API
- **Purpose**: GPT model access
- **Library**: `openai`
- **Version**: 1.0.0+

**Installation**:
```bash
pip install openai
```

**Usage**:
```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a calendar assistant."},
        {"role": "user", "content": "Create event: Team meeting tomorrow at 2pm"}
    ],
    temperature=0.7,
    response_format={"type": "json_object"}
)

result = response.choices[0].message.content
```

**Models Available**:
- `gpt-4`: Most capable, higher cost
- `gpt-4-turbo`: Faster, cost-effective
- `gpt-3.5-turbo`: Fast, economical

### Anthropic Claude API
- **Purpose**: Claude model access
- **Library**: `anthropic`
- **Version**: 0.8.0+

**Installation**:
```bash
pip install anthropic
```

**Usage**:
```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

response = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Create event: Team meeting tomorrow at 2pm"}
    ]
)

result = response.content[0].text
```

**Models Available**:
- `claude-3-opus-20240229`: Most capable
- `claude-3-sonnet-20240229`: Balanced
- `claude-3-haiku-20240307`: Fast, economical

### Gemini API
- **Purpose**: Google's Gemini model access
- **Library**: `google-generativeai`
- **Version**: 0.3.0+

**Installation**:
```bash
pip install google-generativeai
```

**Usage**:
```python
import google.generativeai as genai

genai.configure(api_key="your-api-key")
model = genai.GenerativeModel('gemini-pro')

response = model.generate_content(
    "Create event: Team meeting tomorrow at 2pm"
)

result = response.text
```

**Models Available**:
- `gemini-pro`: Text generation
- `gemini-pro-vision`: Multimodal (text + images)

## Security & Storage

### keyring
- **Purpose**: Secure credential storage
- **Library**: `keyring`
- **Version**: 24.0.0+

**Installation**:
```bash
pip install keyring
```

**Usage**:
```python
import keyring

# Store API key
keyring.set_password('reminder-alf', 'openai_api_key', 'sk-...')

# Retrieve API key
api_key = keyring.get_password('reminder-alf', 'openai_api_key')

# Delete API key
keyring.delete_password('reminder-alf', 'openai_api_key')
```

**macOS Integration**:
- Uses macOS Keychain by default
- Secure, encrypted storage
- No additional configuration needed

### JSON Storage
- **Purpose**: Workflow settings and cache
- **Library**: Built-in `json` module
- **Location**: `~/Library/Application Support/Alfred/Workflow Data/`

**File Structure**:
```
~/Library/Application Support/Alfred/Workflow Data/com.example.reminder-alf/
├── settings.json          # User preferences
├── cache/                 # Temporary cache
│   └── items.json
└── created_items.json    # Tracking created events/reminders
```

**Usage**:
```python
import json
from pathlib import Path

def save_settings(settings: dict, workflow_id: str):
    data_dir = Path.home() / 'Library/Application Support/Alfred/Workflow Data' / workflow_id
    data_dir.mkdir(parents=True, exist_ok=True)
    
    settings_file = data_dir / 'settings.json'
    with open(settings_file, 'w') as f:
        json.dump(settings, f, indent=2)

def load_settings(workflow_id: str) -> dict:
    data_dir = Path.home() / 'Library/Application Support/Alfred/Workflow Data' / workflow_id
    settings_file = data_dir / 'settings.json'
    
    if not settings_file.exists():
        return {}
    
    with open(settings_file, 'r') as f:
        return json.load(f)
```

## Natural Language Processing

### dateutil
- **Purpose**: Human-friendly date/time parsing
- **Library**: `python-dateutil`
- **Version**: 2.8.0+

**Installation**:
```bash
pip install python-dateutil
```

**Usage**:
```python
from dateutil import parser
from dateutil.relativedelta import relativedelta

# Parse natural dates
date = parser.parse("tomorrow at 2pm")
date = parser.parse("next friday")
date = parser.parse("2024-12-25 10:00")

# Relative dates
next_week = datetime.now() + relativedelta(weeks=1)
next_month = datetime.now() + relativedelta(months=1)
```

## Testing & Development

### pytest
- **Purpose**: Testing framework
- **Version**: 7.0.0+

**Installation**:
```bash
pip install pytest pytest-cov pytest-mock
```

**Usage**:
```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_parser.py
```

### black & ruff
- **Purpose**: Code formatting and linting
- **Version**: Latest stable

**Installation**:
```bash
pip install black ruff
```

**Usage**:
```bash
# Format code
black src/

# Lint code
ruff check src/
```

## Dependencies Summary

**requirements.txt**:
```
# Core
pyobjc-framework-EventKit>=9.0
pyobjc-framework-Foundation>=9.0
alfred-workflow>=1.40

# AI Clients
openai>=1.0.0
anthropic>=0.8.0
google-generativeai>=0.3.0

# Utilities
python-dateutil>=2.8.0
keyring>=24.0.0

# Development
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0
black>=23.0.0
ruff>=0.1.0
```

## Platform Requirements

- **OS**: macOS 10.15 (Catalina) or later
- **Alfred**: Alfred 5.0+ with Powerpack
- **Python**: 3.11+
- **Permissions**: Calendar and Reminders access

## Security Considerations

1. **API Keys**:
   - Store in macOS Keychain via `keyring`
   - Never commit to version control
   - Use environment variables for development

2. **Calendar Access**:
   - Request permissions on first use
   - Handle denial gracefully
   - Show clear error messages

3. **Data Privacy**:
   - Process locally when possible
   - Minimize data sent to AI services
   - Don't log sensitive information

## Performance Considerations

1. **Caching**:
   - Cache calendar list (5 minutes)
   - Cache AI responses (1 hour)
   - Clear cache on settings change

2. **Background Processing**:
   - Use alfred-workflow's background jobs
   - Show progress indicators
   - Handle timeouts gracefully

3. **API Rate Limits**:
   - Implement exponential backoff
   - Show user-friendly error messages
   - Cache successful results

## References

- [PyObjC Documentation](https://pyobjc.readthedocs.io/)
- [EventKit Framework](https://developer.apple.com/documentation/eventkit)
- [Alfred Workflow Guide](https://www.deanishe.net/alfred-workflow/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Google Gemini API](https://ai.google.dev/docs)
