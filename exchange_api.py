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

            # Log the response structure for debugging
            logger.debug(f"API Response structure: {data.keys()}")

            # Extract rates from MOEX response
            if 'marketdata' in data:
                securities_data = data['marketdata']['data']
                columns = data['marketdata']['columns']

                logger.debug(f"Columns available: {columns}")
                logger.debug(f"Securities data: {securities_data}")

                # Find the index of MARKETPRICE column (indicative price)
                try:
                    price_index = columns.index('MARKETPRICE')
                    secid_index = columns.index('SECID')
                except ValueError as e:
                    logger.error(f"Required columns not found in MOEX response. Available columns: {columns}")
                    return None

                # Process each security
                for row in securities_data:
                    if len(row) > max(price_index, secid_index):
                        secid = row[secid_index]
                        price = row[price_index]

                        logger.debug(f"Processing security: {secid} with price: {price}")

                        # Match security with our configured pairs
                        for currency, pair in CURRENCY_PAIRS.items():
                            if pair == secid and price is not None:
                                try:
                                    rates[currency] = float(price)
                                    logger.info(f"Successfully parsed {currency} rate: {price}")
                                except (ValueError, TypeError):
                                    logger.warning(f"Invalid rate value for {currency}: {price}")
                                    rates[currency] = None

            if not rates:
                logger.warning("No valid rates found in the MOEX response")

            return rates

        except requests.RequestException as e:
            logger.error(f"Error fetching exchange rates: {str(e)}")
            return None