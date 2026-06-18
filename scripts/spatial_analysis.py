import pandas as pd
import numpy as np
import libpysal as lps
from esda.moran import Moran, Moran_Local
import warnings
warnings.filterwarnings('ignore')

# Load data
print("Loading data...")
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

p_hat_dict = officer_stats['p_hat'].to_dict()
df['p_hat'] = df['created_by_id'].map(p_hat_dict).fillna(5/7)

# Quality weighting rules:
# - p_hat >= 0.85: weight = 1.0 (direct calculation)
# - 0.50 <= p_hat < 0.85: weight = p_hat (soft weighted)
# - p_hat < 0.50: weight = 0.0 (excluded)
def get_quality_weight(p):
    if p >= 0.85:
        return 1.0
    elif p >= 0.50:
        return p
    else:
        return 0.0

df['q_weight'] = df['p_hat'].apply(get_quality_weight)
df['q_PCS'] = df['PCS'] * df['q_weight']

# Test under two definitions of the TRAIN period:
# Definition 1: month in [11, 12, 1, 2]
# Definition 2: month != 3 (which is [11, 12, 1, 2, 4])

for def_name, mask in [("Nov-Feb", df['month'].isin([11, 12, 1, 2])), ("All-except-March", df['month'] != 3)]:
    print(f"\n=== Running Moran's I on {def_name} Period ===")
    train_df = df[mask].copy()
    print(f"Number of records: {len(train_df):,}")
    
    # Aggregate Z_i at grid cell level
    Zi = train_df.groupby(['lat_g', 'lon_g']).agg(
        Z_i=('q_PCS', 'sum'),
        raw_count=('q_PCS', 'count')
    ).reset_index()
    
    # We analyze cells that have at least some activity or is it all cells?
    # In full_analysis.py, they used: Zi_sub = Zi[Zi['raw_count'] >= 5]
    # Let's test with no raw count threshold first, then with raw_count >= 5.
    for min_cnt in [0, 5]:
        print(f"\n--- Min count threshold: {min_cnt} ---")
        Zi_sub = Zi[Zi['raw_count'] >= min_cnt].copy().reset_index(drop=True)
        n_cells = len(Zi_sub)
        print(f"Cells analyzed: {n_cells}")
        if n_cells < 10:
            continue
            
        coords = np.column_stack((Zi_sub['lat_g'], Zi_sub['lon_g']))
        
        # Build spatial weights (k=8 KNN)
        w = lps.weights.KNN.from_array(coords, k=8)
        w.transform = 'r'
        
        # Global Moran's I
        mi = Moran(Zi_sub['Z_i'].values, w, permutations=999)
        print(f"Global Moran's I: {mi.I:.4f}")
        print(f"Expected Moran's I: {mi.EI:.4f}")
        print(f"Z-score: {mi.z_sim:.4f}")
        print(f"p-value: {mi.p_sim:.4f}")
        
        # Local Moran's I
        lisa = Moran_Local(Zi_sub['Z_i'].values, w, permutations=999)
        
        # Classify cells:
        # q = 1: HH, 2: LH, 3: LL, 4: HL
        # Significance threshold p < 0.05
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
        print("LISA Counts:")
        print(Zi_sub['lisa_label'].value_counts())
        
        # Top 5 HH cells by Z_i
        print("Top 5 HH cells:")
        print(Zi_sub[Zi_sub['lisa_label'] == 'HH'].nlargest(5, 'Z_i')[['lat_g', 'lon_g', 'Z_i']])
