# GridLock-R2 — XGBoost Walk-Forward CV
> Modeling spatial spillover and non-linear patterns.

## Model Specification
```
Algorithm: XGBoost Regressor (objective='count:poisson')
Features:  Z_prev, Z_prev2, Z_trend, spatial_lag_Z, spatial_lag_trend, peak_frac, station_id, lat, lon
```


## Overall Lift vs Baseline (Full Months Only)
| K | Baseline | XGBoost | Lift |
|---|---|---|---|
| 10 | 8.70% | 7.99% | **-8.4% ± 10.0%** |
| 20 | 13.15% | 12.40% | **-5.3% ± 17.0%** |
| 50 | 23.45% | 22.73% | **-3.0% ± 6.8%** |

## Feature Importances
XGBoost consistently prioritizes:
1. `Z_prev` (strongest autoregressive signal)
2. `spatial_lag_Z` (baseline misses this entirely)
3. `Z_trend` (momentum)