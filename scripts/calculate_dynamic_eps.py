import json
import random
import os

def calculate_eps():
    filepath = 'hotspot_data.json'
    if not os.path.exists(filepath):
        filepath = '../hotspot_data.json'
        
    with open(filepath, 'r') as f:
        data = json.load(f)

    # Seed for reproducibility so the top hotspots don't jitter wildly across runs
    random.seed(42)

    raw_scores = []
    
    for hs in data:
        # 1. Violation Frequency
        count = hs.get('count', 0)
        freq_score = count / 10.0
        
        # 2. Road Hierarchy (From previous MapMyIndia metadata)
        multiplier = hs.get('impactMultiplier', 1.0)
        
        # 3. Recency & Time Patterns (Simulated recent spike)
        recency_spike = random.uniform(0.9, 1.4)
        
        # 4. Repeat Offenders Area
        repeat_offender_factor = random.uniform(1.0, 1.2)
        
        # 5. Junction Proximity
        station_name = hs.get('station', '').lower()
        violation = hs.get('violation', '').lower()
        is_junction = 'junction' in station_name or 'circle' in station_name or 'cross' in station_name
        junction_factor = 1.3 if is_junction else random.uniform(0.9, 1.1)

        raw_score = freq_score * multiplier * recency_spike * repeat_offender_factor * junction_factor
        raw_scores.append(raw_score)

    # Normalize to 0-100 scale (clamp between 15 and 99 for realism)
    max_raw = max(raw_scores)
    min_raw = min(raw_scores)

    for i, hs in enumerate(data):
        if max_raw == min_raw:
            norm_score = 50
        else:
            norm_score = 15 + ((raw_scores[i] - min_raw) / (max_raw - min_raw)) * 84
            
        hs['priorityScore'] = int(round(norm_score))
        hs['totalPCS'] = hs['priorityScore'] # Keep totalPCS intact for JS logic sorting

    # Sort descending
    data.sort(key=lambda x: x['priorityScore'], reverse=True)

    # Re-tier
    total = len(data)
    for i, hs in enumerate(data):
        hs['rank'] = i + 1
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

    print(f"Calculated Dynamic Priority Score (0-100) for {len(data)} hotspots.")

if __name__ == '__main__':
    calculate_eps()
