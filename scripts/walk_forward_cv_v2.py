"""
walk_forward_cv_v2.py
─────────────────────────────────────────────────────────────────────────────
Improved walk-forward CV with:

  • Negative Binomial GLM  — handles overdispersion (φ ≈ 77) properly
  • Spatial lag feature    — neighbor cell activity (Moran's I = 0.28 proves
                             clustering; baseline misses this entirely)
  • 2-month lag feature    — captures rising / falling trend per cell
  • Peak-hour fraction     — fraction of violations in rush hours (static cell attr)
  • Fairer baseline        — last training month's count (not cumulative),
                             same predictor the model builds on
  • Fold 1 skipped         — with only Nov training data, Z_prev = 0 for all
                             cells so any GLM degenerates to intercept-only

Folds evaluated: 2-4 (full months) + 5 (partial, flagged separately)

Output: walk_forward_cv_v2_results.md
─────────────────────────────────────────────────────────────────────────────
"""

import os, warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import pearsonr, spearmanr
from scipy.spatial import cKDTree

warnings.filterwarnings('ignore')

# ── Paths ─────────────────────────────────────────────────────────────────────
script_dir   = os.path.dirname(os.path.abspath(__file__))
repo_root    = os.path.dirname(script_dir)
cleaned_path = os.path.join(repo_root, 'cleaned_violations.csv')

if not os.path.exists(cleaned_path):
    raise FileNotFoundError("Run scripts/clean_data.py first.")

print(f"Loading clean data …")
df = pd.read_csv(cleaned_path)
df['ts_ist'] = pd.to_datetime(df['ts_ist'], utc=True).dt.tz_convert('Asia/Kolkata')
df['month']  = df['ts_ist'].dt.month
df['hour']   = df['ts_ist'].dt.hour
print(f"Records: {len(df):,}  |  Months: {sorted(df['month'].unique())}")

MONTH_LABEL = {11:'Nov',12:'Dec',1:'Jan',2:'Feb',3:'Mar',4:'Apr'}

# ── Fold definitions (Fold 1 skipped — degenerate) ───────────────────────────
FOLDS = [
    {'name':'Fold 2','label':'Nov–Dec → Jan','train':[11,12],       'test':1,  'partial':False},
    {'name':'Fold 3','label':'Nov–Jan → Feb','train':[11,12,1],     'test':2,  'partial':False},
    {'name':'Fold 4','label':'Nov–Feb → Mar','train':[11,12,1,2],   'test':3,  'partial':False},
    {'name':'Fold 5','label':'Nov–Mar → Apr','train':[11,12,1,2,3], 'test':4,  'partial':True},
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def compute_p_hat(train_df):
    rev = train_df[train_df['validation_status'].isin(['approved','rejected'])].copy()
    if len(rev) == 0:
        return {}
    stats = rev.groupby('created_by_id')['validation_status'].value_counts().unstack(fill_value=0)
    for c in ['approved','rejected']:
        if c not in stats.columns: stats[c] = 0
    stats['p_hat'] = (5 + stats['approved']) / (7 + stats['approved'] + stats['rejected'])
    return stats['p_hat'].to_dict()

DEFAULT_P = 5/7
PEAK_HOURS = set(list(range(8,12)) + list(range(17,20)))

def build_cell_features(clean_df, train_months):
    """
    Returns one row per grid_id with:
      lat, lon, Z_prev (last month), Z_prev2 (2nd-to-last),
      spatial_lag_Z (mean of 8 nearest neighbours' Z_prev),
      peak_frac (fraction of train violations in peak hours),
      cum_count (total clean violations in training)
    """
    last_mo  = train_months[-1]
    prev2_mo = train_months[-2] if len(train_months) >= 2 else None

    # Per-cell monthly counts
    mo_counts = (clean_df.groupby(['grid_id','month']).size()
                 .unstack(fill_value=0))

    cells = (clean_df.groupby('grid_id').agg(
        lat       = ('lat_g','first'),
        lon       = ('lon_g','first'),
        cum_count = ('id' if 'id' in clean_df.columns else 'grid_id', 'count'),
    ).reset_index())

    # Z_prev: last training month
    zprev = (clean_df[clean_df['month']==last_mo]
             .groupby('grid_id').size().reset_index(name='Z_prev'))
    cells = cells.merge(zprev, on='grid_id', how='left').fillna({'Z_prev':0})

    # Z_prev2: second-to-last training month
    if prev2_mo is not None:
        zprev2 = (clean_df[clean_df['month']==prev2_mo]
                  .groupby('grid_id').size().reset_index(name='Z_prev2'))
        cells = cells.merge(zprev2, on='grid_id', how='left').fillna({'Z_prev2':0})
    else:
        cells['Z_prev2'] = 0.0

    # Peak-hour fraction
    clean_df = clean_df.copy()
    clean_df['is_peak'] = clean_df['hour'].isin(PEAK_HOURS).astype(float)
    peak = (clean_df.groupby('grid_id')['is_peak'].mean()
            .reset_index(name='peak_frac'))
    cells = cells.merge(peak, on='grid_id', how='left').fillna({'peak_frac':0.5})

    # Spatial lag of Z_prev (k=8 nearest neighbours)
    coords = cells[['lat','lon']].values
    tree   = cKDTree(coords)
    _, idx = tree.query(coords, k=9)   # k+1 (first = self)
    nbr_idx = idx[:, 1:]
    zprev_vals = cells['Z_prev'].values
    cells['spatial_lag_Z'] = zprev_vals[nbr_idx].mean(axis=1)

    return cells

# ── Run folds ─────────────────────────────────────────────────────────────────
results     = []
report_lines = [
    "# GridLock-R2 — Walk-Forward CV v2 (NB-GLM + Spatial Lag)",
    "> Negative Binomial GLM with spatial lag, 2-month lag, and peak-hour features.",
    "> Baseline = last training month's clean counts (strong, fair comparison).",
    "",
    "## Model Specification",
    "```",
    "Family:   Negative Binomial (alpha estimated from Poisson Pearson χ²/df)",
    "Formula:  y ~ log(Z_prev+1) + log(Z_prev2+1) + log(spatial_lag_Z+1) + peak_frac",
    "Level:    Cell-month panel (one row per grid_id per training month)",
    "Baseline: Top-K cells by last training month's clean violation count",
    "```",
    "",
    "## Per-Fold Results",
    "",
]

print(f"\n{'═'*72}")
print("  WALK-FORWARD CV v2  ·  NB-GLM + Spatial Lag")
print(f"{'═'*72}")

for fold in FOLDS:
    fname     = fold['name']
    label     = fold['label']
    train_mos = fold['train']
    test_mo   = fold['test']
    partial   = fold['partial']

    print(f"\n{'─'*72}")
    print(f"  {fname}: {label}" + (" ⚠️  PARTIAL (8 days)" if partial else ""))
    print(f"{'─'*72}")

    train_raw = df[df['month'].isin(train_mos)].copy()
    test_raw  = df[df['month'] == test_mo].copy()

    p_hat_dict = compute_p_hat(train_raw)
    train_raw['p_hat'] = train_raw['created_by_id'].map(p_hat_dict).fillna(DEFAULT_P)
    test_raw['p_hat']  = test_raw['created_by_id'].map(p_hat_dict).fillna(DEFAULT_P)

    train_clean = train_raw[train_raw['p_hat'] >= 0.50].copy()
    test_clean  = test_raw[test_raw['p_hat'] >= 0.50].copy()
    total_test  = len(test_clean)

    print(f"  Train (clean): {len(train_clean):,}  |  Test (clean): {total_test:,}")

    # ── Cell features ──────────────────────────────────────────────────────
    cells = build_cell_features(train_clean, train_mos)
    all_grids = cells['grid_id'].tolist()

    # ── Training panel (cell × month) ─────────────────────────────────────
    grid_mo = pd.MultiIndex.from_product(
        [all_grids, train_mos], names=['grid_id','month']
    ).to_frame(index=False)

    mo_counts = (train_clean.groupby(['grid_id','month']).size()
                 .reset_index(name='y'))
    panel = grid_mo.merge(mo_counts, on=['grid_id','month'], how='left').fillna({'y':0})

    # Add lagged features: within-panel one-step lag
    mo_order = {m:i for i,m in enumerate(train_mos)}
    panel['mo_idx'] = panel['month'].map(mo_order)

    shifted1 = panel[['grid_id','mo_idx','y']].copy()
    shifted1['mo_idx'] += 1
    shifted1 = shifted1.rename(columns={'y':'Z_prev_lag'})

    shifted2 = panel[['grid_id','mo_idx','y']].copy()
    shifted2['mo_idx'] += 2
    shifted2 = shifted2.rename(columns={'y':'Z_prev2_lag'})

    panel = (panel
             .merge(shifted1, on=['grid_id','mo_idx'], how='left')
             .merge(shifted2, on=['grid_id','mo_idx'], how='left')
             .fillna({'Z_prev_lag':0,'Z_prev2_lag':0}))

    panel = panel.merge(
        cells[['grid_id','spatial_lag_Z','peak_frac']],
        on='grid_id', how='left'
    ).fillna({'spatial_lag_Z':0,'peak_frac':0.5})

    # ── Fit Poisson first → estimate φ → fit NB ───────────────────────────
    formula = 'y ~ np.log(Z_prev_lag+1) + np.log(Z_prev2_lag+1) + np.log(spatial_lag_Z+1) + peak_frac'

    try:
        pois = smf.glm(formula, data=panel, family=sm.families.Poisson()).fit(disp=0)
        phi  = max(pois.pearson_chi2 / pois.df_resid, 1.0)   # overdispersion ratio
        alpha_nb = 1.0 / phi                                   # NB alpha = 1/φ

        nb = smf.glm(
            formula, data=panel,
            family=sm.families.NegativeBinomial(alpha=alpha_nb)
        ).fit(disp=0)

        coefs  = nb.params.to_dict()
        model_ok = True
        print(f"  φ={phi:.1f}  α_NB={alpha_nb:.4f}  "
              f"| log_zprev={coefs.get('np.log(Z_prev_lag + 1)',0):.3f}  "
              f"spatial={coefs.get('np.log(spatial_lag_Z + 1)',0):.3f}  "
              f"peak_frac={coefs.get('peak_frac',0):.3f}")
    except Exception as e:
        print(f"  NB-GLM failed ({e}) — falling back to Poisson")
        try:
            nb = smf.glm(formula, data=panel, family=sm.families.Poisson()).fit(disp=0)
            coefs = nb.params.to_dict()
            model_ok = True
        except Exception as e2:
            print(f"  Poisson also failed: {e2}")
            model_ok = False

    # ── Predict for test month ─────────────────────────────────────────────
    pred = cells.copy()
    if model_ok:
        # Build prediction row per cell using test-context Z values
        pred_input = pd.DataFrame({
            'Z_prev_lag':   pred['Z_prev'],
            'Z_prev2_lag':  pred['Z_prev2'],
            'spatial_lag_Z':pred['spatial_lag_Z'],
            'peak_frac':    pred['peak_frac'],
            'y':            0,          # placeholder (not used in prediction)
        })
        pred['pred_vol'] = nb.predict(pred_input)
    else:
        pred['pred_vol'] = pred['Z_prev']   # fallback

    # Baseline: last training month clean count (= Z_prev)
    pred['baseline'] = pred['Z_prev']

    # ── Evaluate ───────────────────────────────────────────────────────────
    actual = (test_clean.groupby('grid_id').size()
              .reset_index(name='actual'))
    eval_df = pred.merge(actual, on='grid_id', how='left').fillna({'actual':0})

    fold_metrics = {
        'fold':fname, 'label':label, 'partial':partial,
        'n_train':len(train_clean), 'n_test':total_test,
    }

    print(f"\n  {'K':>4} | {'Baseline (last mo)':>18} | {'NB-GLM':>14} | {'Lift':>8}")
    print(f"  {'─'*56}")

    for k in [10, 20, 50]:
        # Baseline
        base_grids = eval_df.nlargest(k,'baseline')['grid_id'].tolist()
        base_vol   = test_clean[test_clean['grid_id'].isin(base_grids)].shape[0]
        base_pct   = base_vol / total_test * 100 if total_test > 0 else 0

        # Model
        mod_grids  = eval_df.nlargest(k,'pred_vol')['grid_id'].tolist()
        mod_vol    = test_clean[test_clean['grid_id'].isin(mod_grids)].shape[0]
        mod_pct    = mod_vol / total_test * 100 if total_test > 0 else 0
        lift       = (mod_pct - base_pct) / base_pct * 100 if base_pct > 0 else 0

        fold_metrics[f'base_k{k}'] = base_pct
        fold_metrics[f'mod_k{k}']  = mod_pct
        fold_metrics[f'lift_k{k}'] = lift

        print(f"  K={k:>2} | {base_pct:>10.2f}%       | "
              f"{mod_pct:>7.2f}%       | {lift:>+7.1f}%")

    # Correlations
    if eval_df['actual'].sum() > 0 and eval_df['pred_vol'].std() > 0:
        pr,  _ = pearsonr(eval_df['pred_vol'],  eval_df['actual'])
        sr,  _ = spearmanr(eval_df['pred_vol'], eval_df['actual'])
        pb,  _ = pearsonr(eval_df['baseline'],  eval_df['actual'])
        sb,  _ = spearmanr(eval_df['baseline'], eval_df['actual'])
    else:
        pr = sr = pb = sb = 0.0

    fold_metrics.update({'pearson_mod':pr,'spearman_mod':sr,
                         'pearson_base':pb,'spearman_base':sb})

    print(f"\n  Pearson  r:  NB-GLM={pr:.4f}  Baseline={pb:.4f}  "
          f"({'↑' if pr>pb else '↓'}{abs(pr-pb):.4f})")
    print(f"  Spearman ρ:  NB-GLM={sr:.4f}  Baseline={sb:.4f}  "
          f"({'↑' if sr>sb else '↓'}{abs(sr-sb):.4f})")

    results.append(fold_metrics)

    # Report section
    flag = " ⚠️ Partial (8 days)" if partial else ""
    report_lines += [
        f"### {fname}: {label}{flag}",
        f"Train: {len(train_clean):,} clean records  |  Test: {total_test:,} clean records",
        "",
        "| K | Baseline (last month) | NB-GLM | Lift |",
        "|---|---|---|---|",
    ]
    for k in [10, 20, 50]:
        report_lines.append(
            f"| {k} | {fold_metrics[f'base_k{k}']:.2f}% | "
            f"{fold_metrics[f'mod_k{k}']:.2f}% | "
            f"{fold_metrics[f'lift_k{k}']:+.1f}% |"
        )
    report_lines += [
        "",
        f"**Pearson r:** NB-GLM={pr:.4f}  Baseline={pb:.4f}  "
        f"| **Spearman ρ:** NB-GLM={sr:.4f}  Baseline={sb:.4f}",
        "",
    ]

# ── Aggregate (Folds 2-4 only, full months) ───────────────────────────────────
res_df   = pd.DataFrame(results)
full_df  = res_df[~res_df['partial']]

print(f"\n{'═'*72}")
print("  AGGREGATE RESULTS  (Folds 2–4, full months)")
print(f"{'═'*72}")

agg_rows = {}
for k in [10, 20, 50]:
    m = full_df[f'lift_k{k}'].mean()
    s = full_df[f'lift_k{k}'].std()
    agg_rows[k] = (m, s)
    reliable = "✅" if abs(m) > s else "⚠️ noisy"
    print(f"  K={k:>2}  mean lift: {m:+.1f}% ± {s:.1f}%  {reliable}")

mr = full_df['spearman_mod'].mean()
sr_std = full_df['spearman_mod'].std()
br = full_df['spearman_base'].mean()
print(f"  Spearman ρ:  NB-GLM={mr:.4f} ± {sr_std:.4f}  |  Baseline={br:.4f}")

# Comparison vs v1 (Poisson, no spatial lag)
print(f"\n  vs v1 (Poisson, no spatial lag) summary:")
print(f"  v1 K=10 mean lift: -19.0% ± 47.9%  →  v2: {agg_rows[10][0]:+.1f}% ± {agg_rows[10][1]:.1f}%")
print(f"  v1 K=20 mean lift: -19.9% ± 38.4%  →  v2: {agg_rows[20][0]:+.1f}% ± {agg_rows[20][1]:.1f}%")
print(f"  v1 K=50 mean lift: -18.8% ± 35.9%  →  v2: {agg_rows[50][0]:+.1f}% ± {agg_rows[50][1]:.1f}%")

# ── Report: summary table ─────────────────────────────────────────────────────
report_lines += [
    "---",
    "",
    "## Aggregate Summary (Folds 2–4, full months only)",
    "",
    "| K | Mean NB-GLM Lift | Std Dev | Reliable? |",
    "|---|---|---|---|",
]
for k in [10, 20, 50]:
    m, s = agg_rows[k]
    reliable = "✅ Yes" if abs(m) > s else "⚠️ Noisy"
    report_lines.append(f"| {k} | {m:+.1f}% | ±{s:.1f}% | {reliable} |")

report_lines += [
    "",
    f"**Mean Spearman ρ (NB-GLM):** {mr:.4f} ± {sr_std:.4f}  |  **Baseline:** {br:.4f}",
    "",
    "## Full Per-Fold Table",
    "",
    "| Fold | K=10 Lift | K=20 Lift | K=50 Lift | Spearman ρ | vs Baseline |",
    "|---|---|---|---|---|---|",
]
for r in results:
    delta_rho = r['spearman_mod'] - r['spearman_base']
    flag = " ⚠️" if r['partial'] else ""
    report_lines.append(
        f"| {r['fold']}: {r['label']}{flag} | "
        f"{r['lift_k10']:+.1f}% | {r['lift_k20']:+.1f}% | {r['lift_k50']:+.1f}% | "
        f"{r['spearman_mod']:.4f} | {delta_rho:+.4f} |"
    )

report_lines += [
    "",
    "> [!NOTE]",
    "> Fold 5 (April, 8 days) excluded from aggregate — partial month makes % shares unstable.",
    "",
    "## What Improved vs v1 (Poisson, no spatial lag)",
    "",
    "| Metric | v1 Poisson | v2 NB-GLM | Change |",
    "|---|---|---|---|",
    f"| K=10 mean lift | -19.0% ± 47.9% | {agg_rows[10][0]:+.1f}% ± {agg_rows[10][1]:.1f}% | {'↑' if agg_rows[10][0]>-19 else '↓'} |",
    f"| K=20 mean lift | -19.9% ± 38.4% | {agg_rows[20][0]:+.1f}% ± {agg_rows[20][1]:.1f}% | {'↑' if agg_rows[20][0]>-19.9 else '↓'} |",
    f"| K=50 mean lift | -18.8% ± 35.9% | {agg_rows[50][0]:+.1f}% ± {agg_rows[50][1]:.1f}% | {'↑' if agg_rows[50][0]>-18.8 else '↓'} |",
    f"| Spearman ρ | ~0.601 | {mr:.4f} | {'↑' if mr>0.601 else '↓'} |",
]

out_md = os.path.join(repo_root, 'walk_forward_cv_v2_results.md')
with open(out_md, 'w') as f:
    f.write('\n'.join(report_lines))

print(f"\n✅  Report saved → {out_md}")
