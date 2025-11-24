"""
NYC Taxi Data Exploration Script

This script performs exploratory data analysis on NYC Yellow Taxi trip records,
identifying data quality issues, distribution patterns, and potential anomalies.

Author: Henrik
Date: November 2024
"""

import pandas as pd
import os

# Load data
data_file = os.path.join('data', 'yellow_tripdata_2024-01.parquet')
df = pd.read_parquet(data_file)

print("=" * 60)
print("NYC TAXI DATA EXPLORATION")
print("=" * 60)

# 1. Check for missing values
print("\n1. MISSING VALUES:")
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
missing_info = pd.DataFrame({
    'Missing Count': missing,
    'Percentage': missing_pct
})
print(missing_info[missing_info['Missing Count'] > 0])

# 2. Trip distance analysis
print("\n2. TRIP DISTANCE ANALYSIS:")
print(f"Average trip distance: {df['trip_distance'].mean():.2f} miles")
print(f"Median trip distance: {df['trip_distance'].median():.2f} miles")
print(f"Max trip distance: {df['trip_distance'].max():.2f} miles")
print(f"Trips with 0 distance: {(df['trip_distance'] == 0).sum():,}")

# 3. Fare analysis
print("\n3. FARE ANALYSIS:")
print(f"Average fare: ${df['fare_amount'].mean():.2f}")
print(f"Median fare: ${df['fare_amount'].median():.2f}")
print(f"Max fare: ${df['fare_amount'].max():.2f}")
print(f"Min fare: ${df['fare_amount'].min():.2f}")

# 4. Payment types
print("\n4. PAYMENT TYPE DISTRIBUTION:")
payment_counts = df['payment_type'].value_counts()
print(payment_counts)

# 5. Passenger count
print("\n5. PASSENGER COUNT:")
passenger_counts = df['passenger_count'].value_counts().sort_index()
print(passenger_counts)

# 6. Data quality issues
print("\n6. POTENTIAL DATA QUALITY ISSUES:")
print(f"Negative fares: {(df['fare_amount'] < 0).sum():,}")
print(f"Zero passengers: {(df['passenger_count'] == 0).sum():,}")
print(f"Trips over 100 miles: {(df['trip_distance'] > 100).sum():,}")

print("\n" + "=" * 60)
