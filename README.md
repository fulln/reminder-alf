# Reminder-Alf 📅

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/fulln/reminder-alf/workflows/Build%20Alfred%20Workflow/badge.svg)](https://github.com/fulln/reminder-alf/actions)
[![Test Coverage](https://img.shields.io/badge/coverage-55%25-green.svg)](https://github.com/fulln/reminder-alf)
[![GitHub Release](https://img.shields.io/github/v/release/fulln/reminder-alf)](https://github.com/fulln/reminder-alf/releases)
[![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Alfred Version](https://img.shields.io/badge/Alfred-5%2B-purple.svg)](https://www.alfredapp.com/)
[![GitHub Downloads](https://img.shields.io/github/downloads/fulln/reminder-alf/total)](https://github.com/fulln/reminder-alf/releases)

AI-powered natural language calendar and reminder management for Alfred on macOS.

[English](#english) | [中文文档](docs/PROJECT_SUMMARY_CN.md)

## Features

- 🤖 **AI-Powered Parsing**: Convert natural language (English/Chinese) into calendar events and reminders
- 📅 **System Integration**: Creates events and reminders directly in macOS Calendar and Reminders apps
- 🔄 **iCloud Sync**: Automatically syncs to iOS via iCloud
- 🗑️ **Undo Support**: Track and delete created items individually or in bulk
- 🔒 **Secure Configuration**: API keys stored in macOS Keychain
- 🌐 **Multi-Provider**: Supports OpenAI, DeepSeek, and custom API endpoints

## 📚 Documentation

- **[Quick Start Guide](docs/QUICKSTART.md)** - 5-minute setup and usage
- **[Installation Guide](docs/INSTALL_ALFRED.md)** - Detailed installation instructions
- **[DeepSeek Setup](docs/DEEPSEEK.md)** - Configure DeepSeek AI (Chinese optimized)
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project
- **[Development Guide](docs/DEVELOPMENT.md)** - Developer documentation
- **[Automation Guide](docs/AUTOMATION.md)** - CI/CD and release automation
- **[Release Guide](docs/RELEASE.md)** - How to publish releases
- **[Project Structure](docs/STRUCTURE.md)** - Directory and file organization
- **[Changelog](CHANGELOG.md)** - Version history

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

**Set Endpoint:**
```
ral config endpoint <url>
```

**Set Timeout:**
```
ral config timeout <seconds>
```

**Set Max Tokens:**
```
ral config tokens <number>
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

Contributions welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## Documentation

For more information, check out the [docs](docs/) directory:
- [Quick Start](docs/QUICKSTART.md)
- [Installation](docs/INSTALL_ALFRED.md)
- [Development](docs/DEVELOPMENT.md)
- [Automation](docs/AUTOMATION.md)

## Acknowledgments

- Built with [alfred-workflow](https://github.com/deanishe/alfred-workflow)
- Uses macOS EventKit via PyObjC
- AI parsing powered by OpenAI and DeepSeek

---

**Made with ❤️ for Alfred users who love natural language interfaces**
