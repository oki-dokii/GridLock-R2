# GridLock-R2 — Data Cleaning Report
> Dataset: `jan to may police violation_anonymized791b166.csv`

**Raw record count:** 298,450

## Step 1 — Timestamp Validation
| Check | Dropped |
|---|---|
| Unparseable `created_datetime` | 5 |
| Future timestamps (> Apr 10 2024) | 0 |
| **Remaining** | **298,445** |

## Step 2 — Spatial Bounds
Bounding box: lat [12.7, 13.35] × lon [77.35, 77.85]

| Check | Dropped |
|---|---|
| Out-of-bounds coordinates | 0 |
| **Remaining** | **298,445** |

## Step 3 — Grid Snapping (110m Resolution)
- Coordinates rounded to 3 decimal places (~110m cell size)
- **Unique grid cells:** 7,814

## Step 4 — Officer Quality Filter (Bayesian Beta p̂)
Prior: Beta(5, 2) → default p̂ = 0.714 for unreviewed officers
Threshold: p̂ ≥ 0.50 to keep a record

| Metric | Value |
|---|---|
| Total officers | 2,666 |
| Officers with p̂ < 0.50 | 123 |
| Records from corrupt officers | 20,349 |
| Records kept (p̂ ≥ 0.50) | 278,096 |

### Worst 10 Officers by p̂
| Officer | Approved | Rejected | Total | p̂ |
|---|---|---|---|---|
| FKUSR01810 | 1 | 39 | 40 | 0.1277 |
| FKUSR02046 | 16 | 106 | 122 | 0.1628 |
| FKUSR01593 | 1 | 27 | 28 | 0.1714 |
| FKUSR00926 | 0 | 20 | 20 | 0.1852 |
| FKUSR01903 | 15 | 72 | 87 | 0.2128 |
| FKUSR02615 | 0 | 16 | 16 | 0.2174 |
| FKUSR00617 | 19 | 82 | 101 | 0.2222 |
| FKUSR01596 | 2 | 22 | 24 | 0.2258 |
| FKUSR00808 | 32 | 119 | 151 | 0.2342 |
| FKUSR01116 | 7 | 37 | 44 | 0.2353 |

## Step 5 — Duplicate Detection
Key: `(officer_id, grid_cell, timestamp_floor_1min)`

| Check | Count |
|---|---|
| Exact duplicates removed | 91,533 |
| **Final clean records** | **186,563** |

## Step 6 — PCS Enrichment
Formula: `PCS = ω (PCU weight) × δ (hour multiplier) × σ (violation severity)`

| Metric | Value |
|---|---|
| Mean PCS (clean dataset) | 1.0627 |
| Max PCS | 9.00 |
| Total PCS sum | 198,266.2 |
| Mean q\_PCS (quality-adjusted) | 0.7562 |

## Cleaning Summary
| Step | Records Dropped | % of Raw |
|---|---|---|
| Bad timestamps | 5 | 0.00% |
| Out-of-bounds coordinates | 0 | 0.00% |
| Corrupt officer records (p̂ < 0.50) | 20,349 | 6.82% |
| Exact duplicates | 91,533 | 30.67% |
| **Total dropped** | **111,887** | **37.49%** |
| **✅ Clean records** | **186,563** | **62.51%** |

## Output Files
- `cleaned_violations.csv` — full cleaned & enriched dataset
- `cleaning_report.md` — this report