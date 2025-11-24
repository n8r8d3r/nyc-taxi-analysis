# NYC Taxi Data Analysis

## Overview
Exploratory data analysis of NYC Yellow Taxi trip records using Python and pandas. This project demonstrates data loading, quality assessment, and cleaning techniques on real-world transportation data.

## Dataset
- **Source:** NYC Taxi & Limousine Commission (TLC)
- **Period:** January 2024
- **Records:** ~3 million taxi trips
- **Format:** Parquet
- **Size:** ~50MB compressed

## Project Structure
```
nyc-taxi-analysis/
├── data/              # Raw data files (not tracked in git)
├── src/               # Python scripts
│   ├── load_data.py      # Initial data loading and inspection
│   ├── explore_data.py   # Data quality analysis
│   └── clean_data.py     # Data filtering and cleaning
├── notebooks/         # Jupyter notebooks (future)
├── docs/             # Additional documentation
└── requirements.txt  # Python dependencies
```

## Key Findings

### Data Quality Issues Identified
- **Negative fares:** 37,448 records (1.2%)
- **Zero-distance trips:** Significant number requiring investigation
- **Missing values:** ~142,000 records in optional fields (passenger_count, airport_fee, etc.)
- **Total anomalies removed:** 240,487 records (8.11%)

### Data Cleaning Rules Applied
- Fare amount must be >= $0
- Trip distance must be > 0 and <= 100 miles
- Passenger count must be between 1-6
- Removed records with invalid combinations

## Technologies Used
- **Python 3.14**
- **pandas** - Data manipulation and analysis
- **pyarrow** - Parquet file support
- **numpy** - Numerical operations

## Setup Instructions

### Prerequisites
- Python 3.11 or higher
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/n8r8d3r/nyc-taxi-analysis.git
cd nyc-taxi-analysis

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows Git Bash

# Install dependencies
pip install -r requirements.txt
```

### Download Data
1. Visit [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
2. Download Yellow Taxi Trip Records for January 2024
3. Place the parquet file in the `data/` directory

### Run Analysis
```bash
# Load and inspect data
python src/load_data.py

# Explore data quality
python src/explore_data.py

# Clean and filter data
python src/clean_data.py
```

## Future Enhancements
- Add data visualizations (trip patterns, fare distributions)
- Time-series analysis (hourly/daily patterns)
- Geographic analysis using pickup/dropoff coordinates
- Predictive modeling (fare estimation, demand forecasting)
- Integration with PySpark for larger datasets

## Author
Henrik - Data Engineer transitioning from Informatica/SQL to Python-based data engineering

## License
MIT License
