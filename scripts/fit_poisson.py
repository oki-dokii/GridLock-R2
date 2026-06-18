import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

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

# Let's group by (grid_id, month, hour, day_type) to get counts for all months
all_grouped = df.groupby(['grid_id', 'month', 'hour', 'day_type']).agg(
    y=('id', 'count'),
    PCS_sum=('PCS', 'sum')
).reset_index()

# Define Z_prev as prior month's PCS sum
pcs_by_month = df.groupby(['grid_id', 'month', 'hour', 'day_type'])['PCS'].sum().reset_index(name='PCS_month')
pcs_shifted = pcs_by_month.copy()
# Shift month forward
month_forward_map = {11: 12, 12: 1, 1: 2, 2: 3, 3: 4}
pcs_shifted['month'] = pcs_shifted['month'].map(month_forward_map)
pcs_shifted = pcs_shifted.rename(columns={'PCS_month': 'Z_prev'}).dropna(subset=['month'])

all_grouped_lagged = all_grouped.merge(pcs_shifted[['grid_id', 'month', 'hour', 'day_type', 'Z_prev']], on=['grid_id', 'month', 'hour', 'day_type'], how='left').fillna({'Z_prev': 0})

# Fit model on all months
model_orig = smf.glm('y ~ C(month) + hour + day_type + Z_prev', data=all_grouped_lagged, family=sm.families.Poisson()).fit()
print("\n--- ORIGINAL RE-FIT ---")
print(model_orig.summary())
