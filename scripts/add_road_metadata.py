import json
import os

def assign_metadata():
    filepath = 'hotspot_data.json'
    if not os.path.exists(filepath):
        filepath = '../hotspot_data.json'
        
    with open(filepath, 'r') as f:
        data = json.load(f)

    for hs in data:
        violation = hs.get('violation', '').lower()
        count = hs.get('count', 0)
        
        if 'main road' in violation or 'arterial' in violation:
            roadType = 'Arterial Road'
            multiplier = 2.0
        elif count >= 1000:
            roadType = 'Collector Road'
            multiplier = 1.2
        else:
            roadType = 'Local Street'
            multiplier = 0.5
            
        hs['roadType'] = roadType
        hs['impactMultiplier'] = multiplier
        
        # Base EPS on count * multiplier, scaled for readability
        new_eps = count * multiplier / 10.0
        hs['totalPCS'] = round(new_eps, 2)

    # Sort by new EPS
    data.sort(key=lambda x: x['totalPCS'], reverse=True)

    # Re-assign rank and tier based on mathematical impact
    total = len(data)
    for i, hs in enumerate(data):
        hs['rank'] = i + 1
        
        # Tiers: 5% Critical, 15% High, 30% Medium, 50% Low
        if i < total * 0.05:
            hs['tier'] = 'critical'
        elif i < total * 0.20:
            hs['tier'] = 'high'
        elif i < total * 0.50:
            hs['tier'] = 'medium'
        else:
            hs['tier'] = 'low'

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Assigned Road Metadata to {len(data)} hotspots. Recalculated EPS and resorted rankings.")

if __name__ == '__main__':
    assign_metadata()
