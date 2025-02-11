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
        """Fetch exchange rates from Russian Central Bank as fallback"""
        try:
            response = requests.get(CBR_API_URL)
            response.raise_for_status()
            data = response.json()

            if 'Valute' in data:
                currencies = {
                    'EUR': 'EUR',
                    'CNY': 'CNY',
                    'BYN': 'BYN',
                    'USD': 'USD',
                    'JPY': 'JPY',
                    'GBP': 'GBP'  # Added GBP to CBR currencies
                }

                for code, cbr_code in currencies.items():
                    if cbr_code in data['Valute']:
                        rate = float(data['Valute'][cbr_code]['Value'])
                        nominal = float(data['Valute'][cbr_code]['Nominal'])
                        self.cbr_rates[code] = round(rate / nominal, 4)
                        logger.debug(f"Fetched CBR rate for {code}: {self.cbr_rates[code]}")

        except requests.RequestException as e:
            logger.error(f"Error fetching CBR rates: {str(e)}")

    def get_exchange_rates(self):
        """Fetch exchange rates from MOEX API with CBR fallback"""
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            data = response.json()
            rates = {}

            if 'marketdata' not in data:
                logger.warning("No marketdata in MOEX response")
                return self.cbr_rates

            securities_data = data['marketdata']['data']
            marketdata_columns = data['marketdata']['columns']

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

            # Process each row in MOEX data
            for row in securities_data:
                if not row:
                    continue

                secid = row[indices['SECID']]
                boardid = row[indices['BOARDID']]
                trading_status = row[indices['TRADINGSTATUS']]
                last_price = row[indices['LAST']]

                # Skip if not on CETS board or not actively trading
                if boardid != 'CETS' or trading_status != 'T':
                    logger.debug(f"Skipping {secid}: board={boardid}, status={trading_status}")
                    continue

                # Map MOEX security ID to currency code
                currency = None
                for curr, pair in CURRENCY_PAIRS.items():
                    if pair == secid:
                        currency = curr
                        break

                if not currency:
                    continue

                try:
                    if last_price is not None:
                        price = float(last_price)
                        if price > 0:
                            if currency == 'JPY':
                                price = price / 100  # Adjust JPY rate
                            rates[currency] = round(price, 4)
                            logger.info(f"Using MOEX rate for {currency}: {rates[currency]} (LAST price)")
                except (ValueError, TypeError) as e:
                    logger.error(f"Error processing MOEX rate for {currency}: {str(e)}")

            # Fill missing rates with CBR data
            for currency in CURRENCY_PAIRS.keys():
                if currency not in rates and currency in self.cbr_rates:
                    rates[currency] = self.cbr_rates[currency]
                    # Special log message for CNY and GBP to indicate intentional CBR usage
                    if currency in ['CNY', 'GBP']:
                        logger.info(f"Using CBR rate for {currency} as preferred source: {self.cbr_rates[currency]}")
                    else:
                        logger.info(f"Using CBR fallback rate for {currency}: {rates[currency]}")

            return rates if rates else self.cbr_rates

        except requests.RequestException as e:
            logger.error(f"Error fetching MOEX rates: {str(e)}")
            logger.info("Using CBR rates as fallback")
            return self.cbr_rates