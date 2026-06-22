import os, warnings, json
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.spatial import cKDTree
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict

warnings.filterwarnings('ignore')

# ── Paths ─────────────────────────────────────────────────────────────────────
script_dir   = os.path.dirname(os.path.abspath(__file__))
repo_root    = os.path.dirname(script_dir)
cleaned_path = os.path.join(repo_root, 'cleaned_violations.csv')

print("Loading clean data …")
df = pd.read_csv(cleaned_path)
df['ts_ist'] = pd.to_datetime(df['ts_ist'], utc=True).dt.tz_convert('Asia/Kolkata')
df['month']  = df['ts_ist'].dt.month
df['hour']   = df['ts_ist'].dt.hour

# Grid definition for GLM (500m)
GRID_DEG = 0.005
df['lat_c'] = (df['lat_g'] / GRID_DEG).round() * GRID_DEG
df['lon_c'] = (df['lon_g'] / GRID_DEG).round() * GRID_DEG
df['grid_c'] = df['lat_c'].round(4).astype(str) + ',' + df['lon_c'].round(4).astype(str)

# Nearest station for XGBoost
STATIONS = {
    'City Market': (12.9716, 77.5946), 'Shivajinagar': (12.9850, 77.6010),
    'Upparpet': (12.9720, 77.5800), 'Malleshwaram': (13.0035, 77.5700),
    'HAL Old Airport': (12.9650, 77.6600), 'KR Pura': (13.0000, 77.6900),
    'Kodigehalli': (13.0710, 77.5880), 'Magadi Road': (12.9740, 77.5510),
    'Rajajinagar': (12.9940, 77.5560), 'Vijayanagara': (12.9650, 77.5270),
    'Byatarayanapura': (13.0600, 77.5380), 'Electronic City': (12.8450, 77.6600),
    'HSR Layout': (12.9116, 77.6389), 'JP Nagar': (12.9063, 77.5857),
    'Whitefield': (12.9698, 77.7499), 'Jeevanbheemanagar': (12.9340, 77.6910),
}
def nearest_station(lat, lon):
    best, best_d = 'Unknown', 1e9
    for name, (slat, slon) in STATIONS.items():
        d = (lat - slat)**2 + (lon - slon)**2
        if d < best_d:
            best, best_d = name, d
    return best

if 'station' not in df.columns:
    df['station'] = df.apply(lambda r: nearest_station(r['lat_g'], r['lon_g']), axis=1)

FOLDS = [
    {'name':'Fold 2','label':'Nov–Dec → Jan','train':[11,12],       'test':1},
    {'name':'Fold 3','label':'Nov–Jan → Feb','train':[11,12,1],     'test':2},
    {'name':'Fold 4','label':'Nov–Feb → Mar','train':[11,12,1,2],   'test':3},
]

# ── Evaluator Helper ─────────────────────────────────────────────────────────
def evaluate_predictions(predicted_top_k_grids, actual_test_df, grid_col, k, total_cells):
    if len(actual_test_df) == 0:
        return {'p': 0, 'r': 0, 'f1': 0, 'acc': 0, 'br': 0, 'n': 0}
    
    actual_counts = actual_test_df.groupby(grid_col).size().reset_index(name='n')
    actual_top_k_grids = set(actual_counts.nlargest(k, 'n')[grid_col].tolist())
    predicted_set = set(predicted_top_k_grids)
    
    tp = len(predicted_set.intersection(actual_top_k_grids))
    fp = len(predicted_set - actual_top_k_grids)
    fn = len(actual_top_k_grids - predicted_set)
    tn = total_cells - tp - fp - fn
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    accuracy = (tp + tn) / total_cells if total_cells > 0 else 0
    base_rate = (total_cells - k) / total_cells if total_cells > 0 else 0
    
    return {
        'p': precision, 'r': recall, 'f1': f1,
        'acc': accuracy, 'br': base_rate, 'n': len(actual_test_df)
    }

# ── XGBoost Model Setup ───────────────────────────────────────────────────────
PEAK_HOURS = set(list(range(8,12)) + list(range(17,20)))

def build_xgb_features(train_clean, train_mos):
    all_grids = train_clean['grid_id'].unique()
    grid_mo = pd.MultiIndex.from_product([all_grids, train_mos], names=['grid_id','month']).to_frame(index=False)
    mo_counts = train_clean.groupby(['grid_id','month']).size().reset_index(name='y')
    panel = grid_mo.merge(mo_counts, on=['grid_id','month'], how='left').fillna({'y':0})
    
    static = train_clean.groupby('grid_id').agg(lat=('lat_g', 'first'), lon=('lon_g', 'first'), station=('station', 'first')).reset_index()
    clean_df = train_clean.copy()
    clean_df['is_peak'] = clean_df['hour'].isin(PEAK_HOURS).astype(float)
    peak = clean_df.groupby('grid_id')['is_peak'].mean().reset_index(name='peak_frac')
    static = static.merge(peak, on='grid_id', how='left').fillna({'peak_frac':0.5})
    
    le = LabelEncoder()
    static['station_id'] = le.fit_transform(static['station'])
    panel = panel.merge(static[['grid_id', 'lat', 'lon', 'station_id', 'peak_frac']], on='grid_id', how='left')
    
    mo_order = {m:i for i,m in enumerate(train_mos)}
    panel['mo_idx'] = panel['month'].map(mo_order)
    
    shifted1 = panel[['grid_id','mo_idx','y']].copy()
    shifted1['mo_idx'] += 1
    shifted1 = shifted1.rename(columns={'y':'Z_prev'})
    
    shifted2 = panel[['grid_id','mo_idx','y']].copy()
    shifted2['mo_idx'] += 2
    shifted2 = shifted2.rename(columns={'y':'Z_prev2'})
    
    panel = panel.merge(shifted1, on=['grid_id','mo_idx'], how='left').fillna({'Z_prev':0})
    panel = panel.merge(shifted2, on=['grid_id','mo_idx'], how='left').fillna({'Z_prev2':0})
    panel['Z_trend'] = panel['Z_prev'] - panel['Z_prev2']
    
    coords = static[['lat', 'lon']].values
    tree = cKDTree(coords)
    _, idx = tree.query(coords, k=9)
    nbr_idx = idx[:, 1:]
    
    zprev_matrix = panel.pivot(index='grid_id', columns='mo_idx', values='Z_prev')
    zprev_matrix = zprev_matrix.reindex(static['grid_id']).fillna(0).values
    zprev2_matrix = panel.pivot(index='grid_id', columns='mo_idx', values='Z_prev2')
    zprev2_matrix = zprev2_matrix.reindex(static['grid_id']).fillna(0).values
    
    sp_lags = []
    for mo_i in range(len(train_mos)):
        sp_lag1 = np.mean(zprev_matrix[nbr_idx, mo_i], axis=1)
        sp_lag2 = np.mean(zprev2_matrix[nbr_idx, mo_i], axis=1)
        df_sp = pd.DataFrame({'grid_id': static['grid_id'], 'mo_idx': mo_i, 'spatial_lag_Z': sp_lag1, 'spatial_lag_trend': sp_lag1 - sp_lag2})
        sp_lags.append(df_sp)
        
    sp_df = pd.concat(sp_lags, ignore_index=True)
    panel = panel.merge(sp_df, on=['grid_id','mo_idx'], how='left').fillna(0)
    
    features = ['Z_prev', 'Z_prev2', 'Z_trend', 'spatial_lag_Z', 'spatial_lag_trend', 'peak_frac', 'station_id']
    return panel, features

def train_xgb(train_df, train_mos):
    panel, features = build_xgb_features(train_df, train_mos)
    train_panel = panel[panel['mo_idx'] >= 2].copy()
    if len(train_panel) == 0:
        return None, features, panel
    X = train_panel[features]
    y = train_panel['y']
    model = xgb.XGBRegressor(objective='count:poisson', n_estimators=100, learning_rate=0.05, max_depth=4, random_state=42)
    model.fit(X, y)
    return model, features, panel

# ── GLM Model Setup ───────────────────────────────────────────────────────────
def compute_p_hat(train_df):
    rev = train_df[train_df['validation_status'].isin(['approved','rejected'])].copy()
    if len(rev) == 0: return {}
    stats = rev.groupby('created_by_id')['validation_status'].value_counts().unstack(fill_value=0)
    for c in ['approved','rejected']:
        if c not in stats.columns: stats[c] = 0
    stats['p_hat'] = (5 + stats['approved']) / (7 + stats['approved'] + stats['rejected'])
    return stats['p_hat'].to_dict()

def tune_blend_weight(pred_df, train_df, train_mos):
    if len(train_mos) < 2: return 0.5
    inner_train_mos = train_mos[:-1]
    inner_test_mo   = train_mos[-1]
    inner_train = train_df[train_df['month'].isin(inner_train_mos)]
    inner_test  = train_df[train_df['month'] == inner_test_mo]
    if len(inner_train) == 0 or len(inner_test) == 0: return 0.5
    
    base_counts = inner_train.groupby('grid_c').size().reset_index(name='baseline')
    last_m = inner_train_mos[-1]
    last_counts = inner_train[inner_train['month'] == last_m].groupby('grid_c').size().reset_index(name='model')
    
    preds = base_counts.merge(last_counts, on='grid_c', how='left').fillna({'model': 0})
    n_test = len(inner_test)
    if n_test == 0: return 0.5
    
    best_w, best_lift = 0.5, -999
    for w in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        preds['blended'] = w * preds['baseline'] + (1 - w) * preds['model']
        base_grids = preds.nlargest(20, 'baseline')['grid_c'].tolist()
        blend_grids = preds.nlargest(20, 'blended')['grid_c'].tolist()
        base_vol = inner_test[inner_test['grid_c'].isin(base_grids)].shape[0]
        blend_vol = inner_test[inner_test['grid_c'].isin(blend_grids)].shape[0]
        lift = blend_vol - base_vol
        if lift > best_lift:
            best_lift = lift; best_w = w
    return best_w

def train_glm(train_clean, train_mos):
    all_grids = train_clean['grid_c'].unique().tolist()
    grid_mo_idx = pd.MultiIndex.from_product([all_grids, train_mos], names=['grid_c','month']).to_frame(index=False)
    mo_counts = train_clean.groupby(['grid_c','month']).size().reset_index(name='y')
    panel = grid_mo_idx.merge(mo_counts, on=['grid_c','month'], how='left').fillna({'y': 0})
    
    mo_order = {m: i for i, m in enumerate(train_mos)}
    panel['mo_idx'] = panel['month'].map(mo_order)
    shifted = panel.copy()
    shifted['mo_idx'] = shifted['mo_idx'] - 1
    shifted = shifted.rename(columns={'y': 'Z_prev_lag'})
    panel = panel.merge(shifted[['grid_c','mo_idx','Z_prev_lag']], on=['grid_c','mo_idx'], how='left').fillna({'Z_prev_lag': 0})
    
    try:
        glm = smf.glm('y ~ np.log(Z_prev_lag + 1)', data=panel, family=sm.families.Poisson()).fit(disp=0)
        coefs = glm.params.to_dict()
    except:
        coefs = None
        
    return coefs, all_grids

# ── Main Loop ─────────────────────────────────────────────────────────────────
results_agg = []
subgroups = {
    'vehicle_type': df['vehicle_type'].dropna().unique().tolist(),
    'police_station': df['police_station'].dropna().unique().tolist(),
}

print("Running Stratified Evaluation...")

for fold in FOLDS:
    fname = fold['name']
    print(f"Processing {fname}...")
    train_df = df[df['month'].isin(fold['train'])].copy()
    test_df  = df[df['month'] == fold['test']].copy()
    
    # XGBoost Prep
    xgb_model, xgb_feats, xgb_panel = train_xgb(train_df, fold['train'])
    test_mo_idx = len(fold['train'])
    pred_panel_xgb = xgb_panel[xgb_panel['mo_idx'] == test_mo_idx - 1].copy()
    pred_panel_xgb['mo_idx'] = test_mo_idx
    shifted_for_pred1 = xgb_panel[xgb_panel['mo_idx'] == test_mo_idx - 1][['grid_id','y']].rename(columns={'y':'Z_prev'})
    shifted_for_pred2 = xgb_panel[xgb_panel['mo_idx'] == test_mo_idx - 2][['grid_id','y']].rename(columns={'y':'Z_prev2'})
    pred_panel_xgb = pred_panel_xgb.drop(columns=['Z_prev', 'Z_prev2', 'Z_trend', 'y']).merge(shifted_for_pred1, on='grid_id', how='left').merge(shifted_for_pred2, on='grid_id', how='left').fillna(0)
    pred_panel_xgb['Z_trend'] = pred_panel_xgb['Z_prev'] - pred_panel_xgb['Z_prev2']
    
    if xgb_model:
        pred_panel_xgb['xgb_pred'] = xgb_model.predict(pred_panel_xgb[xgb_feats])
    else:
        pred_panel_xgb['xgb_pred'] = pred_panel_xgb['Z_prev']
    
    # GLM Prep
    p_hat_dict = compute_p_hat(train_df)
    train_df['p_hat'] = train_df['created_by_id'].map(p_hat_dict).fillna(5/7)
    train_clean = train_df[train_df['p_hat'] >= 0.50].copy()
    
    glm_coefs, glm_grids = train_glm(train_clean, fold['train'])
    last_mo = fold['train'][-1]
    zprev = train_clean[train_clean['month'] == last_mo].groupby('grid_c').size().reset_index(name='Z_prev')
    train_counts = train_clean.groupby('grid_c').size().reset_index(name='train_count')
    
    pred_df_glm = pd.DataFrame({'grid_c': glm_grids})
    pred_df_glm = pred_df_glm.merge(zprev, on='grid_c', how='left').fillna({'Z_prev': 0})
    pred_df_glm = pred_df_glm.merge(train_counts, on='grid_c', how='left').fillna({'train_count': 0})
    
    if glm_coefs:
        pred_df_glm['pred_vol'] = np.exp(glm_coefs['Intercept'] + np.log(pred_df_glm['Z_prev'] + 1) * glm_coefs['np.log(Z_prev_lag + 1)'])
    else:
        pred_df_glm['pred_vol'] = pred_df_glm['Z_prev']
        
    best_w = tune_blend_weight(pred_df_glm, train_clean, fold['train'])
    pred_df_glm['EPS_blend'] = best_w * pred_df_glm['train_count'] + (1 - best_w) * pred_df_glm['pred_vol']
    
    for k in [20, 50]:
        xgb_top_k = pred_panel_xgb.nlargest(k, 'xgb_pred')['grid_id'].tolist()
        glm_top_k = pred_df_glm.nlargest(k, 'EPS_blend')['grid_c'].tolist()
        
        xgb_total_cells = len(pred_panel_xgb)
        glm_total_cells = len(pred_df_glm)
        
        # Overall
        xgb_eval = evaluate_predictions(xgb_top_k, test_df, 'grid_id', k, xgb_total_cells)
        glm_eval = evaluate_predictions(glm_top_k, test_df, 'grid_c', k, glm_total_cells)
        
        results_agg.append({'fold': fname, 'k': k, 'model': 'XGBoost', 'group': 'Overall', 'subgroup': 'Overall', **xgb_eval})
        results_agg.append({'fold': fname, 'k': k, 'model': 'GLM-Ensemble', 'group': 'Overall', 'subgroup': 'Overall', **glm_eval})
        
        # Stratified
        for group_name, sub_vals in subgroups.items():
            for sub_val in sub_vals:
                sub_test = test_df[test_df[group_name] == sub_val]
                x_ev = evaluate_predictions(xgb_top_k, sub_test, 'grid_id', k, xgb_total_cells)
                g_ev = evaluate_predictions(glm_top_k, sub_test, 'grid_c', k, glm_total_cells)
                results_agg.append({'fold': fname, 'k': k, 'model': 'XGBoost', 'group': group_name, 'subgroup': sub_val, **x_ev})
                results_agg.append({'fold': fname, 'k': k, 'model': 'GLM-Ensemble', 'group': group_name, 'subgroup': sub_val, **g_ev})

res_df = pd.DataFrame(results_agg)

# Format to markdown
md = ["# Stratified Evaluation Results\\n\\nThis report measures classification metrics (Precision, Recall, F1, Accuracy) for our models' Predicted Top-K hotspots against actual Top-K subgroups.\\n"]

# Findings
md.append("## Findings: Operational Blind Spots\\n")
k20 = res_df[(res_df['k'] == 20) & (res_df['n'] >= 30) & (res_df['group'] != 'Overall')]
worst_prec = k20.loc[k20['p'].idxmin()]
worst_rec = k20.loc[k20['r'].idxmin()]
md.append(f"- **Lowest Precision Subgroup (K=20):** `{worst_prec['subgroup']}` ({worst_prec['group']}) with {worst_prec['model']} | Precision: {worst_prec['p']:.1%} (n={worst_prec['n']})")
md.append(f"- **Lowest Recall Subgroup (K=20):** `{worst_rec['subgroup']}` ({worst_rec['group']}) with {worst_rec['model']} | Recall: {worst_rec['r']:.1%} (n={worst_rec['n']})")
md.append("\\n---\\n")

def format_table(df_sub):
    agg = df_sub.groupby(['group', 'subgroup', 'model', 'k']).agg({'p':'mean', 'r':'mean', 'f1':'mean', 'acc':'mean', 'br':'mean', 'n':'sum'}).reset_index()
    lines = ["| Subgroup | Model | K | Precision | Recall | F1 Score | Accuracy (vs Base Rate) | n (test) |", "|---|---|---|---|---|---|---|---|"]
    for _, r in agg.sort_values(['group', 'subgroup', 'k', 'model']).iterrows():
        if r['n'] < 30:
            lines.append(f"| {r['subgroup']} | {r['model']} | {r['k']} | `low_confidence: true` | - | - | - | {r['n']:.0f} |")
        else:
            acc_str = f"{r['acc']:.1%} (BR: {r['br']:.1%})"
            lines.append(f"| {r['subgroup']} | {r['model']} | {r['k']} | {r['p']:.1%} | {r['r']:.1%} | {r['f1']:.3f} | {acc_str} | {r['n']:.0f} |")
    return "\\n".join(lines)

md.append("## Overall Metrics\\n")
md.append(format_table(res_df[res_df['group'] == 'Overall']))

md.append("\\n## By Vehicle Type\\n")
md.append(format_table(res_df[res_df['group'] == 'vehicle_type']))

md.append("\\n## By Police Station\\n")
md.append(format_table(res_df[res_df['group'] == 'police_station']))

with open(os.path.join(repo_root, "stratified_evaluation_results.md"), "w") as f:
    f.write("\\n".join(md))

print("Results written to stratified_evaluation_results.md")
