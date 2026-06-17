# Research Papers: Parking-Induced Congestion & AI Enforcement

> 8 papers across 4 angles to legitimise your impact score and hotspot methodology.

---

## 1. Capacity Reduction

### On-street parking: effects on traffic congestion
- **Source:** ResearchGate · 2024
- **What it measures:** Mixed-traffic empirical study using Greenberg model (R²=0.695)
- **Key finding:** Legal parking reduces road capacity by **24%**; illegal double-parking by an additional **26%** — total **50% capacity loss**. Speed drops 0.03 km/h per unit increase in occupancy.
- **Cite for:** Quantifying capacity loss from illegal parking

---

### The influence of parallel curb parking on traffic capacity at an intersection
- **Source:** PMC / NCBI · 2024
- **What it measures:** Traces decades of research (Webster 1968 → Ye & Chen 2011) on how distance between parking area and intersection affects throughput
- **Key finding:** Queue spillback extends to upstream intersections — directly relevant to junction bottlenecks near commercial zones.
- **Cite for:** Intersection capacity and spillback from curb parking

---

## 2. Spillover & Congestion Propagation

### Impact of on-street parking space placement on through traffic
- **Source:** AGILE-GISS · 2025
- **What it measures:** Microscopic simulation across parking placement and demand scenarios
- **Key finding:** Spillover from cruising creates delays even at locations **away from primary routes**. Produces travel-time heatmaps by parking demand level — analogous to a violation heatmap approach.
- **Cite for:** Spatial spillover impact and heatmap methodology legitimacy

---

### Spread of parking difficulty in urban environments: a parking network perspective
- **Source:** IET Intelligent Transport Systems · 2024
- **What it measures:** Models parking failure as a cascading network problem using SIR epidemic analogy
- **Key finding:** One saturated block cascades to adjacent zones. The SIR-based spread model maps cleanly to hotspot severity scoring.
- **Cite for:** Congestion propagation from parking saturation

---

## 3. Bottleneck Analysis

### Traffic bottlenecks: identification and solutions (FHWA-HRT-16-064)
- **Source:** US Federal Highway Administration · 2016
- **What it measures:** Highway Capacity Manual (HCM) framework for bottleneck identification and prioritisation
- **Key finding:** Explicitly lists "cars parked near intersections" and "double-parked cars" as bottleneck causes. A **5% congestion reduction at a bottleneck** yields far greater benefit than at non-bottleneck sections.
- **Cite for:** Government authority on parking-as-bottleneck; ROI of targeted enforcement

---

### Addressing the urban congestion challenge based on traffic bottlenecks
- **Source:** PMC · 2024
- **What it measures:** Bottleneck identification methodology applied to real urban traffic data
- **Key finding:** Bottlenecks **rarely repeat daily**, meaning patrol-based enforcement structurally misses dynamic hotspots — the core gap a predictive system addresses.
- **Cite for:** Why reactive enforcement fails; the case for predictive prioritisation

---

## 4. AI & ML Enforcement

### A deep learning-based illegal parking detection platform
- **Source:** ResearchGate / ACM SIGSPATIAL · 2019
- **What it measures:** End-to-end pipeline: hotspot ranking → camera-based detection → traffic impact quantification
- **Key finding:** "Rank, detect, quantify" architecture: (1) hotspot identification via **spatial autocorrelation**, (2) occupancy estimation, (3) impact score via M/M/∞ queueing model. Near-identical to a proposed AI enforcement stack.
- **Cite for:** Impact score methodology and hotspot ranking pipeline

---

### Adopting machine learning and spatial analysis techniques for driver risk assessment
- **Source:** PMC / Sustainability · 2020
- **What it measures:** GIS-based IDW interpolation on police ticket data (same data type as your dataset) to generate violation hotspot maps
- **Key finding:** KNN model (k=7, Manhattan distance) achieved **99% accuracy** classifying violation types including illegal parking from georeferenced enforcement records.
- **Cite for:** ML on police violation data → hotspot maps

---

## Suggested PPT Citation Block

> *"Our Parking Impact Score is grounded in established traffic engineering principles: illegal on-street parking is documented to reduce road capacity by up to 50% (ResearchGate, 2024), and congestion spillback propagates to adjacent intersections even on non-primary routes (AGILE-GISS, 2025). Our hotspot identification methodology follows the spatial autocorrelation approach validated on urban violation data (PMC, 2020), while our enforcement prioritisation logic aligns with the bottleneck targeting framework recommended by the US Federal Highway Administration (FHWA, 2016)."*

---

## Quick Reference

| # | Paper | Angle | Key Stat | Cite For |
|---|-------|--------|----------|----------|
| 1 | On-street parking: effects on congestion | Capacity | 50% capacity loss | Impact score numbers |
| 2 | Curb parking at intersection capacity | Capacity | Spillback to upstream junctions | Junction bottleneck claims |
| 3 | Parking placement on through traffic | Spillover | Delays away from primary routes | Heatmap legitimacy |
| 4 | Spread of parking difficulty (network) | Propagation | Cascading failure model | Congestion propagation |
| 5 | FHWA Traffic Bottlenecks report | Bottleneck | 5% reduction → outsized gain | Government authority |
| 6 | Urban congestion bottleneck challenge | Bottleneck | Bottlenecks don't repeat daily | Why patrol fails |
| 7 | Deep learning illegal parking detection | AI/ML | Rank→detect→quantify pipeline | Your architecture |
| 8 | ML for driver risk assessment (GIS) | AI/ML | 99% KNN accuracy on ticket data | Your dataset method |
