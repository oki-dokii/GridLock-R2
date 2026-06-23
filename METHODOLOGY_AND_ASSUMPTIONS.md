# GridLock: Methodology & Core Assumptions

This document centralizes all structural assumptions, heuristics, and hardcoded thresholds used throughout the GridLock evaluation pipeline. By explicitly defining these parameters, we aim to provide full transparency on how raw traffic violation data was translated into operational metrics and deployment impact scores.

## 1. Network & Infrastructure Heuristics

To estimate the true physical congestion impact of a violation, we augment point-coordinate data with structural proxies for road capacity and flow density.

### Volume-to-Capacity (V/C) Ratio 
*   **Constant:** `V/C = 0.85`
*   **Rationale:** Rather than modeling dynamic traffic states, we assume a static peak-hour V/C ratio of 0.85 across the network during violation hours. This standard baseline represents a near-capacity state where flow becomes highly sensitive to disruptions (like illegal parking).

### Passenger Car Unit (PCU) Flow 
*   **Constant:** `150 veh/hr/PCU`
*   **Rationale:** We utilize a flat 150 vehicles/hour delay penalty per PCU for any blocked lane. Different vehicle types are assigned standard PCU weights (e.g., Heavy Goods Vehicle = 3.0 PCU, Car = 1.0 PCU, Two-Wheeler = 0.5 PCU) to scale the delay proportionally.

### OpenStreetMap (OSM) Coverage
*   **Metric:** Real road/junction metadata via Overpass API.
*   **Status:** We enriched the top hotspots with actual OSM data (lane counts, road types, proximity to junctions). For grid cells where the Overpass query failed or rate-limited, we fall back to a standard two-lane proxy.

## 2. Operational Dispatch Thresholds

When simulating the deployment of enforcement teams to predicted hotspots, we utilize standard operational capacity constraints.

*   **Patrol Capacity:** `2 teams / zone / shift`
*   **Tow Capacity:** `3.5 vehicles / hour / team`
*   **Rationale:** This limits the "maximum fixable violations" in our simulation. Even if an algorithm perfectly predicts 100 severe violations in a grid, the physical constraint of tow truck turnaround times caps the operational benefit.

## 3. Evaluation & Confidence Thresholds

To prevent over-indexing on statistical noise, especially in low-volume spatial clusters or rare vehicle types, we enforce strict confidence tiers on all subgroup evaluations.

*   **⚠️ Low Confidence Tier (30 ≤ n < 100):** Results are reported but explicitly flagged with a warning icon (`⚠️`). A sample size of under 100 yields a wide margin of error for binomial proportion metrics like Recall. Caution is advised when interpreting pattern shifts (e.g., model routing advantages) in these tiers.
*   **Suppressed Tier (n < 30):** Results are completely hidden (`low_conf`). Sample sizes under 30 are statistically unreliable and are removed to prevent misleading insights.

## 4. Impact Validation (Synthetic Controls)

To validate the causal impact of GridLock deployment, we rely on a matched-control framework rather than naive before-and-after tracking or global Difference-in-Differences (DiD). 

*   **The Parallel Trends Problem:** Placebo testing on historical data revealed that high-volume transit hubs and standard residential grids do not share parallel seasonal trends. Therefore, subtracting global network shifts from targeted hotspots is mathematically invalid.
*   **Target Selection (Avoiding Regression to the Mean):** Selecting target zones based strictly on the immediate pre-intervention period guarantees an artificial "drop" purely due to statistical regression to the mean. Instead, target selection utilizes a trailing average of historical months (e.g., Jan/Feb) that strictly pre-dates the measurement window.
*   **Mechanism (Propensity Score Matching):** The live platform isolates the net intervention effect by tracking enforced hotspots exclusively against a "Synthetic Control" cohort—a matched set of unenforced hotspots that share similar historical volumes, road types, and congestion variances.
