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
    # The prompt explicitly specifies: "ranked by Jan-Feb trailing average volume" for the Top 50.
    rank_months = [pd.Period('2024-01', 'M'), pd.Period('2024-02', 'M')]
    df_ranking = df[df['year_month'].isin(rank_months)]
    historical_volume = df_ranking.groupby('grid_id').size() / len(rank_months)
    k_targets = 50
    treatment_grids = set(historical_volume.sort_values(ascending=False).head(k_targets).index)

    # 2. Get monthly volumes for all grids
    # We group by grid_id and year_month
    monthly_counts = df.groupby(['grid_id', 'year_month']).size().unstack(fill_value=0)

    if args.placebo:
        print("\n=== RUNNING PLACEBO TEST (Self-Trend) ===")
        # Train: Nov(0), Dec(1), Jan(2)
        # Predict: Feb(3)
        train_months = [pd.Period('2023-11', 'M'), pd.Period('2023-12', 'M'), pd.Period('2024-01', 'M')]
        target_month = pd.Period('2024-02', 'M')
        target_idx = 3
    else:
        print("\n=== RUNNING ACTUAL EVALUATION (Self-Trend) ===")
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
        if m not in monthly_counts.columns:
            monthly_counts[m] = 0

    deviations = []
    
    for t_grid in treatment_grids:
        # Get training points
        x = [month_idx[m] for m in train_months]
        y = [monthly_counts.loc[t_grid, m] for m in train_months]
        
        # Fit linear regression
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        
        # Predict
        predicted_full_month = (slope * target_idx) + intercept
        # Ensure prediction isn't negative
        predicted_full_month = max(0, predicted_full_month)
        
        actual_count = monthly_counts.loc[t_grid, target_month]

        if args.placebo:
            # Feb is a full month, no scaling
            predicted_target = predicted_full_month
        else:
            # April is truncated to 8 days, so scale predicted full month down to 8 days
            # April has 30 days
            predicted_target = predicted_full_month * (8.0 / 30.0)
            # The actual April count in the dataset is already just Days 1-8

        if predicted_target == 0 and actual_count == 0:
            dev = 0.0
        elif predicted_target == 0:
            # Undefined or infinitely positive deviation. For robust average, let's limit or use actual change
            # But these are top 50 hotspots, so prediction is very unlikely to be 0
            dev = 100.0 
        else:
            dev = ((actual_count - predicted_target) / predicted_target) * 100.0
            
        deviations.append(dev)

    avg_deviation = np.mean(deviations)

    print(f"\nAverage Predicted vs Actual Deviation across Top 50: {avg_deviation:+.1f}%")

if __name__ == '__main__':
    main()
