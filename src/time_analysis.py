"""
NYC Taxi Time-Based Analysis

Analyzes temporal patterns in taxi trips including hourly distributions,
day-of-week patterns, and time-based fare variations.

Author: Henrik
Date: November 2024
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set_style("whitegrid")

# Load and clean data
print("Loading data...")
data_file = os.path.join('data', 'yellow_tripdata_2024-01.parquet')
df = pd.read_parquet(data_file)

df_clean = df[
    (df['fare_amount'] >= 0) &
    (df['trip_distance'] > 0) &
    (df['trip_distance'] <= 100) &
    (df['passenger_count'] > 0) &
    (df['passenger_count'] <= 6)
].copy()

print(f"Analyzing {len(df_clean):,} trips")

# Extract time components
print("\nExtracting time components...")
df_clean['pickup_hour'] = pd.to_datetime(df_clean['tpep_pickup_datetime']).dt.hour
df_clean['pickup_day'] = pd.to_datetime(df_clean['tpep_pickup_datetime']).dt.day_name()
df_clean['pickup_date'] = pd.to_datetime(df_clean['tpep_pickup_datetime']).dt.date

# Ensure figures directory exists
os.makedirs('docs/figures', exist_ok=True)

print("\n" + "=" * 70)
print("TIME-BASED ANALYSIS")
print("=" * 70)

# Analysis 1: Trips by Hour of Day
print("\n1. HOURLY TRIP DISTRIBUTION")
hourly_trips = df_clean['pickup_hour'].value_counts().sort_index()
print(hourly_trips)

plt.figure(figsize=(14, 6))
plt.bar(hourly_trips.index, hourly_trips.values, edgecolor='black', alpha=0.7, color='steelblue')
plt.xlabel('Hour of Day (24-hour format)', fontsize=12)
plt.ylabel('Number of Trips', fontsize=12)
plt.title('Taxi Trips by Hour of Day - January 2024', fontsize=14, fontweight='bold')
plt.xticks(range(24))
plt.grid(True, alpha=0.3, axis='y')
plt.savefig('docs/figures/hourly_distribution.png', dpi=300, bbox_inches='tight')
print("   Saved: docs/figures/hourly_distribution.png")
plt.close()

# Analysis 2: Average Fare by Hour
print("\n2. AVERAGE FARE BY HOUR")
avg_fare_by_hour = df_clean.groupby('pickup_hour')['fare_amount'].mean().round(2)
print(avg_fare_by_hour)

plt.figure(figsize=(14, 6))
plt.plot(avg_fare_by_hour.index, avg_fare_by_hour.values, marker='o', linewidth=2, markersize=8, color='green')
plt.xlabel('Hour of Day (24-hour format)', fontsize=12)
plt.ylabel('Average Fare ($)', fontsize=12)
plt.title('Average Taxi Fare by Hour - January 2024', fontsize=14, fontweight='bold')
plt.xticks(range(24))
plt.grid(True, alpha=0.3)
plt.savefig('docs/figures/fare_by_hour.png', dpi=300, bbox_inches='tight')
print("   Saved: docs/figures/fare_by_hour.png")
plt.close()

# Analysis 3: Day of Week Pattern
print("\n3. TRIPS BY DAY OF WEEK")
# Order days properly
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_counts = df_clean['pickup_day'].value_counts().reindex(day_order)
print(day_counts)

plt.figure(figsize=(12, 6))
plt.bar(range(len(day_counts)), day_counts.values, edgecolor='black', alpha=0.7, color='coral')
plt.xlabel('Day of Week', fontsize=12)
plt.ylabel('Number of Trips', fontsize=12)
plt.title('Taxi Trips by Day of Week - January 2024', fontsize=14, fontweight='bold')
plt.xticks(range(len(day_counts)), day_order, rotation=45)
plt.grid(True, alpha=0.3, axis='y')
plt.savefig('docs/figures/day_of_week.png', dpi=300, bbox_inches='tight')
print("   Saved: docs/figures/day_of_week.png")
plt.close()

# Peak hours identification
print("\n4. PEAK HOURS IDENTIFICATION")
peak_hours = hourly_trips.nlargest(5)
print("Top 5 busiest hours:")
print(peak_hours)

off_peak_hours = hourly_trips.nsmallest(5)
print("\nTop 5 quietest hours:")
print(off_peak_hours)

print("\n" + "=" * 70)
print("✓ Time analysis complete! Check docs/figures/ for visualizations.")