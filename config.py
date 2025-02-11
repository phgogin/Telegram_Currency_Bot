import os

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN')

# MOEX API Configuration
# Updated URL format to use tomorrow's rates (TOM) for all currency pairs
MOEX_API_BASE_URL = "https://iss.moex.com/iss/engines/currency/markets/selt/securities.json?iss.meta=off&securities=CNYRUB_TOM,USD000UTSTOM,JPYRUB_TOM,EURRUB_TOM,BYNRUB_TOM&iss.only=marketdata,securities&lang=en"

# Russian Central Bank API Configuration
CBR_API_URL = "https://www.cbr-xml-daily.ru/daily_json.js"

# Logging Configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'DEBUG'  # Keep at DEBUG for detailed logging

# Currency pairs to track
CURRENCY_PAIRS = {
    'CNY': 'CNYRUB_TOM',      # Tomorrow CNY rate
    'USD': 'USD000UTSTOM',    # Tomorrow USD rate
    'JPY': 'JPYRUB_TOM',      # Tomorrow JPY rate
    'EUR': 'EURRUB_TOM',      # Tomorrow EUR rate
    'BYN': 'BYNRUB_TOM'       # Tomorrow BYN rate
}