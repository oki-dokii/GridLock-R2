import json
import os

# Base capacity estimates (veh/hr/lane) derived from typical Highway Capacity Manual defaults
CAPACITY_MAP = {
    "Arterial Road": 1200,
    "Collector Road": 900,
    "Local Street": 600
}
DEFAULT_CAPACITY = 800

# PCU mappings (Passenger Car Units)
PCU_MAP = {
    "Two-Wheeler": 0.5,
    "Scooter": 0.5,
    "Car": 1.0,
    "Auto": 0.5,
    "Heavy": 1.5,
    "Bus": 3.0
}
DEFAULT_PCU = 1.0

def calculate_marginal_delay(hotspots):
    # Standard BPR (Bureau of Public Roads) function parameters
    T_f = 60.0  # Assumed free flow time (seconds) for a segment
    alpha = 0.15
    beta = 4.0
    v_c_ratio_base = 0.85 # Assume near-peak conditions for impact relevance

    updated = 0

    for hs in hotspots:
        # Determine base capacity based on road type
        road_type = hs.get("roadType", "Unknown")
        c_base = CAPACITY_MAP.get(road_type, DEFAULT_CAPACITY)
        
        # Assume steady peak-ish volume
        V = v_c_ratio_base * c_base

        # Determine PCU for the obstruction
        vehicle_type = hs.get("vehicle", "Unknown")
        # In GridLock-R2 data, vehicles might be listed inside "vehicle" string
        # Let's find the first matching PCU
        pcu = DEFAULT_PCU
        for v_name, v_pcu in PCU_MAP.items():
            if v_name.lower() in vehicle_type.lower():
                pcu = v_pcu
                break
                
        # A parked PCU functionally blocks ~150 veh/hr of lane capacity
        delta_c = 150.0 * pcu
        
        # We must cap capacity reduction so it doesn't cause negative or near-zero capacity in formulas
        c_new = max(c_base * 0.1, c_base - delta_c)

        # Base delay using BPR Function
        delay_base = T_f * 0.15 * ((V / c_base) ** beta)
        
        # New delay with obstruction
        delay_new = T_f * 0.15 * ((V / c_new) ** beta)
        
        # Marginal delay per passing vehicle
        marginal_delay_per_vehicle = delay_new - delay_base
        
        # Total marginal system delay (seconds per hour of parking)
        total_delay_seconds_per_hour = marginal_delay_per_vehicle * V
        
        hs["marginalImpact"] = {
            "delaySecondsPerHour": round(total_delay_seconds_per_hour, 2),
            "model": "Bureau of Public Roads (BPR) Volume-Delay Function",
            "formula": "T_f * 0.15 * ((V/max(0.1*C, C - assumedCapacityReduction*PCU))^4 - (V/C)^4) * V",
            "assumedCapacity": c_base,
            "assumedVCRatio": v_c_ratio_base,
            "assumedVolume": V,
            "assumedCapacityReductionPerPCU": 150.0,
            "assumedMinimumCapacityFloor": c_base * 0.1,
            "pcuFactor": pcu,
            "note": "Traffic volume (V) is assumed at a near-peak V/C ratio of 0.85. Capacity reduction of 150 veh/hr per PCU is a logical assumption, capped at a 10% capacity floor to prevent numerical blow-ups for heavy vehicles on local roads."
        }
        updated += 1
        
    return hotspots, updated

def main():
    file_path = "hotspot_data.json"
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r") as f:
        data = json.load(f)

    print("Calculating marginal delay metrics using BPR Volume-Delay function...")
    updated_data, count = calculate_marginal_delay(data)
    
    with open(file_path, "w") as f:
        json.dump(updated_data, f, indent=2)

    print(f"Successfully computed and injected marginalImpact for {count} hotspots.")

if __name__ == "__main__":
    main()
