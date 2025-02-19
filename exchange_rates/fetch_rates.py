import requests
import pandas as pd

def get_exchange_rates():
    url = 'https://v6.exchangerate-api.com/v6/4eb043dba172cec94fe70b22/latest/EUR'
    response = requests.get(url)
    data = response.json()

    # Convert DataFrame to dictionary
    conversion_rates = data["conversion_rates"]
    return conversion_rates  # ✅ Return a dictionary instead of a DataFrame

if __name__ == "__main__":
    rates = get_exchange_rates()
    print(rates)  # ✅ Check if the function returns the correct dictionary
