# GitHub Setup Instructions

This document provides step-by-step instructions for setting up your Currency Telegram Bot on GitHub.

## Quick Start

1. **Create a new GitHub repository**:
   - Go to https://github.com/new
   - Name your repository (e.g., "currency-telegram-bot")
   - Make it public or private as desired
   - Don't initialize with README (we already have one)

2. **Upload files to your repository**:
   - Upload all files from this folder to your GitHub repository
   - You can do this via:
     - GitHub web interface (drag and drop)
     - Git commands (see below)
     - GitHub CLI

## Git Commands Setup

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit: Currency Telegram Bot"

# Add your GitHub repository as remote
git remote add origin https://github.com/yourusername/currency-telegram-bot.git

# Push to GitHub
git push -u origin main
```

## Important Files

- **bot.py**: Main bot implementation
- **config.py**: Configuration and API endpoints
- **exchange_api.py**: Currency data fetching logic
- **utils.py**: Utility functions for formatting
- **logger.py**: Logging configuration
- **README.md**: Project documentation
- **requirements-github.txt**: Python dependencies
- **setup.py**: Package installation setup
- **install.sh**: Automated installation script
- **LICENSE**: MIT license
- **.gitignore**: Files to ignore in git

## Installation for Users

Users can install your bot using either:

1. **Direct installation**:
   ```bash
   git clone https://github.com/yourusername/currency-telegram-bot.git
   cd currency-telegram-bot
   pip install -r requirements-github.txt
   ```

2. **Using the installation script**:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

## Environment Variables

Users will need to set:
- `TELEGRAM_BOT_TOKEN`: Their Telegram bot token

## Features to Highlight

- Real-time currency rates from Moscow Exchange
- Fallback to Russian Central Bank rates
- Support for 6 major currencies
- Rate alerts and conversion features
- Robust error handling
- Comprehensive logging

## Repository Customization

Remember to:
- Update the repository URL in README.md
- Change author information in setup.py
- Add your contact information
- Update the repository description on GitHub

## Security Notes

- Never commit your actual bot token
- Use environment variables for sensitive data
- The .gitignore file already excludes sensitive files