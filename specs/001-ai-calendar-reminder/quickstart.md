# Quick Start Guide - AI Calendar Reminder

## Installation

### Prerequisites
- macOS 10.15 (Catalina) or later
- Alfred 5.0+ with Powerpack
- Python 3.11+
- Homebrew (recommended)

### Step 1: Install Python 3.11

```bash
# Using Homebrew
brew install python@3.11

# Verify installation
python3.11 --version
```

### Step 2: Download and Install Workflow

1. Download the latest `.alfredworkflow` file from releases
2. Double-click the file to install in Alfred
3. Alfred will prompt to import the workflow

### Step 3: Install Dependencies

The workflow should automatically install dependencies on first run. If manual installation is needed:

```bash
cd ~/Library/Application\ Support/Alfred/Alfred.alfredpreferences/workflows/[workflow-id]

# Install requirements
pip3.11 install -r requirements.txt
```

### Step 4: Configure AI Service

Open Alfred and type:

```
remind:config
```

Follow the prompts to:
1. Choose AI provider (OpenAI, Anthropic, or Gemini)
2. Enter API key
3. Select model
4. Configure default calendar/reminder list

### Step 5: Grant Permissions

On first use, macOS will request permissions:
- **Calendar Access**: Required to create events
- **Reminders Access**: Required to create reminders

Click "OK" to grant access.

## Basic Usage

### Creating Events

Open Alfred and type `remind` followed by your natural language request:

```
remind Team meeting tomorrow at 2pm for 1 hour
```

```
remind Dentist appointment next Tuesday at 10am
```

```
remind Weekly standup every Monday at 9am
```

### Creating Reminders

```
remind Buy groceries today at 6pm
```

```
remind Call mom on Friday
```

```
remind Water plants every week
```

### Keyword Shortcuts

- `remind` - Create event or reminder from natural language
- `remind:config` - Open configuration
- `remind:list` - List recent items
- `remind:undo` - Undo last created item

## Configuration Options

### AI Provider Settings

#### OpenAI
- **Models**: gpt-4, gpt-4-turbo, gpt-3.5-turbo
- **API Key**: Get from https://platform.openai.com/api-keys
- **Cost**: Pay per token

#### Anthropic Claude
- **Models**: claude-3-opus, claude-3-sonnet, claude-3-haiku
- **API Key**: Get from https://console.anthropic.com/
- **Cost**: Pay per token

#### Google Gemini
- **Models**: gemini-pro
- **API Key**: Get from https://ai.google.dev/
- **Cost**: Free tier available

### Default Settings

```json
{
  "provider": "openai",
  "model": "gpt-4-turbo",
  "temperature": 0.7,
  "max_tokens": 1024,
  "default_calendar": "Work",
  "default_reminder_list": "Tasks",
  "default_event_duration": 60,
  "default_alert_minutes": 15
}
```

Access settings file:
```
~/Library/Application Support/Alfred/Workflow Data/com.example.reminder-alf/settings.json
```

## Examples

### Simple Event

**Input:**
```
remind Coffee with John tomorrow at 3pm
```

**Result:**
- Title: "Coffee with John"
- Date: Tomorrow
- Time: 3:00 PM
- Duration: 1 hour (default)
- Calendar: Default calendar

### Event with Details

**Input:**
```
remind Team meeting next Monday at 2pm for 2 hours in Conference Room A
```

**Result:**
- Title: "Team meeting"
- Date: Next Monday
- Time: 2:00 PM - 4:00 PM
- Location: Conference Room A
- Calendar: Default calendar

### Recurring Event

**Input:**
```
remind Weekly standup every Monday at 9am for 30 minutes
```

**Result:**
- Title: "Weekly standup"
- Recurrence: Every Monday
- Time: 9:00 AM - 9:30 AM
- Calendar: Default calendar

### All-Day Event

**Input:**
```
remind Vacation from Dec 20 to Dec 30
```

**Result:**
- Title: "Vacation"
- Start: Dec 20 (all day)
- End: Dec 30 (all day)
- Calendar: Default calendar

### Simple Reminder

**Input:**
```
remind Buy groceries today at 6pm
```

**Result:**
- Title: "Buy groceries"
- Due: Today at 6:00 PM
- List: Default reminder list

### Reminder with Priority

**Input:**
```
remind URGENT: Submit report by Friday
```

**Result:**
- Title: "Submit report"
- Due: Friday
- Priority: High
- List: Default reminder list

### Recurring Reminder

**Input:**
```
remind Take vitamins every day at 8am
```

**Result:**
- Title: "Take vitamins"
- Recurrence: Daily
- Time: 8:00 AM
- List: Default reminder list

## Advanced Features

### Specifying Calendar

```
remind [Work] Team meeting tomorrow at 2pm
```

The `[Work]` prefix specifies the calendar to use.

### Specifying Reminder List

```
remind [Shopping] Buy milk and eggs
```

The `[Shopping]` prefix specifies the reminder list.

### Custom Alerts

```
remind Doctor appointment next week, remind me 1 day before
```

Sets a custom alert for 1 day (1440 minutes) before the event.

### Adding URLs

```
remind Zoom meeting tomorrow at 10am https://zoom.us/j/123456
```

Attaches the URL to the event.

### Adding Notes

```
remind Project review Friday at 3pm - Prepare slides and demo
```

The text after the dash becomes the event notes.

## Troubleshooting

### "No API key configured"

**Solution:**
```
remind:config
```
Enter your AI provider API key.

### "Calendar access denied"

**Solution:**
1. Open System Preferences → Security & Privacy → Privacy
2. Select "Calendars" from the left sidebar
3. Check the box next to "Alfred"

### "Reminders access denied"

**Solution:**
1. Open System Preferences → Security & Privacy → Privacy
2. Select "Reminders" from the left sidebar
3. Check the box next to "Alfred"

### "Could not parse input"

**Reasons:**
- Input too vague or ambiguous
- Missing required information (like date/time)
- Unsupported format

**Solution:**
Try rephrasing with more specific details:
- Include explicit dates: "tomorrow", "next Monday", "Jan 15"
- Include times: "at 2pm", "from 9am to 11am"
- Be specific: "meeting" vs "team meeting with John"

### "API request failed"

**Reasons:**
- Invalid API key
- Network connection issue
- API service down
- Rate limit exceeded

**Solution:**
1. Check your API key in settings
2. Verify internet connection
3. Check AI provider status page
4. Wait a few minutes if rate limited

### Event created in wrong calendar

**Solution:**
1. Use calendar prefix: `remind [CalendarName] ...`
2. Or change default calendar:
   ```
   remind:config
   ```

## Keyboard Shortcuts

Configure in Alfred Preferences → Workflows → [workflow name]:

- **⌘⌥C**: Open remind command
- **⌘⌥R**: Open remind:config
- **⌘⌥U**: Undo last item

## Tips & Best Practices

### 1. Be Specific

**Good:**
```
remind Team standup every Monday at 9am for 30 minutes
```

**Bad:**
```
remind meeting
```

### 2. Use Natural Language

The AI understands conversational input:
```
remind Coffee with Sarah next week Tuesday afternoon
```

### 3. Include Context

Adding context helps the AI:
```
remind Quarterly review meeting with stakeholders next Friday at 2pm in the main conference room
```

### 4. Use Calendar Prefixes

Organize events by calendar:
```
remind [Work] Sprint planning Monday at 10am
remind [Personal] Dentist appointment Tuesday at 2pm
```

### 5. Review Before Confirming

The workflow shows a preview before creating. Review details and press Enter to confirm.

### 6. Use Undo

Made a mistake?
```
remind:undo
```

### 7. Set Defaults

Configure your most-used settings as defaults:
- Default calendar
- Default reminder list
- Default event duration
- Default alert time

## Privacy & Security

### Data Storage

- **API Keys**: Stored securely in macOS Keychain
- **Settings**: `~/Library/Application Support/Alfred/Workflow Data/`
- **Cache**: Temporary, cleared automatically
- **Created Items**: Local JSON file for undo functionality

### Data Sent to AI

Only the text you enter is sent to the AI service. The workflow does not:
- Send your existing calendar events
- Send personal information
- Track your usage
- Share data with third parties

### Revoking Access

To revoke API access:
1. OpenAI: https://platform.openai.com/api-keys
2. Anthropic: https://console.anthropic.com/
3. Gemini: https://ai.google.dev/

## Updating

### Automatic Updates

Enable in Alfred Preferences:
1. Open Alfred Preferences
2. Navigate to Workflows
3. Select the workflow
4. Check "Automatically check for updates"

### Manual Updates

1. Download latest `.alfredworkflow` file
2. Double-click to install
3. Choose "Replace" when prompted

## Uninstalling

1. Open Alfred Preferences
2. Navigate to Workflows
3. Right-click the workflow
4. Select "Delete Workflow"

Settings and data will remain in:
```
~/Library/Application Support/Alfred/Workflow Data/com.example.reminder-alf/
```

Delete this folder to completely remove all data.

## Getting Help

### Logs

View workflow logs:
```
~/Library/Logs/Alfred/Workflow.log
```

### Debug Mode

Enable debug mode in Alfred Preferences → Workflows → [workflow name] → Environment Variables:
- Add variable: `DEBUG` = `1`

### Support

- GitHub Issues: [repository-url]
- Documentation: [docs-url]
- Email: support@example.com

## FAQ

### Q: Can I use multiple AI providers?

A: Not simultaneously, but you can switch providers in settings at any time.

### Q: Does this work offline?

A: No, an internet connection is required to communicate with AI services.

### Q: Can I edit events after creation?

A: Use the standard Calendar or Reminders app to edit. The workflow only handles creation.

### Q: Is my data private?

A: Yes. Only your input text is sent to the AI service. Your calendar data stays local.

### Q: What languages are supported?

A: Currently English only. The AI can understand informal/conversational English.

### Q: Can I create recurring events?

A: Yes! Use phrases like "every Monday", "daily", "weekly", etc.

### Q: How accurate is the AI parsing?

A: Very accurate for clear, specific inputs. Ambiguous inputs may need clarification.

### Q: Can I undo accidental creations?

A: Yes, use `remind:undo` to delete the most recently created item.

### Q: Does this support time zones?

A: Currently uses system time zone. Multi-timezone support planned for Phase 2.

### Q: Can I batch create multiple events?

A: Not yet. Create one event/reminder at a time. Batch support planned for future.

## Next Steps

- Read the [Data Model documentation](data-model.md)
- Explore [AI Prompt Templates](contracts/ai-prompt.md)
- Review [Technical Research](research.md)
- Check the [API Contracts](contracts/)

## Version History

### v1.0.0 (Phase 1)
- Initial release
- Support for OpenAI, Anthropic, Gemini
- Basic event and reminder creation
- Undo functionality
- Configuration interface

### Planned (Phase 2+)
- Quick add mode
- Template system
- Batch operations
- Multi-language support
- Advanced recurrence rules
- Attendee management
