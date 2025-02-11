import os

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN')

# MOEX API Configuration
# Updated URL format to ensure proper query for all currency pairs
MOEX_API_BASE_URL = "https://iss.moex.com/iss/engines/currency/markets/selt/securities.json?iss.meta=off&securities=USD000UTSTOM,EUR_RUB__TOM,CNYRUB_TOM,JPYRUB_TOM,BYNRUB_TOM&iss.only=marketdata,securities&lang=en"

# Logging Configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'DEBUG'  # Keep at DEBUG for detailed logging

# Currency pairs to track
CURRENCY_PAIRS = {
    'USD': 'USD000UTSTOM',
    'EUR': 'EUR_RUB__TOM',
    'CNY': 'CNYRUB_TOM',
    'JPY': 'JPYRUB_TOM',
    'BYN': 'BYNRUB_TOM'  
}