"""
Investigation: $70 Fare Spike Analysis

Investigates the unusual concentration of trips with fares around $70
to determine if this represents airport runs, flat rates, or data artifacts.

Author: Henrik
Date: November 2024
"""

import pandas as pd
import os

# Load and clean data
data_file = os.path.join('data', 'yellow_tripdata_2024-01.parquet')
df = pd.read_parquet(data_file)

df_clean = df[
    (df['fare_amount'] >= 0) &
    (df['trip_distance'] > 0) &
    (df['trip_distance'] <= 100) &
    (df['passenger_count'] > 0) &
    (df['passenger_count'] <= 6)
].copy()

print("=" * 70)
print("INVESTIGATING $70 FARE SPIKE")
print("=" * 70)

# Focus on fares between $68-$72 (around the spike)
spike_trips = df_clean[(df_clean['fare_amount'] >= 68) & (df_clean['fare_amount'] <= 72)]

print(f"\nTotal trips in $68-$72 range: {len(spike_trips):,}")
print(f"Percentage of all trips: {(len(spike_trips) / len(df_clean) * 100):.2f}%")

# Exact fare amounts in this range
print("\n--- EXACT FARE BREAKDOWN ---")
fare_counts = spike_trips['fare_amount'].value_counts().sort_index()
print(fare_counts.head(10))

# Trip characteristics
print("\n--- TRIP CHARACTERISTICS ---")
print(f"Average trip distance: {spike_trips['trip_distance'].mean():.2f} miles")
print(f"Median trip distance: {spike_trips['trip_distance'].median():.2f} miles")
print(f"Min distance: {spike_trips['trip_distance'].min():.2f} miles")
print(f"Max distance: {spike_trips['trip_distance'].max():.2f} miles")

# Payment types
print("\n--- PAYMENT TYPE DISTRIBUTION ---")
print(spike_trips['payment_type'].value_counts())

# Rate code (might indicate airport or special rates)
print("\n--- RATE CODE DISTRIBUTION ---")
print(spike_trips['RatecodeID'].value_counts())

# Passenger count
print("\n--- PASSENGER COUNT ---")
print(spike_trips['passenger_count'].value_counts().sort_index())

# Look at a few sample records
print("\n--- SAMPLE RECORDS (First 5) ---")
sample_cols = ['fare_amount', 'trip_distance', 'passenger_count', 'payment_type', 'RatecodeID']
print(spike_trips[sample_cols].head())

# Distance vs fare for spike trips
print("\n--- DISTANCE STATISTICS ---")
distance_bins = [0, 10, 15, 20, 30, 100]
spike_trips['distance_bin'] = pd.cut(spike_trips['trip_distance'], bins=distance_bins)
print("\nTrips by distance range:")
print(spike_trips['distance_bin'].value_counts().sort_index())

print("\n" + "=" * 70)