"""
clean_data.py
─────────────────────────────────────────────────────────────────────────────
Full data cleaning pipeline for BTP parking violation records.

Cleaning steps (in order):
  1. Parse & validate timestamps  → drop unparseable / future dates
  2. Spatial bounds check         → drop records outside Greater Bengaluru bbox
  3. Coordinate precision         → snap to 110m grid (3 d.p.)
  4. Officer quality filter       → Bayesian Beta p̂, drop p̂ < 0.50
  5. Duplicate detection          → flag (officer, location, minute) dupes
  6. PCS enrichment               → compute omega, delta, sigma, PCS, q_PCS

Output:
  cleaned_violations.csv          (repo root) — full cleaned dataset
  cleaning_report.md              (repo root) — step-by-step audit trail
─────────────────────────────────────────────────────────────────────────────
"""

import os, warnings
import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')

# ── Paths ─────────────────────────────────────────────────────────────────────
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root  = os.path.dirname(script_dir)
parent_dir = os.path.dirname(repo_root)

for candidate in [
    os.path.join(parent_dir, 'jan to may police violation_anonymized791b166.csv'),
    os.path.join(repo_root,  'jan to may police violation_anonymized791b166.csv'),
    'jan to may police violation_anonymized791b166.csv',
]:
    if os.path.exists(candidate):
        csv_path = candidate
        break

print(f"Loading raw data from: {csv_path}")
df = pd.read_csv(csv_path)
N_RAW = len(df)
print(f"Raw records: {N_RAW:,}")

report = []
report.append("# GridLock-R2 — Data Cleaning Report")
report.append(f"> Dataset: `{os.path.basename(csv_path)}`")
report.append("")
report.append(f"**Raw record count:** {N_RAW:,}")
report.append("")

# ── Step 1: Timestamp parsing & validation ────────────────────────────────────
print("\n[Step 1] Parsing timestamps …")
df['ts_utc'] = pd.to_datetime(df['created_datetime'], errors='coerce', utc=True)
df['ts_ist'] = df['ts_utc'].dt.tz_convert('Asia/Kolkata')

n_bad_ts = df['ts_ist'].isna().sum()
df = df.dropna(subset=['ts_ist']).copy()

# Drop records with future timestamps (dataset ends Apr 8 2024 — give 1-day buffer)
CUTOFF = pd.Timestamp('2024-04-10', tz='Asia/Kolkata')
n_future = (df['ts_ist'] > CUTOFF).sum()
df = df[df['ts_ist'] <= CUTOFF].copy()

df['hour']   = df['ts_ist'].dt.hour
df['dow']    = df['ts_ist'].dt.dayofweek
df['month']  = df['ts_ist'].dt.month
df['date']   = df['ts_ist'].dt.date

step1_dropped = n_bad_ts + n_future
print(f"  Unparseable timestamps : {n_bad_ts:,}")
print(f"  Future timestamps      : {n_future:,}")
print(f"  Remaining              : {len(df):,}")

report.append("## Step 1 — Timestamp Validation")
report.append(f"| Check | Dropped |")
report.append(f"|---|---|")
report.append(f"| Unparseable `created_datetime` | {n_bad_ts:,} |")
report.append(f"| Future timestamps (> Apr 10 2024) | {n_future:,} |")
report.append(f"| **Remaining** | **{len(df):,}** |")
report.append("")

# ── Step 2: Spatial bounds check ──────────────────────────────────────────────
print("[Step 2] Spatial bounds check (Greater Bengaluru bbox) …")

# Strict Greater Bengaluru bounding box
LAT_MIN, LAT_MAX = 12.70, 13.35
LON_MIN, LON_MAX = 77.35, 77.85

n_before = len(df)
df = df[
    df['latitude'].between(LAT_MIN, LAT_MAX) &
    df['longitude'].between(LON_MIN, LON_MAX)
].copy()
n_oob = n_before - len(df)

print(f"  Out-of-bounds coords   : {n_oob:,}")
print(f"  Remaining              : {len(df):,}")

report.append("## Step 2 — Spatial Bounds")
report.append(f"Bounding box: lat [{LAT_MIN}, {LAT_MAX}] × lon [{LON_MIN}, {LON_MAX}]")
report.append(f"")
report.append(f"| Check | Dropped |")
report.append(f"|---|---|")
report.append(f"| Out-of-bounds coordinates | {n_oob:,} |")
report.append(f"| **Remaining** | **{len(df):,}** |")
report.append("")

# ── Step 3: Grid snapping ─────────────────────────────────────────────────────
print("[Step 3] Snapping to 110m grid (3 d.p.) …")
df['lat_g']   = df['latitude'].round(3)
df['lon_g']   = df['longitude'].round(3)
df['grid_id'] = df.apply(lambda r: f"({r['lat_g']:.3f}, {r['lon_g']:.3f})", axis=1)

n_cells = df['grid_id'].nunique()
print(f"  Unique 110m grid cells : {n_cells:,}")

report.append("## Step 3 — Grid Snapping (110m Resolution)")
report.append(f"- Coordinates rounded to 3 decimal places (~110m cell size)")
report.append(f"- **Unique grid cells:** {n_cells:,}")
report.append("")

# ── Step 4: Officer quality filter (Bayesian Beta p̂) ──────────────────────────
print("[Step 4] Computing officer quality scores (Bayesian Beta) …")

reviewed = df[df['validation_status'].isin(['approved', 'rejected'])].copy()
officer_stats = (
    reviewed.groupby('created_by_id')['validation_status']
    .value_counts().unstack(fill_value=0)
)
for col in ['approved', 'rejected']:
    if col not in officer_stats.columns:
        officer_stats[col] = 0

# Bayesian Beta(5, 2) prior → conservative shrinkage toward 0.714
officer_stats['A_o']   = officer_stats['approved']
officer_stats['R_o']   = officer_stats['rejected']
officer_stats['total'] = officer_stats['A_o'] + officer_stats['R_o']
officer_stats['p_hat'] = (5 + officer_stats['A_o']) / (7 + officer_stats['total'])

p_hat_dict = officer_stats['p_hat'].to_dict()
DEFAULT_P  = 5 / 7   # prior mean for unreviewed officers

df['p_hat'] = df['created_by_id'].map(p_hat_dict).fillna(DEFAULT_P)

# Tier assignment
df['officer_tier'] = pd.cut(
    df['p_hat'],
    bins=[0, 0.50, 0.70, 1.01],
    labels=['🔴 Corrupt', '🟡 Soft-weight', '🟢 Reliable'],
    right=False
)

n_officers_total   = df['created_by_id'].nunique()
n_corrupt_officers = officer_stats[officer_stats['p_hat'] < 0.50].shape[0]
n_corrupt_records  = (df['p_hat'] < 0.50).sum()

print(f"  Officers analysed      : {n_officers_total:,}")
print(f"  Corrupt officers (p̂<0.5): {n_corrupt_officers:,}")
print(f"  Corrupt records        : {n_corrupt_records:,}")

# Worst offenders
worst = officer_stats.nsmallest(10, 'p_hat')[['A_o', 'R_o', 'total', 'p_hat']].copy()

# Apply filter
df_clean = df[df['p_hat'] >= 0.50].copy()
print(f"  Records after filter   : {len(df_clean):,}  (removed {n_corrupt_records:,})")

report.append("## Step 4 — Officer Quality Filter (Bayesian Beta p̂)")
report.append(f"Prior: Beta(5, 2) → default p̂ = {DEFAULT_P:.3f} for unreviewed officers")
report.append(f"Threshold: p̂ ≥ 0.50 to keep a record")
report.append("")
report.append(f"| Metric | Value |")
report.append(f"|---|---|")
report.append(f"| Total officers | {n_officers_total:,} |")
report.append(f"| Officers with p̂ < 0.50 | {n_corrupt_officers:,} |")
report.append(f"| Records from corrupt officers | {n_corrupt_records:,} |")
report.append(f"| Records kept (p̂ ≥ 0.50) | {len(df_clean):,} |")
report.append("")
report.append("### Worst 10 Officers by p̂")
report.append("| Officer | Approved | Rejected | Total | p̂ |")
report.append("|---|---|---|---|---|")
for oid, row in worst.iterrows():
    report.append(f"| {oid} | {int(row['A_o'])} | {int(row['R_o'])} | {int(row['total'])} | {row['p_hat']:.4f} |")
report.append("")

# ── Step 5: Duplicate detection ───────────────────────────────────────────────
print("[Step 5] Detecting duplicates (same officer + cell + minute) …")
df_clean['ts_minute'] = df_clean['ts_ist'].dt.floor('min')
dup_mask = df_clean.duplicated(
    subset=['created_by_id', 'grid_id', 'ts_minute'], keep='first'
)
n_dupes = dup_mask.sum()
df_clean = df_clean[~dup_mask].copy()

print(f"  Exact duplicates       : {n_dupes:,}")
print(f"  Remaining              : {len(df_clean):,}")

report.append("## Step 5 — Duplicate Detection")
report.append(f"Key: `(officer_id, grid_cell, timestamp_floor_1min)`")
report.append(f"")
report.append(f"| Check | Count |")
report.append(f"|---|---|")
report.append(f"| Exact duplicates removed | {n_dupes:,} |")
report.append(f"| **Final clean records** | **{len(df_clean):,}** |")
report.append("")

# ── Step 6: PCS enrichment ────────────────────────────────────────────────────
print("[Step 6] Computing PCS scores …")

PCU = {
    'SCOOTER':0.5,'MOPED':0.5,'MOTOR CYCLE':0.5,'MOTORCYCLE':0.5,'TWO WHEELER':0.5,
    'CAR':1.0,'JEEP':1.0,'AUTO':1.0,'PASSENGER AUTO':1.0,'AUTO RICKSHAW':1.0,
    'MAXI-CAB':1.5,'MAXI CAB':1.5,'LGV':1.5,'TEMPO':1.5,'VAN':1.5,'GOODS AUTO':1.5,
    'BUS':3.0,'BMTC':3.0,'PRIVATE BUS':3.0,'LORRY':3.0,'HGV':3.0,
    'TANKER':3.0,'TRUCK':3.0,'TRACTOR':3.0,
}
SIGMA = {
    'DOUBLE PARKING':2.0,'ROAD CROSSING':1.8,'NEAR JUNCTION':1.8,
    'MAIN ROAD':1.6,'BUS STOP':1.4,'ZEBRA':1.4,
    'FOOTPATH':1.2,'WRONG PARKING':1.0,'NO PARKING':1.0,
}

def get_pcu(v):
    v = str(v).upper().strip()
    for k, w in PCU.items():
        if k in v: return w
    return 1.0

def get_sigma(v):
    v = str(v).upper()
    for k, s in SIGMA.items():
        if k in v: return s
    return 1.0

def get_delta(h):
    if pd.isna(h): return 1.0
    h = int(h)
    if 8 <= h < 12 or 17 <= h < 20: return 1.5
    elif 12 <= h < 17:               return 1.2
    return 0.8

df_clean['omega'] = df_clean['vehicle_type'].fillna('UNKNOWN').apply(get_pcu)
df_clean['sigma'] = df_clean['violation_type'].fillna('').astype(str).apply(get_sigma)
df_clean['delta'] = df_clean['hour'].apply(get_delta)
df_clean['PCS']   = df_clean['omega'] * df_clean['delta'] * df_clean['sigma']
df_clean['q_PCS'] = df_clean['PCS'] * df_clean['p_hat']

print(f"  PCS mean (clean)       : {df_clean['PCS'].mean():.4f}")
print(f"  PCS max                : {df_clean['PCS'].max():.2f}")

report.append("## Step 6 — PCS Enrichment")
report.append("Formula: `PCS = ω (PCU weight) × δ (hour multiplier) × σ (violation severity)`")
report.append("")
report.append(f"| Metric | Value |")
report.append(f"|---|---|")
report.append(f"| Mean PCS (clean dataset) | {df_clean['PCS'].mean():.4f} |")
report.append(f"| Max PCS | {df_clean['PCS'].max():.2f} |")
report.append(f"| Total PCS sum | {df_clean['PCS'].sum():,.1f} |")
report.append(f"| Mean q\\_PCS (quality-adjusted) | {df_clean['q_PCS'].mean():.4f} |")
report.append("")

# ── Summary ───────────────────────────────────────────────────────────────────
N_CLEAN = len(df_clean)
n_dropped_total = N_RAW - N_CLEAN
pct_dropped = n_dropped_total / N_RAW * 100

print(f"\n{'─'*55}")
print(f"CLEANING SUMMARY")
print(f"{'─'*55}")
print(f"  Raw records            : {N_RAW:>10,}")
print(f"  Bad timestamps         : {step1_dropped:>10,}  ({step1_dropped/N_RAW*100:.1f}%)")
print(f"  Out-of-bounds coords   : {n_oob:>10,}  ({n_oob/N_RAW*100:.1f}%)")
print(f"  Corrupt officer records: {n_corrupt_records:>10,}  ({n_corrupt_records/N_RAW*100:.1f}%)")
print(f"  Exact duplicates       : {n_dupes:>10,}  ({n_dupes/N_RAW*100:.1f}%)")
print(f"  ─────────────────────────────")
print(f"  Total dropped          : {n_dropped_total:>10,}  ({pct_dropped:.1f}%)")
print(f"  CLEAN records          : {N_CLEAN:>10,}  ({100-pct_dropped:.1f}%)")
print(f"{'─'*55}")

report.append("## Cleaning Summary")
report.append(f"| Step | Records Dropped | % of Raw |")
report.append(f"|---|---|---|")
report.append(f"| Bad timestamps | {step1_dropped:,} | {step1_dropped/N_RAW*100:.2f}% |")
report.append(f"| Out-of-bounds coordinates | {n_oob:,} | {n_oob/N_RAW*100:.2f}% |")
report.append(f"| Corrupt officer records (p̂ < 0.50) | {n_corrupt_records:,} | {n_corrupt_records/N_RAW*100:.2f}% |")
report.append(f"| Exact duplicates | {n_dupes:,} | {n_dupes/N_RAW*100:.2f}% |")
report.append(f"| **Total dropped** | **{n_dropped_total:,}** | **{pct_dropped:.2f}%** |")
report.append(f"| **✅ Clean records** | **{N_CLEAN:,}** | **{100-pct_dropped:.2f}%** |")
report.append("")
report.append("## Output Files")
report.append("- `cleaned_violations.csv` — full cleaned & enriched dataset")
report.append("- `cleaning_report.md` — this report")

# ── Save outputs ──────────────────────────────────────────────────────────────
out_csv = os.path.join(repo_root, 'cleaned_violations.csv')
out_md  = os.path.join(repo_root, 'cleaning_report.md')

print(f"\nSaving cleaned CSV → {out_csv}")
df_clean.to_csv(out_csv, index=False)

with open(out_md, 'w') as f:
    f.write('\n'.join(report))
print(f"Saving cleaning report → {out_md}")

print("\n✅  Done. Re-run plot_violations_vs_impact.py to regenerate heatmap on clean data.")
