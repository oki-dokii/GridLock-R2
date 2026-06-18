import pandas as pd
import numpy as np

# Load data
print("Loading data...")
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

# PCU weights
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

# M6 Officer quality
officer_stats = df[df['validation_status'].isin(['approved', 'rejected'])].groupby('created_by_id')['validation_status'].value_counts().unstack(fill_value=0)
if 'approved' not in officer_stats.columns:
    officer_stats['approved'] = 0
if 'rejected' not in officer_stats.columns:
    officer_stats['rejected'] = 0
officer_stats['A_o'] = officer_stats['approved']
officer_stats['R_o'] = officer_stats['rejected']
officer_stats['p_hat'] = (5 + officer_stats['A_o']) / (7 + officer_stats['A_o'] + officer_stats['R_o'])

p_hat_dict = officer_stats['p_hat'].to_dict()
df['p_hat'] = df['created_by_id'].map(p_hat_dict).fillna(5/7)
df['q_PCS'] = df['PCS'] * df['p_hat']

# Train / Holdout Split
train_df = df[df['month'].isin([11, 12, 1, 2])].copy()
holdout_df = df[df['month'] == 4].copy()

# Zi
Zi = train_df.groupby('grid_id').agg(
    quality_adjusted_Z=('q_PCS', 'sum'),
    raw_count_train=('id', 'count')
).reset_index()

# PI
monthly_top50 = {}
for m in [12, 1, 2]:
    mdf = train_df[train_df['month'] == m]
    m_zi = mdf.groupby('grid_id')['q_PCS'].sum().reset_index()
    top50 = m_zi.nlargest(50, 'q_PCS')['grid_id'].tolist()
    monthly_top50[m] = set(top50)

def get_pi(grid):
    return sum(1 for m in [12, 1, 2] if grid in monthly_top50[m]) / 3.0

Zi['PI'] = Zi['grid_id'].apply(get_pi)

# predicted_weekly_volume
Intercept = 1.3897
month_coef = -0.1536
hour_coef = -0.0047
day_type_coef = -0.1148
Z_prev_coef = 0.0243

train_groups = train_df.groupby(['grid_id', 'hour', 'day_type'])['PCS'].sum().reset_index(name='PCS_sum')

unique_grids = Zi['grid_id'].tolist()
hours = list(range(24))
day_types = [0, 1, 2]
day_weights = {0: 5, 1: 1, 2: 1}

grid_combos = pd.MultiIndex.from_product(
    [unique_grids, hours, day_types],
    names=['grid_id', 'hour', 'day_type']
).to_frame().reset_index(drop=True)

grid_combos = grid_combos.merge(train_groups, on=['grid_id', 'hour', 'day_type'], how='left').fillna({'PCS_sum': 0})
grid_combos['Z_prev'] = grid_combos['PCS_sum'] / 4.0

grid_combos['log_lambda'] = (
    Intercept +
    month_coef +
    grid_combos['hour'] * hour_coef +
    grid_combos['day_type'] * day_type_coef +
    grid_combos['Z_prev'] * Z_prev_coef
)
grid_combos['pred_lambda'] = np.exp(grid_combos['log_lambda'])
grid_combos['weighted_pred'] = grid_combos['pred_lambda'] * grid_combos['day_type'].map(day_weights)

weekly_vol = grid_combos.groupby('grid_id')['weighted_pred'].sum().reset_index(name='pred_weekly_volume')
Zi = Zi.merge(weekly_vol, on='grid_id')
Zi['EPS_v1'] = Zi['quality_adjusted_Z'] * Zi['PI'] * Zi['pred_weekly_volume']

# Holdout evaluation
april_actual = holdout_df.groupby('grid_id').size().reset_index(name='april_actual_count')
total_april = len(holdout_df)

top20_actual_df = april_actual.nlargest(20, 'april_actual_count')
top20_actual = top20_actual_df['grid_id'].tolist()

print(f"Total April city-wide violations: {total_april}")
print("\n--- TOP 20 ACTUAL APRIL CELLS ---")
print(top20_actual_df.to_string(index=False))

# EPS_v1 top 20 evaluation
eps_top20_df = Zi.nlargest(20, 'EPS_v1')
eps_top20 = eps_top20_df['grid_id'].tolist()
eps_actual_counts = []
for g in eps_top20:
    act = holdout_df[holdout_df['grid_id'] == g].shape[0]
    eps_actual_counts.append(act)
eps_top20_df['april_actual_count'] = eps_actual_counts
eps_top20_df['in_top20_actual'] = eps_top20_df['grid_id'].apply(lambda x: "Yes" if x in top20_actual else "No")

print("\n--- EPS_v1 TOP 20 CELLS WITH APRIL ACTUALS ---")
print(eps_top20_df[['grid_id', 'quality_adjusted_Z', 'PI', 'pred_weekly_volume', 'EPS_v1', 'april_actual_count', 'in_top20_actual']].to_string(index=False))

# Baseline top 20 evaluation
base_top20_df = Zi.nlargest(20, 'raw_count_train')
base_top20 = base_top20_df['grid_id'].tolist()
base_actual_counts = []
for g in base_top20:
    act = holdout_df[holdout_df['grid_id'] == g].shape[0]
    base_actual_counts.append(act)
base_top20_df['april_actual_count'] = base_actual_counts
base_top20_df['in_top20_actual'] = base_top20_df['grid_id'].apply(lambda x: "Yes" if x in top20_actual else "No")

print("\n--- RAW BASELINE TOP 20 CELLS WITH APRIL ACTUALS ---")
print(base_top20_df[['grid_id', 'raw_count_train', 'april_actual_count', 'in_top20_actual']].to_string(index=False))
