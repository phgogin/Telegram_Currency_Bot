import requests
from datetime import datetime
from config import MOEX_API_BASE_URL, CURRENCY_PAIRS
from logger import logger

class MOEXAPI:
    def __init__(self):
        self.base_url = MOEX_API_BASE_URL

    def get_exchange_rates(self):
        """Fetch current exchange rates from MOEX"""
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()

            data = response.json()
            rates = {}
            best_prices = {}  # Track best prices across different boards

            # Log the response structure for debugging
            logger.debug(f"API Response structure: {data.keys()}")

            # Extract rates from MOEX response
            if 'marketdata' in data and 'securities' in data:
                securities_data = data['marketdata']['data']
                securities_info = data['securities']['data']
                marketdata_columns = data['marketdata']['columns']
                securities_columns = data['securities']['columns']

                logger.debug(f"Marketdata columns available: {marketdata_columns}")
                logger.debug(f"Securities columns available: {securities_columns}")

                # Find indices for all possible price fields
                try:
                    indices = {
                        'MARKETPRICE': marketdata_columns.index('MARKETPRICE'),
                        'WAPRICE': marketdata_columns.index('WAPRICE'),
                        'LAST': marketdata_columns.index('LAST'),
                        'OPEN': marketdata_columns.index('OPEN'),
                        'SECID': marketdata_columns.index('SECID'),
                        'BOARDID': marketdata_columns.index('BOARDID')
                    }
                except ValueError as e:
                    logger.error(f"Column index error: {str(e)}")
                    return None

                # Process each security
                for row in securities_data:
                    if not row:
                        continue

                    secid = row[indices['SECID']]
                    boardid = row[indices['BOARDID']]
                    logger.debug(f"Processing security: {secid} on board: {boardid}")
                    logger.debug(f"Raw row data: {row}")

                    # Try different price fields in order of preference
                    price = None
                    used_field = None
                    for field in ['MARKETPRICE', 'WAPRICE', 'LAST', 'OPEN']:
                        if idx := indices.get(field):
                            if idx < len(row) and row[idx] is not None:
                                price = row[idx]
                                used_field = field
                                logger.debug(f"Found price using {field} for {secid} on {boardid}: {price}")
                                break

                    # Update best price if this is better than previous
                    if price is not None and price > 0:  # Added price > 0 check
                        for currency, pair in CURRENCY_PAIRS.items():
                            if pair == secid:
                                if currency not in best_prices or price > best_prices[currency]:
                                    best_prices[currency] = price
                                    logger.debug(f"Updated best price for {currency}: {price} from {boardid} using {used_field}")

                # Set final rates using best prices
                for currency, price in best_prices.items():
                    try:
                        rates[currency] = float(price)
                        logger.info(f"Successfully parsed {currency} rate: {price}")
                    except (ValueError, TypeError) as e:
                        logger.error(f"Invalid rate value for {currency}: {price}, Error: {str(e)}")
                        rates[currency] = None

                if not rates:
                    logger.warning("No valid rates found in the MOEX response")
                else:
                    logger.info(f"Fetched rates: {rates}")

            return rates

        except requests.RequestException as e:
            logger.error(f"Error fetching exchange rates: {str(e)}")
            return None