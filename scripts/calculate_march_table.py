import pandas as pd
import numpy as np
import json

# Load data
df = pd.read_csv('jan to may police violation_anonymized791b166.csv')

# Preprocessing
df['ts'] = pd.to_datetime(df['created_datetime'], errors='coerce', utc=True)
df['ts_ist'] = df['ts'].dt.tz_convert('Asia/Kolkata')
df['hour'] = df['ts_ist'].dt.hour
df['dow_num'] = df['ts_ist'].dt.dayofweek
df['month'] = df['ts_ist'].dt.month
df['day_type'] = df['dow_num'].apply(lambda x: 2 if x==6 else (1 if x==5 else 0))

df['lat_g'] = df['latitude'].round(3)
df['lon_g'] = df['longitude'].round(3)
df['grid_id'] = df.apply(lambda r: f"({r['lat_g']:.3f}, {r['lon_g']:.3f})", axis=1)

# Vehicle type normalization
PCU = {
    'SCOOTER': 0.5, 'MOPED': 0.5, 'MOTOR CYCLE': 0.5, 'MOTORCYCLE': 0.5, 'TWO WHEELER': 0.5,
    'CAR': 1.0, 'JEEP': 1.0, 'AUTO': 1.0, 'PASSENGER AUTO': 1.0, 'AUTO RICKSHAW': 1.0,
    'MAXI-CAB': 1.5, 'MAXI CAB': 1.5, 'LGV': 1.5, 'TEMPO': 1.5, 'VAN': 1.5, 'GOODS AUTO': 1.5,
    'BUS': 3.0, 'BMTC': 3.0, 'PRIVATE BUS': 3.0, 'LORRY': 3.0, 'HGV': 3.0,
    'TANKER': 3.0, 'TRUCK': 3.0, 'TRACTOR': 3.0,
}

def get_pcu(vtype):
    v = str(vtype).upper().strip()
    for k, w in PCU.items():
        if k in v:
            return w
    return 1.0

df['omega'] = df['vehicle_type'].fillna('UNKNOWN').apply(get_pcu)

def get_delta(hour):
    if pd.isna(hour): return 1.0
    h = int(hour)
    if 8 <= h < 12 or 17 <= h < 20:  return 1.5
    elif 12 <= h < 17:                return 1.2
    else:                             return 0.8

df['delta'] = df['hour'].apply(get_delta)

SIGMA_MAP = {
    'DOUBLE PARKING': 2.0,
    'ROAD CROSSING': 1.8,
    'NEAR JUNCTION': 1.8,
    'MAIN ROAD': 1.6,
    'BUS STOP': 1.4,
    'ZEBRA': 1.4,
    'FOOTPATH': 1.2,
    'WRONG PARKING': 1.0,
    'NO PARKING': 1.0,
}

def get_sigma(viol_raw):
    v = str(viol_raw).upper()
    for k, s in SIGMA_MAP.items():
        if k in v:
            return s
    return 1.0

df['sigma'] = df['violation_type'].fillna('').astype(str).apply(get_sigma)
df['PCS'] = df['omega'] * df['delta'] * df['sigma']

# ─────────────────────────────────────────────────────────────────────────────
# M6 OFFICER QUALITY SCORE
# ─────────────────────────────────────────────────────────────────────────────
officer_stats = df[df['validation_status'].isin(['approved', 'rejected'])].groupby('created_by_id')['validation_status'].value_counts().unstack(fill_value=0)
if 'approved' not in officer_stats.columns:
    officer_stats['approved'] = 0
if 'rejected' not in officer_stats.columns:
    officer_stats['rejected'] = 0

officer_stats['A_o'] = officer_stats['approved']
officer_stats['R_o'] = officer_stats['rejected']
officer_stats['p_hat'] = (5 + officer_stats['A_o']) / (7 + officer_stats['A_o'] + officer_stats['R_o'])

# Map p_hat to main dataframe
p_hat_dict = officer_stats['p_hat'].to_dict()
df['p_hat'] = df['created_by_id'].map(p_hat_dict).fillna(5/7)

# Filter for March 2024
march_df = df[df['month'] == 3].copy()
print(f"March 2024 records: {len(march_df):,}")

# ─────────────────────────────────────────────────────────────────────────────
# POISSON MODEL PREDICTIONS FOR MARCH
# ─────────────────────────────────────────────────────────────────────────────
# Group March data by grid cell, hour, day_type
march_groups = march_df.groupby(['grid_id', 'hour', 'day_type']).agg(
    count=('PCS', 'count'),
    Z_prev=('PCS', 'sum')
).reset_index()

# Coefficients
Intercept = 1.3897
month_coef = -0.1536
hour_coef = -0.0047
day_type_coef = -0.1148
Z_prev_coef = 0.0243

# Calculate prediction for each group
march_groups['log_pred'] = (
    Intercept +
    month_coef +
    march_groups['hour'] * hour_coef +
    march_groups['day_type'] * day_type_coef +
    march_groups['Z_prev'] * Z_prev_coef
)
march_groups['pred'] = np.exp(march_groups['log_pred'])

# Sum predictions at grid level to get predicted March volume
predicted_volume = march_groups.groupby('grid_id')['pred'].sum().reset_index(name='predicted_march_volume')

# ─────────────────────────────────────────────────────────────────────────────
# HOURLY DISTRIBUTION (TOP 3 PEAK HOURS FOR EACH GRID)
# ─────────────────────────────────────────────────────────────────────────────
grid_hourly = march_df.groupby(['grid_id', 'hour']).size().reset_index(name='count')

def get_top_3_hours(group):
    top_h = group.nlargest(3, 'count')['hour'].tolist()
    top_h_str = [f"{int(h):02d}:00" for h in top_h]
    while len(top_h_str) < 3:
        top_h_str.append("N/A")
    return ", ".join(top_h_str)

top_hours = grid_hourly.groupby('grid_id', group_keys=False).apply(get_top_3_hours).reset_index(name='top_3_peak_hours')

# ─────────────────────────────────────────────────────────────────────────────
# M6 OFFICER CLASSIFICATION COUNTS FOR MARCH
# ─────────────────────────────────────────────────────────────────────────────
march_df['mandatory_review'] = march_df['p_hat'] < 0.50
march_df['soft_weight'] = (march_df['p_hat'] >= 0.50) & (march_df['p_hat'] <= 0.85)

m6_counts = march_df.groupby('grid_id').agg(
    mandatory_reviews_pending=('mandatory_review', 'sum'),
    soft_weight_records=('soft_weight', 'sum')
).reset_index()

# ─────────────────────────────────────────────────────────────────────────────
# MERGE AND OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
master_table = predicted_volume.merge(top_hours, on='grid_id')
master_table = master_table.merge(m6_counts, on='grid_id')

# Sort by predicted_march_volume descending
top_10 = master_table.nlargest(10, 'predicted_march_volume')

print("\nTop 10 Grids in March 2024:")
print(top_10.to_string(index=False))
