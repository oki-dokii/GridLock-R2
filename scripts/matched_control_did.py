import pandas as pd
import numpy as np
import json
import argparse
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--placebo', action='store_true', help='Run placebo test (Nov ranking, Dec vs Jan)')
    args = parser.parse_args()

    # Load Hotspot Metadata (Restricting our pool to the top 500 cells with known OSM data)
    try:
        with open('hotspot_data.json', 'r') as f:
            hotspots = json.load(f)
    except FileNotFoundError:
        print("Error: hotspot_data.json not found.")
        sys.exit(1)

    grid_metadata = {hs['id']: hs.get('roadType', 'Local Street') for hs in hotspots}
    valid_grids = set(grid_metadata.keys())

    # Load Violations Data
    print("Loading violation data...")
    df = pd.read_csv('cleaned_violations.csv', usecols=['grid_id', 'month', 'date', 'ts_ist'])
    # Filter to only the grids we have metadata for
    df = df[df['grid_id'].isin(valid_grids)].copy()

    df['ts_ist'] = pd.to_datetime(df['ts_ist'], format='mixed', utc=True)
    df['year_month'] = df['ts_ist'].dt.to_period('M')
    df['day'] = df['ts_ist'].dt.day

    if args.placebo:
        print("\n=== RUNNING PLACEBO TEST ===")
        rank_months = [pd.Period('2023-11', 'M')]
        pre_month = pd.Period('2023-12', 'M')
        post_month = pd.Period('2024-01', 'M')
    else:
        print("\n=== RUNNING ACTUAL EVALUATION ===")
        rank_months = [pd.Period('2024-01', 'M'), pd.Period('2024-02', 'M')]
        pre_month = pd.Period('2024-03', 'M')
        post_month = pd.Period('2024-04', 'M')

    # 1. Calculate Historical Volume
    df_ranking = df[df['year_month'].isin(rank_months)]
    historical_volume = df_ranking.groupby('grid_id').size() / len(rank_months)
    # Ensure all valid_grids have a value (0 if not present in ranking months)
    historical_volume = historical_volume.reindex(list(valid_grids), fill_value=0)

    # 2. Select Treatment and Control Pools
    k_targets = 50
    sorted_grids = historical_volume.sort_values(ascending=False)
    treatment_grids = set(sorted_grids.head(k_targets).index)
    control_grids = set(sorted_grids.index) - treatment_grids

    # 3. Calculate % Change for matched windows
    df_eval = df[df['year_month'].isin([pre_month, post_month]) & (df['day'] <= 8)]
    eval_counts = df_eval.groupby(['grid_id', 'year_month']).size().unstack(fill_value=0)
    
    # Ensure all valid grids and columns exist
    eval_counts = eval_counts.reindex(list(valid_grids), fill_value=0)
    if pre_month not in eval_counts.columns: eval_counts[pre_month] = 0
    if post_month not in eval_counts.columns: eval_counts[post_month] = 0

    # Calculate % change. Avoid division by zero by setting to NaN if pre == 0
    eval_counts['pct_change'] = np.where(
        eval_counts[pre_month] > 0, 
        (eval_counts[post_month] - eval_counts[pre_month]) / eval_counts[pre_month] * 100, 
        np.nan
    )

    # 4. Nearest-Neighbor Matching
    results_log = []
    matched_effects = []
    
    # Convert control data into a lookup
    control_data = []
    for g in control_grids:
        control_data.append({
            'grid_id': g,
            'road_type': grid_metadata[g],
            'hist_vol': historical_volume[g],
            'pct_change': eval_counts.loc[g, 'pct_change']
        })

    for t_grid in treatment_grids:
        t_road = grid_metadata[t_grid]
        t_vol = historical_volume[t_grid]
        t_change = eval_counts.loc[t_grid, 'pct_change']

        # Skip if treatment cell has NaN pct change (should be rare for top 50, but safe)
        if np.isnan(t_change):
            continue

        # Filter controls by exact road type
        candidate_controls = [c for c in control_data if c['road_type'] == t_road and not np.isnan(c['pct_change'])]
        
        # If not enough controls match exact road type, relax constraint? 
        # The prompt says "same road_type", so we enforce it.
        if len(candidate_controls) < 5:
            # If not enough exact matches, log a warning and use whatever we have, or skip.
            # Let's use whatever we have if > 0, else skip.
            if len(candidate_controls) == 0:
                print(f"Warning: Treatment grid {t_grid} has no valid controls with road type {t_road}. Skipping.")
                continue

        # Sort by distance in historical volume
        candidate_controls.sort(key=lambda x: abs(x['hist_vol'] - t_vol))
        top_k_controls = candidate_controls[:5]

        # Mean control change
        mean_control_change = np.mean([c['pct_change'] for c in top_k_controls])
        net_effect = t_change - mean_control_change
        matched_effects.append(net_effect)

        log_entry = {
            'treatment_grid': t_grid,
            'road_type': t_road,
            'hist_vol': round(t_vol, 1),
            't_pct_change': round(t_change, 1),
            'mean_matched_control_change': round(mean_control_change, 1),
            'net_effect': round(net_effect, 1),
            'matched_controls': [
                {
                    'grid_id': c['grid_id'], 
                    'hist_vol': round(c['hist_vol'], 1), 
                    'pct_change': round(c['pct_change'], 1)
                } for c in top_k_controls
            ]
        }
        results_log.append(log_entry)

    # 5. Output Results
    print("\n--- MATCHING AUDIT LOG ---")
    for log in results_log[:5]: # Print first 5 for brevity
        print(f"Treatment: {log['treatment_grid']} | Road: {log['road_type']} | Vol: {log['hist_vol']} | Change: {log['t_pct_change']:+.1f}%")
        print(f"  Controls: {[f'{c['grid_id']} (Vol:{c['hist_vol']}, {c['pct_change']:+.1f}%)' for c in log['matched_controls']]}")
        print(f"  -> Mean Control Change: {log['mean_matched_control_change']:+.1f}%  |  Net Effect: {log['net_effect']:+.1f}%\n")
    print(f"... (and {len(results_log) - 5} more)")

    final_net_effect = np.mean(matched_effects)
    print("\n" + "="*50)
    print(f"FINAL AVERAGE MATCHED EFFECT (Per-Cell DiD): {final_net_effect:+.1f}%")
    print("="*50 + "\n")

    # Optionally write log to file
    with open('matched_did_audit.json', 'w') as f:
        json.dump(results_log, f, indent=2)

if __name__ == '__main__':
    main()
