# Chopard Watch Pricing Analysis

A data analysis project exploring pricing strategies of Chopard luxury watches across different regions and collections.

## Project Overview

This project analyzes pricing data from Chopard's official website across 5 countries (Switzerland, USA, UK, Japan, EU) to understand:

- How prices vary across different watch collections
- Regional pricing differences for the same products
- Price distribution patterns in the luxury watch market

## Key Findings

- **990 watches** analyzed after data cleaning
- **Price range**: €3,750 - €110,000
- **Average price**: €30,294 (Median: €21,000)
- **L'Heure du Diamant** is the most expensive collection (~€70,000 avg)
- **Happy Sport** is the most accessible collection (~€15,000 avg)
- Prices vary by region, suggesting regional pricing strategies

## Project Structure

```
chopard_pricing_analysis/
├── data/
│   ├── final_processed_data.csv    # Cleaned dataset
│   ├── visualizations/             # Generated charts
│   └── eda_summary_report.txt      # Analysis summary
├── notebooks/
│   ├── 01_exploratory_data_analysis.ipynb  # EDA notebook
│   └── Notes                       # Analysis notes
├── scripts/
│   ├── run_pipeline.py             # Main ETL pipeline
│   └── run_eda.py                  # EDA script
├── src/chopard/
│   ├── config.py                   # Configuration
│   ├── data_ingestion.py           # Data loading
│   ├── processor.py                # Data cleaning & transformation
│   └── exchange.py                 # Currency conversion
├── requirements.txt
└── README.md
```

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Data processing and analysis |
| Pandas | Data manipulation |
| Matplotlib/Seaborn | Visualizations |
| BigQuery | Cloud data warehouse |
| Power BI | Dashboard (coming soon) |

## Data Pipeline

The ETL (Extract-Transform-Load) pipeline:

1. **Extract**: Load raw watch data from Excel/BigQuery
2. **Transform**: 
   - Remove null prices and duplicates
   - Convert all currencies to EUR using live exchange rates
   - Clean and standardize collection names
3. **Load**: Save processed data to CSV and BigQuery

```bash
# Run the pipeline
python scripts/run_pipeline.py
```

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/chopard_pricing_analysis.git
cd chopard_pricing_analysis
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file with your credentials:
```
GCP_PROJECT_ID=your-project-id
BIGQUERY_DATASET_ID=your-dataset
```

## Running the Analysis

**Option 1: Run the pipeline**
```bash
python scripts/run_pipeline.py
```

**Option 2: Explore the notebook**
```bash
jupyter notebook notebooks/01_exploratory_data_analysis.ipynb
```

**Option 3: Run EDA script**
```bash
python scripts/run_eda.py
```

## Sample Visualizations

The analysis generates charts showing:
- Price distribution across all watches
- Average price comparison by collection
- Regional price differences
- Collection composition

## Future Work

- [ ] Power BI interactive dashboard
- [ ] Time series analysis (if historical data becomes available)
- [ ] Competitor price comparison (Rolex, Omega, etc.)

## Author

Built as a data analysis portfolio project to demonstrate ETL pipelines, exploratory data analysis, and data visualization skills.

## License

MIT License - feel free to use this project as a learning reference.
