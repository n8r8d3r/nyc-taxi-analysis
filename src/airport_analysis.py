"""
NYC Taxi Airport Pattern Analysis

Analyzes differences between JFK and LaGuardia taxi trips including
timing patterns, fares, distances, and passenger characteristics.

Author: Henrik
Date: November 2024
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set_style("whitegrid")

print("=" * 70)
print("AIRPORT PATTERN ANALYSIS - JFK vs LaGuardia")
print("=" * 70)

# Load data
data_file = os.path.join('data', 'yellow_tripdata_2024-01.parquet')
df = pd.read_parquet(data_file)

# Load zones
zones_file = os.path.join('data', 'taxi_zone_lookup.csv')
zones = pd.read_csv(zones_file)

# Clean data
df_clean = df[
    (df['fare_amount'] >= 0) &
    (df['trip_distance'] > 0) &
    (df['trip_distance'] <= 100) &
    (df['passenger_count'] > 0) &
    (df['passenger_count'] <= 6)
].copy()

# Join with zones
df_clean = df_clean.merge(
    zones[['LocationID', 'Zone']],
    left_on='PULocationID',
    right_on='LocationID',
    how='left'
).rename(columns={'Zone': 'PU_Zone'}).drop('LocationID', axis=1)

# Extract time info
df_clean['pickup_hour'] = pd.to_datetime(df_clean['tpep_pickup_datetime']).dt.hour
df_clean['pickup_day'] = pd.to_datetime(df_clean['tpep_pickup_datetime']).dt.day_name()

# Filter for airport pickups
jfk_trips = df_clean[df_clean['PU_Zone'].str.contains('JFK', case=False, na=False)]
lga_trips = df_clean[df_clean['PU_Zone'].str.contains('LaGuardia', case=False, na=False)]

print(f"\nJFK Airport pickups: {len(jfk_trips):,}")
print(f"LaGuardia pickups: {len(lga_trips):,}")

# Create figures directory
os.makedirs('docs/figures', exist_ok=True)

# Analysis 1: Pickup Time Distribution
print("\n" + "=" * 70)
print("PICKUP HOUR DISTRIBUTION")
print("=" * 70)

jfk_hourly = jfk_trips['pickup_hour'].value_counts().sort_index()
lga_hourly = lga_trips['pickup_hour'].value_counts().sort_index()

print("\nJFK pickups by hour:")
print(jfk_hourly)
print("\nLaGuardia pickups by hour:")
print(lga_hourly)

# Plot comparison
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

ax1.bar(jfk_hourly.index, jfk_hourly.values, color='steelblue', edgecolor='black', alpha=0.7)
ax1.set_xlabel('Hour of Day', fontsize=12)
ax1.set_ylabel('Number of Pickups', fontsize=12)
ax1.set_title('JFK Airport Pickups by Hour', fontsize=13, fontweight='bold')
ax1.set_xticks(range(24))
ax1.grid(True, alpha=0.3, axis='y')

ax2.bar(lga_hourly.index, lga_hourly.values, color='coral', edgecolor='black', alpha=0.7)
ax2.set_xlabel('Hour of Day', fontsize=12)
ax2.set_ylabel('Number of Pickups', fontsize=12)
ax2.set_title('LaGuardia Pickups by Hour', fontsize=13, fontweight='bold')
ax2.set_xticks(range(24))
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('docs/figures/airport_hourly_comparison.png', dpi=300, bbox_inches='tight')
print("\n   Saved: docs/figures/airport_hourly_comparison.png")
plt.close()

# Analysis 2: Fare Comparison
print("\n" + "=" * 70)
print("FARE ANALYSIS")
print("=" * 70)

print(f"\nJFK Average Fare: ${jfk_trips['fare_amount'].mean():.2f}")
print(f"JFK Median Fare: ${jfk_trips['fare_amount'].median():.2f}")
print(f"\nLaGuardia Average Fare: ${lga_trips['fare_amount'].mean():.2f}")
print(f"LaGuardia Median Fare: ${lga_trips['fare_amount'].median():.2f}")

# Analysis 3: Distance Comparison
print("\n" + "=" * 70)
print("DISTANCE ANALYSIS")
print("=" * 70)

print(f"\nJFK Average Distance: {jfk_trips['trip_distance'].mean():.2f} miles")
print(f"JFK Median Distance: {jfk_trips['trip_distance'].median():.2f} miles")
print(f"\nLaGuardia Average Distance: {lga_trips['trip_distance'].mean():.2f} miles")
print(f"LaGuardia Median Distance: {lga_trips['trip_distance'].median():.2f} miles")

# Analysis 4: Passenger Count
print("\n" + "=" * 70)
print("PASSENGER PATTERNS")
print("=" * 70)

print("\nJFK Passenger Distribution:")
print(jfk_trips['passenger_count'].value_counts().sort_index())

print("\nLaGuardia Passenger Distribution:")
print(lga_trips['passenger_count'].value_counts().sort_index())

# Analysis 5: Late Night International Pattern
print("\n" + "=" * 70)
print("LATE NIGHT PATTERN (Potential International Arrivals)")
print("=" * 70)

late_night_hours = [22, 23, 0, 1, 2, 3, 4, 5]
jfk_late = jfk_trips[jfk_trips['pickup_hour'].isin(late_night_hours)]
lga_late = lga_trips[lga_trips['pickup_hour'].isin(late_night_hours)]

jfk_late_pct = (len(jfk_late) / len(jfk_trips)) * 100
lga_late_pct = (len(lga_late) / len(lga_trips)) * 100

print(f"\nJFK late-night pickups (10PM-5AM): {len(jfk_late):,} ({jfk_late_pct:.1f}%)")
print(f"LaGuardia late-night pickups (10PM-5AM): {len(lga_late):,} ({lga_late_pct:.1f}%)")

print("\n" + "=" * 70)
print("✓ Airport analysis complete!")
print("=" * 70)
