# Currency Exchange Rate Telegram Bot

A sophisticated Telegram bot that provides real-time currency exchange rates with advanced tracking and multi-source data retrieval capabilities.

## Features

- **Real-time Currency Rates**: Fetches current exchange rates from multiple sources
- **Multi-source Data**: Uses Moscow Exchange (MOEX) as primary source with Russian Central Bank (CBR) as fallback
- **Multiple Currency Support**: USD, EUR, CNY, JPY, BYN, GBP
- **Rate Alerts**: Set custom alerts for rate thresholds
- **Currency Conversion**: Convert between supported currencies
- **Rate Mood Indicators**: Visual indicators showing rate trends
- **Robust Error Handling**: Graceful fallbacks and error recovery

## Supported Currencies

- USD (US Dollar)
- EUR (Euro)
- CNY (Chinese Yuan)
- JPY (Japanese Yen)
- BYN (Belarusian Ruble)
- GBP (British Pound)

## Bot Commands

- `/start` - Start the bot and see available commands
- `/stop` - Stop the bot
- `/usdrate` - Get current USD rate
- `/eurrate` - Get current EUR rate
- `/cnyrate` - Get current CNY rate
- `/jpyrate` - Get current JPY rate
- `/bynrate` - Get current BYN rate
- `/gbprate` - Get current GBP rate
- `/allrates` - Get all currency rates
- `/convert` - Convert currencies (e.g., `/convert 100 USD to RUB`)
- `/setalert` - Set rate alert (e.g., `/setalert USD > 100`)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/currency-telegram-bot.git
cd currency-telegram-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export TELEGRAM_BOT_TOKEN=your_bot_token_here
```

4. Run the bot:
```bash
python bot.py
```

## Configuration

The bot uses multiple configuration sources:

- **MOEX API**: Moscow Exchange for real-time trading data
- **CBR API**: Russian Central Bank for fallback rates
- **Telegram Bot API**: For bot functionality

## Project Structure

```
├── bot.py              # Main bot implementation
├── config.py           # Configuration settings
├── exchange_api.py     # API integration for currency data
├── utils.py            # Utility functions for formatting
├── logger.py           # Logging configuration
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Technical Details

### Data Sources

1. **Primary Source - MOEX API**: 
   - Real-time trading data from Moscow Exchange
   - Supports tomorrow's rates (TOM) for all currency pairs
   - Active trading status verification

2. **Fallback Source - CBR API**:
   - Russian Central Bank daily rates
   - Used when MOEX data is unavailable
   - Reliable backup for all supported currencies

### Features

- **Intelligent Rate Selection**: Automatically chooses the best available rate source
- **Rate Mood Indicators**: Visual feedback on rate trends using emojis
- **Async Implementation**: Efficient handling of multiple requests
- **Comprehensive Logging**: Detailed logs for debugging and monitoring
- **Error Recovery**: Graceful handling of API failures and network issues

## Environment Variables

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token (required)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues and questions, please create an issue on the GitHub repository.