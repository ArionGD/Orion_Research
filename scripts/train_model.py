import pandas as pd
import numpy as np
import os
import joblib
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score

def train_specialized_model(df, feature_cols, target_col, model_name, 
                             threshold=0.5, n_est=200, depth=5, lr=0.03):
    print(f"\n{'='*50}")
    print(f"  TRAINING: {model_name.upper()}")
    print(f"  Threshold: {threshold:.0%} | Trees: {n_est} | Depth: {depth}")
    print(f"{'='*50}")
    
    # Ensure features are unique to prevent XGBoost Duplicate Column errors
    feature_cols = list(dict.fromkeys(feature_cols))
    
    df_clean = df.dropna(subset=feature_cols + [target_col])
    
    missing_cols = [c for c in feature_cols if c not in df_clean.columns]
    if missing_cols:
        print(f"Error: Missing columns {missing_cols}")
        return None
    
    X = df_clean[feature_cols]
    y = df_clean[target_col]
    
    print(f"  Total samples (WEEKLY): {len(df_clean)}")
    
    # NON-LINEAR LOGARITHMIC WEIGHTING (Sovereign Evolution)
    # Prioritizing Modern Era (2000-2024) while retaining 1929 wisdom
    years_from_start = (df_clean.index - df_clean.index.min()).days / 365.25
    # Logarithmic decay: weight = log(1 + years)
    sample_weights = np.log1p(years_from_start)
    
    # Stratified Train/Test
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test, w_train, w_test = train_test_split(
        X, y, sample_weights, test_size=0.2, random_state=42, shuffle=True
    )
    
    pos_count = np.sum(y_train == 1)
    neg_count = np.sum(y_train == 0)
    spw = (neg_count / pos_count if pos_count > 0 else 1.0)
    
    model = XGBClassifier(
        n_estimators=n_est,
        learning_rate=lr,
        max_depth=depth,
        scale_pos_weight=spw,
        random_state=42,
        eval_metric='logloss',
        reg_alpha=2.0, # Increased regularization for 'Pure' signals
        reg_lambda=10.0,
        subsample=0.8,
        colsample_bytree=0.8
    )
    
    # Fit with Logarithmic Weights
    model.fit(X_train, y_train, sample_weight=w_train)
    
    # Threshold scan to find sweet spot
    y_proba = model.predict_proba(X_test)[:, 1]
    
    print(f"\n  THRESHOLD SCAN:")
    print(f"  {'THRESH':>8} | {'PRECISION':>10} | {'RECALL':>8} | {'SIGNALS':>8}")
    best_t = 0.50
    best_prec = 0
    for t in [0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80]:
        y_p = (y_proba >= t).astype(int)
        fires = np.sum(y_p == 1)
        if fires == 0:
            print(f"  {t:>8.2f} |        N/A |      N/A |    0/{len(y_test)}")
            continue
        prec = precision_score(y_test, y_p, zero_division=0)
        rec = recall_score(y_test, y_p, zero_division=0)
        print(f"  {t:>8.2f} | {prec:>9.2%} | {rec:>7.2%} | {fires:>4}/{len(y_test)}")
        # Pick best threshold where precision is maximized AND recall > 1%
        if prec > best_prec and rec > 0.01:
            best_prec = prec
            best_t = t
    
    # Final evaluation at best threshold
    y_final = (y_proba >= best_t).astype(int)
    final_prec = precision_score(y_test, y_final, zero_division=0)
    final_rec = recall_score(y_test, y_final, zero_division=0)
    final_fires = np.sum(y_final == 1)
    
    print(f"\n  BEST THRESHOLD: {best_t:.2f}")
    print(f"  FINAL PRECISION: {final_prec:.2%}")
    print(f"  FINAL RECALL: {final_rec:.2%}")
    print(f"  SIGNALS: {final_fires}/{len(y_test)}")
    
    save_path = f'models/arion_v2_{model_name}.joblib'
    joblib.dump(model, save_path)
    config = {'threshold': best_t, 'features': feature_cols, 
              'precision': final_prec, 'recall': final_rec}
    joblib.dump(config, f'models/arion_v2_{model_name}_config.joblib')
    
    return model

def train_all_tiers():
    file_path = 'data/processed/refined_features.csv'
    df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
    # One-Hot Encode Dasha Categories for ML
    df = pd.get_dummies(df, columns=['Mahadasha', 'Antardasha'])
    dasha_cols = [c for c in df.columns if 'Mahadasha_' in c or 'Antardasha_' in c]
    
    speed_cols = [c for c in df.columns if 'Speed' in c and 'Moon' not in c]
    
    # SOVEREIGN CRASH PREDATOR FEATURES (Pure Astro + Strategic technicals)
    crash_feats = [
        'Sovereign_Malefic_Index', 'Saturn_Neptune_Angle', 'aspect_intensity', 
        'Global_Stability_Index', 'True_Node_Lon', 'retrograde_count', 
        'is_hard_aspect', 'is_applying', 'Havoc_Velocity', 'OOB_Count',
        'Mars_OOB_Intensity', 'Bradley_Score', 'Gann_Price_Deg', 'is_gann_collision',
        'Jupiter_Helio_Speed', 'Saturn_Helio_Speed', 'Mars_Helio_Speed',
        # Stress Triggers (Final Validation Layer)
        'VIX_Stress_Ratio', 'Yield_Curve_Inverted'
    ] + speed_cols + dasha_cols
    
    # 1. Train the Specialized CRASH Predator Model (-20% Target)
    print("\n--- PHASE 1: SOVEREIGN CRASH PREDATOR (-20%) ---")
    train_specialized_model(df, crash_feats, 'Crash_20pct_6M', 'crash_predator',
                           n_est=600, depth=4, lr=0.01)
    
    # 2. Train the Specialized CORRECTION Predator Model (-10% Target)
    print("\n--- PHASE 2: SOVEREIGN CORRECTION PREDATOR (-10%) ---")
    train_specialized_model(df, crash_feats, 'Crash_10pct_6M', 'correction_predator',
                           n_est=600, depth=4, lr=0.01)
    
    # 3. Train the Specialized PULSE Predator Model (-5% Target)
    print("\n--- PHASE 3: SOVEREIGN PULSE PREDATOR (-5%) ---")
    train_specialized_model(df, crash_feats, 'Crash_5pct_6M', 'pulse_predator',
                           n_est=600, depth=4, lr=0.01)

if __name__ == "__main__":
    os.makedirs('models', exist_ok=True)
    train_all_tiers()
