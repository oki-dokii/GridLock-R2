# GridLock-R2 — Walk-Forward CV v2 (NB-GLM + Spatial Lag)
> Negative Binomial GLM with spatial lag, 2-month lag, and peak-hour features.
> Baseline = last training month's clean counts (strong, fair comparison).

## Model Specification
```
Family:   Negative Binomial (alpha estimated from Poisson Pearson χ²/df)
Formula:  y ~ log(Z_prev+1) + log(Z_prev2+1) + log(spatial_lag_Z+1) + peak_frac
Level:    Cell-month panel (one row per grid_id per training month)
Baseline: Top-K cells by last training month's clean violation count
```

## Per-Fold Results

### Fold 2: Nov–Dec → Jan
Train: 68,013 clean records  |  Test: 40,331 clean records

| K | Baseline (last month) | NB-GLM | Lift |
|---|---|---|---|
| 10 | 8.31% | 5.32% | -36.0% |
| 20 | 13.66% | 9.51% | -30.3% |
| 50 | 24.18% | 17.85% | -26.2% |

**Pearson r:** NB-GLM=0.6953  Baseline=0.8763  | **Spearman ρ:** NB-GLM=0.5437  Baseline=0.6214

### Fold 3: Nov–Jan → Feb
Train: 109,543 clean records  |  Test: 32,098 clean records

| K | Baseline (last month) | NB-GLM | Lift |
|---|---|---|---|
| 10 | 8.57% | 7.71% | -10.0% |
| 20 | 12.46% | 10.97% | -12.0% |
| 50 | 22.46% | 18.69% | -16.8% |

**Pearson r:** NB-GLM=0.7701  Baseline=0.8849  | **Spearman ρ:** NB-GLM=0.5481  Baseline=0.5930

### Fold 4: Nov–Feb → Mar
Train: 140,179 clean records  |  Test: 34,318 clean records

| K | Baseline (last month) | NB-GLM | Lift |
|---|---|---|---|
| 10 | 9.23% | 8.71% | -5.6% |
| 20 | 13.33% | 12.58% | -5.7% |
| 50 | 23.71% | 21.06% | -11.2% |

**Pearson r:** NB-GLM=0.8304  Baseline=0.9019  | **Spearman ρ:** NB-GLM=0.5219  Baseline=0.5887

### Fold 5: Nov–Mar → Apr ⚠️ Partial (8 days)
Train: 175,609 clean records  |  Test: 9,848 clean records

| K | Baseline (last month) | NB-GLM | Lift |
|---|---|---|---|
| 10 | 8.48% | 7.14% | -15.8% |
| 20 | 12.57% | 11.71% | -6.9% |
| 50 | 24.86% | 23.72% | -4.6% |

**Pearson r:** NB-GLM=0.7935  Baseline=0.8276  | **Spearman ρ:** NB-GLM=0.4562  Baseline=0.4975

---

## Aggregate Summary (Folds 2–4, full months only)

| K | Mean NB-GLM Lift | Std Dev | Reliable? |
|---|---|---|---|
| 10 | -17.2% | ±16.4% | ✅ Yes |
| 20 | -16.0% | ±12.8% | ✅ Yes |
| 50 | -18.0% | ±7.6% | ✅ Yes |

**Mean Spearman ρ (NB-GLM):** 0.5379 ± 0.0140  |  **Baseline:** 0.6010

## Full Per-Fold Table

| Fold | K=10 Lift | K=20 Lift | K=50 Lift | Spearman ρ | vs Baseline |
|---|---|---|---|---|---|
| Fold 2: Nov–Dec → Jan | -36.0% | -30.3% | -26.2% | 0.5437 | -0.0777 |
| Fold 3: Nov–Jan → Feb | -10.0% | -12.0% | -16.8% | 0.5481 | -0.0449 |
| Fold 4: Nov–Feb → Mar | -5.6% | -5.7% | -11.2% | 0.5219 | -0.0668 |
| Fold 5: Nov–Mar → Apr ⚠️ | -15.8% | -6.9% | -4.6% | 0.4562 | -0.0414 |

> [!NOTE]
> Fold 5 (April, 8 days) excluded from aggregate — partial month makes % shares unstable.

## What Improved vs v1 (Poisson, no spatial lag)

| Metric | v1 Poisson | v2 NB-GLM | Change |
|---|---|---|---|
| K=10 mean lift | -19.0% ± 47.9% | -17.2% ± 16.4% | ↑ |
| K=20 mean lift | -19.9% ± 38.4% | -16.0% ± 12.8% | ↑ |
| K=50 mean lift | -18.8% ± 35.9% | -18.0% ± 7.6% | ↑ |
| Spearman ρ | ~0.601 | 0.5379 | ↓ |