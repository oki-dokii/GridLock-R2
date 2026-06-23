import pandas as pd
import numpy as np

def main():
    print("Loading data...")
    df = pd.read_csv('cleaned_violations.csv', usecols=['grid_id', 'month', 'date', 'ts_ist'])
    df['ts_ist'] = pd.to_datetime(df['ts_ist'], format='mixed', utc=True)
    df['year_month'] = df['ts_ist'].dt.to_period('M')
    df['day'] = df['ts_ist'].dt.day

    # Mapping periods
    months = [
        pd.Period('2023-11', 'M'),
        pd.Period('2023-12', 'M'),
        pd.Period('2024-01', 'M'),
        pd.Period('2024-02', 'M'),
        pd.Period('2024-03', 'M'),
        pd.Period('2024-04', 'M')
    ]

    # 1. Target Selection (Jan-Feb Trailing Average, FULL MONTH)
    rank_months = [pd.Period('2024-01', 'M'), pd.Period('2024-02', 'M')]
    df_ranking = df[df['year_month'].isin(rank_months)]
    historical_volume = df_ranking.groupby('grid_id').size() / len(rank_months)
    k_targets = 50
    treatment_grids = set(historical_volume.sort_values(ascending=False).head(k_targets).index)

    # 2. Compute 8-Day Matched Window Shares
    # To keep it completely apples-to-apples across all months including April, we filter to day <= 8
    df_8day = df[df['day'] <= 8].copy()
    
    # Total Network Violations per month (8-day window)
    network_totals = df_8day.groupby('year_month').size()
    
    # Treatment Violations per month (8-day window)
    df_treat = df_8day[df_8day['grid_id'].isin(treatment_grids)]
    treatment_totals = df_treat.groupby('year_month').size()
    
    shares = {}
    print("\n=== PLACEBO / SANITY CHECK: MONTHLY SHARE (8-Day Windows) ===")
    print("Is the Top-50 share stable despite the massive fluctuation in raw counts?")
    print("-" * 65)
    print(f"{'Month':<10} | {'Network Total':<15} | {'Top-50 Total':<15} | {'Top-50 Share'}")
    print("-" * 65)
    
    for m in months:
        nt = network_totals.get(m, 0)
        tt = treatment_totals.get(m, 0)
        if nt > 0:
            share = (tt / nt) * 100
        else:
            share = 0.0
        shares[m] = share
        print(f"{str(m):<10} | {nt:<15} | {tt:<15} | {share:.2f}%")
        
    print("-" * 65)
    
    # Check stability (Nov - Mar)
    pre_shares = [shares[m] for m in months[:-1] if m in shares and network_totals.get(m, 0) > 0]
    mean_share = np.mean(pre_shares)
    std_share = np.std(pre_shares)
    
    print(f"\nMean Share (Nov-Mar): {mean_share:.2f}% (Std Dev: ±{std_share:.2f}%)")
    
    if std_share > 5.0:
        print("\nWARNING: Share is highly volatile. This approach may not be reliable.")
    else:
        print("\nSUCCESS: Share is remarkably stable! The instrument volatility cancels out.")
        
        # Compute the real comparison
        march_share = shares[pd.Period('2024-03', 'M')]
        april_share = shares[pd.Period('2024-04', 'M')]
        
        pp_change = april_share - march_share
        pct_change = (april_share - march_share) / march_share * 100
        
        print("\n=== CLOSING IMPACT METRIC (March vs April) ===")
        print(f"Pre-Intervention (March 1-8): Top-50 generated {march_share:.2f}% of citywide violations")
        print(f"Post-Intervention (April 1-8): Top-50 generated {april_share:.2f}% of citywide violations")
        print("-" * 65)
        print(f"Percentage Point Shift: {pp_change:+.2f} pp")
        print(f"Relative Shift in Share: {pct_change:+.1f}%")
        print("\n(This is the 'share of citywide violations attributable to targeted zones', effectively isolating the spatial impact of GridLock from the global fluctuation of the enforcement scale.)")

if __name__ == '__main__':
    main()
