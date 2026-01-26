# Reminder-Alf 📅

AI-powered natural language calendar and reminder management for Alfred on macOS.

## Features

- 🤖 **AI-Powered Parsing**: Convert natural language (English/Chinese) into calendar events and reminders
- 📅 **System Integration**: Creates events and reminders directly in macOS Calendar and Reminders apps
- 🔄 **iCloud Sync**: Automatically syncs to iOS via iCloud
- 🗑️ **Undo Support**: Track and delete created items individually or in bulk
- 🔒 **Secure Configuration**: API keys stored in macOS Keychain
- 🌐 **Multi-Provider**: Supports OpenAI, DeepSeek, and custom API endpoints

## Requirements

- macOS 10.15+ (Catalina or later)
- Python 3.11+
- Alfred 5 with Powerpack
- API key from OpenAI or DeepSeek

## Installation

### 1. Install Python Dependencies

```bash
# Clone the repository
git clone https://github.com/yourusername/reminder-alf.git
cd reminder-alf

# Install dependencies
python3.11 -m pip install -e .
```

### 2. Grant Permissions

When you first run the workflow, macOS will prompt you to grant permissions:
- **Calendar Access**: Required to create calendar events
- **Reminders Access**: Required to create reminders

### 3. Configure AI Provider

Run the configuration command in Alfred:

```
ral config set openai sk-YOUR_API_KEY gpt-4
```

Or for DeepSeek (optimized for Chinese, cost-effective):

```
ral config set deepseek sk-YOUR_API_KEY deepseek-chat
```

## Usage

### Parse Natural Language

Simply type your event or reminder in natural language:

**English Examples:**
```
ral Meeting with John tomorrow at 2pm
ral Team standup every weekday at 9am
ral Remind me to buy milk
ral Call dentist by Friday at 5pm
```

**Chinese Examples:**
```
ral 明天下午3点开会
ral 提醒我买牛奶
ral 周五下午5点前给医生打电话
```

### Configuration Commands

**Check Status:**
```
ral config status
```

**Set API Configuration:**
```
ral config set <provider> <api-key> [model]
```

**Delete Configuration:**
```
ral config delete [provider]
```

### Delete Commands

**List Recent Items:**
```
ral delete
```
(Shows last 10 created items for selection)

**Delete Specific Item:**
```
ral delete <item-id>
```

**Delete All Tracked Items:**
```
ral delete all
```

**Delete Old Items:**
```
ral delete old [days]
```
(Default: 7 days)

### Help

```
ral help
```

## AI Parsing Rules

The AI follows these rules when parsing:

1. **Calendar Events** require explicit time references:
   - "meeting at 2pm"
   - "lunch tomorrow at noon"
   - "conference from Feb 1-3"

2. **Reminders** are for action items without specific times:
   - "remind me to..."
   - "buy milk"
   - "call John"

3. **Due Dates** can be specified for reminders:
   - "submit report by Friday at 5pm"
   - "pay bill by Jan 30"

4. **Priority Levels** (0-3):
   - 0: None (default)
   - 1: Low (🔵)
   - 2: Medium (🟡)
   - 3: High (🔴)

## Supported AI Providers

### OpenAI

Models: `gpt-4-turbo`, `gpt-4`, `gpt-3.5-turbo`

```bash
ral config set openai sk-... gpt-4-turbo
```

### DeepSeek

Models: `deepseek-chat`, `deepseek-coder`

```bash
ral config set deepseek sk-... deepseek-chat
```

### Custom Endpoints

For OpenAI-compatible endpoints:

```bash
ral config set custom YOUR_API_KEY your-model-name
```

Set custom endpoint URL via environment variable:
```bash
export REMINDER_ALF_CUSTOM_ENDPOINT=https://your-api.com/v1
```

## Configuration Files

- **Config**: `~/Library/Application Support/Alfred/Workflow Data/com.reminder-alf/config.json`
- **Tracking**: `~/Library/Application Support/Alfred/Workflow Data/com.reminder-alf/tracking.json`
- **Logs**: `~/Library/Application Support/Alfred/Workflow Data/com.reminder-alf/logs/`
- **API Keys**: macOS Keychain (service: `alfred-reminder-alf`)

## Development

### Run Tests

```bash
python3.11 -m pytest tests/ -v
```

### Code Coverage

```bash
python3.11 -m pytest tests/ --cov=src --cov-report=html
```

### Linting

```bash
ruff check src/
black src/ --check
```

## Troubleshooting

### "Calendar access denied"

Grant permissions in System Settings > Privacy & Security > Calendar

### "API key invalid"

Check your API key and reconfigure:
```bash
ral config delete
ral config set openai sk-YOUR_NEW_KEY
```

### "No items found"

Try being more specific with dates/times:
- ❌ "meeting tomorrow"
- ✅ "meeting tomorrow at 2pm"

### Parse errors

The AI may struggle with:
- Very vague input ("stuff later")
- Multiple unrelated items in one message
- Ambiguous dates ("next Thursday" when spoken mid-week)

## Privacy & Security

- API keys stored securely in macOS Keychain
- Network requests only to configured AI provider
- No telemetry or usage tracking
- All data stays local except AI API calls

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## Acknowledgments

- Built with [alfred-workflow](https://github.com/deanishe/alfred-workflow)
- Uses macOS EventKit via PyObjC
- AI parsing powered by OpenAI and DeepSeek

---

**Made with ❤️ for Alfred users who love natural language interfaces**
