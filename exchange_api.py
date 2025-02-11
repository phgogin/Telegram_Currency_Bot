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

                # Process all currencies except JPY
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

                    logger.debug(f"Processing {currency} rate from {secid}")

                    try:
                        price = None
                        if currency == 'EUR':
                            logger.debug(f"Processing EUR rate - Raw data: {row}")
                            # For EUR, try all price fields in order
                            if row[indices['LAST']] is not None:
                                price = float(row[indices['LAST']])
                                logger.debug(f"EUR LAST price: {price}")
                            elif row[indices['WAPRICE']] is not None:
                                price = float(row[indices['WAPRICE']])
                                logger.debug(f"EUR WAPRICE: {price}")
                            elif row[indices['MARKETPRICE']] is not None:
                                price = float(row[indices['MARKETPRICE']])
                                logger.debug(f"EUR MARKETPRICE: {price}")
                        # For CNY and BYN, use MARKETPRICE or WAPRICE
                        elif currency in ['CNY', 'BYN']:
                            if row[indices['MARKETPRICE']] is not None:
                                price = float(row[indices['MARKETPRICE']])
                                logger.debug(f"{currency} MARKETPRICE: {price}")
                            elif row[indices['WAPRICE']] is not None:
                                price = float(row[indices['WAPRICE']])
                                logger.debug(f"{currency} WAPRICE: {price}")
                        # For USD, try all price fields
                        else:
                            if row[indices['MARKETPRICE']] is not None:
                                price = float(row[indices['MARKETPRICE']])
                            elif row[indices['WAPRICE']] is not None:
                                price = float(row[indices['WAPRICE']])
                            elif row[indices['LAST']] is not None:
                                price = float(row[indices['LAST']])

                        if price and price > 0:
                            rates[currency] = round(price, 4)
                            logger.info(f"Found rate for {currency}: {rates[currency]}")

                    except (ValueError, TypeError) as e:
                        logger.error(f"Error processing price for {currency}: {str(e)}")

                # Handle JPY and fallback for other missing rates
                if not rates.get('JPY') or len(rates) < len(CURRENCY_PAIRS) - 1:  # -1 for JPY
                    for currency, pair in CURRENCY_PAIRS.items():
                        if currency not in rates or currency == 'JPY':
                            # Find the security info for this currency
                            for row in securities_info:
                                if row[sec_indices['SECID']] == pair and row[sec_indices['BOARDID']] == 'CETS':
                                    try:
                                        if currency == 'JPY':
                                            price = float(63.71)  # JPY uses fixed LICU board value
                                            price = price / 100  # Adjust JPY rate
                                            rates[currency] = round(price, 4)
                                            logger.info(f"Set JPY rate to: {rates[currency]}")
                                            break
                                        elif row[sec_indices['PREVWAPRICE']] is not None:
                                            price = float(row[sec_indices['PREVWAPRICE']])
                                            if price > 0:
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