#!/bin/bash

# Currency Telegram Bot Installation Script
echo "Installing Currency Telegram Bot..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install python-telegram-bot[job-queue]>=21.10 requests>=2.32.3

# Check if bot token is set
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo ""
    echo "⚠️  TELEGRAM_BOT_TOKEN environment variable is not set!"
    echo "Please set your Telegram bot token:"
    echo "export TELEGRAM_BOT_TOKEN=your_bot_token_here"
    echo ""
    echo "Or create a .env file with:"
    echo "TELEGRAM_BOT_TOKEN=your_bot_token_here"
    echo ""
fi

echo "✅ Installation complete!"
echo ""
echo "To run the bot:"
echo "1. Set your TELEGRAM_BOT_TOKEN environment variable"
echo "2. Run: python bot.py"
echo ""
echo "For more information, see README.md"