"""
NYC Taxi Inter-Borough Flow Analysis

Analyzes travel patterns between NYC boroughs to understand
commuter flows, airport traffic, and intra-borough circulation.

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
print("INTER-BOROUGH TRAVEL FLOW ANALYSIS")
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

print(f"Analyzing {len(df_clean):,} trips")

# Join with borough data
df_clean = df_clean.merge(
    zones[['LocationID', 'Borough']],
    left_on='PULocationID',
    right_on='LocationID',
    how='left'
).rename(columns={'Borough': 'PU_Borough'}).drop('LocationID', axis=1)

df_clean = df_clean.merge(
    zones[['LocationID', 'Borough']],
    left_on='DOLocationID',
    right_on='LocationID',
    how='left'
).rename(columns={'Borough': 'DO_Borough'}).drop('LocationID', axis=1)

# Remove unknown boroughs
df_clean = df_clean[df_clean['PU_Borough'].notna() & df_clean['DO_Borough'].notna()]

# Create origin-destination pairs
df_clean['route'] = df_clean['PU_Borough'] + ' → ' + df_clean['DO_Borough']

# Create figures directory
os.makedirs('docs/figures', exist_ok=True)

# Analysis 1: Top Routes
print("\n" + "=" * 70)
print("TOP 20 INTER-BOROUGH ROUTES")
print("=" * 70)

top_routes = df_clean['route'].value_counts().head(20)
print(top_routes)

plt.figure(figsize=(12, 10))
plt.barh(range(len(top_routes)), top_routes.values, color='steelblue', edgecolor='black')
plt.yticks(range(len(top_routes)), top_routes.index, fontsize=10)
plt.xlabel('Number of Trips', fontsize=12)
plt.title('Top 20 Borough-to-Borough Routes - January 2024', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('docs/figures/top_borough_routes.png', dpi=300, bbox_inches='tight')
print("\n   Saved: docs/figures/top_borough_routes.png")
plt.close()

# Analysis 2: Internal vs Cross-Borough
print("\n" + "=" * 70)
print("INTERNAL vs CROSS-BOROUGH TRIPS")
print("=" * 70)

df_clean['trip_type'] = df_clean.apply(
    lambda row: 'Within Borough' if row['PU_Borough'] == row['DO_Borough'] else 'Cross-Borough',
    axis=1
)

trip_type_counts = df_clean['trip_type'].value_counts()
print(trip_type_counts)
print(f"\nPercentage staying within borough: {(trip_type_counts['Within Borough'] / len(df_clean) * 100):.1f}%")
print(f"Percentage crossing boroughs: {(trip_type_counts['Cross-Borough'] / len(df_clean) * 100):.1f}%")

# Analysis 3: Manhattan-centric flows
print("\n" + "=" * 70)
print("MANHATTAN-CENTRIC FLOW PATTERNS")
print("=" * 70)

manhattan_internal = len(df_clean[(df_clean['PU_Borough'] == 'Manhattan') & (df_clean['DO_Borough'] == 'Manhattan')])
to_manhattan = len(df_clean[(df_clean['PU_Borough'] != 'Manhattan') & (df_clean['DO_Borough'] == 'Manhattan')])
from_manhattan = len(df_clean[(df_clean['PU_Borough'] == 'Manhattan') & (df_clean['DO_Borough'] != 'Manhattan')])
manhattan_total = manhattan_internal + to_manhattan + from_manhattan

print(f"\nManhattan internal trips: {manhattan_internal:,} ({manhattan_internal/manhattan_total*100:.1f}%)")
print(f"Trips TO Manhattan: {to_manhattan:,} ({to_manhattan/manhattan_total*100:.1f}%)")
print(f"Trips FROM Manhattan: {from_manhattan:,} ({from_manhattan/manhattan_total*100:.1f}%)")

# Analysis 4: Breakdown by specific cross-borough patterns
print("\n" + "=" * 70)
print("SPECIFIC CROSS-BOROUGH PATTERNS")
print("=" * 70)

# Queens ↔ Manhattan (likely airport related)
queens_to_manhattan = len(df_clean[(df_clean['PU_Borough'] == 'Queens') & (df_clean['DO_Borough'] == 'Manhattan')])
manhattan_to_queens = len(df_clean[(df_clean['PU_Borough'] == 'Manhattan') & (df_clean['DO_Borough'] == 'Queens')])

print(f"\nQueens → Manhattan: {queens_to_manhattan:,} (likely airport arrivals)")
print(f"Manhattan → Queens: {manhattan_to_queens:,} (likely airport departures)")

# Brooklyn ↔ Manhattan
brooklyn_to_manhattan = len(df_clean[(df_clean['PU_Borough'] == 'Brooklyn') & (df_clean['DO_Borough'] == 'Manhattan')])
manhattan_to_brooklyn = len(df_clean[(df_clean['PU_Borough'] == 'Manhattan') & (df_clean['DO_Borough'] == 'Brooklyn')])

print(f"\nBrooklyn → Manhattan: {brooklyn_to_manhattan:,}")
print(f"Manhattan → Brooklyn: {manhattan_to_brooklyn:,}")

# Analysis 5: Average characteristics by trip type
print("\n" + "=" * 70)
print("TRIP CHARACTERISTICS BY TYPE")
print("=" * 70)

print("\nWithin-Borough Trips:")
within = df_clean[df_clean['trip_type'] == 'Within Borough']
print(f"  Average fare: ${within['fare_amount'].mean():.2f}")
print(f"  Average distance: {within['trip_distance'].mean():.2f} miles")

print("\nCross-Borough Trips:")
cross = df_clean[df_clean['trip_type'] == 'Cross-Borough']
print(f"  Average fare: ${cross['fare_amount'].mean():.2f}")
print(f"  Average distance: {cross['trip_distance'].mean():.2f} miles")

print("\n" + "=" * 70)
print("✓ Borough flow analysis complete!")
print("=" * 70)