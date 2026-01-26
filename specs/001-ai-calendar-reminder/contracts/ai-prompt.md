# AI Prompt Templates

## Overview
This document contains the prompt templates used to interact with AI services (OpenAI, Anthropic, Gemini) for parsing natural language input into calendar events and reminders.

## System Prompt

This prompt establishes the AI's role and output format.

```
You are a calendar and reminder assistant. Your job is to parse natural language input and extract structured event or reminder information.

Current date and time: {current_datetime}
User's timezone: {timezone}
Default calendar: {default_calendar}
Default reminder list: {default_reminder_list}

IMPORTANT RULES:
1. Respond ONLY with valid JSON
2. Use ISO 8601 format for all dates/times
3. Infer missing information intelligently (e.g., if no end time, assume 1 hour duration)
4. Determine whether input describes an EVENT (scheduled for specific time) or REMINDER (task to complete)
5. Use 24-hour time format
6. All times should be in the user's timezone: {timezone}

OUTPUT FORMAT:
{{
  "type": "event" | "reminder",
  "event": {{
    "title": "string",
    "start_date": "ISO 8601 datetime",
    "end_date": "ISO 8601 datetime",
    "location": "string or null",
    "notes": "string or null",
    "calendar_name": "string or null",
    "all_day": boolean,
    "url": "string or null",
    "recurrence_frequency": "daily" | "weekly" | "monthly" | "yearly" | null,
    "recurrence_interval": integer,
    "recurrence_end_date": "ISO 8601 datetime or null",
    "alert_minutes_before": integer or null
  }} | null,
  "reminder": {{
    "title": "string",
    "notes": "string or null",
    "due_date": "ISO 8601 datetime or null",
    "priority": 0 | 1 | 2 | 3,
    "list_name": "string or null",
    "url": "string or null",
    "recurrence_frequency": "daily" | "weekly" | "monthly" | "yearly" | null,
    "recurrence_interval": integer,
    "recurrence_end_date": "ISO 8601 datetime or null"
  }} | null,
  "confidence": float (0.0 to 1.0),
  "ambiguities": [
    "string descriptions of any ambiguous elements"
  ]
}}

PRIORITY LEVELS:
- 0: None (default)
- 1: Low (!)
- 2: Medium (!!)
- 3: High (!!!)

EXAMPLES:

Input: "Team meeting tomorrow at 2pm for 1 hour"
Output: {{
  "type": "event",
  "event": {{
    "title": "Team meeting",
    "start_date": "{tomorrow_2pm_iso}",
    "end_date": "{tomorrow_3pm_iso}",
    "location": null,
    "notes": null,
    "calendar_name": null,
    "all_day": false,
    "url": null,
    "recurrence_frequency": null,
    "recurrence_interval": 1,
    "recurrence_end_date": null,
    "alert_minutes_before": null
  }},
  "reminder": null,
  "confidence": 0.95,
  "ambiguities": []
}}

Input: "Buy groceries today at 6pm"
Output: {{
  "type": "reminder",
  "event": null,
  "reminder": {{
    "title": "Buy groceries",
    "notes": null,
    "due_date": "{today_6pm_iso}",
    "priority": 0,
    "list_name": null,
    "url": null,
    "recurrence_frequency": null,
    "recurrence_interval": 1,
    "recurrence_end_date": null
  }},
  "confidence": 0.95,
  "ambiguities": []
}}

Input: "Weekly standup every Monday at 9am"
Output: {{
  "type": "event",
  "event": {{
    "title": "Weekly standup",
    "start_date": "{next_monday_9am_iso}",
    "end_date": "{next_monday_10am_iso}",
    "location": null,
    "notes": null,
    "calendar_name": null,
    "all_day": false,
    "url": null,
    "recurrence_frequency": "weekly",
    "recurrence_interval": 1,
    "recurrence_end_date": null,
    "alert_minutes_before": null
  }},
  "reminder": null,
  "confidence": 0.95,
  "ambiguities": []
}}

Input: "URGENT: Submit report by Friday"
Output: {{
  "type": "reminder",
  "event": null,
  "reminder": {{
    "title": "Submit report",
    "notes": null,
    "due_date": "{friday_end_of_day_iso}",
    "priority": 3,
    "list_name": null,
    "url": null,
    "recurrence_frequency": null,
    "recurrence_interval": 1,
    "recurrence_end_date": null
  }},
  "confidence": 0.90,
  "ambiguities": ["Exact time not specified, assuming end of day"]
}}

Now parse the following input:
```

## Template Variables

The system prompt uses these template variables that must be filled at runtime:

| Variable | Description | Example |
|----------|-------------|---------|
| `{current_datetime}` | Current date and time in ISO 8601 | `2024-01-15T14:30:00-08:00` |
| `{timezone}` | User's timezone | `America/Los_Angeles` |
| `{default_calendar}` | Default calendar name | `Work` |
| `{default_reminder_list}` | Default reminder list | `Tasks` |

## Python Implementation

```python
from datetime import datetime
from zoneinfo import ZoneInfo

def build_system_prompt(
    current_datetime: datetime,
    timezone: str,
    default_calendar: str,
    default_reminder_list: str
) -> str:
    """Build the system prompt with current context."""
    
    # Read template from file or constant
    with open('prompts/system.txt', 'r') as f:
        template = f.read()
    
    # Fill in template variables
    prompt = template.format(
        current_datetime=current_datetime.isoformat(),
        timezone=timezone,
        default_calendar=default_calendar,
        default_reminder_list=default_reminder_list,
        # Example dates for the template
        tomorrow_2pm_iso=(current_datetime + timedelta(days=1)).replace(hour=14, minute=0).isoformat(),
        tomorrow_3pm_iso=(current_datetime + timedelta(days=1)).replace(hour=15, minute=0).isoformat(),
        today_6pm_iso=current_datetime.replace(hour=18, minute=0).isoformat(),
        next_monday_9am_iso=get_next_weekday(current_datetime, 0, 9, 0).isoformat(),
        next_monday_10am_iso=get_next_weekday(current_datetime, 0, 10, 0).isoformat(),
        friday_end_of_day_iso=get_next_weekday(current_datetime, 4, 23, 59).isoformat(),
    )
    
    return prompt

def get_next_weekday(current: datetime, weekday: int, hour: int, minute: int) -> datetime:
    """Get the next occurrence of a weekday at a specific time."""
    days_ahead = weekday - current.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    next_date = current + timedelta(days=days_ahead)
    return next_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
```

## User Message Template

The user's natural language input is sent as a simple user message:

```python
def build_user_message(user_input: str) -> str:
    """Build the user message."""
    return user_input
```

## API-Specific Implementations

### OpenAI

```python
from openai import OpenAI

def call_openai(system_prompt: str, user_input: str, config: AIConfiguration) -> str:
    """Call OpenAI API."""
    client = OpenAI(api_key=config.api_key)
    
    response = client.chat.completions.create(
        model=config.model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        response_format={"type": "json_object"}
    )
    
    return response.choices[0].message.content
```

### Anthropic Claude

```python
from anthropic import Anthropic

def call_anthropic(system_prompt: str, user_input: str, config: AIConfiguration) -> str:
    """Call Anthropic API."""
    client = Anthropic(api_key=config.api_key)
    
    # Combine system prompt and user input for Claude
    full_prompt = f"{system_prompt}\n\nUser input: {user_input}"
    
    response = client.messages.create(
        model=config.model,
        max_tokens=config.max_tokens,
        messages=[
            {"role": "user", "content": full_prompt}
        ],
        temperature=config.temperature
    )
    
    return response.content[0].text
```

### Google Gemini

```python
import google.generativeai as genai

def call_gemini(system_prompt: str, user_input: str, config: AIConfiguration) -> str:
    """Call Gemini API."""
    genai.configure(api_key=config.api_key)
    model = genai.GenerativeModel(config.model)
    
    # Combine system prompt and user input
    full_prompt = f"{system_prompt}\n\nUser input: {user_input}"
    
    response = model.generate_content(full_prompt)
    
    return response.text
```

## Prompt Engineering Notes

### Date/Time Handling

The AI needs clear context about the current time to correctly interpret relative dates:
- "tomorrow" = current_date + 1 day
- "next Monday" = next occurrence of Monday
- "in 2 hours" = current_time + 2 hours

Always include:
- Current date and time in ISO 8601 format
- User's timezone
- Clear examples in the system prompt

### Event vs Reminder Detection

Guidelines for the AI to distinguish:

**Events** (scheduled activities):
- Have specific start/end times
- Keywords: "meeting", "appointment", "call", "lunch", "dinner"
- Time-bounded: "from X to Y", "at X for Y duration"

**Reminders** (tasks):
- May have due dates but not specific time slots
- Keywords: "buy", "remember", "call", "email", "prepare"
- Due-by nature: "by Friday", "before Monday"

### Priority Detection

Keywords indicating priority:
- **High (3)**: "urgent", "ASAP", "critical", "important", "!!!"
- **Medium (2)**: "soon", "!!"
- **Low (1)**: "when you can", "eventually", "!"
- **None (0)**: default

### Recurrence Patterns

Common patterns the AI should recognize:
- "every day" / "daily" → frequency: daily, interval: 1
- "every week" / "weekly" → frequency: weekly, interval: 1
- "every 2 weeks" / "biweekly" → frequency: weekly, interval: 2
- "every month" / "monthly" → frequency: monthly, interval: 1
- "every year" / "annually" → frequency: yearly, interval: 1

### Location Extraction

Keywords that indicate location:
- "at [place]"
- "in [room]"
- URL patterns (Zoom, Google Meet, etc.)

### URL Detection

Patterns to detect:
- `https://...`
- `http://...`
- `zoom.us/...`
- `meet.google.com/...`

### Alert/Reminder Times

Common patterns:
- "remind me X minutes before" → alert_minutes_before: X
- "alert me X hours before" → alert_minutes_before: X * 60
- "remind me 1 day before" → alert_minutes_before: 1440

### Calendar/List Specification

Pattern: `[CalendarName] event details`

Example:
- Input: "[Work] Team meeting tomorrow at 2pm"
- Parse: calendar_name = "Work", title = "Team meeting"

## Error Handling

### Low Confidence Response

If AI confidence < 0.5, include detailed ambiguities:

```json
{
  "type": "event",
  "event": {...},
  "reminder": null,
  "confidence": 0.45,
  "ambiguities": [
    "Could not determine if '2pm' refers to today or tomorrow",
    "Location 'room A' is ambiguous - multiple matches found"
  ]
}
```

### Unparseable Input

If input cannot be parsed at all:

```json
{
  "type": "unknown",
  "event": null,
  "reminder": null,
  "confidence": 0.0,
  "ambiguities": [
    "Input too vague to determine event or reminder",
    "Missing required information: date/time"
  ]
}
```

## Testing Prompts

### Test Cases

```python
test_cases = [
    # Simple event
    {
        "input": "Team meeting tomorrow at 2pm",
        "expected_type": "event",
        "expected_title": "Team meeting"
    },
    
    # Event with duration
    {
        "input": "Lunch with John next Tuesday from 12pm to 1:30pm",
        "expected_type": "event",
        "expected_title": "Lunch with John",
        "expected_duration_minutes": 90
    },
    
    # All-day event
    {
        "input": "Vacation from Dec 20 to Dec 25",
        "expected_type": "event",
        "expected_all_day": True
    },
    
    # Recurring event
    {
        "input": "Weekly standup every Monday at 9am",
        "expected_type": "event",
        "expected_recurrence": "weekly"
    },
    
    # Simple reminder
    {
        "input": "Buy groceries",
        "expected_type": "reminder",
        "expected_title": "Buy groceries"
    },
    
    # Reminder with due date
    {
        "input": "Submit report by Friday 5pm",
        "expected_type": "reminder",
        "expected_has_due_date": True
    },
    
    # High priority reminder
    {
        "input": "URGENT: Call client",
        "expected_type": "reminder",
        "expected_priority": 3
    },
    
    # Event with location
    {
        "input": "Team meeting tomorrow at 2pm in Conference Room A",
        "expected_type": "event",
        "expected_location": "Conference Room A"
    },
    
    # Event with URL
    {
        "input": "Zoom call tomorrow at 3pm https://zoom.us/j/123456",
        "expected_type": "event",
        "expected_url": "https://zoom.us/j/123456"
    },
    
    # Calendar specification
    {
        "input": "[Work] Sprint planning next Monday at 10am",
        "expected_type": "event",
        "expected_calendar": "Work"
    }
]
```

## Optimization Tips

1. **Token Efficiency**: 
   - Remove redundant examples from system prompt
   - Use concise language
   - Consider caching system prompt

2. **Response Speed**:
   - Use faster models (gpt-3.5-turbo, claude-haiku) for simple inputs
   - Set appropriate max_tokens (512-1024 usually sufficient)
   - Use streaming for better perceived performance

3. **Accuracy**:
   - Include diverse examples in system prompt
   - Test with edge cases
   - Collect and learn from failed parses

4. **Cost Management**:
   - Cache successful parses
   - Use cheaper models when possible
   - Implement rate limiting

## Version History

### v1.0 (Current)
- Basic event and reminder parsing
- Support for recurrence
- Priority detection
- Location and URL extraction

### Planned (v2.0)
- Multi-event parsing (batch)
- Attendee extraction
- More complex recurrence rules
- Smart suggestions based on history
- Context awareness (previous events/reminders)

## References

- [OpenAI Chat Completions](https://platform.openai.com/docs/guides/chat)
- [Anthropic Messages API](https://docs.anthropic.com/claude/reference/messages)
- [Google Gemini API](https://ai.google.dev/docs)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
