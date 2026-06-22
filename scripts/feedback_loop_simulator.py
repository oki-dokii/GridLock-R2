import pandas as pd
import numpy as np

print("Loading data...")
df = pd.read_csv('cleaned_violations.csv', usecols=['grid_id', 'month', 'date', 'ts_ist'])
df['ts_ist'] = pd.to_datetime(df['ts_ist'], format='mixed', utc=True)
df['year_month'] = df['ts_ist'].dt.to_period('M')
df['day'] = df['ts_ist'].dt.day

# Pre/Post months for matched windows
pre_month = pd.Period('2024-03', 'M')
post_month = pd.Period('2024-04', 'M')
# Ranking months
rank_months = [pd.Period('2024-01', 'M'), pd.Period('2024-02', 'M')]

# --- 1. Target Selection (Using Jan & Feb Trailing Average) ---
df_ranking = df[df['year_month'].isin(rank_months)]
ranking_counts = df_ranking.groupby('grid_id').size().reset_index(name='historical_violations')
ranking_counts['historical_violations'] = ranking_counts['historical_violations'] / len(rank_months) # average

k_targets = 50
treatment_grids = ranking_counts.sort_values('historical_violations', ascending=False).head(k_targets)['grid_id'].values

# --- 2. Matched Window Evaluation (Days 1-8 of Mar vs Apr) ---
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

md = f"""# Intervention Feedback Loop Tracker (Stub)

This report outlines the **Difference-in-Differences (DiD)** tracking mechanism designed to close the feedback loop. Rather than asserting "violations dropped by X%", this framework isolates the *causal impact* of GridLock dispatch by comparing targeted zones against the natural background trend of unenforced zones.

## Simulation Setup
*   **Target Selection Period:** Jan 2024 – Feb 2024 (Trailing Average)
*   **Pre-Intervention Baseline:** {pre_month} (Days 1-8 matched window)
*   **Post-Intervention Measurement:** {post_month} (Days 1-8 matched window)
*   **Target Selection:** Top {k_targets} hotspots from the historical selection period. *(Selecting targets based on historical data prevents "regression to the mean" artifacts when measuring the change between {pre_month} and {post_month})*
*   **Control Group:** All remaining grid cells in the network

## Mechanism: Difference-in-Differences
Traffic volume and violations fluctuate naturally due to weather, holidays, or macro trends. By tracking an unenforced Control Group, we establish a baseline trend. The true impact of GridLock enforcement is the *difference* between the targeted group's change and the control group's natural change.

### Results on Held-Out Data (Mock Enforcement)
*Note: Since GridLock was not actively deployed in {post_month}, this demonstrates the tracking mechanism on historical data. Both groups reflect natural (unenforced) conditions. The data is explicitly filtered to an 8-day matched window (Days 1-8 of the month) to account for data truncation in the {post_month} dataset.*

| Cohort | Pre-Intervention ({pre_month} matched) | Post-Intervention ({post_month} matched) | % Change |
| :--- | :--- | :--- | :--- |
| **Control (Unenforced)** | {int(results.loc['Control (Unenforced)', 'pre_violations'])} | {int(results.loc['Control (Unenforced)', 'post_violations'])} | {control_change:+.1f}% |
| **Treatment (GridLock Targeted)** | {int(results.loc['Treatment (GridLock Targeted)', 'pre_violations'])} | {int(results.loc['Treatment (GridLock Targeted)', 'post_violations'])} | {treatment_change:+.1f}% |

### GridLock Impact Metric
**Net Intervention Effect (DiD):** `{net_effect:+.1f}%`

*If this were a live deployment, a negative Net Intervention Effect would mathematically prove that targeted patrols suppressed violations faster/more than the natural network trend.*

> [!TIP]
> **Why this matters (The April Data Drop):** Notice that the total violations dropped heavily between March and April 2024 across the entire network (partially due to reporting anomalies and seasonal shifts). A naive "before and after" metric would have falsely claimed a massive reduction caused by GridLock. Because this tracker uses a Difference-in-Differences approach with a matched time-window and trailing-average targeting, it correctly factors out the global network trend and regression-to-the-mean, isolating the true (stub) difference.
"""

with open('/Users/sohambanerjee/.gemini/antigravity/brain/603a2247-f5e9-44a6-a8b8-e6622a1eb543/FEEDBACK_LOOP_TRACKER.md', 'w') as f:
    f.write(md)

print("Feedback loop simulation complete. Report saved.")
