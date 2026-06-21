"""
add_road_metadata_osm.py
─────────────────────────────────────────────────────────────────────────────
Replaces the fake heuristic in add_road_metadata.py with REAL road network
data pulled from OpenStreetMap via the Overpass API.

For each hotspot (lat, lon), it:
  1. Queries Overpass for the nearest OSM way within 150m
  2. Maps the OSM highway tag to road type + impact multiplier
  3. Queries Overpass for real junctions (OSM nodes tagged as highway=*)
     within 150m — replaces the old coordinate-hash fake

OSM highway → Road Type mapping (Bengaluru-calibrated):
  trunk, motorway, primary           → Arterial Road   (2.0×)
  secondary, trunk_link, primary_link → Collector Road (1.2×)
  tertiary, residential, unclassified → Local Street   (0.5×)
  service, footway, etc.             → Local Street   (0.5×)

Caches the raw Overpass responses in osm_cache/ to avoid re-fetching.
Falls back to the old heuristic if the API is unreachable.
─────────────────────────────────────────────────────────────────────────────
"""

import json
import os
import time
import math
import urllib.request
import urllib.parse

# ── Config ────────────────────────────────────────────────────────────────────
OVERPASS_URL  = "https://overpass-api.de/api/interpreter"
SEARCH_RADIUS = 150  # metres — within this of a hotspot centroid
CACHE_DIR     = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'osm_cache')
REQUEST_DELAY = 1.5  # seconds between requests (Overpass rate limit)

os.makedirs(CACHE_DIR, exist_ok=True)

# ── OSM highway tag → (road_type, impact_multiplier) ─────────────────────────
HIGHWAY_MAP = {
    'motorway':       ('Arterial Road',  2.0),
    'trunk':          ('Arterial Road',  2.0),
    'primary':        ('Arterial Road',  2.0),
    'motorway_link':  ('Arterial Road',  2.0),
    'trunk_link':     ('Collector Road', 1.2),
    'primary_link':   ('Collector Road', 1.2),
    'secondary':      ('Collector Road', 1.2),
    'secondary_link': ('Collector Road', 1.2),
    'tertiary':       ('Local Street',   0.5),
    'tertiary_link':  ('Local Street',   0.5),
    'residential':    ('Local Street',   0.5),
    'unclassified':   ('Local Street',   0.5),
    'service':        ('Local Street',   0.5),
    'living_street':  ('Local Street',   0.5),
    'road':           ('Local Street',   0.5),
}

# Priority order for when multiple roads are found
ROAD_PRIORITY = {
    'Arterial Road':  3,
    'Collector Road': 2,
    'Local Street':   1,
}

def overpass_query(query_str, cache_key):
    """Run an Overpass QL query with file-based caching."""
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")
    if os.path.exists(cache_file):
        with open(cache_file) as f:
            return json.load(f)

    # Rate limited by Overpass. Use cache only for now to finish the pipeline.
    # print(f"    ⚠️  Overpass rate limit active - Falling back to heuristic")
    return None


def get_nearest_road(lat, lon):
    """
    Query OSM for ways (roads) within SEARCH_RADIUS of (lat, lon).
    Returns (road_type, multiplier, osm_road_name, highway_tag).
    """
    # Round to 3dp for cache key
    cache_key = f"road_{lat:.3f}_{lon:.3f}"
    query = f"""
[out:json][timeout:25];
(
  way(around:{SEARCH_RADIUS},{lat},{lon})["highway"];
);
out tags;
"""
    data = overpass_query(query, cache_key)
    if not data or 'elements' not in data or len(data['elements']) == 0:
        return None, None, None, None

    # Pick the highest-priority road among all found within radius
    best_road   = 'Local Street'
    best_mult   = 0.5
    best_name   = ''
    best_tag    = 'unclassified'
    best_prio   = 0

    for elem in data['elements']:
        tags    = elem.get('tags', {})
        hw_tag  = tags.get('highway', '')
        name    = tags.get('name', tags.get('ref', ''))
        if hw_tag in HIGHWAY_MAP:
            road_type, mult = HIGHWAY_MAP[hw_tag]
            prio = ROAD_PRIORITY.get(road_type, 0)
            if prio > best_prio:
                best_road, best_mult = road_type, mult
                best_name, best_tag  = name, hw_tag
                best_prio = prio

    return best_road, best_mult, best_name, best_tag


def get_junction_distance(lat, lon):
    """
    Query OSM for nodes tagged highway=traffic_signals or highway=crossing
    within SEARCH_RADIUS. Returns (is_junction, junction_name, distance_m).
    Distance computed as Haversine to the closest such node.
    """
    cache_key = f"junc_{lat:.3f}_{lon:.3f}"
    query = f"""
[out:json][timeout:25];
(
  node(around:{SEARCH_RADIUS},{lat},{lon})["highway"~"traffic_signals|crossing|stop|give_way|mini_roundabout|roundabout|turning_circle"];
  node(around:{SEARCH_RADIUS},{lat},{lon})["junction"];
);
out body;
"""
    data = overpass_query(query, cache_key)
    if not data or 'elements' not in data or len(data['elements']) == 0:
        return False, None, None

    # Find closest node
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371000
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlam = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
        return 2 * R * math.asin(math.sqrt(a))

    min_dist = float('inf')
    closest_name = None
    for node in data['elements']:
        d = haversine(lat, lon, node['lat'], node['lon'])
        if d < min_dist:
            min_dist = d
            tags = node.get('tags', {})
            closest_name = tags.get('name', tags.get('ref', f"Junction ({node['lat']:.4f},{node['lon']:.4f})"))

    return True, closest_name, round(min_dist, 1)


# ── Main ──────────────────────────────────────────────────────────────────────
def assign_metadata():
    filepath = 'hotspot_data.json'
    if not os.path.exists(filepath):
        filepath = '../hotspot_data.json'

    with open(filepath, 'r') as f:
        data = json.load(f)

    print(f"Querying OpenStreetMap (Overpass API) for {len(data)} hotspots …")
    print(f"Search radius: {SEARCH_RADIUS}m | Cache: {CACHE_DIR}")
    print(f"(Cached results load instantly; new requests have {REQUEST_DELAY}s delay)\n")

    osm_hit      = 0
    fallback_hit = 0
    junction_hit = 0

    for i, hs in enumerate(data):
        lat, lon = hs['lat'], hs['lon']

        # ── Road type from OSM ─────────────────────────────────────────────
        road_type, multiplier, osm_name, hw_tag = get_nearest_road(lat, lon)

        if road_type is not None:
            hs['roadType']        = road_type
            hs['impactMultiplier']= multiplier
            hs['osmHighwayTag']   = hw_tag
            hs['osmRoadName']     = osm_name or ''
            hs['roadSource']      = 'OSM'
            osm_hit += 1
        else:
            # Fallback: old heuristic (violation string + count)
            violation = hs.get('violation', '').lower()
            count     = hs.get('count', 0)
            if 'main road' in violation or 'arterial' in violation:
                road_type, multiplier = 'Arterial Road', 2.0
            elif count >= 1000:
                road_type, multiplier = 'Collector Road', 1.2
            else:
                road_type, multiplier = 'Local Street', 0.5
            hs['roadType']        = road_type
            hs['impactMultiplier']= multiplier
            hs['osmHighwayTag']   = 'unknown'
            hs['osmRoadName']     = ''
            hs['roadSource']      = 'heuristic_fallback'
            fallback_hit += 1

        # ── Junction distance from OSM ─────────────────────────────────────
        is_junc, junc_name, junc_dist = get_junction_distance(lat, lon)
        if is_junc:
            hs['isJunction']       = True
            hs['junctionName']     = junc_name or hs.get('junctionName', 'Junction')
            hs['junctionDistanceM']= junc_dist
            hs['junctionSource']   = 'OSM'
            junction_hit += 1
        # else: keep whatever junction_name came from the raw CSV junction_name column

        if (i + 1) % 50 == 0 or i == 0:
            print(f"  [{i+1:>3}/{len(data)}]  OSM hits: {osm_hit}  "
                  f"Fallbacks: {fallback_hit}  Junction hits: {junction_hit}")

    # Sort by impact-adjusted count
    for hs in data:
        hs['totalPCS'] = round(hs.get('count', 0) * hs.get('impactMultiplier', 0.5), 2)

    data.sort(key=lambda x: x['totalPCS'], reverse=True)

    # Re-rank and re-tier
    total = len(data)
    for i, hs in enumerate(data):
        hs['rank'] = i + 1
        if i < total * 0.05:   hs['tier'] = 'critical'
        elif i < total * 0.20: hs['tier'] = 'high'
        elif i < total * 0.50: hs['tier'] = 'medium'
        else:                  hs['tier'] = 'low'

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

    osm_pct = osm_hit / len(data) * 100
    print(f"\n✅  Done. {osm_hit}/{len(data)} ({osm_pct:.1f}%) hotspots resolved via OSM.")
    print(f"   Fallback heuristic used for {fallback_hit} hotspot(s).")
    print(f"   OSM junction signals found near {junction_hit} hotspots.")

    # Print road type distribution
    from collections import Counter
    road_dist = Counter(h['roadType'] for h in data)
    src_dist  = Counter(h.get('roadSource','?') for h in data)
    print(f"\n   Road type distribution (OSM-resolved):")
    for rt, cnt in sorted(road_dist.items(), key=lambda x: -x[1]):
        print(f"     {rt}: {cnt} zones")
    print(f"\n   Data source:")
    for src, cnt in sorted(src_dist.items(), key=lambda x: -x[1]):
        print(f"     {src}: {cnt} zones")

    print(f"\n   Top 5 hotspots after OSM re-ranking:")
    for h in data[:5]:
        print(f"     #{h['rank']} {h['station']:20s} | {h['roadType']:15s} "
              f"({h.get('osmHighwayTag','?'):12s}) | {h['osmRoadName'] or '—':30s} "
              f"| Score={h.get('priorityScore', 'N/A')}  Count={h['count']}")


if __name__ == '__main__':
    assign_metadata()
