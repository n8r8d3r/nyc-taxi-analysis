"""
NYC Taxi Data Visualization Script

Creates visualizations to explore patterns in taxi trip data including
fare distributions, trip distances, and temporal patterns.

Author: Henrik
Date: November 2024
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Load cleaned data
print("Loading data...")
data_file = os.path.join('data', 'yellow_tripdata_2024-01.parquet')
df = pd.read_parquet(data_file)

# Apply same cleaning rules as before
df_clean = df[
    (df['fare_amount'] >= 0) &
    (df['trip_distance'] > 0) &
    (df['trip_distance'] <= 100) &
    (df['passenger_count'] > 0) &
    (df['passenger_count'] <= 6)
].copy()

print(f"Working with {len(df_clean):,} clean records")

# Create output directory for plots
os.makedirs('docs/figures', exist_ok=True)

# Visualization 1: Fare Amount Distribution
print("\n1. Creating fare distribution plot...")
plt.figure(figsize=(12, 6))
plt.hist(df_clean['fare_amount'], bins=50, range=(0, 100), edgecolor='black', alpha=0.7)
plt.xlabel('Fare Amount ($)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('Distribution of Taxi Fares (January 2024)', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.savefig('docs/figures/fare_distribution.png', dpi=300, bbox_inches='tight')
print("   Saved: docs/figures/fare_distribution.png")
plt.close()

# Visualization 2: Trip Distance Distribution
print("2. Creating trip distance distribution...")
plt.figure(figsize=(12, 6))
plt.hist(df_clean['trip_distance'], bins=50, range=(0, 25), edgecolor='black', alpha=0.7, color='green')
plt.xlabel('Trip Distance (miles)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('Distribution of Trip Distances (January 2024)', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.savefig('docs/figures/distance_distribution.png', dpi=300, bbox_inches='tight')
print("   Saved: docs/figures/distance_distribution.png")
plt.close()

# Visualization 3: Passenger Count
print("3. Creating passenger count plot...")
passenger_counts = df_clean['passenger_count'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
plt.bar(passenger_counts.index, passenger_counts.values, edgecolor='black', alpha=0.7, color='coral')
plt.xlabel('Number of Passengers', fontsize=12)
plt.ylabel('Number of Trips', fontsize=12)
plt.title('Trips by Passenger Count (January 2024)', fontsize=14, fontweight='bold')
plt.xticks(passenger_counts.index)
plt.grid(True, alpha=0.3, axis='y')
plt.savefig('docs/figures/passenger_count.png', dpi=300, bbox_inches='tight')
print("   Saved: docs/figures/passenger_count.png")
plt.close()

print("\n✓ All visualizations created successfully!")
print("  Check the docs/figures/ directory to view the plots.")
