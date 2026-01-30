"""
Chopard Pricing Analysis - Exploratory Data Analysis Script

This script performs EDA on the processed watch data:
1. Basic statistics
2. Collection analysis
3. Regional price comparison
4. Generates visualizations
5. Creates summary report

Usage:
    python scripts/run_eda.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Set style for charts
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Create output directory
os.makedirs('data/visualizations', exist_ok=True)


def load_data():
    """Load the processed data from Phase 1."""
    print("Loading processed data...")
    df = pd.read_csv('data/final_processed_data.csv')
    print(f"  Loaded {len(df)} records")
    return df


def basic_statistics(df):
    """Calculate and print basic statistics."""
    print("\n" + "="*60)
    print("BASIC STATISTICS")
    print("="*60)
    
    print("\nDataset Shape:")
    print(f"  Rows: {df.shape[0]}")
    print(f"  Columns: {df.shape[1]}")
    
    print("\nPrice Statistics (EUR):")
    price_stats = df['price_eur'].describe()
    print(f"  Count:   {price_stats['count']:,.0f}")
    print(f"  Mean:    {price_stats['mean']:,.0f} EUR")
    print(f"  Median:  {price_stats['50%']:,.0f} EUR")
    print(f"  Std Dev: {price_stats['std']:,.0f} EUR")
    print(f"  Min:     {price_stats['min']:,.0f} EUR")
    print(f"  Max:     {price_stats['max']:,.0f} EUR")
    
    return price_stats


def analyze_collections(df):
    """Analyze prices by collection."""
    print("\n" + "="*60)
    print("COLLECTION ANALYSIS")
    print("="*60)
    
    # Group by collection
    collection_stats = df.groupby('collection').agg({
        'price_eur': ['count', 'mean', 'median', 'min', 'max']
    }).round(0)
    
    collection_stats.columns = ['Count', 'Mean', 'Median', 'Min', 'Max']
    collection_stats = collection_stats.sort_values('Mean', ascending=False)
    
    print("\nCollections by Average Price:")
    for collection, row in collection_stats.iterrows():
        print(f"\n  {collection}:")
        print(f"    Count:  {int(row['Count'])} watches")
        print(f"    Mean:   {row['Mean']:,.0f} EUR")
        print(f"    Median: {row['Median']:,.0f} EUR")
        print(f"    Range:  {row['Min']:,.0f} - {row['Max']:,.0f} EUR")
    
    return collection_stats


def analyze_regions(df):
    """Analyze prices by country/region."""
    print("\n" + "="*60)
    print("REGIONAL PRICE ANALYSIS")
    print("="*60)
    
    # Group by country
    region_stats = df.groupby('country').agg({
        'price_eur': ['count', 'mean', 'median']
    }).round(0)
    
    region_stats.columns = ['Count', 'Mean', 'Median']
    region_stats = region_stats.sort_values('Mean', ascending=False)
    
    print("\nPrices by Region:")
    for country, row in region_stats.iterrows():
        print(f"  {country}: Mean {row['Mean']:,.0f} EUR, Median {row['Median']:,.0f} EUR ({int(row['Count'])} watches)")
    
    # Calculate price premium
    min_mean = region_stats['Mean'].min()
    region_stats['Premium %'] = ((region_stats['Mean'] - min_mean) / min_mean * 100).round(1)
    
    print("\nPrice Premium vs Lowest Region:")
    for country, row in region_stats.iterrows():
        if row['Premium %'] > 0:
            print(f"  {country}: +{row['Premium %']}% premium")
        else:
            print(f"  {country}: Baseline (lowest prices)")
    
    return region_stats


def create_visualizations(df, collection_stats, region_stats):
    """Create and save all visualizations."""
    print("\n" + "="*60)
    print("CREATING VISUALIZATIONS")
    print("="*60)
    
    # Chart 1: Price Distribution
    print("\nChart 1: Price Distribution...")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data=df, x='price_eur', bins=30, kde=True, color='steelblue', ax=ax)
    
    mean_price = df['price_eur'].mean()
    median_price = df['price_eur'].median()
    
    ax.axvline(mean_price, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_price:,.0f} EUR')
    ax.axvline(median_price, color='green', linestyle='-', linewidth=2, label=f'Median: {median_price:,.0f} EUR')
    
    ax.set_title('Distribution of Chopard Watch Prices', fontsize=14, fontweight='bold')
    ax.set_xlabel('Price (EUR)', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.legend()
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K EUR'))
    
    plt.tight_layout()
    plt.savefig('data/visualizations/01_price_distribution.png', dpi=150)
    plt.close()
    print("  Saved: data/visualizations/01_price_distribution.png")
    
    # Chart 2: Prices by Collection
    print("Chart 2: Prices by Collection...")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    collection_order = df.groupby('collection')['price_eur'].median().sort_values(ascending=False).index
    sns.boxplot(data=df, x='collection', y='price_eur', order=collection_order, palette='coolwarm', ax=ax)
    
    ax.set_title('Price Distribution by Collection', fontsize=14, fontweight='bold')
    ax.set_xlabel('Collection', fontsize=12)
    ax.set_ylabel('Price (EUR)', fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K EUR'))
    
    plt.tight_layout()
    plt.savefig('data/visualizations/02_price_by_collection.png', dpi=150)
    plt.close()
    print("  Saved: data/visualizations/02_price_by_collection.png")
    
    # Chart 3: Prices by Region
    print("Chart 3: Regional Price Comparison...")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    region_order = df.groupby('country')['price_eur'].median().sort_values(ascending=False).index
    sns.boxplot(data=df, x='country', y='price_eur', order=region_order, palette='viridis', ax=ax)
    
    ax.set_title('Regional Price Comparison', fontsize=14, fontweight='bold')
    ax.set_xlabel('Country/Region', fontsize=12)
    ax.set_ylabel('Price (EUR)', fontsize=12)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K EUR'))
    
    plt.tight_layout()
    plt.savefig('data/visualizations/03_price_by_region.png', dpi=150)
    plt.close()
    print("  Saved: data/visualizations/03_price_by_region.png")
    
    # Chart 4: Collection Composition
    print("Chart 4: Collection Composition...")
    
    fig, ax = plt.subplots(figsize=(10, 8))
    collection_counts = df['collection'].value_counts()
    
    wedges, texts, autotexts = ax.pie(
        collection_counts.values, 
        labels=collection_counts.index,
        autopct='%1.1f%%',
        colors=sns.color_palette('husl', len(collection_counts)),
        explode=[0.05 if i == 0 else 0 for i in range(len(collection_counts))]
    )
    
    ax.set_title('Watch Distribution by Collection', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('data/visualizations/04_collection_composition.png', dpi=150)
    plt.close()
    print("  Saved: data/visualizations/04_collection_composition.png")
    
    # Chart 5: Price Heatmap
    print("Chart 5: Price Heatmap (Collection x Region)...")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    pivot = df.pivot_table(
        values='price_eur', 
        index='collection', 
        columns='country', 
        aggfunc='mean'
    ).round(0)
    
    sns.heatmap(pivot, annot=True, fmt=',.0f', cmap='YlOrRd', 
                ax=ax, cbar_kws={'label': 'Average Price (EUR)'})
    
    ax.set_title('Average Price: Collection x Region', fontsize=14, fontweight='bold')
    ax.set_xlabel('Country', fontsize=12)
    ax.set_ylabel('Collection', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('data/visualizations/05_price_heatmap.png', dpi=150)
    plt.close()
    print("  Saved: data/visualizations/05_price_heatmap.png")
    
    print("\nAll visualizations saved to data/visualizations/")


def generate_insights(df, collection_stats, region_stats):
    """Generate key insights from the analysis."""
    print("\n" + "="*60)
    print("KEY INSIGHTS")
    print("="*60)
    
    insights = []
    
    # Insight 1: Most popular collection
    most_popular = df['collection'].value_counts().idxmax()
    popular_count = df['collection'].value_counts().max()
    popular_pct = (popular_count / len(df)) * 100
    insight1 = f"1. {most_popular} is the most popular collection ({popular_count} watches, {popular_pct:.1f}%)"
    insights.append(insight1)
    print(f"\n{insight1}")
    
    # Insight 2: Most expensive collection
    most_expensive = collection_stats['Mean'].idxmax()
    exp_mean = collection_stats.loc[most_expensive, 'Mean']
    insight2 = f"2. {most_expensive} is the most expensive (avg {exp_mean:,.0f} EUR)"
    insights.append(insight2)
    print(insight2)
    
    # Insight 3: Regional price difference
    max_region = region_stats['Mean'].idxmax()
    min_region = region_stats['Mean'].idxmin()
    price_diff_pct = region_stats.loc[max_region, 'Premium %']
    insight3 = f"3. {max_region} is {price_diff_pct:.1f}% more expensive than {min_region}"
    insights.append(insight3)
    print(insight3)
    
    # Insight 4: Price distribution
    skewness = df['price_eur'].skew()
    if skewness > 1:
        shape = "highly right-skewed"
    elif skewness > 0.5:
        shape = "moderately right-skewed"
    else:
        shape = "relatively symmetric"
    insight4 = f"4. Price distribution is {shape} (skewness: {skewness:.2f})"
    insights.append(insight4)
    print(insight4)
    
    # Insight 5: Price range
    most_varied = (collection_stats['Max'] - collection_stats['Min']).idxmax()
    var_range = collection_stats.loc[most_varied, 'Max'] - collection_stats.loc[most_varied, 'Min']
    insight5 = f"5. {most_varied} has the widest price range ({var_range:,.0f} EUR)"
    insights.append(insight5)
    print(insight5)
    
    return insights


def save_eda_report(df, collection_stats, region_stats, insights):
    """Save a summary report."""
    report_path = 'data/eda_summary_report.txt'
    
    with open(report_path, 'w') as f:
        f.write("="*60 + "\n")
        f.write("CHOPARD PRICING ANALYSIS - EDA SUMMARY REPORT\n")
        f.write("="*60 + "\n\n")
        
        f.write("DATASET OVERVIEW\n")
        f.write(f"  Total watches: {len(df)}\n")
        f.write(f"  Collections: {df['collection'].nunique()}\n")
        f.write(f"  Regions: {df['country'].nunique()}\n\n")
        
        f.write("PRICE SUMMARY (EUR)\n")
        f.write(f"  Mean:   {df['price_eur'].mean():,.0f}\n")
        f.write(f"  Median: {df['price_eur'].median():,.0f}\n")
        f.write(f"  Min:    {df['price_eur'].min():,.0f}\n")
        f.write(f"  Max:    {df['price_eur'].max():,.0f}\n\n")
        
        f.write("KEY INSIGHTS\n")
        for insight in insights:
            f.write(f"  {insight}\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write("Visualizations saved in: data/visualizations/\n")
    
    print(f"\nReport saved: {report_path}")


def main():
    """Main EDA function."""
    print("\n" + "="*60)
    print("CHOPARD PRICING - EXPLORATORY DATA ANALYSIS")
    print("="*60)
    
    # Step 1: Load data
    df = load_data()
    
    # Step 2: Basic statistics
    price_stats = basic_statistics(df)
    
    # Step 3: Collection analysis
    collection_stats = analyze_collections(df)
    
    # Step 4: Regional analysis
    region_stats = analyze_regions(df)
    
    # Step 5: Create visualizations
    create_visualizations(df, collection_stats, region_stats)
    
    # Step 6: Generate insights
    insights = generate_insights(df, collection_stats, region_stats)
    
    # Step 7: Save report
    save_eda_report(df, collection_stats, region_stats, insights)
    
    print("\n" + "="*60)
    print("EDA COMPLETE")
    print("="*60)
    print("\nOutputs:")
    print("  - data/visualizations/  (5 charts)")
    print("  - data/eda_summary_report.txt")
    print("\n")
    
    return df


if __name__ == "__main__":
    main()
