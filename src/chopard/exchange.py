"""
Exchange Rate Module
Fetches live currency exchange rates from a public API.
"""

import requests
import json
from datetime import datetime

def get_exchange_rates(base_currency="EUR"):
    """
    Fetches the latest exchange rates from a public API.
    
    Returns:
        Dictionary where keys are currencies (USD, GBP, etc.) 
        and values are the rate relative to the base currency.
    """
    api_url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        
        data = response.json()
        rates = data.get("rates", {})
        
        print(f"Fetched {len(rates)} exchange rates (Base: {base_currency})")
        return rates
        
    except Exception as e:
        print(f"Error fetching exchange rates: {e}")
        return {}

if __name__ == "__main__":
    # Test the function
    current_rates = get_exchange_rates()
    
    print(f"1 EUR = {current_rates.get('USD')} USD")
    
    # Save rates to file
    if current_rates:
        data_to_save = {
            "timestamp": datetime.now().isoformat(),
            "base_currency": "EUR",
            "rates": current_rates
        }
        with open('data/exchange_rates.json', 'w') as f:
            json.dump(data_to_save, f, indent=4)
        print("Exchange rates saved to data/exchange_rates.json")