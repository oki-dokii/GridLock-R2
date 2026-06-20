"""
export_hotspot_json.py
─────────────────────────────────────────────────────────────────────────────
Reads cleaned_violations.csv and exports top-500 hotspot cells as JSON.
Each cell includes all fields needed by the field officer app:
  lat, lon, clean_count, total_PCS, avg_PCS,
  dominant_vehicle, dominant_violation, best_patrol_hour, station
─────────────────────────────────────────────────────────────────────────────
"""
import os, json
import numpy as np
import pandas as pd

script_dir   = os.path.dirname(os.path.abspath(__file__))
repo_root    = os.path.dirname(script_dir)
cleaned_path = os.path.join(repo_root, 'cleaned_violations.csv')

print("Loading cleaned data …")
df = pd.read_csv(cleaned_path)
df['ts_ist'] = pd.to_datetime(df['ts_ist'], utc=True).dt.tz_convert('Asia/Kolkata')
df['hour']   = df['ts_ist'].dt.hour

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

print("Aggregating per cell …")
hotspots = []

for grid_id, grp in df.groupby('grid_id'):
    lat = grp['lat_g'].iloc[0]
    lon = grp['lon_g'].iloc[0]
    count = len(grp)
    total_pcs = grp['PCS'].sum() if 'PCS' in grp.columns else count
    avg_pcs   = grp['PCS'].mean() if 'PCS' in grp.columns else 1.0

    # Dominant vehicle
    vtype = grp['vehicle_type'].dropna()
    dom_vehicle = vtype.mode()[0] if len(vtype) > 0 else 'Unknown'

    # Dominant violation
    viol = grp['violation_type'].dropna().astype(str)
    dom_violation = viol.mode()[0] if len(viol) > 0 else 'Unknown'

    # Best patrol hour
    hour_counts = grp['hour'].value_counts()
    best_hour = int(hour_counts.idxmax()) if len(hour_counts) > 0 else 9

    station = nearest_station(lat, lon)

    hotspots.append({
        'id':       grid_id,
        'lat':      round(float(lat), 4),
        'lon':      round(float(lon), 4),
        'count':    int(count),
        'totalPCS': round(float(total_pcs), 2),
        'avgPCS':   round(float(avg_pcs), 3),
        'vehicle':  str(dom_vehicle).title(),
        'violation':str(dom_violation).title(),
        'bestHour': best_hour,
        'station':  station,
    })

# Sort by totalPCS descending, take top 500
hotspots.sort(key=lambda x: x['totalPCS'], reverse=True)
top500 = hotspots[:500]

# Rank and tier
for i, h in enumerate(top500):
    h['rank'] = i + 1
    if i < 10:
        h['tier'] = 'critical'
    elif i < 30:
        h['tier'] = 'high'
    elif i < 100:
        h['tier'] = 'medium'
    else:
        h['tier'] = 'low'

out_path = os.path.join(repo_root, 'hotspot_data.json')
with open(out_path, 'w') as f:
    json.dump(top500, f, indent=2)

print(f"✅  Exported {len(top500)} hotspots → {out_path}")
print(f"    Top 3:")
for h in top500[:3]:
    print(f"      #{h['rank']} {h['station']} ({h['lat']},{h['lon']}) — {h['count']} violations, PCS={h['totalPCS']}")
