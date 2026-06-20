# GridLock-R2 — Walk-Forward Cross-Validation Results
> Expanding-window CV on cleaned data (186,563 records). 5 folds, one test month each.

## Fold Definitions
| Fold | Train Period | Test Period | Test Days | Partial? |
|---|---|---|---|---|
| Fold 1 | Nov 2023 | Dec 2023 | 31 | No |
| Fold 2 | Nov–Dec 2023 | Jan 2024 | 31 | No |
| Fold 3 | Nov 2023–Jan 2024 | Feb 2024 | 29 | No |
| Fold 4 | Nov 2023–Feb 2024 | Mar 2024 | 31 | No |
| Fold 5 | Nov 2023–Mar 2024 | Apr 2024 | 8  | ⚠️ Yes |

## Per-Fold Results

### Fold 1: Nov → Dec
Train records: 27,523  |  Test records: 39,245

| K | Baseline | Vol-Only | Lift | Soft-PI | Lift |
|---|---|---|---|---|---|
| 10 | 6.56% | 0.61% | -90.7% | 0.61% | -90.7% |
| 20 | 10.45% | 2.36% | -77.4% | 2.36% | -77.4% |
| 50 | 20.35% | 5.60% | -72.5% | 5.60% | -72.5% |

**Pearson r:** Model=nan  Baseline=0.8606  | **Spearman ρ:** Model=nan  Baseline=0.6441

### Fold 2: Nov–Dec → Jan
Train records: 68,013  |  Test records: 40,331

| K | Baseline | Vol-Only | Lift | Soft-PI | Lift |
|---|---|---|---|---|---|
| 10 | 8.09% | 8.31% | +2.7% | 8.31% | +2.7% |
| 20 | 13.37% | 13.66% | +2.2% | 12.77% | -4.5% |
| 50 | 24.44% | 24.18% | -1.1% | 24.18% | -1.1% |

**Pearson r:** Model=0.7551  Baseline=0.8866  | **Spearman ρ:** Model=0.6214  Baseline=0.6667

### Fold 3: Nov–Jan → Feb
Train records: 109,543  |  Test records: 32,098

| K | Baseline | Vol-Only | Lift | Soft-PI | Lift |
|---|---|---|---|---|---|
| 10 | 7.89% | 8.57% | +8.7% | 7.89% | +0.1% |
| 20 | 12.66% | 12.46% | -1.5% | 12.38% | -2.2% |
| 50 | 21.88% | 22.46% | +2.6% | 21.89% | +0.0% |

**Pearson r:** Model=0.8568  Baseline=0.8896  | **Spearman ρ:** Model=0.5930  Baseline=0.6369

### Fold 4: Nov–Feb → Mar
Train records: 140,179  |  Test records: 34,318

| K | Baseline | Vol-Only | Lift | Soft-PI | Lift |
|---|---|---|---|---|---|
| 10 | 8.91% | 9.23% | +3.5% | 8.82% | -1.1% |
| 20 | 13.72% | 13.33% | -2.8% | 13.79% | +0.5% |
| 50 | 24.78% | 23.71% | -4.3% | 24.82% | +0.1% |

**Pearson r:** Model=0.8857  Baseline=0.9189  | **Spearman ρ:** Model=0.5887  Baseline=0.6488

### Fold 5: Nov–Mar → Apr ⚠️ Partial (8 days)
Train records: 175,609  |  Test records: 9,848

| K | Baseline | Vol-Only | Lift | Soft-PI | Lift |
|---|---|---|---|---|---|
| 10 | 7.91% | 9.10% | +15.0% | 9.10% | +15.0% |
| 20 | 12.18% | 12.57% | +3.3% | 13.06% | +7.3% |
| 50 | 24.18% | 24.86% | +2.8% | 25.23% | +4.4% |

**Pearson r:** Model=0.8236  Baseline=0.8070  | **Spearman ρ:** Model=0.4975  Baseline=0.5086

---

## Overall Summary (Folds 1–4, full months only)

| K | Mean Vol-Only Lift | Std Dev | Reliable? |
|---|---|---|---|
| 10 | -19.0% | ±47.9% | ⚠️ Noisy |
| 20 | -19.9% | ±38.4% | ⚠️ Noisy |
| 50 | -18.8% | ±35.9% | ⚠️ Noisy |

**Mean Spearman ρ (model):** 0.6010 ± 0.0178  |  **Baseline:** 0.6491

> [!NOTE]
> Fold 5 (April) is excluded from aggregate stats — only 8 days of test data make the percentage shares unreliable. The mean lift above is the honest figure.

## Full Per-Fold Table (Vol-Only Lift %)

| Fold | K=10 | K=20 | K=50 | Spearman ρ |
|---|---|---|---|---|
| Fold 1: Nov → Dec | -90.7% | -77.4% | -72.5% | nan |
| Fold 2: Nov–Dec → Jan | +2.7% | +2.2% | -1.1% | 0.6214 |
| Fold 3: Nov–Jan → Feb | +8.7% | -1.5% | +2.6% | 0.5930 |
| Fold 4: Nov–Feb → Mar | +3.5% | -2.8% | -4.3% | 0.5887 |
| Fold 5: Nov–Mar → Apr ⚠️ | +15.0% | +3.3% | +2.8% | 0.4975 |