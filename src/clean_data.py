import pandas as pd
import os

# Load data
data_file = os.path.join('data', 'yellow_tripdata_2024-01.parquet')
df = pd.read_parquet(data_file)

print(f"Original dataset: {len(df):,} rows")

# Filter out data quality issues
# Keep only trips that make sense
df_clean = df[
    (df['fare_amount'] >= 0) &           # No negative fares
    (df['trip_distance'] > 0) &          # Actual trips
    (df['trip_distance'] <= 100) &       # Reasonable distance
    (df['passenger_count'] > 0) &        # At least one passenger
    (df['passenger_count'] <= 6)         # Reasonable passenger count
].copy()

print(f"Clean dataset: {len(df_clean):,} rows")
print(f"Removed: {len(df) - len(df_clean):,} rows ({((len(df) - len(df_clean)) / len(df) * 100):.2f}%)")

# Show the improvement
print("\n--- BEFORE CLEANING ---")
print(f"Negative fares: {(df['fare_amount'] < 0).sum():,}")
print(f"Zero distance: {(df['trip_distance'] == 0).sum():,}")

print("\n--- AFTER CLEANING ---")
print(f"Negative fares: {(df_clean['fare_amount'] < 0).sum():,}")
print(f"Zero distance: {(df_clean['trip_distance'] == 0).sum():,}")
