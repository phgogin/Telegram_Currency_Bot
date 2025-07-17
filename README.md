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
