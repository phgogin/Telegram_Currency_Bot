import requests
from datetime import datetime
from config import MOEX_API_BASE_URL, CURRENCY_PAIRS, CBR_API_URL
from logger import logger

class MOEXAPI:
    def __init__(self):
        self.base_url = MOEX_API_BASE_URL
        self.valid_boards = ['CETS']
        self.cbr_rates = {}
        self._fetch_cbr_rates()

    def _fetch_cbr_rates(self):
        """Fetch exchange rates from Russian Central Bank"""
        try:
            response = requests.get(CBR_API_URL)
            response.raise_for_status()
            data = response.json()

            # Process CBR rates
            if 'Valute' in data:
                currencies = {
                    'EUR': 'EUR',
                    'CNY': 'CNY',
                    'BYN': 'BYN',
                    'USD': 'USD',
                    'JPY': 'JPY'
                }

                for code, cbr_code in currencies.items():
                    if cbr_code in data['Valute']:
                        rate = float(data['Valute'][cbr_code]['Value'])
                        nominal = float(data['Valute'][cbr_code]['Nominal'])
                        self.cbr_rates[code] = round(rate / nominal, 4)
                        logger.info(f"Fetched CBR rate for {code}: {self.cbr_rates[code]}")

        except requests.RequestException as e:
            logger.error(f"Error fetching CBR rates: {str(e)}")

    def get_exchange_rates(self):
        """Fetch exchange rates from MOEX API"""
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()

            data = response.json()
            rates = {}

            # Extract rates from MOEX response
            if 'marketdata' in data and 'securities' in data:
                securities_data = data['marketdata']['data']
                marketdata_columns = data['marketdata']['columns']

                # Find indices for required fields
                try:
                    indices = {
                        'LAST': marketdata_columns.index('LAST'),
                        'TRADINGSTATUS': marketdata_columns.index('TRADINGSTATUS'),
                        'BOARDID': marketdata_columns.index('BOARDID'),
                        'SECID': marketdata_columns.index('SECID')
                    }
                except ValueError as e:
                    logger.error(f"Column index error: {str(e)}")
                    return self.cbr_rates

                # Process all currencies
                for row in securities_data:
                    if not row:
                        continue

                    secid = row[indices['SECID']]
                    boardid = row[indices['BOARDID']]
                    trading_status = row[indices['TRADINGSTATUS']]

                    # Only process CETS board data and active trading
                    if boardid != 'CETS' or trading_status != 'T':
                        continue

                    # Get the currency from CURRENCY_PAIRS mapping
                    currency = None
                    for curr, pair in CURRENCY_PAIRS.items():
                        if pair == secid:
                            currency = curr
                            break

                    if not currency:
                        continue

                    try:
                        # Use LAST price as Indicative Rate
                        if row[indices['LAST']] is not None:
                            price = float(row[indices['LAST']])
                            if price > 0:
                                if currency == 'JPY':
                                    price = price / 100  # Adjust JPY rate
                                rates[currency] = round(price, 4)
                                logger.info(f"Found MOEX rate for {currency}: {rates[currency]}")

                    except (ValueError, TypeError) as e:
                        logger.error(f"Error processing price for {currency}: {str(e)}")

                if rates:
                    logger.info(f"Successfully fetched MOEX rates: {rates}")
                    return rates
                else:
                    logger.warning("No valid rates found in MOEX response, falling back to CBR rates")
                    return self.cbr_rates

            return self.cbr_rates

        except requests.RequestException as e:
            logger.error(f"Error fetching MOEX rates: {str(e)}")
            logger.info("Falling back to CBR rates")
            return self.cbr_rates