import pandas as pd
import numpy as np
import os
import sys
from interpret.glassbox import ExplainableBoostingClassifier

# Root Path
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"

def run_ebm_miner_v70():
    print("=== ACE: SOVEREIGN EBM MINER (THE GLASS-BOX) ===")
    
    file_path = os.path.join(ROOT, 'data/enriched/US/ENERGY_MasterV70.csv')
    if not os.path.exists(file_path):
        print("Error: Dataset not found.")
        return
        
    df = pd.read_csv(file_path)
    
    # 1. Target: The Crash (-12% in 45 days)
    df['Forward_Min'] = df['Close'].shift(-45).rolling(window=45, min_periods=1).min()
    df['Future_DD'] = (df['Forward_Min'] - df['Close']) / df['Close']
    df['Is_Crash'] = (df['Future_DD'] <= -0.12).astype(int)
    
    # 2. Variable Selection
    exclude = ['Date', 'Close', 'Forward_Min', 'Future_DD', 'Is_Crash']
    X = df.drop(columns=exclude).fillna(0)
    y = df['Is_Crash']
    
    # 3. Fit EBM Classifer (The Ultimate Glass-Box)
    print("\nFitting Glass-Box model (Microsoft InterpretML)...")
    ebm = ExplainableBoostingClassifier(interactions=10, random_state=42)
    ebm.fit(X, y)
    
    # 4. Extract Global Importances
    print("\n" + "="*70)
    print("EBM GLOBAL IMPORTANCE: THE SHAPE OF DESTRUCTION")
    print("="*70)
    
    exp = ebm.explain_global()
    data = exp.data()
    
    # Sort and Display Top 15 Interpretive Features
    features = pd.DataFrame({
        'Feature': data['names'],
        'Importance': data['scores']
    }).sort_values(by='Importance', ascending=False).head(15)
    
    for idx, row in features.iterrows():
        print(f"FEATURE: {row['Feature']:<20} | Glass-Box Importance: {row['Importance']:.4f}")
    print("="*70)
    
    # Accuracy Report
    print(f"\nModel Internal Accuracy (The Logic Seal): {ebm.score(X, y):.4f}")

if __name__ == "__main__":
    run_ebm_miner_v70()
