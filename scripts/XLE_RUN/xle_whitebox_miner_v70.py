import pandas as pd
import numpy as np
import os
import sys
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split

# Root Path
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"

def run_whitebox_miner_v70():
    print("=== ACE: SOVEREIGN WHITE-BOX MINER V70 (70% DEPTH) ===")
    
    file_path = os.path.join(ROOT, 'data/enriched/US/ENERGY_MasterV70.csv')
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found. Run enrichment v70 first.")
        return
        
    df = pd.read_csv(file_path)
    
    # 1. Labeling Tier 2/3 drops (Target)
    df['Forward_Min'] = df['Close'].shift(-45).rolling(window=45, min_periods=1).min()
    df['Future_DD'] = (df['Forward_Min'] - df['Close']) / df['Close']
    # 70% Depth specific: Identify clean structural resets
    df['Is_Crash'] = (df['Future_DD'] <= -0.15).astype(int) 
    
    # 2. Encoding categorical
    df_encoded = pd.get_dummies(df, columns=['Mahadasha', 'Antardasha'])
    
    exclude = ['Date', 'Close', 'Forward_Min', 'Future_DD', 'Is_Crash']
    X = df_encoded.drop(columns=exclude)
    y = df_encoded['Is_Crash']
    
    # 3. Decision Tree fit (White Box)
    # Increased depth to 6 to capture Yogas/Aspects combinations
    dt = DecisionTreeClassifier(max_depth=6, min_samples_leaf=15, class_weight='balanced')
    dt.fit(X, y)
    
    # 4. Rules extraction
    rules = export_text(dt, feature_names=list(X.columns))
    
    print("\n" + "="*70)
    print("V70 SOVEREIGN PATTERN EXTRACTION (RULES)")
    print("="*70)
    print(rules)
    print("="*70)
    
    # Importance ranking
    importances = pd.Series(dt.feature_importances_, index=X.columns).sort_values(ascending=False).head(15)
    print("\nTop 15 Sovereign High-Impact Triggers:")
    print(importances)

if __name__ == "__main__":
    run_whitebox_miner_v70()
