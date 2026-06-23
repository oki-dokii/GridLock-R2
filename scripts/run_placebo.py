import pandas as pd
import numpy as np

print("Loading data...")
df = pd.read_csv('cleaned_violations.csv', usecols=['grid_id', 'month', 'date', 'ts_ist'])
df['ts_ist'] = pd.to_datetime(df['ts_ist'], format='mixed', utc=True)
df['year_month'] = df['ts_ist'].dt.to_period('M')
df['day'] = df['ts_ist'].dt.day

# Pre/Post months for matched windows
pre_month = pd.Period('2023-12', 'M')
post_month = pd.Period('2024-01', 'M')
# Ranking months
rank_months = [pd.Period('2023-11', 'M')]

# --- 1. Target Selection (Using Nov Trailing Average) ---
df_ranking = df[df['year_month'].isin(rank_months)]
ranking_counts = df_ranking.groupby('grid_id').size().reset_index(name='historical_violations')

k_targets = 50
treatment_grids = ranking_counts.sort_values('historical_violations', ascending=False).head(k_targets)['grid_id'].values

# --- 2. Matched Window Evaluation (Days 1-8 of Dec vs Jan) ---
df_eval = df[df['year_month'].isin([pre_month, post_month]) & (df['day'] <= 8)]
eval_counts = df_eval.groupby(['grid_id', 'year_month']).size().unstack(fill_value=0)

if pre_month not in eval_counts.columns: eval_counts[pre_month] = 0
if post_month not in eval_counts.columns: eval_counts[post_month] = 0

eval_counts['group'] = 'Control (Unenforced)'
eval_counts.loc[eval_counts.index.isin(treatment_grids), 'group'] = 'Treatment (GridLock Targeted)'

results = eval_counts.groupby('group')[[pre_month, post_month]].sum()
results.columns = ['pre_violations', 'post_violations']
results['pct_change'] = ((results['post_violations'] - results['pre_violations']) / results['pre_violations']) * 100

control_change = results.loc['Control (Unenforced)', 'pct_change']
treatment_change = results.loc['Treatment (GridLock Targeted)', 'pct_change']

net_effect = treatment_change - control_change

print(f"--- AGGREGATE SUM % CHANGE ---")
print(f"Control Change: {control_change:+.1f}%")
print(f"Treatment Change: {treatment_change:+.1f}%")
print(f"Net Effect: {net_effect:+.1f}%\n")

# --- 3. Alternative Normalization: Per-Cell Average % Change ---
# Instead of summing across the group, we calculate the % change for each cell, then average those percentages.
# We must be careful of cells that go from 0 to something, or are 0 in both.
# Alternatively, a log-difference or just averaging the raw count change.

# Let's calculate the per-cell raw change, and per-cell % change.
eval_counts['cell_diff'] = eval_counts[post_month] - eval_counts[pre_month]
# To avoid division by zero in per-cell % change, we can add a small epsilon or only look at cells with >0 pre_violations.
eval_counts_valid = eval_counts[eval_counts[pre_month] > 0].copy()
eval_counts_valid['cell_pct_change'] = (eval_counts_valid['cell_diff'] / eval_counts_valid[pre_month]) * 100

per_cell_avg = eval_counts_valid.groupby('group')['cell_pct_change'].mean()
print(f"--- PER-CELL AVERAGE % CHANGE (Pre > 0) ---")
print(f"Control Average Change: {per_cell_avg.loc['Control (Unenforced)']:+.1f}%")
print(f"Treatment Average Change: {per_cell_avg.loc['Treatment (GridLock Targeted)']:+.1f}%")
print(f"Net Effect: {per_cell_avg.loc['Treatment (GridLock Targeted)'] - per_cell_avg.loc['Control (Unenforced)']:+.1f}%")

