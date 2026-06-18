import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

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

# Split train / holdout
train_df = df[df['month'].isin([11, 12, 1, 2])].copy()
holdout_df = df[df['month'] == 4].copy()

# Fit Poisson model on train data
train_grouped = train_df.groupby(['grid_id', 'month', 'hour', 'day_type']).agg(
    y=('id', 'count'),
    PCS_sum=('PCS', 'sum')
).reset_index()

pcs_by_month = train_df.groupby(['grid_id', 'month', 'hour', 'day_type'])['PCS'].sum().reset_index(name='PCS_month')
pcs_shifted = pcs_by_month.copy()
pcs_shifted['month'] = pcs_shifted['month'].map({11: 12, 12: 1, 1: 2})
pcs_shifted = pcs_shifted.rename(columns={'PCS_month': 'Z_prev'}).dropna(subset=['month'])

train_grouped_lagged = train_grouped.merge(pcs_shifted[['grid_id', 'month', 'hour', 'day_type', 'Z_prev']], on=['grid_id', 'month', 'hour', 'day_type'], how='left').fillna({'Z_prev': 0})

poisson_model = smf.glm('y ~ C(month) + hour + day_type + np.log(Z_prev + 1)', data=train_grouped_lagged, family=sm.families.Poisson()).fit()
coefs = poisson_model.params.to_dict()
Intercept = coefs['Intercept']
hour_coef = coefs['hour']
day_type_coef = coefs['day_type']
log_Z_coef = coefs['np.log(Z_prev + 1)']

# Persistence Index
monthly_top50 = {}
for m in [12, 1, 2]:
    mdf = train_df[train_df['month'] == m]
    m_zi = mdf.groupby('grid_id')['q_PCS'].sum().reset_index()
    top50 = m_zi.nlargest(50, 'q_PCS')['grid_id'].tolist()
    monthly_top50[m] = set(top50)

def get_pi(grid):
    return sum(1 for m in [12, 1, 2] if grid in monthly_top50[m]) / 3.0

Zi = train_df.groupby('grid_id').agg(
    quality_adjusted_Z=('q_PCS', 'sum'),
    raw_count_train=('id', 'count')
).reset_index()
Zi['PI'] = Zi['grid_id'].apply(get_pi)

# Actual April counts
april_actual = holdout_df.groupby('grid_id').size().reset_index(name='april_actual_count')
top20_actual = set(april_actual.nlargest(20, 'april_actual_count')['grid_id'].tolist())

# Predict Case A (Training Average Monthly PCS)
unique_grids = Zi['grid_id'].tolist()
hours = list(range(24))
day_types = [0, 1, 2]
day_weights = {0: 5, 1: 1, 2: 1}

grid_combos = pd.MultiIndex.from_product(
    [unique_grids, hours, day_types],
    names=['grid_id', 'hour', 'day_type']
).to_frame().reset_index(drop=True)

train_groups = train_df.groupby(['grid_id', 'hour', 'day_type'])['PCS'].sum().reset_index(name='PCS_sum')
combos_a = grid_combos.merge(train_groups, on=['grid_id', 'hour', 'day_type'], how='left').fillna({'PCS_sum': 0})
combos_a['Z_prev'] = combos_a['PCS_sum'] / 4.0

combos_a['log_lambda'] = Intercept + combos_a['hour'] * hour_coef + combos_a['day_type'] * day_type_coef + np.log(combos_a['Z_prev'] + 1) * log_Z_coef
combos_a['pred_lambda'] = np.exp(combos_a['log_lambda'])
combos_a['weighted_pred'] = combos_a['pred_lambda'] * combos_a['day_type'].map(day_weights)
weekly_vol_a = combos_a.groupby('grid_id')['weighted_pred'].sum().reset_index(name='pred_weekly_volume')

eval_df_a = Zi.merge(weekly_vol_a, on='grid_id')
eval_df_a['EPS_v1'] = eval_df_a['PI'] * eval_df_a['pred_weekly_volume']

# Predict Case B (Actual March PCS)
march_df = df[df['month'] == 3].copy()
march_groups = march_df.groupby(['grid_id', 'hour', 'day_type'])['PCS'].sum().reset_index(name='PCS_march')
combos_b = grid_combos.merge(march_groups, on=['grid_id', 'hour', 'day_type'], how='left').fillna({'PCS_march': 0})
combos_b['Z_prev'] = combos_b['PCS_march']

combos_b['log_lambda'] = Intercept + combos_b['hour'] * hour_coef + combos_b['day_type'] * day_type_coef + np.log(combos_b['Z_prev'] + 1) * log_Z_coef
combos_b['pred_lambda'] = np.exp(combos_b['log_lambda'])
combos_b['weighted_pred'] = combos_b['pred_lambda'] * combos_b['day_type'].map(day_weights)
weekly_vol_b = combos_b.groupby('grid_id')['weighted_pred'].sum().reset_index(name='pred_weekly_volume')

eval_df_b = Zi.merge(weekly_vol_b, on='grid_id')
eval_df_b['EPS_v1'] = eval_df_b['PI'] * eval_df_b['pred_weekly_volume']

# Output helper functions
def print_detailed_top20(eval_df, label):
    top20 = eval_df.nlargest(20, 'EPS_v1').copy()
    actuals = []
    for g in top20['grid_id']:
        act = holdout_df[holdout_df['grid_id'] == g].shape[0]
        actuals.append(act)
    top20['april_actual'] = actuals
    top20['in_top20_actual'] = top20['grid_id'].apply(lambda x: "Yes" if x in top20_actual else "No")
    print(f"\n--- DETAILED TOP 20 FOR {label} ---")
    print(top20[['grid_id', 'PI', 'pred_weekly_volume', 'EPS_v1', 'april_actual', 'in_top20_actual']].to_string(index=False))

print_detailed_top20(eval_df_a, "CASE A (TRAINING AVERAGE MONTHLY PCS)")
print_detailed_top20(eval_df_b, "CASE B (ACTUAL MARCH PCS)")
