from setuptools import setup, find_packages

# Read requirements.txt
with open("requirements.txt") as f:
    required_packages = f.read().splitlines()

setup(
    name="chopard_analysis",
    version="0.1.0",
    author="Shaik Tanzeel Ahmed",
    author_email="shaiktanzeelahmed@gmail.com",
    description="A package for analyzing Chopard watch pricing data",
    packages=find_packages(),  
    install_requires=required_packages,  # Loads all dependencies from requirements.txt
    python_requires=">=3.7",
)
