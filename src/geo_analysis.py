"""
NYC Taxi Geographic Analysis

Analyzes trip patterns by borough and neighborhood using taxi zone lookup data.
Identifies top pickup/dropoff locations and inter-borough travel patterns.

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
print("GEOGRAPHIC ANALYSIS - NYC TAXI ZONES")
print("=" * 70)

# Load trip data
print("\n1. Loading trip data...")
data_file = os.path.join('data', 'yellow_tripdata_2024-01.parquet')
df = pd.read_parquet(data_file)

# Clean data
df_clean = df[
    (df['fare_amount'] >= 0) &
    (df['trip_distance'] > 0) &
    (df['trip_distance'] <= 100) &
    (df['passenger_count'] > 0) &
    (df['passenger_count'] <= 6)
].copy()

print(f"   Working with {len(df_clean):,} clean trips")

# Load zone lookup data (CSV format!)
print("\n2. Loading taxi zone lookup data...")
zones_file = os.path.join('data', 'taxi_zone_lookup.csv')
zones = pd.read_csv(zones_file)

print(f"   Loaded {len(zones)} taxi zones")
print("\n   Zone data sample:")
print(zones.head())

# Join trip data with zone names
print("\n3. Joining trip data with zone information...")

# Merge pickup zones
df_clean = df_clean.merge(
    zones[['LocationID', 'Borough', 'Zone']],
    left_on='PULocationID',
    right_on='LocationID',
    how='left'
)
df_clean.rename(columns={'Borough': 'PU_Borough', 'Zone': 'PU_Zone'}, inplace=True)
df_clean.drop('LocationID', axis=1, inplace=True)

# Merge dropoff zones
df_clean = df_clean.merge(
    zones[['LocationID', 'Borough', 'Zone']],
    left_on='DOLocationID',
    right_on='LocationID',
    how='left'
)
df_clean.rename(columns={'Borough': 'DO_Borough', 'Zone': 'DO_Zone'}, inplace=True)
df_clean.drop('LocationID', axis=1, inplace=True)

print("   ✓ Zone data joined successfully")

# Create figures directory
os.makedirs('docs/figures', exist_ok=True)

# Analysis 1: Top Pickup Locations
print("\n" + "=" * 70)
print("TOP 15 PICKUP LOCATIONS")
print("=" * 70)
top_pickup = df_clean['PU_Zone'].value_counts().head(15)
print(top_pickup)

plt.figure(figsize=(14, 8))
plt.barh(range(len(top_pickup)), top_pickup.values, color='steelblue', edgecolor='black')
plt.yticks(range(len(top_pickup)), top_pickup.index)
plt.xlabel('Number of Trips', fontsize=12)
plt.title('Top 15 Taxi Pickup Locations - January 2024', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('docs/figures/top_pickup_zones.png', dpi=300, bbox_inches='tight')
print("\n   Saved: docs/figures/top_pickup_zones.png")
plt.close()

# Analysis 2: Top Dropoff Locations
print("\n" + "=" * 70)
print("TOP 15 DROPOFF LOCATIONS")
print("=" * 70)
top_dropoff = df_clean['DO_Zone'].value_counts().head(15)
print(top_dropoff)

plt.figure(figsize=(14, 8))
plt.barh(range(len(top_dropoff)), top_dropoff.values, color='coral', edgecolor='black')
plt.yticks(range(len(top_dropoff)), top_dropoff.index)
plt.xlabel('Number of Trips', fontsize=12)
plt.title('Top 15 Taxi Dropoff Locations - January 2024', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('docs/figures/top_dropoff_zones.png', dpi=300, bbox_inches='tight')
print("\n   Saved: docs/figures/top_dropoff_zones.png")
plt.close()

# Analysis 3: Trips by Borough
print("\n" + "=" * 70)
print("TRIPS BY BOROUGH (PICKUP)")
print("=" * 70)
borough_pickups = df_clean['PU_Borough'].value_counts()
print(borough_pickups)

plt.figure(figsize=(10, 6))
plt.bar(borough_pickups.index, borough_pickups.values, color='green', edgecolor='black', alpha=0.7)
plt.xlabel('Borough', fontsize=12)
plt.ylabel('Number of Pickups', fontsize=12)
plt.title('Taxi Pickups by NYC Borough - January 2024', fontsize=14, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('docs/figures/pickups_by_borough.png', dpi=300, bbox_inches='tight')
print("\n   Saved: docs/figures/pickups_by_borough.png")
plt.close()

print("\n" + "=" * 70)
print("✓ Geographic analysis complete!")
print("=" * 70)
