import pandas as pd
import numpy as np
import argparse
from scipy.stats import linregress

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--placebo', action='store_true', help='Run placebo test (Nov-Jan -> predict Feb)')
    args = parser.parse_args()

    print("Loading data...")
    df = pd.read_csv('cleaned_violations.csv', usecols=['grid_id', 'month', 'date', 'ts_ist'])
    df['ts_ist'] = pd.to_datetime(df['ts_ist'], format='mixed', utc=True)
    df['year_month'] = df['ts_ist'].dt.to_period('M')

    # Mapping periods to indices
    month_idx = {
        pd.Period('2023-11', 'M'): 0,
        pd.Period('2023-12', 'M'): 1,
        pd.Period('2024-01', 'M'): 2,
        pd.Period('2024-02', 'M'): 3,
        pd.Period('2024-03', 'M'): 4,
        pd.Period('2024-04', 'M'): 5,
    }

    # 1. Target Selection (Jan-Feb Trailing Average)
    rank_months = [pd.Period('2024-01', 'M'), pd.Period('2024-02', 'M')]
    df_ranking = df[df['year_month'].isin(rank_months)]
    historical_volume = df_ranking.groupby('grid_id').size() / len(rank_months)
    k_targets = 50
    treatment_grids = set(historical_volume.sort_values(ascending=False).head(k_targets).index)

    # Filter strictly to the Treatment Group
    df_treat = df[df['grid_id'].isin(treatment_grids)].copy()

    # Get combined monthly totals for the Treatment Group
    aggregate_counts = df_treat.groupby('year_month').size()

    if args.placebo:
        print("\n=== RUNNING PLACEBO TEST (Aggregate Trend) ===")
        # Train: Nov(0), Dec(1), Jan(2)
        # Predict: Feb(3)
        train_months = [pd.Period('2023-11', 'M'), pd.Period('2023-12', 'M'), pd.Period('2024-01', 'M')]
        target_month = pd.Period('2024-02', 'M')
        target_idx = 3
    else:
        print("\n=== RUNNING ACTUAL EVALUATION (Aggregate Trend) ===")
        # Train: Nov(0), Dec(1), Jan(2), Feb(3), Mar(4)
        # Predict: Apr(5)
        train_months = [
            pd.Period('2023-11', 'M'), pd.Period('2023-12', 'M'), pd.Period('2024-01', 'M'),
            pd.Period('2024-02', 'M'), pd.Period('2024-03', 'M')
        ]
        target_month = pd.Period('2024-04', 'M')
        target_idx = 5

    # Make sure all columns exist
    for m in train_months + [target_month]:
        if m not in aggregate_counts.index:
            aggregate_counts[m] = 0

    # Get training points
    x = [month_idx[m] for m in train_months]
    y = [aggregate_counts[m] for m in train_months]
    
    # Fit linear regression
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    
    # Predict
    predicted_full_month = (slope * target_idx) + intercept
    predicted_full_month = max(0, predicted_full_month)
    
    actual_count = aggregate_counts[target_month]

    if args.placebo:
        predicted_target = predicted_full_month
    else:
        # Scale predicted full month down to 8 days
        predicted_target = predicted_full_month * (8.0 / 30.0)
        # We need actual April count, but filtered strictly to day <= 8
        # Since April in our dataset IS truncated to 8 days, we can just take the raw sum,
        # but let's be explicit and strictly sum only Day <= 8 to be completely safe.
        actual_count = df_treat[(df_treat['year_month'] == target_month) & (df_treat['ts_ist'].dt.day <= 8)].shape[0]

    if predicted_target == 0 and actual_count == 0:
        dev = 0.0
    elif predicted_target == 0:
        dev = 100.0 
    else:
        dev = ((actual_count - predicted_target) / predicted_target) * 100.0
        
    print(f"Training counts: {dict(zip([str(m) for m in train_months], y))}")
    print(f"Predicted target count: {predicted_target:.1f}")
    print(f"Actual target count: {actual_count}")
    print(f"\nPredicted vs Actual Deviation: {dev:+.1f}%")

if __name__ == '__main__':
    main()
