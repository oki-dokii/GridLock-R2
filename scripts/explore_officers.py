import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('jan to may police violation_anonymized791b166.csv')

# Calculate approval and rejection counts per officer (created_by_id)
officer_stats = df.groupby('created_by_id')['validation_status'].value_counts().unstack(fill_value=0)
if 'approved' not in officer_stats.columns:
    officer_stats['approved'] = 0
if 'rejected' not in officer_stats.columns:
    officer_stats['rejected'] = 0

officer_stats['total_reviewed'] = officer_stats['approved'] + officer_stats['rejected']

# Calculate p_hat_o using Bayesian Beta filter: (5 + A_o) / (7 + A_o + R_o)
officer_stats['p_hat'] = (5 + officer_stats['approved']) / (7 + officer_stats['approved'] + officer_stats['rejected'])

# Print top 5 and bottom 5 officers by p_hat
print("Worst 10 officers by p_hat:")
print(officer_stats.sort_values(by='p_hat').head(10))

print("\nBest 10 officers by p_hat:")
print(officer_stats.sort_values(by='p_hat', ascending=False).head(10))
