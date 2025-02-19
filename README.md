# chopard_analysis
This repository contains a structured data pipeline for analyzing the pricing strategy of Chopard watches across different regions. The project integrates data ingestion, processing, and transformation, making it easy to analyze price trends and variations over time.

Project Overview
Goals:
Extract pricing data from Google BigQuery & Google Drive
Clean, process, and filter relevant pricing details
Standardize currency mappings and handle missing data
Save processed data for further visualization in Power BI


Key Features:
Automated Data Ingestion from BigQuery & Google Drive
Data Cleaning & Processing to remove inconsistencies
Structured Python Package for easy imports
Configuration Management with .env for secure credentials


Upgrade Pip & Dependencies
python -m pip install --upgrade pip
pip install --upgrade setuptools wheel
pip freeze | cut -d= -f1 | xargs pip install --upgrade  # Mac/Linux
pip freeze | ForEach-Object {pip install --upgrade $_.split('==')[0]}  # Windows (PowerShell)

How to Run This Project
1) Clone the Repository : git clone https://github.com/ShaikTanzeel/chopard_analysis_v2.git
cd chopard_analysis_v2

2) Set Up a Virtual Environment (Recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3) Install Dependencies
pip install -r requirements.txt

4) Set Up Environment Variables
GCP_PROJECT_ID=your-google-cloud-project-id
GOOGLE_APPLICATION_CREDENTIALS=config/your-service-account.json

5) Verify Output