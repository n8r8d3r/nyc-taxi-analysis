"""
Late Night Tipping Analysis: Does Alcohol Make People More Generous?
Hypothesis: Do people tip better during bar-closing hours?
"""

import pandas as pd
import numpy as np

# Load the data
print("Loading taxi data...")
df = pd.read_parquet('data/yellow_tripdata_2024-01.parquet')

print(f"Total records: {len(df):,}")

# Convert pickup time to datetime if it's not already
df['pickup_hour'] = pd.to_datetime(df['tpep_pickup_datetime']).dt.hour

# Filter for valid tipping records (same as before)
print("\n" + "="*60)
print("FILTERING DATA")
print("="*60)

filtered_df = df[
    (df['payment_type'] == 1) &  # Credit card only
    (df['fare_amount'] > 0) &
    (df['tip_amount'] >= 0) &
    (df['passenger_count'] >= 1) &
    (df['passenger_count'] <= 6)
].copy()

print(f"Records after filtering: {len(filtered_df):,}")

# Calculate tip percentage
filtered_df['tip_percentage'] = (filtered_df['tip_amount'] / filtered_df['fare_amount'] * 100)

# Remove extreme outliers
filtered_df = filtered_df[filtered_df['tip_percentage'] <= 100]

print(f"Records after removing outliers: {len(filtered_df):,}")

# Define time periods
def categorize_time(hour):
    if 0 <= hour < 6:
        return 'Late Night (12am-6am)'
    elif 6 <= hour < 12:
        return 'Morning (6am-12pm)'
    elif 12 <= hour < 18:
        return 'Afternoon (12pm-6pm)'
    else:
        return 'Evening (6pm-12am)'

filtered_df['time_period'] = filtered_df['pickup_hour'].apply(categorize_time)

# Show distribution of trips by time period
print("\n" + "="*60)
print("TRIP DISTRIBUTION BY TIME PERIOD")
print("="*60)
print(filtered_df['time_period'].value_counts().sort_index())

# Overall tipping by time period
print("\n" + "="*60)
print("TIPPING BEHAVIOR BY TIME PERIOD")
print("="*60)

time_summary = filtered_df.groupby('time_period').agg({
    'tip_amount': ['count', 'mean', 'median'],
    'tip_percentage': ['mean', 'median', 'std'],
    'fare_amount': ['mean', 'median']
}).round(2)

print(time_summary)

# Zero tip analysis by time
print("\n" + "="*60)
print("ZERO TIP RATE BY TIME PERIOD")
print("="*60)

for period in ['Late Night (12am-6am)', 'Morning (6am-12pm)', 
               'Afternoon (12pm-6pm)', 'Evening (6pm-12am)']:
    subset = filtered_df[filtered_df['time_period'] == period]
    if len(subset) > 0:
        zero_tips = (subset['tip_amount'] == 0).sum()
        pct = zero_tips / len(subset) * 100
        print(f"{period}: {pct:.2f}% left no tip")

# Hour-by-hour breakdown for late night
print("\n" + "="*60)
print("HOUR-BY-HOUR LATE NIGHT ANALYSIS (Midnight-6am)")
print("="*60)

late_night = filtered_df[filtered_df['pickup_hour'].isin([0, 1, 2, 3, 4, 5])]

hourly = late_night.groupby('pickup_hour').agg({
    'tip_amount': 'count',
    'tip_percentage': ['mean', 'median']
}).round(2)

print(hourly)

# Drunk solo vs drunk groups
print("\n" + "="*60)
print("LATE NIGHT: SOLO VS GROUP TIPPING")
print("="*60)

late_night['rider_type'] = late_night['passenger_count'].apply(
    lambda x: 'Solo' if x == 1 else 'Group'
)

late_night_groups = late_night.groupby('rider_type').agg({
    'tip_amount': ['count', 'mean', 'median'],
    'tip_percentage': ['mean', 'median'],
    'fare_amount': ['mean']
}).round(2)

print(late_night_groups)

# Zero tips: late night solo vs groups
print("\nLate Night Zero Tip Rates:")
for rider_type in ['Solo', 'Group']:
    subset = late_night[late_night['rider_type'] == rider_type]
    if len(subset) > 0:
        zero_tips = (subset['tip_amount'] == 0).sum()
        pct = zero_tips / len(subset) * 100
        print(f"  {rider_type}: {pct:.2f}%")

# Generous tipping (20%+) by time and rider type
print("\n" + "="*60)
print("GENEROUS TIPPING (20%+) ANALYSIS")
print("="*60)

def is_generous(pct):
    return pct >= 20

# All times
print("\nAll Day:")
for rider_type in ['Solo', 'Group']:
    subset = filtered_df[filtered_df['passenger_count'].apply(
        lambda x: rider_type == 'Solo' if x == 1 else rider_type == 'Group'
    )]
    generous = subset['tip_percentage'].apply(is_generous).sum()
    pct = generous / len(subset) * 100
    print(f"  {rider_type}: {pct:.2f}% tip 20% or more")

# Late night only
print("\nLate Night (12am-6am):")
for rider_type in ['Solo', 'Group']:
    subset = late_night[late_night['rider_type'] == rider_type]
    if len(subset) > 0:
        generous = subset['tip_percentage'].apply(is_generous).sum()
        pct = generous / len(subset) * 100
        print(f"  {rider_type}: {pct:.2f}% tip 20% or more")

# Prime bar closing time: 2am-4am
print("\n" + "="*60)
print("PRIME BAR CLOSING TIME (2am-4am)")
print("="*60)

bar_closing = filtered_df[filtered_df['pickup_hour'].isin([2, 3])]

if len(bar_closing) > 0:
    bar_stats = bar_closing.agg({
        'tip_percentage': ['mean', 'median', 'count']
    }).round(2)
    
    print(f"Total trips: {len(bar_closing):,}")
    print(f"Mean tip percentage: {bar_closing['tip_percentage'].mean():.2f}%")
    print(f"Median tip percentage: {bar_closing['tip_percentage'].median():.2f}%")
    
    zero_tip_rate = (bar_closing['tip_amount'] == 0).sum() / len(bar_closing) * 100
    print(f"Zero tip rate: {zero_tip_rate:.2f}%")
    
    generous_rate = (bar_closing['tip_percentage'] >= 20).sum() / len(bar_closing) * 100
    print(f"Generous (20%+) rate: {generous_rate:.2f}%")

print("\n" + "="*60)
print("CONCLUSION")
print("="*60)
print("\nCompare late night (potentially intoxicated) tippers vs daytime.")
print("Are drunk people more generous? Or do they just mash buttons randomly?")
print("And does the solo vs group dynamic change when alcohol is involved?")
