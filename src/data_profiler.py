"""
Automated Data Quality Profiler

Analyzes dataset and automatically generates quality rules based on
statistical patterns, distributions, and data characteristics.

Author: Henrik
Date: November 2024
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

class DataProfiler:
    """Automatically profile a dataset and suggest quality rules"""
    
    def __init__(self, df):
        self.df = df
        self.profile = {}
        
    def generate_profile(self):
        """Generate comprehensive data profile"""
        print("=" * 70)
        print("AUTOMATED DATA PROFILING")
        print("=" * 70)
        
        print(f"\nDataset shape: {self.df.shape[0]:,} rows × {self.df.shape[1]} columns")
        
        for column in self.df.columns:
            print(f"\n{'='*70}")
            print(f"Column: {column}")
            print(f"{'='*70}")
            
            col_profile = self._profile_column(column)
            self.profile[column] = col_profile
            
            self._print_column_profile(column, col_profile)
            
        return self.profile
    
    def _profile_column(self, column):
        """Profile a single column"""
        col_data = self.df[column]
        
        profile = {
            'dtype': str(col_data.dtype),
            'null_count': int(col_data.isnull().sum()),
            'null_percentage': float((col_data.isnull().sum() / len(col_data)) * 100),
            'unique_count': int(col_data.nunique()),
            'sample_values': col_data.dropna().head(5).tolist()
        }
        
        # Numeric columns get statistical analysis
        if pd.api.types.is_numeric_dtype(col_data):
            profile.update({
                'min': float(col_data.min()),
                'max': float(col_data.max()),
                'mean': float(col_data.mean()),
                'median': float(col_data.median()),
                'std': float(col_data.std()),
                'q1': float(col_data.quantile(0.25)),
                'q3': float(col_data.quantile(0.75)),
            })
            
            # Detect outliers using IQR method
            iqr = profile['q3'] - profile['q1']
            lower_bound = profile['q1'] - (1.5 * iqr)
            upper_bound = profile['q3'] + (1.5 * iqr)
            
            outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
            profile['outlier_count'] = int(len(outliers))
            profile['outlier_percentage'] = float((len(outliers) / len(col_data)) * 100)
            
            # Suggest reasonable bounds (3 standard deviations)
            profile['suggested_min'] = float(profile['mean'] - (3 * profile['std']))
            profile['suggested_max'] = float(profile['mean'] + (3 * profile['std']))
            
        # Datetime columns
        elif pd.api.types.is_datetime64_any_dtype(col_data):
            profile.update({
                'min_date': str(col_data.min()),
                'max_date': str(col_data.max()),
            })
            
        # String/categorical columns
        else:
            profile['most_common'] = col_data.value_counts().head(5).to_dict()
            
        return profile
    
    def _print_column_profile(self, column, profile):
        """Print profile for a column"""
        print(f"  Data Type: {profile['dtype']}")
        print(f"  Null Values: {profile['null_count']:,} ({profile['null_percentage']:.2f}%)")
        print(f"  Unique Values: {profile['unique_count']:,}")
        
        if 'min' in profile:  # Numeric
            print(f"\n  Statistics:")
            print(f"    Min: {profile['min']:.2f}")
            print(f"    Max: {profile['max']:.2f}")
            print(f"    Mean: {profile['mean']:.2f}")
            print(f"    Median: {profile['median']:.2f}")
            print(f"    Std Dev: {profile['std']:.2f}")
            print(f"\n  Outliers (IQR method): {profile['outlier_count']:,} ({profile['outlier_percentage']:.2f}%)")
            print(f"\n  Suggested Quality Rules:")
            print(f"    Accept range: {profile['suggested_min']:.2f} to {profile['suggested_max']:.2f}")
            
        elif 'min_date' in profile:  # Datetime
            print(f"  Date Range: {profile['min_date']} to {profile['max_date']}")
            
        else:  # Categorical
            print(f"  Sample Values: {profile['sample_values'][:3]}")
            if 'most_common' in profile:
                print(f"  Most Common Values:")
                for value, count in list(profile['most_common'].items())[:3]:
                    print(f"    '{value}': {count:,} occurrences")
    
    def suggest_quality_rules(self):
        """Generate quality rules based on profile"""
        print("\n" + "=" * 70)
        print("SUGGESTED QUALITY RULES")
        print("=" * 70)
        
        rules = {}
        
        for column, profile in self.profile.items():
            column_rules = []
            
            # Rule: Check for nulls if column has low null percentage
            if profile['null_percentage'] < 5:
                column_rules.append({
                    'rule': 'not_null',
                    'description': f"{column} should not be null (currently {profile['null_percentage']:.2f}% null)"
                })
            
            # Rules for numeric columns
            if 'min' in profile:
                # Rule: Value should be within reasonable range
                column_rules.append({
                    'rule': 'value_range',
                    'min': profile['suggested_min'],
                    'max': profile['suggested_max'],
                    'description': f"{column} should be between {profile['suggested_min']:.2f} and {profile['suggested_max']:.2f}"
                })
                
                # Rule: Flag if value is exactly 0 (often indicates missing data)
                zero_count = (self.df[column] == 0).sum()
                if zero_count > 0:
                    column_rules.append({
                        'rule': 'warn_zeros',
                        'description': f"{column} has {zero_count:,} zero values - verify if valid",
                        'severity': 'warning'
                    })
            
            if column_rules:
                rules[column] = column_rules
                
        # Print suggested rules
        for column, column_rules in rules.items():
            print(f"\n{column}:")
            for rule in column_rules:
                severity = rule.get('severity', 'error')
                print(f"  [{severity.upper()}] {rule['description']}")
                
        return rules


# Main execution
if __name__ == "__main__":
    # Load data
    data_file = os.path.join('data', 'yellow_tripdata_2024-01.parquet')
    print(f"Loading data from {data_file}...")
    df = pd.read_parquet(data_file)
    
    # Take a sample for faster profiling (you can use full dataset)
    df_sample = df.sample(n=100000, random_state=42)
    print(f"Using sample of {len(df_sample):,} records for profiling\n")
    
    # Profile the data
    profiler = DataProfiler(df_sample)
    profile = profiler.generate_profile()
    
    # Generate quality rule suggestions
    rules = profiler.suggest_quality_rules()
    
    print("\n" + "=" * 70)
    print("✓ Profiling complete!")
    print("=" * 70)