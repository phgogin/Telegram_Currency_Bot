from datetime import datetime

def format_currency_message(rates):
    """Format currency rates message according to specifications"""
    if not rates:
        return "Sorry, unable to fetch currency rates at the moment."

    current_date = datetime.now().strftime("%d.%m.%Y")

    message_lines = [
        f"CURRENT DATE: {current_date}",
        "(Indicative rates from Moscow Exchange)"
    ]

    currency_formats = {
        'USD': '1USD = {:.4f} ROUBLES',
        'EUR': '1EUR = {:.4f} ROUBLES',
        'CNY': '1CNY = {:.4f} ROUBLES',
        'JPY': '1JPY = {:.4f} ROUBLES',
        'BYN': '1BYN = {:.4f} ROUBLES'
    }

    for currency, format_string in currency_formats.items():
        rate = rates.get(currency)
        if rate:
            message_lines.append(format_string.format(float(rate)))
        else:
            message_lines.append(f"{currency} rate unavailable")

    return "\n".join(message_lines)