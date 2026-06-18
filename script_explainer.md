# Gridlock Scripts — A Complete Beginner's Guide

## Part 1: What Does "Training a Model" Even Mean?

Before diving into the scripts, let's understand the big picture.

**The goal of Gridlock** is to answer: *"Which street grid cells in Bengaluru are most likely to have parking violations in the future?"* Instead of guessing, the model learns patterns from historical data.

### The Core Idea

Think of it like a detective building a case. You have months of records:
- *Where* violations happened (GPS coordinates)
- *When* they happened (hour, day, month)
- *What* type of vehicle was involved
- *How severe* the violation was

A model **learns the relationship** between all these factors and the *frequency* of violations. Once it understands those relationships, it can predict: *"Next month, grid cell X will probably have Y violations."*

### What "Training" Actually Means

"Training" is just fitting a mathematical equation to your historical data so that the equation's output (predictions) is as close to reality as possible.

In this project, the equation is called a **Poisson GLM (Generalized Linear Model)**. It's specifically designed for count data — things you count (like number of violations), not things you measure (like temperature).

The output is: `predicted violations = e^(intercept + a×hour + b×day_type + c×prior_month_score)`

The coefficients `a`, `b`, `c` are what the model "learns" from data.

### The Train / Holdout Split

A critical concept: **never test yourself on the same material you studied from**.

- **Training data**: Nov 2023 – Feb 2024 → the model studies this
- **Holdout data**: April 2024 → the model is tested on this (data it has never seen)

March 2024 is sometimes used as the "last known month" to feed into the model as a prior signal.

---

## Part 2: The Three Layers of Scoring

Before looking at any script, understand the three "ingredients" that combine into a final score for each grid cell:

### 1. PCS — Parking Congestion Score (per violation)
Each violation record is given a severity weight:

```
PCS = ω (vehicle weight) × δ (time-of-day weight) × σ (violation type weight)
```

| Factor | Symbol | Example |
|--------|--------|---------|
| Vehicle type | ω (omega) | Scooter=0.5, Car=1.0, Bus=3.0 |
| Time of day | δ (delta) | Peak hour (8–12, 17–20)=1.5, Off-peak=0.8 |
| Violation severity | σ (sigma) | Double parking=2.0, No parking=1.0 |

### 2. p̂ — Officer Quality Score (Bayesian)
Not all officers are equally reliable. Some consistently get their reports approved; others get rejected often.

```
p̂ = (5 + Approved) / (7 + Approved + Rejected)
```

The `5` and `7` are **Bayesian priors** — they say "assume the officer is moderately good until we have evidence otherwise". This prevents an officer with only 1 approval from looking perfect.

### 3. EPS — Enforcement Priority Score (per grid cell)
The final ranking score:

```
EPS = PI × predicted_weekly_volume
```

Where:
- **PI (Persistence Index)** = How consistently has this cell appeared in the Top 50 hotspots over 3 months? (0 to 1)
- **predicted_weekly_volume** = What the Poisson model predicts for a typical week

---

## Part 3: The Scripts — In Pipeline Order

### Stage 0: Raw Exploration

---

#### [`explore.py`](file:///c:/Users/thris/OneDrive%20-%20iiit-b/Projects/Gridlock/GridLock-R2/scripts/explore.py)
**Purpose: Sanity-check the raw dataset**

This is the very first script anyone runs on a new dataset. It simply loads the first 100 rows and prints the column names and one sample record.

```python
df = pd.read_csv('jan to may police violation_anonymized791b166.csv', nrows=100)
print(df.columns)
print(df.iloc[0])
```

**Why it matters:** Before writing any analysis, you need to know what columns exist (`latitude`, `longitude`, `vehicle_type`, `violation_type`, `created_datetime`, etc.) and what format they're in. This is the "open the textbook and look at the table of contents" step.

---

#### [`inspect_types.py`](file:///c:/Users/thris/OneDrive%20-%20iiit-b/Projects/Gridlock/GridLock-R2/scripts/inspect_types.py)
**Purpose: Understand the categorical values in the data**

Prints every unique value in `vehicle_type`, `updated_vehicle_type`, and `violation_type`.

**Key insight:** `violation_type` is stored as a JSON-like string (e.g., `"['NO PARKING', 'FOOTPATH']"`), so the script parses it carefully. This exploration revealed exactly which violation type strings exist, which were then used to build the `SIGMA_MAP` in later scripts.

---

#### [`inspect_pcu.py`](file:///c:/Users/thris/OneDrive%20-%20iiit-b/Projects/Gridlock/GridLock-R2/scripts/inspect_pcu.py)
**Purpose: Verify PCU (Passenger Car Unit) weight assignments**

PCU is a traffic engineering standard that converts different vehicle types to equivalent "car units". A bus is equivalent to 3 cars; a scooter to 0.5 cars.

This script applies the PCU lookup to every row and prints the total PCU sum by vehicle type — essentially checking: "Do our vehicle weight assignments make sense given the distribution of vehicles in the data?"

---

#### [`explore_officers.py`](file:///c:/Users/thris/OneDrive%20-%20iiit-b/Projects/Gridlock/GridLock-R2/scripts/explore_officers.py)
**Purpose: Profile officer performance using the Bayesian p̂ formula**

For every officer (`created_by_id`), calculates their approval rate using the Bayesian formula:

```python
p_hat = (5 + approved) / (7 + approved + rejected)
```

Then prints the **10 worst** and **10 best** officers by p̂.

**Why Bayesian?** Without the prior (5, 7), an officer with 1 approval and 0 rejections would appear to have a perfect 100% approval rate. The prior pulls everyone toward a reasonable baseline (≈71%) until there's enough evidence.

**Output insight:** This told the team which officers might be submitting unreliable records, informing the decision to weight violations by officer quality.

---

### Stage 1: Feature Engineering & Model Fitting

---

#### [`fit_poisson.py`](file:///c:/Users/thris/OneDrive%20-%20iiit-b/Projects/Gridlock/GridLock-R2/scripts/fit_poisson.py)
**Purpose: The first attempt at fitting the Poisson model on all data**

This is where the actual "model training" happens for the first time.

**Step-by-step:**

1. **Grid the city** — GPS coordinates are rounded to 3 decimal places (~100m grid cells):
   ```python
   df['lat_g'] = df['latitude'].round(3)
   df['lon_g'] = df['longitude'].round(3)
   df['grid_id'] = f"({lat_g:.3f}, {lon_g:.3f})"
   ```

2. **Compute PCS** — Each row gets ω × δ × σ

3. **Create a lagged variable (Z_prev)** — For each grid cell, the PCS sum from the *previous* month:
   - November's data becomes December's Z_prev
   - December's data becomes January's Z_prev
   - etc.
   This is a **temporal autocorrelation feature** — if a location was bad last month, it's probably bad this month too.

4. **Group and count** — Aggregate to `(grid_id, month, hour, day_type)` level, counting violations (this becomes `y`, the thing we're predicting)

5. **Fit the GLM:**
   ```python
   model = smf.glm('y ~ C(month) + hour + day_type + Z_prev',
                   data=grouped, family=sm.families.Poisson()).fit()
   ```
   - `C(month)` = month as a categorical (each month gets its own coefficient)
   - `hour`, `day_type` = continuous predictors
   - `Z_prev` = the lagged PCS signal
   - `family=Poisson()` = tells statsmodels we're predicting counts

**What comes out:** The model coefficients (intercept, hour_coef, day_type_coef, Z_prev_coef). These numbers *are* the trained model.

> **Note:** This version uses raw `Z_prev` (linear). A later version (`run_evaluation_v2.py`) improves this to `log(Z_prev + 1)` to handle the skewed distribution better.

---

### Stage 2: Spatial Analysis

---

#### [`spatial_analysis.py`](file:///c:/Users/thris/OneDrive%20-%20iiit-b/Projects/Gridlock/GridLock-R2/scripts/spatial_analysis.py)
**Purpose: Test whether violations cluster in space (Moran's I)**

Before committing to a spatial hotspot model, you need to verify: *do violations actually cluster geographically, or are they randomly scattered?* If they're random, there's no spatial pattern to exploit.

**Moran's I** is a statistical measure of spatial autocorrelation:
- **I ≈ +1**: Strong clustering (violations cluster together)
- **I ≈ 0**: Random
- **I ≈ -1**: Perfect dispersion (violations deliberately avoid each other)

**How it works:**
1. Aggregate quality-weighted PCS (`q_PCS = PCS × p̂`) to grid cells → get `Z_i` per cell
2. Build a **spatial weights matrix** using K-Nearest Neighbors (k=8):
   ```python
   w = lps.weights.KNN.from_array(coords, k=8)
   ```
   Each cell's 8 nearest neighbors are connected. This encodes: "neighboring cells should influence each other."
3. Run **Global Moran's I** → single number for the whole city
4. Run **Local Moran's I (LISA)** → per-cell classification:
   - **HH (High-High)**: Hot cell surrounded by hot neighbors = true hotspot
   - **LL (Low-Low)**: Cold cell surrounded by cold neighbors = true coldspot
   - **HL (High-Low)**: Hot cell surrounded by cold neighbors = isolated spike
   - **LH (Low-High)**: Cold cell surrounded by hot neighbors = embedded in hotspot

The script tests 4 configurations (Nov–Feb, all months except March; with/without a minimum observation threshold).

**Why this matters:** If Moran's I is significantly positive (p < 0.05), it validates that spatial clustering is real — justifying the grid-based hotspot ranking approach.

---

#### [`run_moran_all.py`](file:///c:/Users/thris/OneDrive%20-%20iiit-b/Projects/Gridlock/GridLock-R2/scripts/run_moran_all.py)
**Purpose: Condensed, cleaner version of the Moran's I analysis**

Runs the same Moran's I analysis as `spatial_analysis.py` but more efficiently — directly iterating over the 4 configurations with a named loop. Adds officer quality weighting (`q_weight`) more explicitly:

```python
# Three tiers of officer trust:
if p >= 0.85:   weight = 1.0   # Fully trusted
elif p >= 0.50: weight = p     # Soft-weighted
else:           weight = 0.0   # Excluded entirely
```

Also prints the **Top 15 HH cells** (the most important hotspots) for each configuration.

---

### Stage 3: Generating Predictions

---

#### [`calculate_march_table.py`](file:///c:/Users/thris/OneDrive%20-%20iiit-b/Projects/Gridlock/GridLock-R2/scripts/calculate_march_table.py)
**Purpose: Apply the fitted model to produce a ranked March 2024 prediction table**

This script takes the Poisson model coefficients (hardcoded from a prior run) and applies them to March 2024 data to produce an actionable table.

**What it outputs for each grid cell:**
1. **`predicted_march_volume`** — Model's predicted total violations for March
2. **`top_3_peak_hours`** — The 3 busiest hours observed in March data (e.g., "08:00, 17:00, 09:00")
3. **`mandatory_reviews_pending`** — How many March violations came from officers with p̂ < 0.50 (needs human review)
4. **`soft_weight_records`** — How many came from officers with 0.50 ≤ p̂ ≤ 0.85

The **hardcoded coefficients** used:
```python
Intercept = 1.3897
month_coef = -0.1536
hour_coef = -0.0047
day_type_coef = -0.1148
Z_prev_coef = 0.0243
```

> These came from the original `fit_poisson.py` run. Hardcoding them makes this script reproducible without re-fitting.

Finally, it prints the **Top 10 grid cells** ranked by predicted March volume — the deployment-ready priority list.

---

### Stage 4: Evaluation (Did the Model Actually Work?)

---

#### [`detailed_evaluation.py`](file:///c:/Users/thris/OneDrive%20-%20iiit-b/Projects/Gridlock/GridLock-R2/scripts/detailed_evaluation.py)
**Purpose: First detailed evaluation of EPS_v1 against the April holdout**

This is where we answer: *"If we had used this model in February to predict where to deploy officers in April, would those predictions have been right?"*

**The pipeline:**
1. Train on Nov–Feb, hold out April
2. Compute `Z_i` (quality-adjusted PCS sum per grid)
3. Compute **Persistence Index (PI)**:
   - For each of Dec, Jan, Feb: find the top 50 cells by monthly q_PCS
   - PI = fraction of those 3 months where the cell was in the top 50
   - A cell that was top 50 in all 3 months gets PI = 1.0; one that never made it gets PI = 0.0
4. Use hardcoded Poisson coefficients to predict `pred_weekly_volume` per cell
5. Compute: `EPS_v1 = quality_adjusted_Z × PI × pred_weekly_volume`
6. **Compare the model's Top 20 cells vs. the actual April Top 20 cells**

**Two metrics:**
- **Volume Share**: What % of April's total violations fell inside the predicted Top 20 cells?
- **Stability Count**: How many of the model's Top 20 also appear in the actual April Top 20? (out of 20)

**Versus Baseline:** The baseline is just "rank by raw count in training data" — no model, no weights. A good model should beat this.

---

#### [`detailed_evaluation_v2.py`](file:///c:/Users/thris/OneDrive%20-%20iiit-b/Projects/Gridlock/GridLock-R2/scripts/detailed_evaluation_v2.py)
**Purpose: Improved evaluation — re-fits the model on training data instead of using hardcoded coefficients**

Key improvements over v1:
1. **Re-fits the Poisson model live** on training data (no hardcoded coefficients)
2. Uses **`log(Z_prev + 1)`** instead of raw `Z_prev` — better handles the fact that PCS values are heavily right-skewed
3. Tests **two versions of Z_prev**:
   - **Case A**: Use the average monthly PCS from training (what you'd know before March)
   - **Case B**: Use actual March PCS (what you'd know just before April — more informative)
4. **Simplified EPS formula**: `EPS = PI × pred_weekly_volume` (removes `quality_adjusted_Z` from the product to avoid double-counting, since quality is already baked into PI)

---

#### [`evaluate_holdout.py`](file:///c:/Users/thris/OneDrive%20-%20iiit-b/Projects/Gridlock/GridLock-R2/scripts/evaluate_holdout.py)
**Purpose: The definitive, clean evaluation script — the main benchmark**

This is the most complete and polished evaluation script. It:

1. Fully re-fits the Poisson GLM on training data
2. Extracts and prints all fitted coefficients
3. Runs both Case A and Case B predictions
4. Reports for each:
   - **Volume Share %** — model vs. baseline
   - **Stability Count** — model vs. baseline
   - Per-cell breakdown of the Top 10 predicted cells with their actual April counts

**The structure is cleanest here**, with clearly labelled sections and comparison between the model and the naive baseline. This is the script you'd show in a research paper or to a stakeholder.

---

#### [`run_evaluation_v2.py`](file:///c:/Users/thris/OneDrive%20-%20iiit-b/Projects/Gridlock/GridLock-R2/scripts/run_evaluation_v2.py)
**Purpose: The most modular and step-by-step evaluation — best for debugging**

Essentially the same pipeline as `evaluate_holdout.py` but written in very granular, well-commented steps with print statements at every stage:

```
Loading data...
Grouping training data for Poisson GLM...
Fitting Poisson GLM on train data...
--- Full model summary ---
Calculating Persistence Index...
Predicting weekly volume...
--- EVALUATION USING TRAINING AVERAGE MONTHLY PCS FOR Z_PREV ---
...
```

**Best used when:** Something is going wrong and you need to trace which step is producing incorrect outputs.

---

## Part 4: The Full Pipeline at a Glance

```
Raw Data
    │
    ├─► explore.py            → "What does the data look like?"
    ├─► inspect_types.py      → "What vehicle/violation types exist?"
    ├─► inspect_pcu.py        → "Are PCU weights assigned correctly?"
    └─► explore_officers.py   → "Which officers are reliable?"
    │
    ▼
Feature Engineering (in every downstream script)
    ├─► Grid cells (lat/lon rounded to 3 decimals)
    ├─► PCS = ω × δ × σ
    ├─► p̂ per officer (Bayesian Beta)
    └─► q_PCS = PCS × p̂
    │
    ▼
    ├─► fit_poisson.py         → First model fit (linear Z_prev)
    ├─► spatial_analysis.py    → Is clustering real? (Moran's I)
    └─► run_moran_all.py       → Clean Moran's I across 4 configurations
    │
    ▼
    ├─► calculate_march_table.py → Apply model → ranked March prediction table
    │
    ▼
    ├─► detailed_evaluation.py    → v1 evaluation (hardcoded coefs)
    ├─► detailed_evaluation_v2.py → v2 evaluation (re-fit, log transform)
    ├─► evaluate_holdout.py       → Definitive holdout benchmark
    └─► run_evaluation_v2.py      → Step-by-step debug-friendly version
```

---

## Part 5: Key Design Decisions Explained

| Decision | Why |
|---|---|
| Poisson GLM instead of neural network | Count data (violations) naturally follows a Poisson distribution. Simpler, interpretable, works on small-ish datasets. |
| Bayesian officer quality score | Prevents officers with very few records from appearing artificially perfect or terrible. |
| log(Z_prev + 1) instead of raw Z_prev | PCS values are heavily skewed (a few hotspots have enormous values). Log-transforming compresses the scale. |
| Persistence Index | A location that's consistently in the top 50 is more trustworthy than one that spiked once. |
| Holdout in April (not March) | March is used as the "prior month" input. You can't use April as both input and test. |
| 100m grid cells | Coarse enough to aggregate enough violations per cell for statistical significance; fine enough to be operationally useful to deploy officers. |
