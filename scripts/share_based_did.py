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
    df_8day = df[df['day'] <= 8].copy()
    
    network_totals = df_8day.groupby('year_month').size()
    df_treat = df_8day[df_8day['grid_id'].isin(treatment_grids)]
    treatment_totals = df_treat.groupby('year_month').size()
    
    shares = {}
    print("\n=== RAW MONTHLY SHARE (8-Day Windows) ===")
    print("-" * 65)
    print(f"{'Month':<10} | {'Network Total':<15} | {'Top-50 Total':<15} | {'Top-50 Share'}")
    print("-" * 65)
    
    for m in months:
        nt = network_totals.get(m, 0)
        tt = treatment_totals.get(m, 0)
        share = (tt / nt) * 100 if nt > 0 else 0.0
        shares[m] = share
        print(f"{str(m):<10} | {nt:<15} | {tt:<15} | {share:.2f}%")
        
    print("-" * 65)
    
    # 3. PLACEBO TESTS (Month-to-Month Swings)
    print("\n=== PLACEBO TESTS (Noise Floor Check) ===")
    
    # Dec -> Jan Placebo
    dec_share = shares[pd.Period('2023-12', 'M')]
    jan_share = shares[pd.Period('2024-01', 'M')]
    dec_jan_shift = jan_share - dec_share
    print(f"Placebo 1 (Dec->Jan): {dec_share:.2f}% -> {jan_share:.2f}% ({dec_jan_shift:+.2f} pp)")
    
    # Jan -> Feb Placebo
    feb_share = shares[pd.Period('2024-02', 'M')]
    jan_feb_shift = feb_share - jan_share
    print(f"Placebo 2 (Jan->Feb): {jan_share:.2f}% -> {feb_share:.2f}% ({jan_feb_shift:+.2f} pp)")

    # Feb -> Mar Placebo
    mar_share = shares[pd.Period('2024-03', 'M')]
    feb_mar_shift = mar_share - feb_share
    print(f"Placebo 3 (Feb->Mar): {feb_share:.2f}% -> {mar_share:.2f}% ({feb_mar_shift:+.2f} pp)")

    # 4. ACTUAL EVALUATION
    apr_share = shares[pd.Period('2024-04', 'M')]
    mar_apr_shift = apr_share - mar_share
    
    print("\n=== ACTUAL EVALUATION (March vs April) ===")
    print(f"Intervention (Mar->Apr): {mar_share:.2f}% -> {apr_share:.2f}% ({mar_apr_shift:+.2f} pp)")
    
    print("\n=== CONCLUSION ===")
    max_placebo = max(abs(dec_jan_shift), abs(jan_feb_shift), abs(feb_mar_shift))
    
    if abs(mar_apr_shift) > max_placebo:
        print(f"SUCCESS: The intervention shift ({abs(mar_apr_shift):.2f} pp) exceeds the maximum placebo noise floor ({max_placebo:.2f} pp).")
    else:
        print(f"FAILURE: The intervention shift ({abs(mar_apr_shift):.2f} pp) is smaller than historical placebo swings (up to {max_placebo:.2f} pp).")
        print("The observed 'impact' is statistically indistinguishable from background noise.")

if __name__ == '__main__':
    main()
