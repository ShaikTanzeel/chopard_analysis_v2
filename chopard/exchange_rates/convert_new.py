import pandas as pd

def convert_to_eur(df, rates_df):
    """
    Converts 'price' and 'price_before' to EUR using exchange rates.

    Args:
        df (pd.DataFrame): The main dataset containing 'currency', 'price', and 'price_before'.
        rates_df (pd.DataFrame): The exchange rates DataFrame with 'Currency' and 'Exchange Rate'.

    Returns:
        pd.DataFrame: Updated DataFrame with 'price_eur' and 'price_before_eur' columns.
    """
    
    # Ensure rates_df is indexed by currency for quick lookup
    rates_dict = rates_df.set_index('Currency')['Exchange Rate'].to_dict()

    def convert_row(row):
        """Helper function to convert a single row's prices."""
        currency = row['currency']
        exchange_rate = rates_dict.get(currency, None)  # Get exchange rate (default None if missing)
        
        if exchange_rate:
            row['price_eur'] = row['price'] / exchange_rate
            row['price_before_eur'] = row['price_before'] / exchange_rate
        else:
            row['price_eur'] = None
            row['price_before_eur'] = None
        
        return row

    # Apply conversion to each row
    df = df.apply(convert_row, axis=1)

    print("✅ Currency conversion complete. Prices now in EUR.")
    
    return df

if __name__ == "__main__":
    # Load the processed data
    df = pd.read_csv("data/processed_data.csv")

    # Load exchange rates
    rates_df = pd.read_csv("exchange_rates/exchange_rates.csv")

    # Convert prices to EUR
    df = convert_to_eur(df, rates_df)

    # Save updated data
    df.to_csv("data/processed_data_with_eur.csv", index=False)
    print("✅ Converted prices saved to 'data/processed_data_with_eur.csv'.")
