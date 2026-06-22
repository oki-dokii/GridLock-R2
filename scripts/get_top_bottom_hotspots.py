import json
import os

with open('hotspot_data.json', 'r') as f:
    data = json.load(f)

# Sort by priorityScore (assuming it exists, else use totalPCS)
def get_score(hs):
    return hs.get('priorityScore', hs.get('totalPCS', 0))

data_sorted = sorted(data, key=get_score, reverse=True)

top_10 = data_sorted[:10]
bottom_10 = data_sorted[-10:]

print("TOP 10:")
for i, hs in enumerate(top_10):
    print(f"{i+1}. {hs['station']} - {hs.get('osmRoadName', 'Unknown')} ({hs['lat']}, {hs['lon']}) | Score: {get_score(hs)}")

print("\nBOTTOM 10:")
for i, hs in enumerate(bottom_10):
    print(f"{i+1}. {hs['station']} - {hs.get('osmRoadName', 'Unknown')} ({hs['lat']}, {hs['lon']}) | Score: {get_score(hs)}")
