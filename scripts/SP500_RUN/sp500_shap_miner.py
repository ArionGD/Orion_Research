import pandas as pd
import numpy as np
import os
import sys
import xgboost as xgb
import shap

# Root Path
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"

def run_sp500_shap_miner():
    print("=== ACE: SP500 SHAP MINER (100-YEAR TRANSPARENCY) ===")
    
    file_path = os.path.join(ROOT, 'data/enriched/US/SP500/SP500_MasterV70.csv')
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return
        
    df = pd.read_csv(file_path)
    
    # 1. Target: Macro Reset (-8% in 45 days)
    df['Forward_Min'] = df['Close'].shift(-45).rolling(window=45, min_periods=1).min()
    df['Future_DD'] = (df['Forward_Min'] - df['Close']) / df['Close']
    df['Is_Crash'] = (df['Future_DD'] <= -0.08).astype(int)
    
    # 2. Variable Selection
    exclude = ['Date', 'Close', 'Forward_Min', 'Future_DD', 'Is_Crash']
    X = pd.get_dummies(df.drop(columns=exclude), columns=['Mahadasha', 'Antardasha']).fillna(0)
    y = df['Is_Crash']
    
    # 3. Train High-Velocity Oracle
    print("\nTraining XGBoost Oracle on 100 years of Macro DNA...")
    model = xgb.XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42)
    model.fit(X, y)
    
    # 4. Extract SHAP Explanations (The Glass-Box equivalent)
    print("Calculating SHAP values (Sovereign Interaction Keys)...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    
    # 5. Global Feature Importance (Mean SHAP)
    vals = np.abs(shap_values).mean(0)
    feature_importance = pd.DataFrame(list(zip(X.columns, vals)), columns=['col_name','feature_importance_vals'])
    feature_importance.sort_values(by=['feature_importance_vals'], ascending=False, inplace=True)
    
    print("\n" + "="*70)
    print("SP500 SHAP GLOBAL IMPORTANCE (100-YEARS)")
    print("="*70)
    for idx, row in feature_importance.head(15).iterrows():
        print(f"FEATURE: {row['col_name']:<20} | SHAP Importance: {row['feature_importance_vals']:.4f}")
    print("="*70)
    
    print(f"\nMacro Logic Seal Accuracy: {model.score(X, y):.4f}")

if __name__ == "__main__":
    run_sp500_shap_miner()
