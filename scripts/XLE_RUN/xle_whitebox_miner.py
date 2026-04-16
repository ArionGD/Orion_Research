import pandas as pd
import numpy as np
import os
import sys
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split

# Root Path
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"

def run_whitebox_dte_miner():
    print("=== ACE: SOVEREIGN WHITE-BOX MINER (DTE) ===")
    
    file_path = os.path.join(ROOT, 'data/enriched/US/ENERGY_XLE_v50.csv')
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found. Run enrichment first.")
        return
        
    df = pd.read_csv(file_path)
    
    # 1. Labeling: Find the target (Tier 2/3 drops)
    # Target = Does the price drop > 10% in the next 30 days?
    df['Forward_Min'] = df['Close'].shift(-30).rolling(window=30, min_periods=1).min()
    df['Future_DD'] = (df['Forward_Min'] - df['Close']) / df['Close']
    df['Is_Crash'] = (df['Future_DD'] <= -0.10).astype(int)
    
    # 2. Feature Selection (Drop price/dates/leaks)
    exclude = ['Date', 'Close', 'Forward_Min', 'Future_DD', 'Is_Crash']
    
    # Encode Categorical (Dasha)
    df_encoded = pd.get_dummies(df, columns=['Mahadasha', 'Antardasha'])
    
    X = df_encoded.drop(columns=exclude)
    y = df_encoded['Is_Crash']
    
    # 3. Fit White-Box Decision Tree
    # Max depth 4 to keep rules "Human Readable"
    dt = DecisionTreeClassifier(max_depth=5, min_samples_leaf=20, class_weight='balanced')
    dt.fit(X, y)
    
    # 4. Extract Rules
    rules = export_text(dt, feature_names=list(X.columns))
    
    print("\n" + "="*60)
    print("EXTRACTED SOVEREIGN RULES (XLE KILL-ZONES)")
    print("="*60)
    print(rules)
    print("="*60)
    
    # Summary of Importance
    importances = pd.Series(dt.feature_importances_, index=X.columns).sort_values(ascending=False).head(10)
    print("\nTop 10 Sovereign Triggers (Variable Importance):")
    print(importances)

if __name__ == "__main__":
    run_whitebox_dte_miner()
