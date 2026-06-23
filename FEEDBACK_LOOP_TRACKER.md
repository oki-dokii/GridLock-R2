# Validation Discipline: Closing the Feedback Loop

Building an enforcement routing model is only half the problem; measuring whether the resulting dispatch *actually* reduced congestion is the other. 

Rather than presenting a mocked "success metric," this document outlines the rigorous validation discipline required to build an honest feedback loop. We stepped through increasingly sophisticated measurement frameworks, stress-tested them on historical data, and caught structural flaws at each stage before they could produce false insights.

---

### Phase 1: The Naive "Before & After" Trap
*   **The Setup:** We tracked violations in the top 50 targeted hotspots from March 2024 to April 2024.
*   **The Result:** Violations dropped by a massive **73.6%**.
*   **The Trap (The April Data Drop):** A naive reading would claim a 73% success rate. However, total network violations dropped universally between March and April due to dataset reporting truncation (April data ends on the 8th). *Before-and-after tracking without a control group is highly susceptible to macro-level anomalies.*

---

### Phase 2: Simple Difference-in-Differences (DiD)
To isolate the true intervention effect, we deployed a Difference-in-Differences tracker. We used a trailing historical average (Jan-Feb) to select targets—avoiding regression to the mean—and measured the difference between the targeted hotspots and an unenforced control group (the rest of the city) during matched 8-day windows in March and April.

*   **Treatment (Hotspots) Change:** -1.0%
*   **Control (Rest of City) Change:** +10.3%
*   **Net Effect:** -11.4%

*This looks like a rigorous mechanism. But to be certain, we ran a placebo test.*

---

### Phase 3: The Placebo Stress-Test
A valid DiD tracker relies on the **Parallel Trends Assumption**: the control and treatment groups must fluctuate similarly in the absence of an intervention. 

To verify this, we ran the exact same script on a historical window where we know *no enforcement occurred*: Ranking targets on November 2023, and evaluating the shift from December to January.

**Placebo Results (Expected Net Effect: ~0%):**
*   **Aggregate Sum Net Effect:** +23.1%
*   **Per-Cell Average Net Effect:** +82.7%

**The Diagnosis: Parallel Trends Violation**
The simple DiD failed the placebo test spectacularly. Our top 50 hotspots are dense commercial hubs and transit intersections, while the ~450 control cells are sparse residential grids. These two cohorts are structurally heterogeneous; they do not react to holidays, weather, or monthly seasonality in the same way. 

*(Note on the metrics: The aggregate sum and per-cell average disagree wildly because a few high-variance cells dominate the sum, whereas the per-cell average is heavily skewed by low-count residential cells jumping from 1 to 2 violations. Neither metric is trustworthy when the cohorts are this heterogeneous).*

---

### The Final Architecture: Synthetic Controls
Because high-volume hotspots behave differently than the rest of the city, subtracting the global network trend is mathematically invalid. 

**The Solution:** The live GridLock platform will implement **Propensity Score Matching (PSM)** or **Synthetic Controls**. We must track our enforced hotspots exclusively against a matched cohort of unenforced hotspots that share similar historical volumes, road types, and congestion variances. 

By stress-testing our own measurement frameworks, we avoid defending a flawed simulation and establish a truly causal tracking pipeline for deployment.
