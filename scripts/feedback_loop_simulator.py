import pandas as pd
import numpy as np

print("Loading data...")
# Read violations data
df = pd.read_csv('cleaned_violations.csv', usecols=['grid_id', 'month', 'date', 'ts_ist'])
df['ts_ist'] = pd.to_datetime(df['ts_ist'], format='mixed', utc=True)
df['year_month'] = df['ts_ist'].dt.to_period('M')
df['day'] = df['ts_ist'].dt.day

# Filter to match the 8-day window of April (days 1-8) for all months
# to ensure an apples-to-apples comparison
df_matched = df[df['day'] <= 8].copy()

# Group by grid and month
monthly_counts = df_matched.groupby(['grid_id', 'year_month']).size().reset_index(name='violations')

# Get available months
months = sorted(monthly_counts['year_month'].unique())
if len(months) < 2:
    print("Not enough months to simulate feedback loop.")
    exit()

post_month = months[-1]
pre_month = months[-2]

print(f"Simulating intervention (Matched 8-Day Windows):")
print(f"  Pre-Intervention Baseline: {pre_month}")
print(f"  Post-Intervention Measurement: {post_month}")

pre_data = monthly_counts[monthly_counts['year_month'] == pre_month].set_index('grid_id')['violations']
post_data = monthly_counts[monthly_counts['year_month'] == post_month].set_index('grid_id')['violations']

all_grids = set(pre_data.index).union(set(post_data.index))
eval_df = pd.DataFrame(index=list(all_grids))
eval_df['pre_violations'] = pre_data.reindex(eval_df.index).fillna(0)
eval_df['post_violations'] = post_data.reindex(eval_df.index).fillna(0)

k_targets = 50
treatment_grids = eval_df.sort_values('pre_violations', ascending=False).head(k_targets).index

eval_df['group'] = 'Control (Unenforced)'
eval_df.loc[treatment_grids, 'group'] = 'Treatment (GridLock Targeted)'

results = eval_df.groupby('group')[['pre_violations', 'post_violations']].sum()
results['pct_change'] = ((results['post_violations'] - results['pre_violations']) / results['pre_violations']) * 100

control_change = results.loc['Control (Unenforced)', 'pct_change']
treatment_change = results.loc['Treatment (GridLock Targeted)', 'pct_change']

net_effect = treatment_change - control_change

md = f"""# Intervention Feedback Loop Tracker (Stub)

This report outlines the **Difference-in-Differences (DiD)** tracking mechanism designed to close the feedback loop. Rather than asserting "violations dropped by X%", this framework isolates the *causal impact* of GridLock dispatch by comparing targeted zones against the natural background trend of unenforced zones.

## Simulation Setup
*   **Pre-Intervention Baseline:** {pre_month} (Days 1-8 matched window)
*   **Post-Intervention Measurement:** {post_month} (Days 1-8 matched window)
*   **Target Selection:** Top {k_targets} hotspots (Simulated treatment group)
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
"""

with open('/Users/sohambanerjee/.gemini/antigravity/brain/603a2247-f5e9-44a6-a8b8-e6622a1eb543/FEEDBACK_LOOP_TRACKER.md', 'w') as f:
    f.write(md)

print("Feedback loop simulation complete. Report saved.")
