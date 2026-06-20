"""
walk_forward_cv.py
─────────────────────────────────────────────────────────────────────────────
Walk-forward (expanding window) cross-validation on CLEAN data.

5 folds:
  Fold 1  Train: Nov          Test: Dec   (31 days)
  Fold 2  Train: Nov–Dec      Test: Jan   (31 days)
  Fold 3  Train: Nov–Jan      Test: Feb   (29 days)
  Fold 4  Train: Nov–Feb      Test: Mar   (31 days)
  Fold 5  Train: Nov–Mar      Test: Apr   (8 days — partial, flagged)

For each fold:
  • p̂ computed strictly from training data
  • PI computed strictly from training data
  • Cell-month Poisson GLM (Vol-Only + Soft-PI variants)
  • Baseline = top-K by cumulative training count
  • Metrics: lift at K=10/20/50, Pearson r, Spearman ρ

Output: walk_forward_cv_results.md
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
    raise FileNotFoundError("Run scripts/clean_data.py first to produce cleaned_violations.csv")

print(f"Loading clean data from: {cleaned_path}")
df = pd.read_csv(cleaned_path)
df['ts_ist'] = pd.to_datetime(df['ts_ist'], utc=True).dt.tz_convert('Asia/Kolkata')
df['month']  = df['ts_ist'].dt.month
print(f"Clean records: {len(df):,}  |  Months: {sorted(df['month'].unique())}")

# Month label map for display
MONTH_LABEL = {11:'Nov', 12:'Dec', 1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr'}

# ── Fold definitions ──────────────────────────────────────────────────────────
FOLDS = [
    {'name':'Fold 1', 'label':'Nov → Dec',     'train':[11],          'test':12, 'partial':False},
    {'name':'Fold 2', 'label':'Nov–Dec → Jan', 'train':[11,12],       'test':1,  'partial':False},
    {'name':'Fold 3', 'label':'Nov–Jan → Feb', 'train':[11,12,1],     'test':2,  'partial':False},
    {'name':'Fold 4', 'label':'Nov–Feb → Mar', 'train':[11,12,1,2],   'test':3,  'partial':False},
    {'name':'Fold 5', 'label':'Nov–Mar → Apr', 'train':[11,12,1,2,3], 'test':4,  'partial':True},
]

# ── Helper: compute p̂ from a training DataFrame ────────────────────────────
def compute_p_hat(train_df):
    reviewed = train_df[train_df['validation_status'].isin(['approved','rejected'])].copy()
    if len(reviewed) == 0:
        return {}
    stats = (reviewed.groupby('created_by_id')['validation_status']
             .value_counts().unstack(fill_value=0))
    for c in ['approved','rejected']:
        if c not in stats.columns:
            stats[c] = 0
    stats['p_hat'] = (5 + stats['approved']) / (7 + stats['approved'] + stats['rejected'])
    return stats['p_hat'].to_dict()

DEFAULT_P = 5/7

# ── Helper: compute Persistence Index from training months ────────────────────
def compute_pi(train_df, train_months):
    """How many of the last 4 (or available) training months was cell in top-50?"""
    lookback = train_months[-4:]  # use up to last 4 months
    if len(lookback) < 2:
        return {}          # not enough history for meaningful PI
    monthly_top50 = {}
    for m in lookback:
        mdf = train_df[train_df['month'] == m]
        top50 = mdf.groupby('grid_id').size().nlargest(50).index.tolist()
        monthly_top50[m] = set(top50)
    all_grids = train_df['grid_id'].unique()
    pi = {}
    for g in all_grids:
        pi[g] = sum(1 for m in lookback if g in monthly_top50.get(m, set())) / len(lookback)
    return pi

# ── Run folds ─────────────────────────────────────────────────────────────────
results = []
report_lines = []

report_lines += [
    "# GridLock-R2 — Walk-Forward Cross-Validation Results",
    "> Expanding-window CV on cleaned data (186,563 records). 5 folds, one test month each.",
    "",
    "## Fold Definitions",
    "| Fold | Train Period | Test Period | Test Days | Partial? |",
    "|---|---|---|---|---|",
    "| Fold 1 | Nov 2023 | Dec 2023 | 31 | No |",
    "| Fold 2 | Nov–Dec 2023 | Jan 2024 | 31 | No |",
    "| Fold 3 | Nov 2023–Jan 2024 | Feb 2024 | 29 | No |",
    "| Fold 4 | Nov 2023–Feb 2024 | Mar 2024 | 31 | No |",
    "| Fold 5 | Nov 2023–Mar 2024 | Apr 2024 | 8  | ⚠️ Yes |",
    "",
]

print(f"\n{'═'*70}")
print(f"  WALK-FORWARD CROSS-VALIDATION")
print(f"{'═'*70}")

for fold in FOLDS:
    fname      = fold['name']
    label      = fold['label']
    train_mos  = fold['train']
    test_mo    = fold['test']
    partial    = fold['partial']

    print(f"\n{'─'*70}")
    print(f"  {fname}: Train={label.split('→')[0].strip()}  |  Test={MONTH_LABEL[test_mo]}"
          + (" ⚠️ PARTIAL (8 days)" if partial else ""))
    print(f"{'─'*70}")

    train_df = df[df['month'].isin(train_mos)].copy()
    test_df  = df[df['month'] == test_mo].copy()

    # ── p̂ from training data ──────────────────────────────────────────────
    p_hat_dict = compute_p_hat(train_df)
    train_df['p_hat'] = train_df['created_by_id'].map(p_hat_dict).fillna(DEFAULT_P)
    test_df['p_hat']  = test_df['created_by_id'].map(p_hat_dict).fillna(DEFAULT_P)

    # Clean subsets
    train_clean = train_df[train_df['p_hat'] >= 0.50].copy()
    test_clean  = test_df[test_df['p_hat'] >= 0.50].copy()

    print(f"  Train (clean): {len(train_clean):,}  |  Test (clean): {len(test_clean):,}")

    # ── All grid IDs seen in training ─────────────────────────────────────
    all_grids = train_clean['grid_id'].unique().tolist()

    # ── Cumulative training counts (baseline) ─────────────────────────────
    train_counts = (train_clean.groupby('grid_id').size()
                    .reset_index(name='train_count'))

    # ── Z_prev: last training month's clean counts ─────────────────────────
    last_mo = train_mos[-1]
    zprev   = (train_clean[train_clean['month'] == last_mo]
               .groupby('grid_id').size()
               .reset_index(name='Z_prev'))

    # ── Build cell-month training panel ───────────────────────────────────
    grid_mo = pd.MultiIndex.from_product(
        [all_grids, train_mos], names=['grid_id','month']
    ).to_frame(index=False)

    mo_counts = (train_clean.groupby(['grid_id','month']).size()
                 .reset_index(name='y'))
    panel = grid_mo.merge(mo_counts, on=['grid_id','month'], how='left').fillna({'y': 0})

    # Create lagged Z_prev within panel
    mo_order = {m: i for i, m in enumerate(train_mos)}
    panel['mo_idx'] = panel['month'].map(mo_order)
    shifted = panel.copy()
    shifted['mo_idx'] = shifted['mo_idx'] - 1
    shifted = shifted.rename(columns={'y': 'Z_prev_lag'})
    panel = panel.merge(
        shifted[['grid_id','mo_idx','Z_prev_lag']],
        on=['grid_id','mo_idx'], how='left'
    ).fillna({'Z_prev_lag': 0})

    # ── Fit Poisson GLM ────────────────────────────────────────────────────
    try:
        glm = smf.glm(
            'y ~ np.log(Z_prev_lag + 1)',
            data=panel,
            family=sm.families.Poisson()
        ).fit(disp=0)
        coefs = glm.params.to_dict()
        glm_ok = True
        print(f"  GLM coefs: intercept={coefs['Intercept']:.4f}, "
              f"log_zprev={coefs['np.log(Z_prev_lag + 1)']:.4f}")
    except Exception as e:
        print(f"  GLM failed: {e} — using baseline only")
        glm_ok = False

    # ── Generate predictions ───────────────────────────────────────────────
    pred_df = pd.DataFrame({'grid_id': all_grids})
    pred_df = pred_df.merge(zprev, on='grid_id', how='left').fillna({'Z_prev': 0})
    pred_df = pred_df.merge(train_counts, on='grid_id', how='left').fillna({'train_count': 0})

    if glm_ok:
        pred_df['pred_vol'] = np.exp(
            coefs['Intercept'] +
            np.log(pred_df['Z_prev'] + 1) * coefs['np.log(Z_prev_lag + 1)']
        )
    else:
        pred_df['pred_vol'] = pred_df['Z_prev']  # fallback: use last month count

    # PI
    pi_dict = compute_pi(train_clean, train_mos)
    pred_df['PI'] = pred_df['grid_id'].map(pi_dict).fillna(0)
    pred_df['EPS_vol']     = pred_df['pred_vol']
    pred_df['EPS_soft_pi'] = (pred_df['PI'] + 0.5) * pred_df['pred_vol']

    # ── Evaluate ───────────────────────────────────────────────────────────
    actual = (test_clean.groupby('grid_id').size()
              .reset_index(name='actual'))
    total_test_clean = len(test_clean)

    fold_metrics = {'fold': fname, 'label': label, 'partial': partial}
    fold_metrics['n_train'] = len(train_clean)
    fold_metrics['n_test']  = len(test_clean)

    print(f"\n  {'K':>4} | {'Baseline':>9} | {'Vol-Only':>12} | {'Soft-PI':>12}")
    print(f"  {'─'*50}")

    for k in [10, 20, 50]:
        # Baseline
        base_grids = pred_df.nlargest(k, 'train_count')['grid_id'].tolist()
        base_vol   = test_clean[test_clean['grid_id'].isin(base_grids)].shape[0]
        base_pct   = base_vol / total_test_clean * 100 if total_test_clean > 0 else 0

        # Vol-Only model
        vol_grids = pred_df.nlargest(k, 'EPS_vol')['grid_id'].tolist()
        vol_vol   = test_clean[test_clean['grid_id'].isin(vol_grids)].shape[0]
        vol_pct   = vol_vol / total_test_clean * 100 if total_test_clean > 0 else 0
        vol_lift  = ((vol_pct - base_pct) / base_pct * 100) if base_pct > 0 else 0

        # Soft-PI model
        spi_grids = pred_df.nlargest(k, 'EPS_soft_pi')['grid_id'].tolist()
        spi_vol   = test_clean[test_clean['grid_id'].isin(spi_grids)].shape[0]
        spi_pct   = spi_vol / total_test_clean * 100 if total_test_clean > 0 else 0
        spi_lift  = ((spi_pct - base_pct) / base_pct * 100) if base_pct > 0 else 0

        fold_metrics[f'base_k{k}']    = base_pct
        fold_metrics[f'vol_k{k}']     = vol_pct
        fold_metrics[f'vol_lift_k{k}']= vol_lift
        fold_metrics[f'spi_k{k}']     = spi_pct
        fold_metrics[f'spi_lift_k{k}']= spi_lift

        print(f"  K={k:>2} | {base_pct:>7.2f}%  | "
              f"{vol_pct:>6.2f}% ({vol_lift:+.1f}%) | "
              f"{spi_pct:>6.2f}% ({spi_lift:+.1f}%)")

    # Correlation metrics
    corr_df = pred_df.merge(actual, on='grid_id', how='left').fillna({'actual': 0})
    if corr_df['actual'].sum() > 0 and corr_df['pred_vol'].std() > 0:
        pr, _ = pearsonr(corr_df['pred_vol'], corr_df['actual'])
        sr, _ = spearmanr(corr_df['pred_vol'], corr_df['actual'])
        pb, _ = pearsonr(corr_df['train_count'], corr_df['actual'])
        sb, _ = spearmanr(corr_df['train_count'], corr_df['actual'])
    else:
        pr = sr = pb = sb = 0.0

    fold_metrics['pearson_model']   = pr
    fold_metrics['spearman_model']  = sr
    fold_metrics['pearson_base']    = pb
    fold_metrics['spearman_base']   = sb

    print(f"\n  Pearson  r  — Model: {pr:.4f}  |  Baseline: {pb:.4f}  "
          f"({'↑' if pr>pb else '↓'}{abs(pr-pb):.4f})")
    print(f"  Spearman ρ  — Model: {sr:.4f}  |  Baseline: {sb:.4f}  "
          f"({'↑' if sr>sb else '↓'}{abs(sr-sb):.4f})")

    results.append(fold_metrics)

# ── Build summary ─────────────────────────────────────────────────────────────
res_df = pd.DataFrame(results)

# Full-month folds only (exclude Fold 5)
full_df = res_df[~res_df['partial']]

print(f"\n{'═'*70}")
print(f"  SUMMARY  (mean ± std  across full-month folds only, Folds 1–4)")
print(f"{'═'*70}")

summary_rows = {}
for k in [10, 20, 50]:
    m_lift = full_df[f'vol_lift_k{k}'].mean()
    s_lift = full_df[f'vol_lift_k{k}'].std()
    summary_rows[k] = (m_lift, s_lift)
    print(f"  K={k:>2}  Vol-Only lift:  {m_lift:+.1f}% ± {s_lift:.1f}%")

m_sr = full_df['spearman_model'].mean()
s_sr = full_df['spearman_model'].std()
m_sb = full_df['spearman_base'].mean()
print(f"  Spearman ρ model: {m_sr:.4f} ± {s_sr:.4f}  |  baseline: {m_sb:.4f}")

# ── Write report ──────────────────────────────────────────────────────────────
report_lines.append("## Per-Fold Results")
report_lines.append("")

for r in results:
    flag = " ⚠️ Partial (8 days)" if r['partial'] else ""
    report_lines.append(f"### {r['fold']}: {r['label']}{flag}")
    report_lines.append(f"Train records: {r['n_train']:,}  |  Test records: {r['n_test']:,}")
    report_lines.append("")
    report_lines.append("| K | Baseline | Vol-Only | Lift | Soft-PI | Lift |")
    report_lines.append("|---|---|---|---|---|---|")
    for k in [10, 20, 50]:
        report_lines.append(
            f"| {k} | {r[f'base_k{k}']:.2f}% | {r[f'vol_k{k}']:.2f}% | "
            f"{r[f'vol_lift_k{k}']:+.1f}% | {r[f'spi_k{k}']:.2f}% | "
            f"{r[f'spi_lift_k{k}']:+.1f}% |"
        )
    report_lines.append("")
    report_lines.append(
        f"**Pearson r:** Model={r['pearson_model']:.4f}  Baseline={r['pearson_base']:.4f}  "
        f"| **Spearman ρ:** Model={r['spearman_model']:.4f}  Baseline={r['spearman_base']:.4f}"
    )
    report_lines.append("")

report_lines.append("---")
report_lines.append("")
report_lines.append("## Overall Summary (Folds 1–4, full months only)")
report_lines.append("")
report_lines.append("| K | Mean Vol-Only Lift | Std Dev | Reliable? |")
report_lines.append("|---|---|---|---|")
for k in [10, 20, 50]:
    m, s = summary_rows[k]
    reliable = "✅ Yes" if abs(m) > s else "⚠️ Noisy"
    report_lines.append(f"| {k} | {m:+.1f}% | ±{s:.1f}% | {reliable} |")

report_lines.append("")
report_lines.append(
    f"**Mean Spearman ρ (model):** {m_sr:.4f} ± {s_sr:.4f}  "
    f"|  **Baseline:** {m_sb:.4f}"
)
report_lines.append("")
report_lines.append("> [!NOTE]")
report_lines.append(
    "> Fold 5 (April) is excluded from aggregate stats — only 8 days of test data "
    "make the percentage shares unreliable. The mean lift above is the honest figure."
)

# Per-fold table
report_lines.append("")
report_lines.append("## Full Per-Fold Table (Vol-Only Lift %)")
report_lines.append("")
report_lines.append("| Fold | K=10 | K=20 | K=50 | Spearman ρ |")
report_lines.append("|---|---|---|---|---|")
for r in results:
    partial_flag = " ⚠️" if r['partial'] else ""
    report_lines.append(
        f"| {r['fold']}: {r['label']}{partial_flag} | "
        f"{r['vol_lift_k10']:+.1f}% | {r['vol_lift_k20']:+.1f}% | "
        f"{r['vol_lift_k50']:+.1f}% | {r['spearman_model']:.4f} |"
    )

out_md = os.path.join(repo_root, 'walk_forward_cv_results.md')
with open(out_md, 'w') as f:
    f.write('\n'.join(report_lines))

print(f"\n✅  Report saved → {out_md}")
