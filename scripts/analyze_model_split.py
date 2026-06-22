import pandas as pd

data = []
with open('stratified_evaluation_results.md', 'r') as f:
    for line in f:
        if line.startswith('| ') and not line.startswith('| Subgroup') and not line.startswith('| :---') and not line.startswith('| Overall'):
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) >= 9:
                subgroup = parts[0]
                model = parts[1]
                k = parts[2]
                try:
                    # Strip ** and % and ⚠️
                    rec_str = parts[5].replace('*', '').replace('%', '').replace('⚠️', '').strip()
                    if rec_str == 'low_conf':
                        continue
                    rec = float(rec_str)
                    n_str = parts[8].replace('⚠️', '').strip()
                    n = int(n_str)
                    
                    if k == '20':
                        data.append({
                            'subgroup': subgroup,
                            'model': model,
                            'recall': rec,
                            'n': n
                        })
                except Exception as e:
                    pass

df = pd.DataFrame(data)

pivot = df.pivot_table(index=['subgroup', 'n'], columns='model', values='recall').reset_index()
pivot = pivot.dropna()

xgboost_wins = pivot[pivot['XGBoost'] > pivot['GLM-Ensemble']]
glm_wins = pivot[pivot['GLM-Ensemble'] > pivot['XGBoost']]
ties = pivot[pivot['GLM-Ensemble'] == pivot['XGBoost']]

print(f"XGBoost Wins: {len(xgboost_wins)}")
print(f"GLM Wins: {len(glm_wins)}")
print(f"Ties: {len(ties)}")

print("\n--- Top XGBoost Wins (Margin) ---")
xgboost_wins = xgboost_wins.copy()
xgboost_wins['diff'] = xgboost_wins['XGBoost'] - xgboost_wins['GLM-Ensemble']
print(xgboost_wins.sort_values('diff', ascending=False).head(15).to_string())

print("\n--- Summary Stats ---")
print(f"XGBoost wins median n: {xgboost_wins['n'].median()}")
print(f"GLM wins median n: {glm_wins['n'].median()}")

print("\n--- Subgroup Types in XGBoost Wins ---")
veh_types = [x for x in xgboost_wins['subgroup'] if x.isupper() and 'Station' not in x and len(x) > 2]
stations = [x for x in xgboost_wins['subgroup'] if x not in veh_types]
print(f"Vehicle Types ({len(veh_types)}):", veh_types)
print(f"Stations ({len(stations)}):", stations)

