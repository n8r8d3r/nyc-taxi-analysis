"""
Retail Data Profiling

Profile the messy Online Retail dataset to identify data quality issues
common in retail/e-commerce systems.

Author: Henrik
Date: November 2024
"""

import pandas as pd
import os
import sys

# Import our profiler class
sys.path.append(os.path.dirname(__file__))
from data_profiler import DataProfiler

print("=" * 70)
print("RETAIL DATA QUALITY PROFILING")
print("=" * 70)

# Load the Excel file
data_file = os.path.join('data', 'online_retail.xlsx')
print(f"\nLoading data from {data_file}...")
print("(This may take a minute - Excel files are slow...)\n")

df = pd.read_excel(data_file)

print(f"Loaded {len(df):,} records")
print(f"Columns: {df.columns.tolist()}\n")

# Show sample data
print("Sample records:")
print(df.head())

# Profile the data
print("\n" + "=" * 70)
print("Starting automated profiling...")
print("=" * 70)

profiler = DataProfiler(df)
profile = profiler.generate_profile()

# Generate quality rules
rules = profiler.suggest_quality_rules()

print("\n" + "=" * 70)
print("✓ Retail data profiling complete!")
print("=" * 70)

# Specific retail data quality checks
print("\n" + "=" * 70)
print("RETAIL-SPECIFIC QUALITY ISSUES")
print("=" * 70)

# Check for negative quantities (returns/cancellations)
if 'Quantity' in df.columns:
    negative_qty = df[df['Quantity'] < 0]
    print(f"\nNegative Quantities (returns): {len(negative_qty):,} ({len(negative_qty)/len(df)*100:.2f}%)")
    
# Check for zero prices
if 'UnitPrice' in df.columns:
    zero_price = df[df['UnitPrice'] == 0]
    print(f"Zero Prices: {len(zero_price):,} ({len(zero_price)/len(df)*100:.2f}%)")
    
    negative_price = df[df['UnitPrice'] < 0]
    print(f"Negative Prices: {len(negative_price):,} ({len(negative_price)/len(df)*100:.2f}%)")

# Check for missing customer IDs
if 'CustomerID' in df.columns:
    missing_customer = df[df['CustomerID'].isnull()]
    print(f"\nMissing Customer IDs: {len(missing_customer):,} ({len(missing_customer)/len(df)*100:.2f}%)")

# Check Description field for common issues
if 'Description' in df.columns:
    # Look for extremely short descriptions
    df['desc_length'] = df['Description'].astype(str).str.len()
    short_desc = df[df['desc_length'] < 3]
    print(f"\nSuspiciously short descriptions (<3 chars): {len(short_desc):,}")
    
    # Look for duplicate descriptions (might indicate data entry issues)
    duplicate_desc = df['Description'].value_counts()
    print(f"Most common description: '{duplicate_desc.index[0]}' appears {duplicate_desc.iloc[0]:,} times")