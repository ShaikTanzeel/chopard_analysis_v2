import fetch_rates

def convert_to_eur(amount, currency):
    """
    Convert a given amount from any currency to EUR.
    
    Parameters:
    - amount (float): The amount to convert
    - currency (str): The currency code (e.g., 'USD', 'GBP')

    Returns:
    - float: The equivalent amount in EUR
    """
    exchange_rates = fetch_rates.get_exchange_rates()

    if currency not in exchange_rates:
        raise ValueError(f"Currency '{currency}' not found in exchange rates.")
    
    conversion_rate = exchange_rates[currency]
    return round(amount / conversion_rate, 2)


# test
if __name__ == "__main__":
    test_amount = 100  # Example amount
    test_currency = "USD"  # Convert from USD to EUR

    converted_value = convert_to_eur(test_amount, test_currency)
    print(f"{test_amount} {test_currency} is equivalent to {converted_value} EUR")
