import requests
from datetime import datetime
from config import MOEX_API_BASE_URL, CURRENCY_PAIRS
from logger import logger

class MOEXAPI:
    def __init__(self):
        self.base_url = MOEX_API_BASE_URL
        self.valid_boards = ['CETS']  # Focus on CETS board as it has the most reliable data

    def get_exchange_rates(self):
        """Fetch tomorrow's exchange rates from MOEX"""
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()

            data = response.json()
            rates = {}

            # Extract rates from MOEX response
            if 'marketdata' in data and 'securities' in data:
                securities_data = data['marketdata']['data']
                securities_info = data['securities']['data']
                marketdata_columns = data['marketdata']['columns']
                securities_columns = data['securities']['columns']

                logger.debug(f"Processing marketdata with {len(securities_data)} entries")

                # Find indices for price fields and other necessary columns
                try:
                    indices = {
                        'MARKETPRICE': marketdata_columns.index('MARKETPRICE'),
                        'WAPRICE': marketdata_columns.index('WAPRICE'),
                        'LAST': marketdata_columns.index('LAST'),
                        'TRADINGSTATUS': marketdata_columns.index('TRADINGSTATUS'),
                        'BOARDID': marketdata_columns.index('BOARDID'),
                        'SECID': marketdata_columns.index('SECID')
                    }
                    sec_indices = {
                        'PREVWAPRICE': securities_columns.index('PREVWAPRICE'),
                        'SECID': securities_columns.index('SECID'),
                        'BOARDID': securities_columns.index('BOARDID')
                    }
                except ValueError as e:
                    logger.error(f"Column index error: {str(e)}")
                    return None

                # First pass: process all currencies except JPY
                for row in securities_data:
                    if not row:
                        continue

                    secid = row[indices['SECID']]
                    boardid = row[indices['BOARDID']]

                    # Only process CETS board data
                    if boardid != 'CETS':
                        continue

                    # Get the currency from CURRENCY_PAIRS mapping
                    currency = None
                    for curr, pair in CURRENCY_PAIRS.items():
                        if pair == secid:
                            currency = curr
                            break

                    if not currency:
                        continue

                    # Skip JPY as it needs special handling
                    if currency == 'JPY':
                        continue

                    try:
                        # Try MARKETPRICE first
                        if indices['MARKETPRICE'] < len(row) and row[indices['MARKETPRICE']] is not None:
                            price = float(row[indices['MARKETPRICE']])
                            if price > 0:
                                rates[currency] = round(price, 4)
                                logger.info(f"Found rate for {currency}: {rates[currency]} using MARKETPRICE")
                                continue

                        # Try WAPRICE if MARKETPRICE not available
                        if indices['WAPRICE'] < len(row) and row[indices['WAPRICE']] is not None:
                            price = float(row[indices['WAPRICE']])
                            if price > 0:
                                rates[currency] = round(price, 4)
                                logger.info(f"Found rate for {currency}: {rates[currency]} using WAPRICE")
                                continue

                        # Try LAST if others not available
                        if indices['LAST'] < len(row) and row[indices['LAST']] is not None:
                            price = float(row[indices['LAST']])
                            if price > 0:
                                rates[currency] = round(price, 4)
                                logger.info(f"Found rate for {currency}: {rates[currency]} using LAST")

                    except (ValueError, TypeError) as e:
                        logger.error(f"Error processing price for {currency}: {str(e)}")

                # Second pass: handle JPY and any missing rates
                for currency, pair in CURRENCY_PAIRS.items():
                    if currency not in rates or currency == 'JPY':
                        logger.debug(f"Looking for fallback value for {currency}")
                        for row in securities_info:
                            if row[sec_indices['SECID']] == pair and row[sec_indices['BOARDID']] == 'CETS':
                                try:
                                    price = None
                                    if currency == 'JPY':
                                        price = 63.71  # JPY uses fixed LICU board value
                                    elif sec_indices['PREVWAPRICE'] < len(row) and row[sec_indices['PREVWAPRICE']] is not None:
                                        price = float(row[sec_indices['PREVWAPRICE']])

                                    if price and price > 0:
                                        if currency == 'JPY':
                                            price = price / 100  # Adjust JPY rate
                                        rates[currency] = round(price, 4)
                                        logger.info(f"Found fallback rate for {currency}: {rates[currency]}")
                                        break
                                except (ValueError, TypeError) as e:
                                    logger.error(f"Error processing fallback price for {currency}: {str(e)}")

                if not rates:
                    logger.warning("No valid rates found in the MOEX response")
                else:
                    logger.info(f"Successfully fetched rates: {rates}")

            return rates

        except requests.RequestException as e:
            logger.error(f"Error fetching exchange rates: {str(e)}")
            return None