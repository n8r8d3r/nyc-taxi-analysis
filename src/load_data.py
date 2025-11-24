import pandas as pd
import os

# Define data path
data_file = os.path.join('data', 'yellow_tripdata_2024-01.parquet')

# Load the data
print(f"Loading data from {data_file}...")
df = pd.read_parquet(data_file)

# Basic information
print(f"\nDataset loaded successfully!")
print(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"\nColumn names:")
print(df.columns.tolist())

# Show first few rows
print(f"\nFirst 5 rows:")
print(df.head())

# Data types
print(f"\nData types:")
print(df.dtypes)

# Basic statistics
print(f"\nBasic statistics:")
print(df.describe())
