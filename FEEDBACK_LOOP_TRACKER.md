# Intervention Feedback Loop Tracker (Stub)

This report outlines the **Difference-in-Differences (DiD)** tracking mechanism designed to close the feedback loop. Rather than asserting "violations dropped by X%", this framework isolates the *causal impact* of GridLock dispatch by comparing targeted zones against the natural background trend of unenforced zones.

## Simulation Setup
*   **Pre-Intervention Baseline:** 2024-03 (Days 1-8 matched window)
*   **Post-Intervention Measurement:** 2024-04 (Days 1-8 matched window)
*   **Target Selection:** Top 50 hotspots (Simulated treatment group)
*   **Control Group:** All remaining grid cells in the network

## Mechanism: Difference-in-Differences
Traffic volume and violations fluctuate naturally due to weather, holidays, or macro trends. By tracking an unenforced Control Group, we establish a baseline trend. The true impact of GridLock enforcement is the *difference* between the targeted group's change and the control group's natural change.

### Results on Held-Out Data (Mock Enforcement)
*Note: Since GridLock was not actively deployed in 2024-04, this demonstrates the tracking mechanism on historical data. Both groups reflect natural (unenforced) conditions. The data is explicitly filtered to an 8-day matched window (Days 1-8 of the month) to account for data truncation in the 2024-04 dataset.*

| Cohort | Pre-Intervention (2024-03 matched) | Post-Intervention (2024-04 matched) | % Change |
| :--- | :--- | :--- | :--- |
| **Control (Unenforced)** | 6327 | 7605 | +20.2% |
| **Treatment (GridLock Targeted)** | 2679 | 2069 | -22.8% |

### GridLock Impact Metric
**Net Intervention Effect (DiD):** `-43.0%`

*If this were a live deployment, a negative Net Intervention Effect would mathematically prove that targeted patrols suppressed violations faster/more than the natural network trend.*
