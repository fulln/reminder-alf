#!/usr/bin/env bash
# Setup script for Reminder-Alf Alfred Workflow

set -e

echo "🚀 Setting up Reminder-Alf..."
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3.11 &> /dev/null; then
    echo "❌ Python 3.11 is required but not found."
    echo "Please install Python 3.11 from https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3.11 --version)
echo "✅ Found: $PYTHON_VERSION"
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
python3.11 -m pip install -e . -q

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo ""

# Run tests
echo "Running tests..."
python3.11 -m pytest tests/ -q --tb=no

if [ $? -eq 0 ]; then
    echo "✅ All tests passed"
else
    echo "❌ Some tests failed. Please check the output above."
    exit 1
fi
echo ""

# Create necessary directories
echo "Creating configuration directories..."
CONFIG_DIR="$HOME/Library/Application Support/Alfred/Workflow Data/com.reminder-alf"
mkdir -p "$CONFIG_DIR"
mkdir -p "$CONFIG_DIR/logs"
echo "✅ Created: $CONFIG_DIR"
echo ""

# Instructions
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Install the Alfred workflow:"
echo "   - Double-click 'Reminder-Alf.alfredworkflow'"
echo "   - OR copy workflow contents to Alfred preferences"
echo ""
echo "2. Configure your AI provider:"
echo "   For OpenAI:"
echo "   rem config set openai sk-YOUR_API_KEY gpt-4"
echo ""
echo "   For Anthropic:"
echo "   rem config set anthropic sk-ant-YOUR_API_KEY claude-3-sonnet-20240229"
echo ""
echo "3. Start using it!"
echo "   rem Meeting tomorrow at 2pm"
echo "   rem Remind me to buy milk"
echo "   rem 明天下午3点开会"
echo ""
echo "For help: rem help"
echo "For docs: See README.md"
echo ""
