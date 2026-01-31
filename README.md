# Reminder-Alf 📅

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Test Coverage](https://img.shields.io/badge/coverage-55%25-green.svg)](https://github.com/fulln/reminder-alf)
[![GitHub Release](https://img.shields.io/github/v/release/fulln/reminder-alf)](https://github.com/fulln/reminder-alf/releases)
[![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

AI-powered natural language calendar and reminder management for macOS.

[English](#features) | [中文文档](docs/PROJECT_SUMMARY_CN.md)

## Features

- 🤖 **AI-Powered Parsing**: Convert natural language (English/Chinese) into calendar events and reminders
- 📅 **System Integration**: Creates events and reminders directly in macOS Calendar and Reminders apps
- 🔄 **iCloud Sync**: Automatically syncs to iOS via iCloud
- 🗑️ **Undo Support**: Track and delete created items individually or in bulk
- 🔒 **Secure Configuration**: API keys stored in macOS Keychain
- 🌐 **Multi-Provider**: Supports OpenAI, DeepSeek, and custom API endpoints
- 🚀 **Raycast Integration**: Native Raycast extension for quick access

## 📚 Documentation

- **[Quick Start Guide](docs/QUICKSTART.md)** - 5-minute setup and usage
- **[Raycast Installation](docs/INSTALL_RAYCAST.md)** - Raycast extension setup
- **[DeepSeek Setup](docs/DEEPSEEK.md)** - Configure DeepSeek AI (Chinese optimized)
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project
- **[Development Guide](docs/DEVELOPMENT.md)** - Developer documentation
- **[Changelog](CHANGELOG.md)** - Version history

## Requirements

- macOS 10.15+ (Catalina or later)
- Python 3.11+
- API key from OpenAI or DeepSeek

## Installation

```bash
# Clone the repository
git clone https://github.com/fulln/reminder-alf.git
cd reminder-alf

# Install (this adds the 'ral' command to your PATH)
python3.11 -m pip install -e .

# Configure AI provider (DeepSeek recommended for Chinese)
ral config set deepseek sk-YOUR_API_KEY deepseek-chat

# Or use OpenAI
ral config set openai sk-YOUR_API_KEY gpt-4
```

### With Raycast Extension (Optional)

```bash
cd raycast-extension
npm install
npm run dev
```

Then open Raycast and search for "Reminder Alf"

## Usage

### CLI Usage

```bash
# Parse natural language
ral parse "Meeting tomorrow at 2pm"
ral parse "明天下午3点开会"

# Configuration
ral config status
ral config set openai sk-xxx gpt-4
ral config set deepseek sk-xxx deepseek-chat

# List items
ral list
ral list 20

# Delete items
ral delete <item-id>
ral delete all
ral delete old 7

# Help
ral help
```

### Raycast Usage

1. Open Raycast (⌘ + Space)
2. Search for:
   - **"Create Event or Reminder"** - Parse natural language input
   - **"List Recent Items"** - View and delete tracked items
   - **"Configuration Status"** - Check and update AI configuration

## Supported AI Providers

### OpenAI
```bash
ral config set openai sk-... gpt-4-turbo
```

### DeepSeek (Recommended for Chinese)
```bash
ral config set deepseek sk-... deepseek-chat
```

### Custom Endpoints
```bash
ral config set custom YOUR_API_KEY your-model-name
ral config endpoint https://your-api.com/v1
```

## Configuration Files

- **Config**: `~/.config/reminder-alf/config.json`
- **Tracking**: `~/.config/reminder-alf/tracking.json`
- **API Keys**: macOS Keychain (service: `reminder-alf`)

## Development

### Run Tests

```bash
python3.11 -m pytest src/tests/ -v
```

### Code Coverage

```bash
python3.11 -m pytest src/tests/ --cov=src --cov-report=html
```

## Privacy & Security

- API keys stored securely in macOS Keychain
- Network requests only to configured AI provider
- No telemetry or usage tracking
- All data stays local except AI API calls

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Uses macOS EventKit via PyObjC
- AI parsing powered by OpenAI and DeepSeek
- Raycast extension framework

---

**Made with ❤️ for macOS users who love natural language interfaces**
