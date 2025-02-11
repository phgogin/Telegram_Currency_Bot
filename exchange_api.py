import requests
from datetime import datetime
from config import MOEX_API_BASE_URL, CURRENCY_PAIRS
from logger import logger

class MOEXAPI:
    def __init__(self):
        self.base_url = MOEX_API_BASE_URL
        self.valid_boards = ['CETS', 'SELT', 'MTLX', 'AUCB']

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
                        'HIGHBID': marketdata_columns.index('HIGHBID'),
                        'BIDDEPTH': marketdata_columns.index('BIDDEPTH'),
                        'LOWOFFER': marketdata_columns.index('LOWOFFER'),
                        'OFFERDEPTH': marketdata_columns.index('OFFERDEPTH'),
                        'SPREAD': marketdata_columns.index('SPREAD'),
                        'HIGH': marketdata_columns.index('HIGH'),
                        'LOW': marketdata_columns.index('LOW'),
                        'OPEN': marketdata_columns.index('OPEN'),
                        'LAST': marketdata_columns.index('LAST'),
                        'WAPRICE': marketdata_columns.index('WAPRICE'),
                        'MARKETPRICE': marketdata_columns.index('MARKETPRICE'),
                        'SECID': marketdata_columns.index('SECID'),
                        'BOARDID': marketdata_columns.index('BOARDID'),
                        'TRADINGSTATUS': marketdata_columns.index('TRADINGSTATUS'),
                        'PREVWAPRICE': marketdata_columns.index('PREVWAPRICE')
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
                    trading_status = row[indices['TRADINGSTATUS']]

                    logger.debug(f"Processing security: {secid} on board: {boardid} status: {trading_status}")
                    logger.debug(f"Raw row data: {row}")

                    # Skip processing if not a valid trading board
                    if boardid not in self.valid_boards:
                        logger.debug(f"Skipping non-trading board: {boardid}")
                        continue

                    # Try different price fields in order of preference
                    price = None
                    used_field = None

                    # Define price fields order based on currency
                    if 'CNY' in secid:
                        price_fields = ['MARKETPRICE', 'WAPRICE', 'LAST', 'HIGH', 'LOW', 'OPEN']
                    elif 'JPY' in secid:
                        # For JPY, try to get any available price even if trading is closed
                        price_fields = ['MARKETPRICE', 'WAPRICE', 'PREVWAPRICE', 'LAST', 'HIGH', 'LOW', 'OPEN']
                        # Only skip if not in normal or trading status for non-JPY currencies
                        
                    else:
                        price_fields = ['WAPRICE', 'MARKETPRICE', 'LAST', 'HIGH', 'LOW', 'OPEN']

                    for field in price_fields:
                        if idx := indices.get(field):
                            if idx < len(row) and row[idx] is not None:
                                try:
                                    current_price = float(row[idx])
                                    if current_price > 0:
                                        # For JPY, adjust the scaling factor
                                        if 'JPY' in secid:
                                            current_price = current_price / 100  # JPY is quoted per 100 units
                                            logger.debug(f"Adjusted JPY price from {row[idx]} to {current_price}")
                                        price = current_price
                                        used_field = field
                                        logger.debug(f"Found price using {field} for {secid} on {boardid}: {price}")
                                        break
                                except (ValueError, TypeError):
                                    continue

                    # Update best price if this is better than previous
                    if price is not None and price > 0:
                        for currency, pair in CURRENCY_PAIRS.items():
                            matched = False
                            if isinstance(pair, list):  # Handle multiple security IDs (e.g., BYN)
                                if secid in pair:
                                    matched = True
                            elif pair == secid:
                                matched = True

                            if matched:
                                if currency not in best_prices or price > best_prices[currency]:
                                    best_prices[currency] = price
                                    logger.debug(f"Updated price for {currency} using {secid}: {price} (from {used_field})")

                # Set final rates using best prices
                for currency, price in best_prices.items():
                    try:
                        if price is not None and price > 0:
                            rates[currency] = round(float(price), 4)  # Round to 4 decimal places
                            logger.info(f"Final {currency} rate: {rates[currency]} (from price: {price})")
                        else:
                            logger.warning(f"Invalid price for {currency}: {price}")
                            rates[currency] = None
                    except (ValueError, TypeError) as e:
                        logger.error(f"Invalid rate value for {currency}: {price}, Error: {str(e)}")
                        rates[currency] = None

                if not rates:
                    logger.warning("No valid rates found in the MOEX response")
                else:
                    logger.info(f"All fetched rates: {rates}")

            return rates

        except requests.RequestException as e:
            logger.error(f"Error fetching exchange rates: {str(e)}")
            return None