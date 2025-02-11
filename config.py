import os

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN')

# MOEX API Configuration
MOEX_API_BASE_URL = "https://iss.moex.com/iss/engines/currency/markets/selt/securities.json?iss.meta=off&iss.only=marketdata&securities=USD000UTSTOM,EUR_RUB__TOM,CNYRUB_TOM,JPYRUB_TOM,BYN000UTSTOM"

# Logging Configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'DEBUG'  # Changed to DEBUG for more detailed logging

# Currency pairs to track
CURRENCY_PAIRS = {
    'USD': 'USD000UTSTOM',
    'EUR': 'EUR_RUB__TOM',
    'CNY': 'CNYRUB_TOM',
    'JPY': 'JPYRUB_TOM',
    'BYN': 'BYN000UTSTOM'
}