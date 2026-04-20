import pandas as pd
import numpy as np
import os
import sys
from interpret.glassbox import ExplainableBoostingClassifier

# Root Path
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"

def run_sp500_ebm_miner():
    print("=== ACE: SP500 GLASS-BOX MINER (CENTURY INTERACTIONS) ===")
    
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
    # Use dummy columns for Dasha
    X = pd.get_dummies(df.drop(columns=exclude), columns=['Mahadasha', 'Antardasha']).fillna(0)
    y = df['Is_Crash']
    
    # 3. Fit Glass-Box Oracle (Optimized for 100-year scale)
    print("\nFitting Macro Glass-Box (EBM) to 100 years of DNA...")
    ebm = ExplainableBoostingClassifier(interactions=5, max_bins=128, random_state=42)
    ebm.fit(X, y)
    
    # 4. Extract Global Importance
    print("\n" + "="*70)
    print("SP500 EBM GLOBAL IMPORTANCE: THE MACRO INTERACTION KEY")
    print("="*70)
    
    exp = ebm.explain_global()
    data = exp.data()
    
    features = pd.DataFrame({
        'Feature': data['names'],
        'Importance': data['scores']
    }).sort_values(by='Importance', ascending=False).head(15)
    
    for idx, row in features.iterrows():
        print(f"FEATURE: {row['Feature']:<20} | Glass-Box Importance: {row['Importance']:.4f}")
    print("="*70)
    
    print(f"\nMacro Logic Seal Accuracy: {ebm.score(X, y):.4f}")

if __name__ == "__main__":
    run_sp500_ebm_miner()
