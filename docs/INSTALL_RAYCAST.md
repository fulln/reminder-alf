# Raycast Extension Installation Guide

## Prerequisites

- macOS 10.15+ (Catalina or later)
- Python 3.11+
- Node.js 22.14+
- npm 7+
- Raycast (free version is sufficient)

## Step 1: Install Python Backend

```bash
# Clone the repository
git clone https://github.com/fulln/reminder-alf.git
cd reminder-alf

# Install Python dependencies
python3.11 -m pip install -e .
```

## Step 2: Configure AI Provider

```bash
# For OpenAI
python -m src.cli config set openai sk-YOUR_API_KEY gpt-4

# For DeepSeek (recommended for Chinese users)
python -m src.cli config set deepseek sk-YOUR_API_KEY deepseek-chat
```

## Step 3: Grant macOS Permissions

When you first create an event or reminder, macOS will prompt for permissions:
- **Calendar Access**: Required to create calendar events
- **Reminders Access**: Required to create reminders

Go to **System Settings > Privacy & Security** to grant permissions if needed.

## Step 4: Install Raycast Extension

```bash
cd raycast-extension
npm install
npm run dev
```

This will start the extension in development mode. You can now open Raycast and search for "Reminder Alf".

## Step 5: Configure Extension (Optional)

If you installed Python in a non-standard location, set environment variables:

```bash
# In your ~/.zshrc or ~/.bashrc
export PYTHON_PATH=/path/to/python3.11
export REMINDER_ALF_PATH=/path/to/reminder-alf
```

## Available Commands

Once installed, you'll have three commands in Raycast:

1. **Create Event or Reminder**
   - Enter natural language in English or Chinese
   - Example: "Meeting tomorrow at 2pm" or "明天下午3点开会"

2. **List Recent Items**
   - View recently created events and reminders
   - Delete items directly from the list

3. **Configuration Status**
   - Check current AI configuration
   - Update provider, API key, or model

## Troubleshooting

### "Python not found" error
- Make sure Python 3.11+ is installed
- Set `PYTHON_PATH` environment variable

### "Not configured" error
- Run `python -m src.cli config set <provider> <api_key>`

### Calendar/Reminders not created
- Check permissions in System Settings > Privacy & Security
- Verify AI configuration with `python -m src.cli config status`

### Extension not appearing in Raycast
- Make sure `npm run dev` is running
- Restart Raycast (⌘+Q then reopen)

## Publishing (For Developers)

To publish the extension to Raycast Store:

```bash
cd raycast-extension
npm run publish
```

Note: You'll need to follow [Raycast's publishing guidelines](https://developers.raycast.com/basics/publish-an-extension).
