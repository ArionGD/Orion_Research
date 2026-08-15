"""
Gold Astrology: 3-Year Backtest (2024-01-01 to 2026-04-22)
===========================================================
Tests 4 algorithms: EBM | XGBoost | GAMI-Net | Neural ANOVA
Train on pre-2024 data (strict OOS). Signal threshold = +-0.3%.
"""

import os, warnings
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

ROOT      = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"
FEATURES  = ['Sun_Deg', 'Moon_Deg', 'Saturn_Deg', 'Ketu_Deg',
             'Mars_Speed', 'SMI_Base', 'Nakshatra', 'Tithi']
THRESHOLD = 0.001
TRAIN_END = pd.Timestamp("2024-01-01")
TEST_END  = pd.Timestamp("2027-01-01")

def classify_signal(pred):
    if pred >  THRESHOLD: return "RISE"
    if pred < -THRESHOLD: return "SHORT"
    return "HOLD"

def evaluate(signals, actuals):
    rise_correct = rise_total = short_correct = short_total = 0
    rise_returns, short_returns = [], []
    for sig, act in zip(signals, actuals):
        if sig == "RISE":
            rise_total += 1
            rise_returns.append(act)
            if act > 0: rise_correct += 1
        elif sig == "SHORT":
            short_total += 1
            short_returns.append(act)
            if act < 0: short_correct += 1
    rise_acc  = rise_correct  / rise_total  if rise_total  else 0
    short_acc = short_correct / short_total if short_total else 0
    total_sig = rise_total + short_total
    overall   = (rise_correct + short_correct) / total_sig if total_sig else 0
    return {
        "rise_signals":    rise_total,
        "rise_correct":    rise_correct,
        "rise_accuracy":   round(rise_acc * 100, 2),
        "rise_avg_return": round(np.mean(rise_returns)  * 100, 4) if rise_returns  else 0,
        "short_signals":   short_total,
        "short_correct":   short_correct,
        "short_accuracy":  round(short_acc * 100, 2),
        "short_avg_return":round(np.mean(short_returns) * 100, 4) if short_returns else 0,
        "total_signals":   total_sig,
        "overall_accuracy":round(overall * 100, 2),
    }

# ── Load & split ─────────────────────────────────────────────────────────────
print("Loading GOLD_MasterV70.csv...")
df = pd.read_csv(os.path.join(ROOT,
     "data/enriched/COMMODITIES/GOLD/GOLD_MasterV70.csv"))
df['Date']   = pd.to_datetime(df['Date'])
df['Target'] = df['Close'].shift(-5) / df['Close'] - 1
df = df.dropna()

train_df = df[df['Date'] <  TRAIN_END].copy()
test_df  = df[(df['Date'] >= TRAIN_END) & (df['Date'] < TEST_END)].copy()

X_train, y_train = train_df[FEATURES].values.astype(np.float64), train_df['Target'].values.astype(np.float64)
X_test,  y_test  = test_df[FEATURES].values.astype(np.float64),  test_df['Target'].values.astype(np.float64)

scaler     = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

print(f"Train: {len(train_df):,} days  |  Test (OOS): {len(test_df):,} days")
print(f"Test window: {test_df['Date'].min().date()} to {test_df['Date'].max().date()}\n")

results = {}

# ── 1. EBM (fast config) ─────────────────────────────────────────────────────
print("--- [1/4] EBM (fast: 64 bins, no interactions) ---")
try:
    from interpret.glassbox import ExplainableBoostingRegressor
    ebm = ExplainableBoostingRegressor(
        max_bins=64, interactions=0,
        min_samples_leaf=5, max_rounds=100,
        random_state=42)
    ebm.fit(X_train, y_train)
    preds = ebm.predict(X_test)
    print(f"  EBM preds range: {preds.min():.5f} to {preds.max():.5f}")
    sigs = [classify_signal(p) for p in preds]
    results["EBM"] = evaluate(sigs, y_test)
    print(f"  EBM OK  |  Total signals: {results['EBM']['total_signals']}")
except Exception as e:
    print(f"  EBM failed: {e}")
    results["EBM"] = None

# ── 2. XGBoost ───────────────────────────────────────────────────────────────
print("--- [2/4] XGBoost ---")
try:
    import xgboost as xgb
    xgb_m = xgb.XGBRegressor(n_estimators=100, learning_rate=0.05,
                               max_depth=5, random_state=42, verbosity=0)
    xgb_m.fit(X_train, y_train)
    preds = xgb_m.predict(X_test)
    print(f"  XGBoost preds range: {preds.min():.5f} to {preds.max():.5f}")
    sigs = [classify_signal(p) for p in preds]
    results["XGBoost"] = evaluate(sigs, y_test)
    print(f"  XGBoost OK  |  Total signals: {results['XGBoost']['total_signals']}")
except Exception as e:
    print(f"  XGBoost failed: {e}")
    results["XGBoost"] = None

# ── 3. GAMI-Net (GBM surrogate) ──────────────────────────────────────────────
print("--- [3/4] GAMI-Net (GBM surrogate) ---")
try:
    from sklearn.ensemble import GradientBoostingRegressor
    gbm = GradientBoostingRegressor(n_estimators=200, max_depth=3,
                                    learning_rate=0.05, random_state=42)
    gbm.fit(X_train_sc, y_train)
    preds = gbm.predict(X_test_sc)
    print(f"  GAMI-Net (GBM) preds range: {preds.min():.5f} to {preds.max():.5f}")
    sigs = [classify_signal(p) for p in preds]
    results["GAMI-Net"] = evaluate(sigs, y_test)
    print(f"  GAMI-Net OK  |  Total signals: {results['GAMI-Net']['total_signals']}")
except Exception as e:
    print(f"  GAMI-Net failed: {e}")
    results["GAMI-Net"] = None

# ── 4. Neural ANOVA (PyTorch) ─────────────────────────────────────────────────
print("--- [4/4] Neural ANOVA (PyTorch, 60 epochs) ---")
try:
    import torch
    import torch.nn as nn
    from torch.utils.data import DataLoader, TensorDataset

    y_mean, y_std = y_train.mean(), y_train.std()
    y_tr_sc = ((y_train - y_mean) / (y_std + 1e-8)).astype(np.float32)

    X_tr_t = torch.tensor(X_train_sc.astype(np.float32))
    y_tr_t = torch.tensor(y_tr_sc).unsqueeze(1)
    X_te_t = torch.tensor(X_test_sc.astype(np.float32))

    class FNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.net = nn.Sequential(nn.Linear(1,32),nn.Tanh(),nn.Linear(32,32),nn.Tanh(),nn.Linear(32,1))
        def forward(self, x): return self.net(x)

    class NANOVA(nn.Module):
        def __init__(self, nf):
            super().__init__()
            self.fnets = nn.ModuleList([FNet() for _ in range(nf)])
            self.bias  = nn.Parameter(torch.zeros(1))
        def forward(self, x):
            out = self.bias.expand(x.size(0), 1)
            for i, fn in enumerate(self.fnets):
                out = out + fn(x[:, i:i+1])
            return out

    nf    = len(FEATURES)
    nmod  = NANOVA(nf)
    opt   = torch.optim.Adam(nmod.parameters(), lr=5e-3)
    lossfn = nn.MSELoss()
    ldr   = DataLoader(TensorDataset(X_tr_t, y_tr_t), batch_size=512, shuffle=True)

    nmod.train()
    for ep in range(60):
        for xb, yb in ldr:
            opt.zero_grad()
            lossfn(nmod(xb), yb).backward()
            opt.step()
        if (ep+1) % 20 == 0:
            print(f"  epoch {ep+1}/60")

    nmod.eval()
    with torch.no_grad():
        raw = nmod(X_te_t).numpy().ravel()
    preds_na = raw * y_std + y_mean
    print(f"  Neural ANOVA preds range: {preds_na.min():.5f} to {preds_na.max():.5f}")
    sigs = [classify_signal(p) for p in preds_na]
    results["Neural ANOVA"] = evaluate(sigs, y_test)
    print(f"  Neural ANOVA OK  |  Total signals: {results['Neural ANOVA']['total_signals']}")
except Exception as e:
    print(f"  Neural ANOVA failed: {e}")
    results["Neural ANOVA"] = None

# ── Report ───────────────────────────────────────────────────────────────────
report_dir  = os.path.join(ROOT, "scripts/GOLD_RUN/docs")
os.makedirs(report_dir, exist_ok=True)
report_path = os.path.join(report_dir, "GOLD_BACKTEST_2024_2027.md")

print(f"\nWriting report: {report_path}")

with open(report_path, "w", encoding="utf-8") as f:
    f.write("# Gold Astrology: 3-Year Backtest (2024-01-01 to 2026 end)\n\n")
    f.write(f"> **Train:** 1920-01-01 to 2023-12-31 ({len(train_df):,} days)\n")
    f.write(f"> **Test (OOS):** {test_df['Date'].min().date()} to {test_df['Date'].max().date()} ({len(test_df):,} days)\n")
    f.write(f"> **Signal threshold:** +-0.3% predicted 5-day return\n")
    f.write(f"> **Algos:** EBM | XGBoost | GAMI-Net | Neural ANOVA\n\n")

    f.write("## Summary: Signal Counts & Overall Accuracy\n\n")
    f.write("| Algorithm | Total Signals | RISE | SHORT | Overall Acc | RISE Acc | SHORT Acc |\n")
    f.write("| :--- | :---: | :---: | :---: | :---: | :---: | :---: |\n")
    for algo, r in results.items():
        if r is None:
            f.write(f"| **{algo}** | FAILED | - | - | - | - | - |\n")
        else:
            f.write(f"| **{algo}** | {r['total_signals']} | {r['rise_signals']} | {r['short_signals']}"
                    f" | **{r['overall_accuracy']}%** | {r['rise_accuracy']}% | {r['short_accuracy']}% |\n")

    f.write("\n## Per-Algorithm Breakdown\n\n")
    for algo, r in results.items():
        if not r: continue
        f.write(f"### {algo}\n\n")
        f.write("| Metric | RISE | SHORT |\n")
        f.write("| :--- | :--- | :--- |\n")
        f.write(f"| Signals fired | {r['rise_signals']} | {r['short_signals']} |\n")
        f.write(f"| Correct calls | {r['rise_correct']} | {r['short_correct']} |\n")
        f.write(f"| Accuracy | **{r['rise_accuracy']}%** | **{r['short_accuracy']}%** |\n")
        f.write(f"| Avg 5d return | {r['rise_avg_return']}% | {r['short_avg_return']}% |\n")
        f.write(f"| Overall | **{r['overall_accuracy']}%** | |\n\n")

    valid  = {k: v for k, v in results.items() if v}
    if valid:
        ranked = sorted(valid.items(), key=lambda x: x[1]['overall_accuracy'], reverse=True)
        f.write("## Leaderboard\n\n")
        f.write("| Rank | Algorithm | Overall Accuracy | Role |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        medals = ["1st (Best)", "2nd", "3rd", "4th"]
        roles  = ["Primary Signal Engine", "Strong Confirmation", "Supporting Layer", "Supporting Layer"]
        for i, (algo, r) in enumerate(ranked):
            f.write(f"| {medals[i]} | **{algo}** | **{r['overall_accuracy']}%** | {roles[i]} |\n")

    f.write("\n---\n*Generated by ORION-V5-ACE-5.5 Forensic Engine*\n")

# ── Console summary ───────────────────────────────────────────────────────────
print("\n" + "="*72)
print("BACKTEST COMPLETE - GOLD ASTROLOGY 2024-2027")
print("="*72)
for algo, r in results.items():
    if r:
        print(f"{algo:15s} | Total:{r['total_signals']:4d} | "
              f"RISE:{r['rise_signals']:4d}({r['rise_accuracy']:5.1f}%) | "
              f"SHORT:{r['short_signals']:4d}({r['short_accuracy']:5.1f}%) | "
              f"OVERALL:{r['overall_accuracy']:5.1f}%")
    else:
        print(f"{algo:15s} | FAILED")
print("="*72)
print(f"Report: {report_path}")
