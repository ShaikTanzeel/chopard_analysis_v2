from setuptools import setup, find_packages

setup(
    name="CHOPARD_ANALYSIS",
    version="0.1",
    description="A package for strategic business analysis of Chopard",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "selenium",
        "beautifulsoup4",
        "google-cloud-bigquery"
    ]
)
