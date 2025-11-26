"""
NYC Taxi Geographic Data Exploration

Initial exploration of pickup and dropoff location data to understand
spatial patterns and prepare for geographic analysis.

Author: Henrik
Date: November 2024
"""

import pandas as pd
import os

# Load data
data_file = os.path.join('data', 'yellow_tripdata_2024-01.parquet')
df = pd.read_parquet(data_file)

print("=" * 70)
print("GEOGRAPHIC DATA EXPLORATION")
print("=" * 70)

# Check what location columns we have
print("\nAvailable columns:")
print(df.columns.tolist())

# Look at location-related columns
print("\n--- LOCATION DATA SAMPLE ---")
location_cols = [col for col in df.columns if 'location' in col.lower() or 'lat' in col.lower() or 'lon' in col.lower()]
if location_cols:
    print(f"\nLocation columns found: {location_cols}")
    print(df[location_cols].head(10))
else:
    print("\nNo lat/lon columns found. Checking for location IDs...")
    id_cols = [col for col in df.columns if 'Location' in col or 'location' in col]
    print(f"Location ID columns: {id_cols}")
    print(df[id_cols].head(10))
    print(df[id_cols].describe())

print("\n" + "=" * 70)
