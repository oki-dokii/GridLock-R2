import pandas as pd
import numpy as np
import libpysal as lps
from esda.moran import Moran, Moran_Local
import warnings
warnings.filterwarnings('ignore')

# Load data
df = pd.read_csv('jan to may police violation_anonymized791b166.csv')

# Preprocessing
df['ts'] = pd.to_datetime(df['created_datetime'], errors='coerce', utc=True)
df['ts_ist'] = df['ts'].dt.tz_convert('Asia/Kolkata')
df['hour'] = df['ts_ist'].dt.hour
df['dow_num'] = df['ts_ist'].dt.dayofweek
df['month'] = df['ts_ist'].dt.month
df['lat_g'] = df['latitude'].round(3)
df['lon_g'] = df['longitude'].round(3)

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

# M6 Officer Quality
officer_stats = df[df['validation_status'].isin(['approved', 'rejected'])].groupby('created_by_id')['validation_status'].value_counts().unstack(fill_value=0)
if 'approved' not in officer_stats.columns:
    officer_stats['approved'] = 0
if 'rejected' not in officer_stats.columns:
    officer_stats['rejected'] = 0
officer_stats['p_hat'] = (5 + officer_stats['approved']) / (7 + officer_stats['approved'] + officer_stats['rejected'])
p_hat_dict = officer_stats['p_hat'].to_dict()
df['p_hat'] = df['created_by_id'].map(p_hat_dict).fillna(5/7)

def get_quality_weight(p):
    if p >= 0.85:
        return 1.0
    elif p >= 0.50:
        return p
    else:
        return 0.0

df['q_weight'] = df['p_hat'].apply(get_quality_weight)
df['q_PCS'] = df['PCS'] * df['q_weight']

# Run the 4 configurations
configs = [
    ("Nov-Feb (All Cells)", df['month'].isin([11, 12, 1, 2]), 0),
    ("Nov-Feb (Count >= 5)", df['month'].isin([11, 12, 1, 2]), 5),
    ("All-except-March (All Cells)", df['month'] != 3, 0),
    ("All-except-March (Count >= 5)", df['month'] != 3, 5),
]

for name, mask, threshold in configs:
    train_df = df[mask].copy()
    
    # Group by grid cell coordinates to compute quality-weighted Z_i
    Zi = train_df.groupby(['lat_g', 'lon_g']).agg(
        Z_i=('q_PCS', 'sum'),
        raw_count=('q_PCS', 'count')
    ).reset_index()
    
    # Rename coordinates to grid_lat, grid_lon
    Zi.rename(columns={'lat_g': 'grid_lat', 'lon_g': 'grid_lon'}, inplace=True)
    
    Zi_sub = Zi[Zi['raw_count'] >= threshold].copy().reset_index(drop=True)
    
    coords = np.column_stack((Zi_sub['grid_lat'], Zi_sub['grid_lon']))
    w = lps.weights.KNN.from_array(coords, k=8)
    w.transform = 'r'
    
    mi = Moran(Zi_sub['Z_i'].values, w, permutations=999)
    lisa = Moran_Local(Zi_sub['Z_i'].values, w, permutations=999)
    
    # Classify
    labels = []
    for i in range(len(Zi_sub)):
        p_val = lisa.p_sim[i]
        q = lisa.q[i]
        if p_val < 0.05:
            if q == 1:
                labels.append("HH")
            elif q == 2:
                labels.append("LH")
            elif q == 3:
                labels.append("LL")
            elif q == 4:
                labels.append("HL")
        else:
            labels.append("not significant")
            
    Zi_sub['lisa_label'] = labels
    counts = Zi_sub['lisa_label'].value_counts()
    
    print(f"\nConfiguration: {name}")
    print(f"Global Moran's I: {mi.I:.6f}")
    print(f"EI: {mi.EI:.6f}, Z-score: {mi.z_sim:.6f}, p-value: {mi.p_sim:.6f}")
    print("Quadrant Counts:")
    for cat in ["HH", "HL", "LH", "LL", "not significant"]:
        print(f"  {cat}: {counts.get(cat, 0)}")
    
    print("Top 15 HH cells:")
    top15 = Zi_sub[Zi_sub['lisa_label'] == 'HH'].nlargest(15, 'Z_i')
    print(top15[['grid_lat', 'grid_lon', 'Z_i', 'raw_count']].to_string(index=False))
