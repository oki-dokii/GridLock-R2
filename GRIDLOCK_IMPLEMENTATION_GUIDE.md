# GridLock — Complete Implementation Guide
### Illegal Parking Intelligence System | Flipkart Hackathon Round 2
> **This document is the single source of truth for building the final award-winning prototype.**
> Cross-references every claim back to the computed results in `DATA_ANALYSIS_RESULTS.md` and the research in `MASTER_RESEARCH_COMBINED.md`.
> Last updated: June 17, 2026.

---

## TABLE OF CONTENTS

1. [System Architecture Overview](#1-system-architecture-overview)
2. [Tech Stack Decision](#2-tech-stack-decision)
3. [Data Pipeline — What to Build First](#3-data-pipeline--what-to-build-first)
4. [Core Algorithm Implementation](#4-core-algorithm-implementation)
5. [Frontend Dashboard — Every Screen](#5-frontend-dashboard--every-screen)
6. [Backend API Design](#6-backend-api-design)
7. [Complete Feature Checklist](#7-complete-feature-checklist)
8. [Team Division of Work (4 Members)](#8-team-division-of-work-4-members)
9. [The "Award-Winning" Differentiators](#9-the-award-winning-differentiators)
10. [Demo Flow for Judges](#10-demo-flow-for-judges)
11. [Numbers to Hard-Code / Highlight](#11-numbers-to-hard-code--highlight)
12. [Common Pitfalls to Avoid](#12-common-pitfalls-to-avoid)

---

## 1. System Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                    GRIDLOCK SYSTEM ARCHITECTURE                  │
└──────────────────────────────────────────────────────────────────┘

RAW DATA LAYER
┌─────────────────────────────────────────────────┐
│  298,450 parking violation records (CSV/Parquet) │
│  Nov 2023 – Apr 2024 | 42 BTP Stations          │
│  Fields: timestamp, lat, lon, vehicle_type,      │
│          violation_type, officer_id, status       │
└──────────────┬──────────────────────────────────┘
               │
               ▼
PREPROCESSING (Module M6 — Officer Quality Filter)
┌─────────────────────────────────────────────────┐
│  Bayesian Beta Filter                            │
│  • 123 officers flagged (p̂ < 0.50) → HOLD       │
│  • 232 officers auto-approved (p̂ ≥ 0.85)        │
│  • 2,022 officers soft-weighted by p̂_o           │
│  Output: quality-weighted violation records      │
└──────────────┬──────────────────────────────────┘
               │
               ▼
SCORING ENGINE (Modules M1 → M4)
┌─────────────────────────────────────────────────┐
│  M1: PCS_k = ω(c_k) × δ(t_k) × σ(s_k)         │
│      Mean=1.015, Max=9.0 (bus+double+peak)       │
│                                                  │
│  M2: Z_i = Σ PCS_k per 110m grid cell           │
│      7,814 cells | Top cell Z_i = 5,918.7        │
│      Moran's I = 0.2785 (p=0.001, CLUSTERED)    │
│      LISA: 495 HH cells = Priority-1             │
│                                                  │
│  M3: Poisson GLM → λ̂(h,d,month,Z_prev)          │
│      AIC=316,091.7 | Z_prev z-score=455          │
│                                                  │
│  M4: M/D/1 Queue → 117 commuter-min/hr/hotspot  │
│      SIR Cascade: ρ≥0.85 infects neighbors       │
└──────────────┬──────────────────────────────────┘
               │
               ▼
DISPATCH ENGINE (Module M5 — EPS)
┌─────────────────────────────────────────────────┐
│  EPS_i = Z_i × PI_i × λ̂ × (1/ρ) × θ            │
│  Top cell EPS_norm = 100.0 (12.981, 77.610)     │
│  16 PI=1.0 cells in top-30 dispatch queue       │
│  Resource: 37 tow trucks, ~500 clamps, ASIs     │
└──────────────┬──────────────────────────────────┘
               │
               ▼
DASHBOARD + API
┌─────────────────────────────────────────────────┐
│  Heatmap | Live Dispatch Queue | LOS Simulator  │
│  Officer Quality Panel | Trend Forecasts        │
│  Revenue Impact | SIR Cascade Visualiser        │
└─────────────────────────────────────────────────┘
```

**The pipeline is: Raw Violations → Quality Filter → PCU Score → Spatial Hotspot → Temporal Forecast → Impact Quantification → Dispatch Queue → Dashboard.**

---

## 2. Tech Stack Decision

### Recommended Stack (Justified)

| Layer | Technology | Why |
|-------|-----------|-----|
| **Backend** | Python (FastAPI) | All analysis already done in Python; statsmodels, esda, scipy already used |
| **Data** | Pandas + GeoPandas + Parquet | 298k rows — parquet is fast; geopandas for spatial ops |
| **Spatial** | PySAL (esda) | Moran's I + LISA already computed here; no need to switch |
| **ML / Stats** | statsmodels (GLM Poisson) | Model already fitted; AIC=316,091 |
| **Frontend** | React + Leaflet.js / Mapbox GL | Interactive heatmap is the centrepiece |
| **Charts** | Recharts or Plotly | Temporal heatmaps, bar charts, LOS gauges |
| **DB** | SQLite (demo) or PostgreSQL | Store precomputed Z_i, EPS scores, officer quality |
| **Deployment** | Docker + localhost or Railway.app | For demo; no need for full cloud |

> **If demo is a Jupyter Notebook**: Use Folium for maps, Plotly for charts, ipywidgets for interactive inputs. This is the fastest path if time is short.

> **If demo is a web app**: FastAPI backend + React frontend. Use the precomputed `DATA_ANALYSIS_RESULTS.md` numbers as static data to avoid re-running the full analysis live.

---

## 3. Data Pipeline — What to Build First

Build these in order. Each step's output feeds the next.

### Step 0: Data Ingestion & Cleaning
```python
# What to do:
# 1. Load the 298,450-row CSV
# 2. Parse timestamps → extract: hour, day_of_week, month, day_type (weekday/weekend)
# 3. Snap lat/lon to 110m grid cells (round to 3 decimal places: lat_g, lon_g)
# 4. Map vehicle_type → vehicle_class → PCU weight ω(c)
# 5. Map violation_type → σ(s) severity weight
# 6. Map hour → δ(t) temporal multiplier
# 7. Compute PCS_k = ω × δ × σ for each record
```

**PCU Weights ω(c):**
- SCOOTER / MOTOR CYCLE / MOPED → **0.5**
- CAR / PASSENGER AUTO / JEEP → **1.0**
- MAXI-CAB / LGV / TEMPO / VAN → **1.5**
- BMTC BUS / PRIVATE BUS / LORRY / HGV / TANKER → **3.0**

**Temporal Multipliers δ(t):**
- 08:00–12:00 & 17:00–20:00 → **1.5**
- 12:00–17:00 → **1.2**
- 20:00–08:00 → **0.8**

**Violation Severity σ(s):**
- DOUBLE PARKING → **2.0**
- NEAR ROAD CROSSING / JUNCTION → **1.8**
- PARKING ON MAIN ROAD → **1.6**
- NEAR BUS STOP / ZEBRA CROSSING → **1.4**
- FOOTPATH PARKING → **1.2**
- WRONG / NO PARKING (general) → **1.0**

---

### Step 1: Officer Quality Filter (M6)
```python
# Bayesian Beta Filter
# Prior: α₀=5, β₀=2 (reflects 67% city-wide approval baseline)
# For each officer o:
#   p̂_o = (α₀ + A_o) / (α₀ + β₀ + A_o + R_o)
# Tiers:
#   p̂ ≥ 0.85 → auto-approved (232 officers)
#   0.50 ≤ p̂ < 0.85 → weight record by p̂_o (2,022 officers)
#   p̂ < 0.50 → HOLD for manual review (123 officers, 20,349 records)
# Apply weights: effective_PCS_k = PCS_k × p̂_o (for soft-weighted tier)
```

**Known worst officers to flag:** FKUSR01810 (p̂=0.128), FKUSR02046 (p̂=0.163), FKUSR01593 (p̂=0.171)

---

### Step 2: Grid Cell Aggregation (Z_i)
```python
# Group by (lat_g, lon_g):
#   total_PCS = Σ effective_PCS_k
#   raw_count = count of records
#   avg_PCS = total_PCS / raw_count
#   peak_violations = count where hour in [8,9,10,11]
#   heavy_vehicle_pcu = Σ PCS where ω=3.0

# Top cell (12.981, 77.610): Z_i = 5,918.7, raw_count = 4,411
```

---

### Step 3: Spatial Analysis (M2)
```python
# Moran's I (already computed: I=0.2785, p=0.001)
# LISA classification (already computed):
#   HH = 495 cells → Priority-1 Permanent Post
#   HL = 305 cells → Monitor/Surge
#   LH = 674 cells → Cascade Risk
#   LL = 2,595 cells → No Action
# You can use precomputed values — no need to rerun esda in demo
```

---

### Step 4: Persistence Index (PI)
```python
# For each grid cell, across 4 full months (Dec 2023 – Mar 2024):
#   Rank the cell within that month's Top-50
#   m_i = number of months it appeared in Top-50
#   PI_i = m_i / 4
# Results:
#   PI=1.0 → 20 cells (Chronic) ← THESE ARE YOUR HERO CELLS
#   PI=0.75 → 15 cells
#   PI=0.50 → 19 cells
#   PI=0.25 → 37 cells
#   PI=0.00 → 7,723 cells
```

---

### Step 5: Poisson GLM Forecast (M3)
```python
# Formula: log(λ_i,h,d) = 1.3897 + (-0.0047)*h + (-0.1148)*day_type 
#          + month_coefficients + (0.0243)*Z_prev
# 
# For real-time forecasting: take Z_i from same hour last week as Z_prev
# Output: λ̂_i,h,d = predicted violation count at cell i at hour h on day d
#
# You can pre-compute λ̂ for 24h × 7days matrix and serve as a lookup table
# Peak enforcement window: 09:45–11:30 IST (confirmed by hourly distribution)
```

---

### Step 6: EPS Ranking (M5)
```python
# EPS_i = Z_i × PI_i × (λ̂_i,h,d + 1) × (1/ρ) × θ_i
#
# ρ (utilization) = (λ̂_peak × L_v) / (S₀ × L_lane)
#   S₀ = 1800 PCU/hr, L_lane = 100m, L_ref = 4.5m
#   α = 1.3 → S_eff = S₀ × (1 - L_v/L_lane)^α
#   ρ = λ_background / S_eff (λ_background = 1400 PCU/hr at peak)
#
# θ_i = e^(-κ × d(i, r*))
#   κ calibrated: 5km → θ ≈ 0.4
#   For demo: use distance to nearest of 42 BTP stations
#
# Top cell: (12.981, 77.610), EPS_norm = 100.0
# Dispatch threshold: ρ ≥ 0.70
```

---

## 4. Core Algorithm Implementation

### 4.1 Features A–K (The Impact Engine)

Each violation gets scored through this chain before entering Z_i:

```
Raw Violation
     │
     ▼ Feature A: Maneuver Friction
PCS_static = PCU_weight × temporal_multiplier × violation_severity
Total_A = PCS_static × (1 + M_f)
  M_f: Scooter=0.1, Car/Auto=0.5, Van/LGV=0.8, Bus/Truck=1.5
     │
     ▼ Feature B: Intersection Proximity
Total_B = Total_A × W_intersection
  W: ≤100m from junction → 1.5×, 100-200m → 1.25×, >200m → 1.0×
  (50.45% of dataset is AT a named junction — massive amplifier)
     │
     ▼ Feature D: Temporal Ripple
Total_D = Total_B × F_temporal
  F: 10AM-12PM → 2.0×, 8-10AM/5-8PM → 1.5×, 12-5PM/8-11PM → 1.0×, night → 0.3×
     │
     ▼ Feature E: Carriageway Constraint
Total_E = Total_D × C_road
  C: Narrow market streets (Chickpet, City Market) → 1.8×
     Arterial/IT corridors → 1.3×, Wide multi-lane → 1.0×
     │
     ▼ Feature F: Unpredictability Index
Total_F = Total_E × P_random
  P: Near zebra/traffic light → 1.7×, Road crossing → 1.6×
     Double parking → 1.5×, Main road → 1.4×, Standard → 1.0×
     │
     ▼ FINAL IMPACT SCORE per violation
```

> **Note for demo:** You don't need to re-run all of this from scratch. The Z_i scores in `DATA_ANALYSIS_RESULTS.md` (P1.2) are the ground truth. Features A–K are the *explanatory framework* for your dashboard — show them as the "why this cell scores what it does" breakdown.

### 4.2 LOS Simulator (Feature C)
```python
# HCM Level of Service from intersection delay
β = 0.45  # seconds per PCU (calibrated from VISSIM Malaysia study)
baseline_delay = 34.0  # seconds (LOS C baseline)
pcu_load = sum(PCS_k for k in cell_violations_at_peak)
adjusted_delay = baseline_delay + (β × pcu_load)

LOS_grades = {
    (0, 10.0): 'A',      # Free Flow
    (10.0, 20.0): 'B',   # Stable
    (20.0, 35.0): 'C',   # Noticeable Delay
    (35.0, 55.0): 'D',   # Saturated
    (55.0, 80.0): 'E',   # Unstable
    (80.0, float('inf')): 'F'  # GRIDLOCK
}
# Example: Top hotspot (Z_i=5918) → ~50+ PCU daily → LOS D or E
```

### 4.3 SIR Cascade (Feature G context)
```python
# For visualisation only — show congestion propagation
# Parameters from Paper 7 (IET ITS, 2024):
β_spread = 0.3    # transmission rate
γ = 0.1           # recovery rate
threshold = 0.85  # ρ ≥ 0.85 triggers cascade

# At each timestep:
# If ρ_i ≥ threshold:
#   For each adjacent cell j in N(i):
#     dI_j/dt += β_spread × S_j × (I_i / |N(i)|) - γ × I_j
# 
# Key message: Failing to enforce at hotspot i at 9:30 AM
# means by 10:15 AM, 3 adjacent cells are infected.
```

### 4.4 Commuter-Minutes Lost (Pitch Number)
```python
# M/D/1 Queue (Paper 5, Yue 2022)
S0 = 1800        # PCU/hr/lane (IRC standard)
lambda_bg = 1400 # background demand PCU/hr
L_ref = 4.5      # car length (m)
L_lane = 100.0   # segment length (m)
alpha = 1.3      # calibration exponent

avg_daily_pcu = Z_i / num_days  # daily PCU load for this cell
L_v = avg_daily_pcu * L_ref

S_eff = S0 * (1 - L_v/L_lane)**alpha  # → 1695 PCU/hr for top cell
rho = lambda_bg / S_eff               # → 0.826

W = rho / (2 * S_eff * (1 - rho))    # avg delay seconds/vehicle → 5.0s
D_total = W * lambda_bg * 3600        # vehicle-seconds
commuter_min_lost = D_total / 60      # → 117 commuter-min/hr

# HEADLINE: 20 chronic cells × 117 = 2,340 commuter-min/hr
# = 39 person-hours of productivity lost EVERY morning
```

---

## 5. Frontend Dashboard — Every Screen

### Screen 1: Live Command Dashboard (Main View)
**Purpose:** The "wow" opening view for judges.

**Elements:**
- **Full-screen Leaflet/Mapbox map** of Bengaluru with:
  - Colour-coded heatmap overlay (green → yellow → orange → red) based on Z_i
  - 20 chronic PI=1.0 hotspots highlighted with pulsing red markers
  - 495 HH (LISA) cells shown as red polygons
  - Tow truck position indicators (37 trucks, positioned at nearest BTP station)
  - Clickable cells → popup with: Z_i, PI, EPS_norm, LOS grade, commuter-min lost/hr

- **Real-time dispatch queue panel (right sidebar):**
  - Ranked list of top-10 cells by current-hour EPS
  - Each entry shows: location, Z_i, EPS_norm, recommended action (tow truck / clamp team)
  - "Deploy" button (visual only for demo)

- **Header stats strip:**
  - Total violations today (predicted by GLM)
  - City-wide commuter-minutes being lost right now
  - Active hotspots (ρ ≥ 0.70)
  - Tow trucks available

- **Current hour indicator** with colour (red = 08:00–12:00 peak)

---

### Screen 2: Hotspot Intelligence Explorer
**Purpose:** Deep-dive for a single hotspot — for judges who ask "how does it work?"

**Elements:**
- Select a hotspot from dropdown or click on map
- **Score breakdown panel:** PCU weight | Temporal multiplier | Violation type severity | Intersection proximity | Final Z_i
- **Monthly persistence chart:** Bar chart showing cell's Z_i score for Dec'23 → Mar'24 (4 months). Shows PI=1.0 cells are consistently in top-50
- **Violation type breakdown:** Donut chart (Wrong Parking 55%, No Parking 46%, etc.)
- **Vehicle type breakdown:** Bar chart (Scooter 31.78% count vs 18.64% congestion impact — this gap IS the innovation)
- **Peak hour chart:** Hourly violation count for this specific cell
- **LOS Simulator widget:** Interactive slider for PCU load → shows LOS grade changing from B → C → D → F

---

### Screen 3: Temporal Intelligence
**Purpose:** Show the GLM prediction model is actually useful.

**Elements:**
- **24-hour violation density chart** (from Section 10.6): annotated with enforcement windows
  - Mark 09:45–11:30 as "🔴 Priority Deployment Window"
- **Station × Hour heatmap** (from Section P2.2): colour-coded grid (10 stations × 14 hours)
  - Shivajinagar H10 = 4,997 (darkest red)
  - Upparpet H09 = 4,632
- **Day-of-week breakdown:** Sunday=50,162 vs Monday=34,680 (lowest)
- **GLM Forecast toggle:** Switch between "observed" and "predicted" — show the model tracks real data well
- **Prediction for next 24h:** Bar chart of predicted hotspot intensity by hour

---

### Screen 4: Officer Quality Dashboard
**Purpose:** Show the data integrity problem and your Bayesian solution.

**Elements:**
- **Scatter plot:** Officers ranked by p̂_o (x-axis) vs total records submitted (y-axis)
  - Colour: green (auto-approve) / yellow (soft-weight) / red (manual review)
  - Annotate: FKUSR01810 (p̂=0.128), FKUSR02046 (p̂=0.163)
- **Summary stats cards:**
  - 123 officers flagged → 20,349 records held
  - 232 officers auto-approved → ~32,000 records fast-tracked
  - Without filter: 42% of dataset unreviewed → phantom hotspots
- **Station rejection rate heatmap:** Kodigehalli (39.9%) vs lowest stations
- **Before / After comparison:** Show how hotspot map changes when you apply vs. remove quality filter (this is very powerful)

---

### Screen 5: Impact Quantification & Revenue
**Purpose:** Make the business case.

**Elements:**
- **Commuter Impact panel:**
  - "Each chronic hotspot wastes **117 commuter-min/hr** at peak"
  - "All 20 chronic cells = **39 person-hours** of lost productivity every morning"
  - "Resolving one hotspot restores **500 vehicles/hr** outer lane capacity"
  - "Queue delay cut by **105 seconds** per resolved event" (Yue 2022)

- **Revenue calculator:**
  - Potential: ₹37.87 Cr (5 months full dataset)
  - Realistic (67% approval × 60% collection): **₹15.23 Cr / 5 months**
  - Annual: **₹36.5 Cr/year**
  - Show fine breakdown: Two-wheelers ₹13.79 Cr | Cars ₹19.77 Cr | Heavy ₹4.32 Cr

- **Pareto efficiency chart:**
  - X-axis: % of locations targeted
  - Y-axis: % of violations covered
  - Mark: "1,092 locations (10%) → 80% of violations covered"
  - Call this out: "8–10× efficiency gain vs. uniform patrol"

- **SIR Cascade animation:** Show congestion spreading from one saturated hotspot to adjacent cells at ρ≥0.85 (animated over time)

---

### Screen 6: Enforcement Dispatch Console
**Purpose:** The operational output — what BTP actually uses.

**Elements:**
- **Time input:** Set current time (defaults to "now") — EPS recalculates in real-time
- **Resource input:** Number of available tow trucks + clamp teams (defaults: 37 trucks, 500 clamps)
- **Dispatch queue table** (top-20 cells):
  | Rank | Location Name | EPS Score | Action | Vehicle | Time Window | Est. Violations | Est. Min Saved |
  |------|--------------|-----------|--------|---------|-------------|-----------------|----------------|
  | 1 | Kamaraj Road, Sri Nagamma Devi Circle | 100.0 | Tow + Fine | 1 truck + 2 ASI | 09:45-12:00 | 18-22 | 3,100 |
  
- **One-click PDF/print dispatch order** (pre-formatted like BTP drives)
- **Resource allocation map:** Shows which truck covers which zone with route drawn

---

## 6. Backend API Design

### Core Endpoints

```
GET  /api/hotspots
     → Returns all 7,814 grid cells with Z_i, PI, LISA class, EPS
     Query params: min_pi=0.75 | lisa=HH | min_z=1000

GET  /api/hotspots/{lat_g}/{lon_g}
     → Full detail for a single cell (all scores, history, feature breakdown)

GET  /api/dispatch?hour={h}&day_type={d}&trucks={n}
     → Returns top-K dispatch queue ranked by EPS for current parameters

GET  /api/officers
     → All 2,377 officers with p̂_o, tier, total records

GET  /api/temporal?station={name}&hour_from={h}&hour_to={h2}
     → Station × hour violation matrix (for heatmap)

GET  /api/forecast?lat_g={l}&lon_g={g}&hour={h}&day_type={d}
     → GLM prediction: λ̂ for next N hours

GET  /api/impact/{lat_g}/{lon_g}
     → M/D/1 queue computation: commuter-min lost, LOS grade, capacity restored

GET  /api/cascade/{lat_g}/{lon_g}
     → SIR model: which cells are at risk if this hotspot is not resolved

GET  /api/revenue
     → Revenue projection breakdown by vehicle class

GET  /api/stats/summary
     → City-wide summary: chronic cells, HH cells, total violations, commuter loss
```

---

## 7. Complete Feature Checklist

> **Legend:** 🔴 Critical (must-have for demo) | 🟡 High (strong differentiator) | 🟢 Good (polish)

### Data & Model

- [ ] 🔴 Load + clean 298,450 violation records
- [ ] 🔴 Officer Quality Bayesian Filter (M6): compute p̂_o for all 2,377 officers, flag 123
- [ ] 🔴 PCS scoring (M1): PCU × temporal × violation severity per record
- [ ] 🔴 Grid cell aggregation: Z_i scores for 7,814 cells at 110m resolution
- [ ] 🔴 Persistence Index (PI): classify 20 chronic PI=1.0 cells
- [ ] 🔴 LISA classification: identify 495 HH (Priority-1) cells
- [ ] 🔴 Poisson GLM (M3): fit model, extract coefficients, generate hourly λ̂ lookup table
- [ ] 🔴 EPS ranking (M5): top-30 dispatch queue with normalized scores
- [ ] 🟡 M/D/1 queue: commuter-min lost per hotspot at peak (117 min/hr)
- [ ] 🟡 LOS Calculator: adjusted delay → LOS grade (A–F) per cell
- [ ] 🟡 SIR Cascade model: propagation simulation (for animation only)
- [ ] 🟡 Features A–K: full impact score decomposition per violation
- [ ] 🟡 Moran's I: confirm I=0.2785 and surface it in UI (spatial legitimacy)
- [ ] 🟢 KD-Tree proximity: junction proximity distances for intersection multiplier (B)
- [ ] 🟢 Revenue projection: breakdown by vehicle class (₹37.87 Cr potential)

### Frontend Dashboard

- [ ] 🔴 Leaflet/Mapbox interactive map centred on Bengaluru
- [ ] 🔴 Heatmap overlay: Z_i-based colour gradient (green → red)
- [ ] 🔴 20 PI=1.0 chronic hotspots: pulsing red markers
- [ ] 🔴 495 LISA-HH cells: red polygon overlay
- [ ] 🔴 Clickable cell popup: Z_i, PI, EPS, LOS, commuter-min lost, recommended action
- [ ] 🔴 Live dispatch queue panel: top-10 cells ranked by current-hour EPS
- [ ] 🔴 Header stats strip: violations today, city commuter-minutes lost, active hotspots
- [ ] 🟡 Score breakdown panel: show how a cell's Z_i is composed (features A–K)
- [ ] 🟡 Monthly persistence chart: 4-month Z_i trend for each cell
- [ ] 🟡 Vehicle vs. congestion gap chart: raw count % vs PCU footprint % (the "invisible" insight)
- [ ] 🟡 Station × Hour heatmap grid (P2.2): 10 stations × 14 hours
- [ ] 🟡 24-hour violation density chart: annotated with deployment windows
- [ ] 🟡 Officer quality scatter plot: p̂_o vs total records (colour-coded by tier)
- [ ] 🟡 Before/After map: with vs. without quality filter applied
- [ ] 🟡 LOS Simulator widget: interactive PCU slider → LOS grade update
- [ ] 🟡 SIR cascade animation: congestion spreading from one hotspot
- [ ] 🟡 Revenue breakdown donut chart
- [ ] 🟡 Pareto efficiency curve: % locations vs % violations
- [ ] 🟡 Dispatch console: time/resource inputs, downloadable dispatch order
- [ ] 🟢 Day-of-week bar chart: Sunday (50,162) vs Monday (34,680)
- [ ] 🟢 Monthly trend: Nov 2023 → Apr 2024 with GLM overlay
- [ ] 🟢 Station rejection rate heatmap
- [ ] 🟢 GLM "observed vs predicted" toggle on temporal charts
- [ ] 🟢 Fine calculator: how much revenue one dispatch session earns

### Backend API

- [ ] 🔴 /api/hotspots — all cells with full scores
- [ ] 🔴 /api/dispatch — real-time EPS queue
- [ ] 🟡 /api/hotspots/{lat}/{lon} — cell detail
- [ ] 🟡 /api/impact/{lat}/{lon} — commuter impact
- [ ] 🟡 /api/temporal — station × hour matrix
- [ ] 🟡 /api/forecast — GLM prediction
- [ ] 🟡 /api/officers — officer quality data
- [ ] 🟢 /api/cascade — SIR propagation
- [ ] 🟢 /api/revenue — projection breakdown
- [ ] 🟢 /api/stats/summary — city-wide summary

### Demo & Presentation

- [ ] 🔴 Pre-loaded demo with all computed numbers (no live data run needed)
- [ ] 🔴 Demo script: 3-minute walkthrough hitting the 5 key moments (see Section 10)
- [ ] 🔴 All 17 paper citations surfaced in UI (hover tooltips on stats)
- [ ] 🔴 Operationally realistic dispatch output format (matches BTP workflow)
- [ ] 🟡 "Before GridLock vs. After GridLock" comparison slide in UI
- [ ] 🟡 Mobile-responsive layout (judges may view on phone)
- [ ] 🟢 Dark mode / light mode toggle
- [ ] 🟢 Loading animation / skeleton screens

---

## 8. Team Division of Work (4 Members)

> Each person owns a clear domain. Interfaces are defined below to prevent conflicts.

---

### 👤 Person 1 — Data Engineer & Model Lead

**Own:** The entire pipeline from raw CSV → precomputed JSON/Parquet that the API serves.

**Tasks:**
- [ ] Data cleaning script: parse timestamps, map vehicle/violation types, compute PCU weights
- [ ] Officer Quality Filter (M6): Bayesian Beta computation for all 2,377 officers
- [ ] PCS scoring (M1): implement formula, validate against `DATA_ANALYSIS_RESULTS.md` P1.1 (mean=1.015)
- [ ] Grid cell aggregation: Z_i for 7,814 cells, validate top cell = 5,918.7
- [ ] Persistence Index (PI): 4-month Top-50 membership, validate 20 PI=1.0 cells
- [ ] Moran's I + LISA: re-run esda, validate I=0.2785 and 495 HH cells
- [ ] Poisson GLM: re-run statsmodels, validate AIC=316,091.7, Z_prev coeff=0.0243
- [ ] EPS ranking (M5): full formula, validate top cell EPS_norm=100.0
- [ ] Export: all results to JSON files (hotspots.json, officers.json, temporal.json, dispatch.json)
- [ ] M/D/1 queue computation: commuter-min lost for top-20 cells

**Deliverables:**
- `pipeline/data_processor.py`
- `pipeline/model.py`
- `data/hotspots.json` — all 7,814 cells with Z_i, PI, LISA, EPS
- `data/officers.json` — 2,377 officers with p̂_o, tier
- `data/temporal.json` — station × hour matrix
- `data/dispatch.json` — top-30 ranked cells with full EPS breakdown

**Interface contract (for Person 2):**
```json
// hotspots.json entry format:
{
  "lat_g": 12.981, "lon_g": 77.610,
  "z_i": 5918.68, "raw_count": 4411, "avg_pcs": 1.342,
  "peak_violations": 2883, "heavy_vehicle_pcu": 207.0,
  "pi": 1.0, "lisa": "HH",
  "eps_norm": 100.0, "rho": 0.94, "lambda_peak": 710,
  "commuter_min_lost_hr": 117, "los_grade": "E",
  "recommended_action": "Deploy 1 tow truck + 2 ASI (09:45–12:00)"
}
```

---

### 👤 Person 2 — Backend API Developer

**Own:** FastAPI server that serves the precomputed data from Person 1's JSON files.

**Tasks:**
- [ ] FastAPI project setup, CORS, routing
- [ ] Load JSON data files into memory at startup (no live computation needed)
- [ ] `GET /api/hotspots` with query params (min_pi, lisa, min_z, min_eps)
- [ ] `GET /api/hotspots/{lat_g}/{lon_g}` — cell detail + feature breakdown
- [ ] `GET /api/dispatch?hour={h}&day_type={d}&trucks={n}` — filtered EPS queue
- [ ] `GET /api/temporal?station={name}` — station × hour matrix slice
- [ ] `GET /api/officers?tier={tier}` — officer list with filters
- [ ] `GET /api/impact/{lat_g}/{lon_g}` — commuter impact data
- [ ] `GET /api/stats/summary` — city-wide aggregates
- [ ] `GET /api/cascade/{lat_g}/{lon_g}` — return list of at-risk neighbour cells
- [ ] `GET /api/revenue` — revenue projection
- [ ] Write OpenAPI spec so Person 3 can develop frontend in parallel
- [ ] Deploy locally (uvicorn) with auto-reload

**Deliverables:**
- `backend/main.py` — FastAPI app
- `backend/routers/` — separate routers per domain
- `backend/models.py` — Pydantic response schemas
- Running on `http://localhost:8000`

**Interface contract (for Person 3):**
```
Base URL: http://localhost:8000
CORS: allow all origins (for demo)
Response format: JSON always
Docs: http://localhost:8000/docs (Swagger UI auto-generated)
```

---

### 👤 Person 3 — Frontend Developer (Map & Charts)

**Own:** The React dashboard. Map + all chart screens.

**Tasks:**
- [ ] React project setup (Vite + React + Leaflet.js + Recharts)
- [ ] App routing: 6 screens (Command, Explorer, Temporal, Officer, Impact, Dispatch)
- [ ] **Screen 1 — Live Command Dashboard:**
  - Leaflet map centred on Bengaluru (12.97, 77.59, zoom 12)
  - Heatmap overlay using `leaflet.heat` from Z_i scores
  - 20 PI=1.0 markers (pulsing CSS animation)
  - Cell click → popup with full stats
  - Right sidebar dispatch queue (top-10 by EPS)
  - Header stats strip
- [ ] **Screen 2 — Hotspot Explorer:**
  - Dropdown to select hotspot
  - Score breakdown: donut chart (PCU / temporal / violation type contributions)
  - Monthly bar chart (4-month PI trend)
  - Vehicle count vs congestion footprint: side-by-side bar chart
  - Peak hour line chart for the cell
- [ ] **Screen 3 — Temporal:**
  - 24-hour area chart (annotated)
  - Station × Hour heatmap grid (use CSS grid or Recharts)
  - Day-of-week bar chart
- [ ] **Screen 4 — Officer Quality:**
  - Scatter plot (Recharts): p̂_o vs total records
  - 3 stat cards (123/232/2022 split)
  - Station rejection rate horizontal bar chart
- [ ] **Screen 5 — Impact:**
  - Commuter impact stats (animated counters)
  - Revenue donut chart (3 vehicle classes)
  - Pareto curve (area chart)
  - SIR cascade animation (CSS/Canvas based)
- [ ] **Screen 6 — Dispatch Console:**
  - Time + resource input form
  - Ranked dispatch table
  - Print/PDF button

**Tech notes:**
- Use **Leaflet.js** (not Google Maps — no API key needed for demo)
- Use **leaflet-heat** for heatmap layer
- Use **Recharts** for all non-map charts
- Fetch from `http://localhost:8000/api/...`
- Hard-code fallback data from JSON files if API is down (for demo safety)

---

### 👤 Person 4 — UX, Presentation & Research Validation

**Own:** Everything that makes it look award-winning and academically credible.

**Tasks:**

**Design system:**
- [ ] Define colour palette: dark background (#0f1117), accent red (#FF3B30), green (#34C759), amber (#FF9500)
- [ ] Typography: Inter or Outfit (Google Fonts) for headers, JetBrains Mono for numbers
- [ ] Component library: cards, badges (LOS grade badges), status indicators
- [ ] Responsive layout (support 1280px+ and tablet)
- [ ] CSS animations: pulsing markers, SIR cascade, counter animations, loading states

**Citation overlay system:**
- [ ] Every key stat in the UI has a (ⓘ) hover tooltip citing the paper it comes from
  - "50% capacity loss" → "ResearchGate, 2024 (Paper 1)"
  - "30% of CBD traffic is cruising" → "Shoup 2006 (Paper 8)"
  - "117 commuter-min/hr" → "M/D/1 queue model, Yue 2022 (Paper 5)"
  - "PI=1.0: 20 cells" → "Dataset analysis: Dec'23–Mar'24"
- [ ] Full citation panel accessible from footer

**Narrative & copy:**
- [ ] Write the text for each dashboard card (must be crisp and impactful)
  - e.g., "39 person-hours of productivity wasted every morning across 20 hotspots"
  - e.g., "Targeting 10% of locations resolves 80% of violations"
- [ ] Operationally realistic dispatch output text (BTP format)
- [ ] "Before GridLock / After GridLock" comparison panel text

**Demo script (3-minute run):**
- [ ] Practice the 5-moment demo flow (Section 10 below)
- [ ] Prepare answers to top-5 judge questions (Section 12 below)

**Validation:**
- [ ] Cross-check all numbers in the UI against `DATA_ANALYSIS_RESULTS.md`
- [ ] Ensure no number on any screen contradicts any other screen
- [ ] Test that all 17 paper citations are referenced somewhere in the UI

---

## 9. The "Award-Winning" Differentiators

These are the things that separate a good prototype from an award-winning one. Do not skip these.

### 1. The PCU "Hidden Impact" Reveal
**The moment:** Show that scooters are 31.78% of raw violations but only 18.64% of congestion footprint — while cars at 29.78% cause 34.92%. This is counterintuitive and memorable.
**Implementation:** Side-by-side bar chart. Label it: "What raw dashboards show" vs "What actually matters."

### 2. The Officer Quality Problem
**The moment:** Show that 123 officers have >50% rejection rates and their records are corrupting the hotspot map. Show the before/after map.
**Implementation:** Screen 4. The "phantom hotspot" concept is genuinely novel and shows deep data literacy.

### 3. The 0.26% Insight
**The moment:** "20 cells out of 7,814 — 0.26% of the city — are chronically responsible for a disproportionate share of congestion. GridLock targets these 20 cells. Current patrol covers all 7,814."
**Implementation:** Large counter: "20 / 7,814" with the fraction displayed prominently.

### 4. Real Dispatch Output
**The moment:** Show that the system outputs something a BTP officer could actually act on TODAY.
**Implementation:** Dispatch console with the exact BTP-formatted recommendation: "Deploy 1 towing vehicle + 1 ASI to [Location] between [Time]. Expected 18–22 violations. Estimated 3,100 commuter-minutes saved."

### 5. The Cascade Visualisation
**The moment:** Animate congestion spreading from one saturated hotspot to adjacent cells in real-time.
**Implementation:** SIR model animation on the map. This is visually striking and backed by Paper 7.

### 6. Live LOS Grade Change
**The moment:** In the Hotspot Explorer, drag the PCU slider and watch the LOS badge change from B → C → D → F in real-time.
**Implementation:** Feature C. Uses HCM standard. Judges who know traffic engineering will immediately recognise this as legitimate.

---

## 10. Demo Flow for Judges

**Total time: 3 minutes. Practice this until it's smooth.**

### Moment 1 — The Problem (30 seconds)
> Open Screen 1 (Live Command Dashboard).
> "Bengaluru has 298,450 parking violations in 5 months. But 42% are unreviewed and 29% are rejected. BTP has 37 tow trucks for 42 stations. They have no idea which 154 hotspots to hit first, or when."

### Moment 2 — The Hidden Insight (45 seconds)
> Click on a chronic PI=1.0 hotspot marker.
> "This cell at Kamaraj Road — 4,411 raw violations. But raw count hides the truth."
> Switch to Hotspot Explorer → show the vehicle vs congestion gap chart.
> "Cars are only 30% of violations but 35% of congestion. Scooters are 32% of violations but only 19% of actual road blockage. Our PCS score captures this. A scooter off-peak scores 0.4. A bus double-parked at peak scores 9.0. That's a 22.5× difference — completely invisible to a count-based dashboard."

### Moment 3 — The Data Quality Problem (30 seconds)
> Switch to Officer Quality screen.
> "Before we use any of this data, we run it through a Bayesian quality filter. 123 officers have >50% rejection rates. Officer FKUSR01810 has a 12.7% approval rate. Without filtering, his 39 records create phantom hotspots. We hold 20,349 records for review and weight the rest by officer reliability."

### Moment 4 — The Cascade (20 seconds)
> Switch back to map, trigger cascade animation.
> "Not enforcing at 9:30 AM means by 10:15 AM, congestion has cascaded to 3 adjacent cells. Early intervention is exponentially more valuable. This is Paper 7's SIR epidemic model applied to traffic networks."

### Moment 5 — The Output (45 seconds)
> Open Dispatch Console. Set time to 09:45 AM, weekday.
> "GridLock outputs what BTP can act on right now. Rank 1: Kamaraj Road, EPS score 100. Deploy 1 tow truck + 2 officers, 09:45–12:00. Expected 18–22 violations. This resolves **117 commuter-minutes of lost productivity per hour**. Scale to all 20 chronic cells: 39 person-hours saved every single morning. At the current fine rate, that's ₹36.5 crore per year in realised enforcement revenue with 8–10× fewer patrol-hours than city-wide patrol."

---

## 11. Numbers to Hard-Code / Highlight

These are your most impactful stats. Memorise them. Display them prominently.

| Stat | Value | Source |
|------|-------|--------|
| Total violations in dataset | **298,450** | Dataset |
| Unreviewed backlog | **42% (125,254)** | Dataset |
| Rejection rate | **29% (49,754)** | Dataset |
| Top cell Z_i | **5,918.7** | P1.2 |
| Moran's I | **0.2785 (p=0.001)** | P1.3 |
| HH (Priority-1) cells | **495** | P1.4 |
| PI=1.0 chronic cells | **20** | P3.2 |
| Commuter-min lost/hr (per hotspot) | **117** | P3.1 |
| Total city-wide per morning | **39 person-hours** | Computed |
| 80% violations covered by | **10% of locations (1,092)** | Section 1.5 |
| Officers flagged (p̂<0.50) | **123 officers, 20,349 records** | P1.6 |
| Capacity loss from illegal parking | **50%** | Paper 1 |
| CBD cruising overhead | **30% of traffic** | Paper 8 (Shoup) |
| VISSIM delay reduction | **20–21%** | Paper 13 |
| KNN accuracy on police data | **99%** | Paper 12 |
| Revenue potential | **₹37.87 Cr / 5 months** | P3.3 |
| Realistic annual revenue | **₹36.5 Cr/year** | P3.3 |
| Efficiency gain | **8–10× vs. uniform patrol** | Section 1.5 |
| EPS top cell | **EPS_norm = 100.0** | P1.7 |
| Scooter PCU footprint gap | **31.78% count → 18.64% congestion** | Section 1.2 |
| Car PCU amplification | **29.78% count → 34.92% congestion** | Section 1.2 |
| Heavy vehicle amplification | **1.74% count → 6.11% congestion (3.5×)** | Section 1.2 |

---

## 12. Common Pitfalls to Avoid

### Technical
- ❌ **Don't run the full Moran's I / LISA live during demo** — precompute and serve from JSON. It's slow.
- ❌ **Don't show raw count heatmaps** — always show Z_i (PCS-weighted). Raw count is the old way.
- ❌ **Don't forget the officer filter** — it's one of the strongest differentiators and is trivially removable, making the dataset wrong.
- ❌ **Don't hardcode only 1 city zone** — make the map show all 42 stations' areas.

### Presentation
- ❌ **Don't say "we detect illegal parking"** — you don't use cameras. You use GPS violation records + ML. Say "we predict and prioritise enforcement."
- ❌ **Don't use "we" for the FHWA or any paper result** — cite sources explicitly.
- ❌ **Don't present the revenue number without caveats** — always say "at 67% approval, 60% collection rate, realistic estimate: ₹15.23 Cr / 5 months."
- ❌ **Don't leave the officer quality screen for last** — it's a credibility anchor. Show it early.

### Scope
- ❌ **Don't try to build real-time camera integration** — out of scope for this hackathon. The system uses historical + predicted data.
- ❌ **Don't try to do route optimisation** — the dispatch queue + θ_i (distance-to-station) is sufficient.
- ❌ **Don't build a mobile app** — responsive web is enough.

---

## Appendix A — Key Grid Cells for Demo

Pre-load these specific cells for the demo. They are the most compelling.

| Cell | lat | lon | Z_i | PI | EPS_norm | Story |
|------|-----|-----|-----|----|----------|-------|
| **Kamaraj Road, Shivajinagar** | 12.981 | 77.610 | 5,918.7 | 1.00 | 100.0 | The #1 chronic hotspot. Commercial zone. Morning peak. |
| **Sahakar Nagar Road** | 13.184 | 77.680 | 3,009.5 | 1.00 | 84.3 | Heavy vehicle zone. avg_PCS=1.563 (high severity) |
| **HAL Old Airport corridor** | 12.940 | 77.696 | 2,114.8 | 1.00 | ~26 | avg_PCS=2.182 — heavy vehicles dominant. Only 969 raw count but high impact |
| **Low count, high PCS cell** | 12.996 | 77.669 | 1,919.8 | 1.00 | ~27 | 669 raw violations but avg_PCS=2.87 — raw count hides this |

> Use "low count, high PCS cell" to make the point: **a raw-count dashboard would rank this #17. GridLock correctly elevates it to #10 because heavy vehicles dominate at peak.**

---

## Appendix B — File Output Map

```
GridLock-R2/
├── pipeline/
│   ├── data_processor.py      ← Person 1: cleaning, PCS scoring
│   ├── quality_filter.py      ← Person 1: Bayesian Beta
│   ├── spatial_analysis.py    ← Person 1: Moran's I, LISA, KDE
│   ├── temporal_model.py      ← Person 1: Poisson GLM
│   └── eps_ranking.py         ← Person 1: EPS formula
├── data/
│   ├── hotspots.json          ← 7,814 cells with all scores
│   ├── officers.json          ← 2,377 officers
│   ├── temporal.json          ← station × hour matrix
│   ├── dispatch.json          ← top-30 EPS queue
│   └── chronic_cells.json     ← 20 PI=1.0 cells (for demo highlighting)
├── backend/
│   ├── main.py                ← Person 2: FastAPI app
│   ├── routers/               ← Person 2: endpoint modules
│   └── models.py              ← Person 2: Pydantic schemas
├── frontend/
│   ├── src/
│   │   ├── App.jsx            ← Person 3: routing
│   │   ├── screens/           ← Person 3: 6 screens
│   │   ├── components/        ← Person 3: reusable map/chart components
│   │   └── styles/            ← Person 4: design system CSS
│   └── public/
│       └── data/              ← fallback static JSON (copy from data/)
└── GRIDLOCK_IMPLEMENTATION_GUIDE.md  ← This file
```

---

*All numbers in this document are sourced from `DATA_ANALYSIS_RESULTS.md` and `MASTER_RESEARCH_COMBINED.md`. Do not change any number without re-running the analysis pipeline.*
