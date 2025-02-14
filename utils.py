from datetime import datetime
from typing import Dict, Optional

# Store previous rates for comparison
previous_rates: Dict[str, float] = {}

def get_rate_mood(currency: str, current_rate: float) -> str:
    """Determine emoji mood based on rate changes"""
    if currency not in previous_rates:
        previous_rates[currency] = current_rate
        return "😐"  # Neutral face for first reading

    change = ((current_rate - previous_rates[currency]) / previous_rates[currency]) * 100
    previous_rates[currency] = current_rate  # Update previous rate

    # Define moods based on percentage changes
    if change > 2.5:
        return "📈😰"  # Strong rise (inverse mood)
    elif change > 0.5:
        return "😢"  # Moderate rise (inverse mood)
    elif change < -2.5:
        return "📉🚀"  # Strong fall (inverse mood)
    elif change < -0.5:
        return "😊"  # Moderate fall (inverse mood)
    else:
        return "😐"  # Stable

def format_currency_message(rates: Optional[Dict[str, float]]) -> str:
    """Format currency rates message according to specifications"""
    if not rates:
        return "Sorry, unable to fetch currency rates at the moment."

    current_date = datetime.now().strftime("%d.%m.%Y")

    message_lines = [
        f"CURRENT DATE: {current_date}",
        "(Indicative rates from Moscow Exchange)"
    ]

    currency_formats = {
        'USD': '1USD = {:.4f} ROUBLES {}',
        'EUR': '1EUR = {:.4f} ROUBLES {}',
        'CNY': '1CNY = {:.4f} ROUBLES {}',
        'JPY': '1JPY = {:.4f} ROUBLES {}',
        'BYN': '1BYN = {:.4f} ROUBLES {}',
        'GBP': '1GBP = {:.4f} ROUBLES {}'
    }

    for currency, format_string in currency_formats.items():
        rate = rates.get(currency)
        if rate:
            mood = get_rate_mood(currency, float(rate))
            message_lines.append(format_string.format(float(rate), mood))
        else:
            message_lines.append(f"{currency} rate unavailable ❌")

    return "\n".join(message_lines)