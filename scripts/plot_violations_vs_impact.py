"""
plot_violations_vs_impact.py
─────────────────────────────────────────────────────────────────────────────
Generates a 2-panel publication figure:
  Panel 1  →  Scatter heatmap: raw violation count vs avg PCS per violation
              Points sized by Z_i (total PCS), coloured by LISA quadrant.
              Top-20 hotspot cells labelled.
  Panel 2  →  2-D hexbin density of the same space (log-log).

Output: violations_vs_impact.png  (repo root)
─────────────────────────────────────────────────────────────────────────────
"""

import os, warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

warnings.filterwarnings('ignore')

# ── Paths ─────────────────────────────────────────────────────────────────────
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root  = os.path.dirname(script_dir)

# Prefer the cleaned dataset produced by clean_data.py
cleaned_path = os.path.join(repo_root, 'cleaned_violations.csv')
if os.path.exists(cleaned_path):
    csv_path = cleaned_path
    print(f"✅  Using cleaned dataset: {csv_path}")
else:
    raise FileNotFoundError(
        "cleaned_violations.csv not found. Run scripts/clean_data.py first."
    )

print(f"Loading data from {csv_path} …")
df = pd.read_csv(csv_path)

# ── Preprocessing ─────────────────────────────────────────────────────────────
df['ts']     = pd.to_datetime(df['created_datetime'], errors='coerce', utc=True)
df['ts_ist'] = df['ts'].dt.tz_convert('Asia/Kolkata')
df['hour']   = df['ts_ist'].dt.hour
df['dow']    = df['ts_ist'].dt.dayofweek
df['month']  = df['ts_ist'].dt.month
df['lat_g']  = df['latitude'].round(3)
df['lon_g']  = df['longitude'].round(3)
df['grid_id']= df.apply(lambda r: f"({r['lat_g']:.3f}, {r['lon_g']:.3f})", axis=1)

# PCU weights
PCU = {
    'SCOOTER':0.5,'MOPED':0.5,'MOTOR CYCLE':0.5,'MOTORCYCLE':0.5,'TWO WHEELER':0.5,
    'CAR':1.0,'JEEP':1.0,'AUTO':1.0,'PASSENGER AUTO':1.0,'AUTO RICKSHAW':1.0,
    'MAXI-CAB':1.5,'MAXI CAB':1.5,'LGV':1.5,'TEMPO':1.5,'VAN':1.5,'GOODS AUTO':1.5,
    'BUS':3.0,'BMTC':3.0,'PRIVATE BUS':3.0,'LORRY':3.0,'HGV':3.0,
    'TANKER':3.0,'TRUCK':3.0,'TRACTOR':3.0,
}
def get_pcu(v):
    v = str(v).upper().strip()
    for k, w in PCU.items():
        if k in v: return w
    return 1.0

SIGMA = {
    'DOUBLE PARKING':2.0,'ROAD CROSSING':1.8,'NEAR JUNCTION':1.8,
    'MAIN ROAD':1.6,'BUS STOP':1.4,'ZEBRA':1.4,
    'FOOTPATH':1.2,'WRONG PARKING':1.0,'NO PARKING':1.0,
}
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

df['omega'] = df['vehicle_type'].fillna('UNKNOWN').apply(get_pcu)
df['sigma'] = df['violation_type'].fillna('').astype(str).apply(get_sigma)
df['delta'] = df['hour'].apply(get_delta)
df['PCS']   = df['omega'] * df['delta'] * df['sigma']

# ── Cell-level aggregation ────────────────────────────────────────────────────
print("Aggregating per grid cell …")
cell = df.groupby('grid_id').agg(
    raw_count  = ('id',  'count'),
    total_PCS  = ('PCS', 'sum'),
    avg_PCS    = ('PCS', 'mean'),
    lat        = ('lat_g', 'first'),
    lon        = ('lon_g', 'first'),
).reset_index()

# ── Nearest-station label lookup ──────────────────────────────────────────────
STATIONS = {
    'City Market':        (12.9716, 77.5946),
    'Shivajinagar':       (12.9850, 77.6010),
    'Upparpet':           (12.9720, 77.5800),
    'Malleshwaram':       (13.0035, 77.5700),
    'HAL Old Airport':    (12.9650, 77.6600),
    'KR Pura':            (13.0000, 77.6900),
    'Kodigehalli':        (13.0710, 77.5880),
    'Magadi Road':        (12.9740, 77.5510),
    'Rajajinagar':        (12.9940, 77.5560),
    'Vijayanagara':       (12.9650, 77.5270),
    'Byatarayanapura':    (13.0600, 77.5380),
    'Electronic City':    (12.8450, 77.6600),
    'HSR Layout':         (12.9116, 77.6389),
    'JP Nagar':           (12.9063, 77.5857),
    'Whitefield':         (12.9698, 77.7499),
    'Jeevanbheemanagar':  (12.9340, 77.6910),
}
def nearest_station(lat, lon):
    best, best_d = 'Unknown', 1e9
    for name, (slat, slon) in STATIONS.items():
        d = (lat - slat)**2 + (lon - slon)**2
        if d < best_d:
            best, best_d = name, d
    return best

cell['station'] = cell.apply(lambda r: nearest_station(r['lat'], r['lon']), axis=1)

# ── LISA quadrant (lightweight, no pysal dependency) ─────────────────────────
print("Computing spatial lag (LISA proxy) …")
# Use a simple spatial lag: for each cell, mean total_PCS of k=8 nearest neighbours
from scipy.spatial import cKDTree

coords = cell[['lat', 'lon']].values
tree   = cKDTree(coords)
K      = 8
_, idx = tree.query(coords, k=K+1)   # +1 because first result is self
nbr_idx = idx[:, 1:]                  # exclude self

z_scores = (cell['total_PCS'].values - cell['total_PCS'].mean()) / cell['total_PCS'].std()
spatial_lag = z_scores[nbr_idx].mean(axis=1)

def lisa_quad(zi, lag):
    if   zi > 0 and lag > 0: return 'HH'
    elif zi < 0 and lag > 0: return 'LH'
    elif zi > 0 and lag < 0: return 'HL'
    else:                     return 'LL'

cell['z_score']    = z_scores
cell['spatial_lag']= spatial_lag
cell['lisa']       = [lisa_quad(z, l) for z, l in zip(z_scores, spatial_lag)]

print(cell['lisa'].value_counts().to_string())

# ── Filter to active cells only ───────────────────────────────────────────────
active = cell[cell['raw_count'] >= 5].copy()
print(f"\nActive cells (≥5 violations): {len(active):,}  /  Total: {len(cell):,}")

# Top-20 by total_PCS for labelling
top20 = active.nlargest(20, 'total_PCS').copy()

# ── Colour map by LISA quadrant ───────────────────────────────────────────────
QUAD_COLOR = {
    'HH': '#ef4444',   # red    — priority enforcement
    'LH': '#f97316',   # orange — cascade risk
    'HL': '#eab308',   # yellow — isolated surge
    'LL': '#64748b',   # slate  — low priority
}
colors = active['lisa'].map(QUAD_COLOR).fillna('#64748b')

# Point size proportional to total_PCS (sqrt to compress range)
sizes = (np.sqrt(active['total_PCS']) / np.sqrt(active['total_PCS'].max()) * 260 + 10).values

# ── Dark theme ────────────────────────────────────────────────────────────────
plt.style.use('dark_background')
BG   = '#0b0f1a'
GRID = '#1e293b'

fig = plt.figure(figsize=(20, 9), facecolor=BG)
fig.subplots_adjust(left=0.06, right=0.97, top=0.88, bottom=0.12, wspace=0.35)

# ══════════════════════════════════════════════════════════════════════════════
# PANEL 1 — Scatter heatmap
# ══════════════════════════════════════════════════════════════════════════════
ax1 = fig.add_subplot(1, 2, 1, facecolor=BG)

# Background LL / LH / HL cells (smaller, dimmer)
mask_bg = active['lisa'] == 'LL'
ax1.scatter(
    active.loc[mask_bg, 'raw_count'],
    active.loc[mask_bg, 'avg_PCS'],
    s=sizes[mask_bg.values],
    c='#334155', alpha=0.35, linewidths=0, zorder=1,
)

# Non-LL cells
mask_fg = ~mask_bg
ax1.scatter(
    active.loc[mask_fg, 'raw_count'],
    active.loc[mask_fg, 'avg_PCS'],
    s=sizes[mask_fg.values],
    c=colors[mask_fg.values],
    alpha=0.72, linewidths=0.4, edgecolors='white', zorder=2,
)

# Top-20 labelled (white glow outline)
for _, row in top20.iterrows():
    ax1.scatter(row['raw_count'], row['avg_PCS'],
                s=190, c=QUAD_COLOR.get(row['lisa'], '#ef4444'),
                linewidths=1.2, edgecolors='white', zorder=5, alpha=0.95)
    label = f"{row['station']}\n({int(row['raw_count'])}v, {row['avg_PCS']:.2f}PCS)"
    txt = ax1.annotate(
        label,
        xy=(row['raw_count'], row['avg_PCS']),
        xytext=(8, 4), textcoords='offset points',
        fontsize=6.5, color='white', zorder=6,
        fontstyle='italic',
    )
    txt.set_path_effects([
        pe.withStroke(linewidth=2.5, foreground='#0b0f1a')
    ])

# Quadrant dividers at median
med_x = active['raw_count'].median()
med_y = active['avg_PCS'].median()
ax1.axvline(med_x, color='#475569', lw=0.8, ls='--', zorder=0)
ax1.axhline(med_y, color='#475569', lw=0.8, ls='--', zorder=0)

# Quadrant corner annotations
ax1.text(0.98, 0.98, 'Volume + Severity\n⚡ TOP PRIORITY', transform=ax1.transAxes,
         ha='right', va='top', fontsize=7.5, color='#ef4444',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#1e1e2e', alpha=0.7))
ax1.text(0.02, 0.98, 'High Impact,\nLow Volume', transform=ax1.transAxes,
         ha='left', va='top', fontsize=7.5, color='#f97316',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#1e1e2e', alpha=0.7))
ax1.text(0.98, 0.02, 'Volume Trap\n(scooters/footpath)', transform=ax1.transAxes,
         ha='right', va='bottom', fontsize=7.5, color='#94a3b8',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#1e1e2e', alpha=0.7))
ax1.text(0.02, 0.02, 'Low Priority', transform=ax1.transAxes,
         ha='left', va='bottom', fontsize=7.5, color='#475569',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#1e1e2e', alpha=0.7))

ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_xlabel('Violation Count per Cell  (log scale)', color='#cbd5e1', fontsize=11, labelpad=8)
ax1.set_ylabel('Avg Congestion Severity per Violation — PCS  (log scale)', color='#cbd5e1', fontsize=11, labelpad=8)
ax1.set_title('Parking Violations vs. Congestion Impact\nper 110m Grid Cell', color='white', fontsize=13, fontweight='bold', pad=12)
ax1.tick_params(colors='#64748b', which='both')
ax1.spines['bottom'].set_color(GRID)
ax1.spines['left'].set_color(GRID)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.grid(True, which='major', color=GRID, lw=0.6, alpha=0.8)
ax1.grid(True, which='minor', color=GRID, lw=0.3, alpha=0.4)

legend_elements = [
    Patch(facecolor='#ef4444', label='HH — High vol + high impact cluster'),
    Patch(facecolor='#f97316', label='LH — Low vol, surrounded by high impact'),
    Patch(facecolor='#eab308', label='HL — High vol, isolated from cluster'),
    Patch(facecolor='#64748b', label='LL — Low priority'),
    Line2D([0], [0], marker='o', color='none', markerfacecolor='white',
           markeredgecolor='#94a3b8', markersize=6, label='Top-20 hotspot'),
]
leg = ax1.legend(handles=legend_elements, loc='lower right',
                 fontsize=8, framealpha=0.2, facecolor='#1e293b',
                 edgecolor='#334155', labelcolor='white')

# ══════════════════════════════════════════════════════════════════════════════
# PANEL 2 — 2-D hexbin density
# ══════════════════════════════════════════════════════════════════════════════
ax2 = fig.add_subplot(1, 2, 2, facecolor=BG)

x_log = np.log10(active['raw_count'].clip(lower=1))
y_log = np.log10(active['avg_PCS'].clip(lower=0.01))

hb = ax2.hexbin(
    x_log, y_log,
    gridsize=42,
    cmap='inferno',
    mincnt=1,
    bins='log',
    linewidths=0.2,
)

# Overlay top-20 as bright dots
top20_x = np.log10(top20['raw_count'].clip(lower=1))
top20_y = np.log10(top20['avg_PCS'].clip(lower=0.01))
ax2.scatter(top20_x, top20_y, c='#00f5ff', s=80, zorder=5,
            linewidths=1.0, edgecolors='white', label='Top-20 hotspots')

for _, row in top20.iterrows():
    rx = np.log10(max(row['raw_count'], 1))
    ry = np.log10(max(row['avg_PCS'], 0.01))
    txt = ax2.annotate(
        row['station'],
        xy=(rx, ry), xytext=(5, 3), textcoords='offset points',
        fontsize=6, color='#00f5ff', zorder=6,
    )
    txt.set_path_effects([pe.withStroke(linewidth=2, foreground='#0b0f1a')])

# Median dividers
ax2.axvline(np.log10(med_x), color='#475569', lw=0.8, ls='--')
ax2.axhline(np.log10(med_y), color='#475569', lw=0.8, ls='--')

cb = fig.colorbar(hb, ax=ax2, pad=0.02, fraction=0.046)
cb.set_label('Cell density (log scale)', color='#cbd5e1', fontsize=9)
cb.ax.tick_params(colors='#64748b')

# Custom tick labels (convert log10 back to real values)
x_ticks = [1, 2, 3, 3.699]     # log10(10, 100, 1000, 5000)
y_ticks = [np.log10(0.5), np.log10(1.0), np.log10(2.0), np.log10(5.0)]
ax2.set_xticks(x_ticks)
ax2.set_xticklabels([f'{10**t:.0f}' for t in x_ticks], color='#64748b', fontsize=9)
ax2.set_yticks(y_ticks)
ax2.set_yticklabels([f'{10**t:.1f}' for t in y_ticks], color='#64748b', fontsize=9)

ax2.set_xlabel('Violation Count per Cell  (log scale)', color='#cbd5e1', fontsize=11, labelpad=8)
ax2.set_ylabel('Avg PCS per Violation  (log scale)', color='#cbd5e1', fontsize=11, labelpad=8)
ax2.set_title('Cell Density Heatmap\n(concentration of enforcement opportunity)', color='white', fontsize=13, fontweight='bold', pad=12)
ax2.tick_params(colors='#64748b')
ax2.spines['bottom'].set_color(GRID)
ax2.spines['left'].set_color(GRID)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.legend(fontsize=8, framealpha=0.2, facecolor='#1e293b',
           edgecolor='#334155', labelcolor='white')

# ── Super-title & footer ──────────────────────────────────────────────────────
fig.suptitle(
    'GridLock-R2  ·  BTP Bengaluru  ·  Parking Violation Frequency vs Congestion Severity',
    color='white', fontsize=15, fontweight='bold', y=0.97
)
fig.text(0.5, 0.01,
    f'Dataset: 298,450 violations · Nov 2023–Apr 2024 · {len(active):,} active 110m grid cells · '
    'PCS = PCU × Δ(hour) × σ(violation type)  |  LISA quadrant via k=8 spatial lag',
    ha='center', va='bottom', fontsize=7.5, color='#475569'
)

# ── Save ──────────────────────────────────────────────────────────────────────
out_path = os.path.join(repo_root, 'violations_vs_impact.png')
plt.savefig(out_path, dpi=160, bbox_inches='tight', facecolor=BG)
plt.close()
print(f"\n✅  Saved → {out_path}")
print("Open with:  open violations_vs_impact.png")
