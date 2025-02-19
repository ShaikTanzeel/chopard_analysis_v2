# chopard_analysis
This repository contains a structured data pipeline for analyzing the pricing strategy of Chopard watches across different regions. The project integrates data ingestion, processing, and transformation, making it easy to analyze price trends and variations over time.

## Project Overview
### Goals:
- Extract pricing data from Google BigQuery & Google Drive
- Clean, process, and filter relevant pricing details
- Standardize currency mappings and handle missing data
- Save processed data for further visualization in Power BI

### Key Features:
- Automated Data Ingestion from BigQuery & Google Drive
- Data Cleaning & Processing to remove inconsistencies
- Structured Python Package for easy imports
- Configuration Management with .env for secure credentials

## Upgrade Pip & Dependencies
```sh
python -m pip install --upgrade pip

```

## How to Run This Project
### 1) Clone the Repository
```sh
git clone https://github.com/ShaikTanzeel/chopard_analysis_v2.git
cd chopard_analysis_v2
```

### 2) Set Up a Virtual Environment (Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3) Install Dependencies
```sh
pip install -e .
```

### 4) Set Up Environment Variables & Configurations
1. Create a `config` directory at the root level of the project.
2. Place the JSON file `config/main-crow-418809-6fbb97b44180.json` inside the `config` directory.

### 5) Run the Data Pipeline
Execute the following command to run the pipeline script:
```sh
python scripts/run_pipeline.py
```

### What the Pipeline Does
1. Fetches raw data from BigQuery.
2. Processes the data according to the script logic.
3. Retrieves the latest exchange rates from a live API.
4. Converts all currencies into Euros using the fetched exchange rates.
5. Saves the final processed data to `data/final_processed_data.csv`.
6. Pushes the processed data back to BigQuery for further analysis using PowerBI.

