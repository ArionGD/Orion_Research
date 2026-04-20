import pandas as pd
import numpy as np
import os
import sys
from sklearn.tree import DecisionTreeClassifier, export_text

# Root Path
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"

def run_sp500_miner_v70():
    print("=== ACE: SP500 WHITE-BOX MINER V70 (MACRO) ===")
    
    file_path = os.path.join(ROOT, 'data/enriched/US/SP500/SP500_MasterV70.csv')
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found. Wait for enrichment to finish.")
        return
        
    df = pd.read_csv(file_path)
    
    # 1. Labeling Macro Resets (Target)
    # SP500 is less volatile than XLE. -8% in 45 days is a Tier 3 event.
    df['Forward_Min'] = df['Close'].shift(-45).rolling(window=45, min_periods=1).min()
    df['Future_DD'] = (df['Forward_Min'] - df['Close']) / df['Close']
    df['Is_Crash'] = (df['Future_DD'] <= -0.08).astype(int)
    
    # 2. Variable Selection
    exclude = ['Date', 'Close', 'Forward_Min', 'Future_DD', 'Is_Crash']
    X = pd.get_dummies(df.drop(columns=exclude), columns=['Mahadasha', 'Antardasha']).fillna(0)
    y = df['Is_Crash']
    
    # 3. Train White-Box Oracle
    print("Training Decision Tree (Macro Logic)...")
    clf = DecisionTreeClassifier(max_depth=5, min_samples_leaf=20, class_weight='balanced')
    clf.fit(X, y)
    
    # 4. Export Lethal Rules
    rules = export_text(clf, feature_names=list(X.columns))
    
    print("\n" + "="*70)
    print("THE SP500 MACRO RESET RULES (DTE)")
    print("="*70)
    print(rules)
    print("="*70)
    
    # 5. Global Feature Importance
    importances = pd.DataFrame({
        'Feature': X.columns,
        'Importance': clf.feature_importances_
    }).sort_values(by='Importance', ascending=False).head(10)
    
    print("\nTop Macro Reset Drivers:")
    print(importances)

if __name__ == "__main__":
    run_sp500_miner_v70()
