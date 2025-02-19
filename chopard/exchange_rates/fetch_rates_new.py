import requests
import pandas as pd
import os

def get_exchange_rates():
    """Fetches exchange rates and saves them to a CSV file."""
    url = 'https://v6.exchangerate-api.com/v6/4eb043dba172cec94fe70b22/latest/EUR'
    response = requests.get(url)
    data = response.json()

    # Convert the 'conversion_rates' dictionary to a DataFrame
    conversion_rates = data["conversion_rates"]
    rates_df = pd.DataFrame(list(conversion_rates.items()), columns=['Currency', 'Exchange Rate'])
    
    # Ensure 'exchange_rates' directory exists
    os.makedirs("exchange_rates", exist_ok=True)
    
    # Save exchange rates to CSV
    rates_df.to_csv("exchange_rates/exchange_rates.csv", index=False)
    print("✅ Exchange rates fetched and saved to 'exchange_rates/exchange_rates.csv'")
    
    return rates_df  # Return the DataFrame

if __name__ == "__main__":
    rates = get_exchange_rates()
    print(rates.head())