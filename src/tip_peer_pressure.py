"""
Tipping Behavior Analysis: Solo vs Group Riders
Hypothesis: Does peer pressure affect tipping behavior?
"""

import pandas as pd
import numpy as np

# Load the data
print("Loading taxi data...")
#df = pd.read_parquet('yellow_tripdata_2024-01.parquet')
df = pd.read_parquet('data/yellow_tripdata_2024-01.parquet')

print(f"Total records: {len(df):,}")
print(f"\nColumns available: {df.columns.tolist()}")

# Data quality check - what payment types do we have?
print("\n" + "="*60)
print("PAYMENT TYPE DISTRIBUTION")
print("="*60)
print(df['payment_type'].value_counts())
print("\nNote: Only credit card payments (type 1) record tips")

# Filter for valid records:
# - Credit card payments only (payment_type == 1)
# - Positive fares and tips
# - Valid passenger counts (1-6 is reasonable)
print("\n" + "="*60)
print("FILTERING DATA")
print("="*60)

filtered_df = df[
    (df['payment_type'] == 1) &  # Credit card only
    (df['fare_amount'] > 0) &
    (df['tip_amount'] >= 0) &
    (df['passenger_count'] >= 1) &
    (df['passenger_count'] <= 6)  # Reasonable passenger range
].copy()

print(f"Records after filtering: {len(filtered_df):,}")
print(f"Percentage retained: {len(filtered_df)/len(df)*100:.1f}%")

# Calculate tip percentage
filtered_df['tip_percentage'] = (filtered_df['tip_amount'] / filtered_df['fare_amount'] * 100)

# Remove extreme outliers (tip > 100% of fare is suspicious)
filtered_df = filtered_df[filtered_df['tip_percentage'] <= 100]

print(f"Records after removing extreme outliers: {len(filtered_df):,}")

# Passenger count distribution
print("\n" + "="*60)
print("PASSENGER COUNT DISTRIBUTION")
print("="*60)
print(filtered_df['passenger_count'].value_counts().sort_index())

# Create grouping: Solo (1) vs Groups (2+)
filtered_df['rider_type'] = filtered_df['passenger_count'].apply(
    lambda x: 'Solo' if x == 1 else 'Group'
)

# Basic statistics by rider type
print("\n" + "="*60)
print("TIPPING BEHAVIOR: SOLO VS GROUPS")
print("="*60)

summary = filtered_df.groupby('rider_type').agg({
    'tip_amount': ['count', 'mean', 'median'],
    'tip_percentage': ['mean', 'median', 'std'],
    'fare_amount': ['mean', 'median']
}).round(2)

print(summary)

# Detailed breakdown by exact passenger count
print("\n" + "="*60)
print("TIPPING BEHAVIOR BY PASSENGER COUNT")
print("="*60)

detailed = filtered_df.groupby('passenger_count').agg({
    'tip_amount': ['count', 'mean', 'median'],
    'tip_percentage': ['mean', 'median'],
    'fare_amount': ['mean']
}).round(2)

print(detailed)

# Look at the distribution of tip percentages
print("\n" + "="*60)
print("TIP PERCENTAGE QUARTILES")
print("="*60)

for rider_type in ['Solo', 'Group']:
    data = filtered_df[filtered_df['rider_type'] == rider_type]['tip_percentage']
    print(f"\n{rider_type} riders:")
    print(f"  25th percentile: {data.quantile(0.25):.2f}%")
    print(f"  50th percentile: {data.quantile(0.50):.2f}%")
    print(f"  75th percentile: {data.quantile(0.75):.2f}%")
    print(f"  Mean: {data.mean():.2f}%")

# What percentage tip nothing?
print("\n" + "="*60)
print("ZERO TIP ANALYSIS")
print("="*60)

for rider_type in ['Solo', 'Group']:
    subset = filtered_df[filtered_df['rider_type'] == rider_type]
    zero_tips = (subset['tip_amount'] == 0).sum()
    pct = zero_tips / len(subset) * 100
    print(f"{rider_type}: {zero_tips:,} trips with $0 tip ({pct:.2f}%)")

# Standard tip percentages (15%, 18%, 20%, 25%)
print("\n" + "="*60)
print("COMMON TIP PERCENTAGE RANGES")
print("="*60)

def categorize_tip(pct):
    if pct == 0:
        return 'No tip'
    elif pct < 15:
        return 'Under 15%'
    elif 15 <= pct < 18:
        return '15-18%'
    elif 18 <= pct < 20:
        return '18-20%'
    elif 20 <= pct < 25:
        return '20-25%'
    else:
        return '25%+'

filtered_df['tip_category'] = filtered_df['tip_percentage'].apply(categorize_tip)

tip_cats = filtered_df.groupby(['rider_type', 'tip_category']).size().unstack(fill_value=0)
tip_cats_pct = tip_cats.div(tip_cats.sum(axis=1), axis=0) * 100

print("\nPercentage of trips in each tip category:")
print(tip_cats_pct.round(1))

print("\n" + "="*60)
print("CONCLUSION")
print("="*60)
print("\nCompare the mean/median tip percentages between Solo and Group riders.")
print("If groups tip significantly higher, peer pressure might be at play.")
print("If they tip similarly or lower, maybe not so much!")