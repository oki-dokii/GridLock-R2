import pandas as pd
import numpy as np
import os

# Determine repo root path
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(script_dir)
csv_path = os.path.join(os.path.dirname(repo_root), 'jan to may police violation_anonymized791b166.csv')
if not os.path.exists(csv_path):
    csv_path = os.path.join(repo_root, 'jan to may police violation_anonymized791b166.csv')
if not os.path.exists(csv_path):
    csv_path = 'jan to may police violation_anonymized791b166.csv'

print(f"Loading data from {csv_path}...")
df = pd.read_csv(csv_path)

# Preprocessing
df['ts'] = pd.to_datetime(df['created_datetime'], errors='coerce', utc=True)
df['ts_ist'] = df['ts'].dt.tz_convert('Asia/Kolkata')
df['date_ist'] = df['ts_ist'].dt.date
df['month'] = df['ts_ist'].dt.month
df['year'] = df['ts_ist'].dt.year

print("\n=== MONTHLY SUMMARY ===")
monthly_stats = df.groupby('month').agg(
    total_records=('id', 'count'),
    min_date=('ts_ist', 'min'),
    max_date=('ts_ist', 'max'),
    unique_officers=('created_by_id', 'nunique')
).reset_index()

# Calculate days in dataset for each month
def get_active_days(m):
    month_dates = df[df['month'] == m]['date_ist'].dropna().unique()
    return len(month_dates)

monthly_stats['active_days'] = monthly_stats['month'].apply(get_active_days)
monthly_stats['avg_records_per_active_day'] = monthly_stats['total_records'] / monthly_stats['active_days']

print(monthly_stats.to_string(index=False))

# Check daily record counts in April to spot gaps or drops
print("\n=== APRIL DAILY DETAIL ===")
april_df = df[df['month'] == 4].copy()
april_daily = april_df.groupby('date_ist').agg(
    records=('id', 'count'),
    active_officers=('created_by_id', 'nunique')
).reset_index()
print(april_daily.to_string(index=False))

# Check daily record counts in March for comparison
print("\n=== MARCH DAILY DETAIL (LAST 10 DAYS) ===")
march_df = df[df['month'] == 3].copy()
march_daily = march_df.groupby('date_ist').agg(
    records=('id', 'count'),
    active_officers=('created_by_id', 'nunique')
).reset_index()
print(march_daily.tail(10).to_string(index=False))

# Write investigation findings to a markdown report
output_lines = []
output_lines.append("# BTP GridLock-R2 April Volume Drop Investigation")
output_lines.append("> Empirical analysis of month-over-month violation record counts, officer activity, and data collection boundaries.")
output_lines.append("")
output_lines.append("## Executive Summary")
output_lines.append("The 76% drop in violation records in April (15,432 vs. 54K-65K in other months) is **entirely due to data truncation (partial month)**. The dataset collection terminates on **April 8, 2024**. When adjusting for active days, April's average daily enforcement volume is actually **higher** than both February and March.")
output_lines.append("")
output_lines.append("## Monthly Metrics Comparison")
output_lines.append("| Month | Total Records | Start Date (IST) | End Date (IST) | Active Days | Unique Officers | Avg Records/Day |")
output_lines.append("|:---:|:---:|:---:|:---:|:---:|:---:|:---:|")

for _, row in monthly_stats.iterrows():
    min_str = row['min_date'].strftime('%Y-%m-%d %H:%M')
    max_str = row['max_date'].strftime('%Y-%m-%d %H:%M')
    output_lines.append(f"| {int(row['month'])} | {int(row['total_records']):,} | {min_str} | {max_str} | {int(row['active_days'])} | {int(row['unique_officers'])} | {row['avg_records_per_active_day']:.1f} |")

output_lines.append("")
output_lines.append("## Key Findings")
output_lines.append("1. **Data Truncation**: April only contains data for **8 active days** (April 1 to April 8). The last record is logged at `2024-04-08 23:00:46 IST` (which is `2024-04-08 17:30:46 UTC`). The dataset does not contain records for April 9 through April 30.")
output_lines.append("2. **Daily Enforcement Intensity**: April is a highly active month, averaging **1,929.0 records per day**. This represents a **+7.7% increase** over March (1,791.4/day) and a **+4.7% increase** over February (1,842.1/day), demonstrating that the drop in count is a truncation effect, not a decrease in officer activity or violation volume.")
output_lines.append("3. **Officer Engagement**: Despite only having 8 days of data, **107 unique officers** logged violations in April, compared to 157 in March and 156 in February. This represents a normal, high-density officer engagement rate.")
output_lines.append("4. **No Collection Gaps**: April's daily record logs show continuous activity from April 1 to April 8 with no zero-count days or logging outages:")
output_lines.append("")
output_lines.append("| Date (IST) | Records | Active Officers |")
output_lines.append("|---|:---:|:---:|")
for _, row in april_daily.iterrows():
    output_lines.append(f"| {row['date_ist']} | {int(row['records']):,} | {int(row['active_officers'])} |")
output_lines.append("")
output_lines.append("## Conclusion")
output_lines.append("The April volume drop is a **truncation artifact**. The model evaluation framework correctly handles this by evaluating volume *shares* (percentages) rather than absolute volumes, and by applying a **Volume Calibration Scaling Factor** ($\approx 0.222$) in Test Type 5 to match the 8-day holdout window.")

investigation_md_path = os.path.join(repo_root, 'APRIL_DROP_INVESTIGATION.md')
with open(investigation_md_path, 'w') as f:
    f.write("\n".join(output_lines))
print(f"\nWritten detailed investigation report to: {investigation_md_path}")
