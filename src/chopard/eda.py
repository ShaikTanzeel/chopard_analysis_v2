"""
Exploratory Data Analysis (EDA) Module
Loads data and performs basic analysis to understand the dataset.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from chopard.processor import extract_data_from_bigquery

def perform_eda():
    """
    Loads data and performs exploratory analysis to understand structure and quality.
    """
    # Step 1: Fetch data from BigQuery
    print("Step 1: Fetching data...")
    df = extract_data_from_bigquery("raw_pricing")
    
    # Step 2: Check basic structure
    print("\nStep 2: Data Structure")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    print("\nColumn Info:")
    print(df.info())

    # Step 3: Check for missing values
    print("\nStep 3: Missing Values")
    missing = df.isnull().sum()
    print(missing[missing > 0])
    
    # Step 4: Look at currency distribution
    print("\nStep 4: Currency Distribution")
    currency_counts = df['currency'].value_counts()
    print(currency_counts)
    
    # Step 5: Basic price statistics
    print("\nStep 5: Price Statistics")
    print(df['price'].describe())

    # Step 6: Generate a simple histogram
    print("\nStep 6: Generating Price Distribution Chart...")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['price'], bins=30, kde=True)
    plt.title("Distribution of Watch Prices")
    plt.xlabel("Price")
    plt.ylabel("Count")
    
    output_path = "data/eda_price_distribution.png"
    plt.savefig(output_path)
    print(f"Chart saved to: {output_path}")

if __name__ == "__main__":
    perform_eda()