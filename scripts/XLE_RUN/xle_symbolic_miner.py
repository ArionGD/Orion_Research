import pandas as pd
import numpy as np
import os
import sys
from gplearn.genetic import SymbolicClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Root Path
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"

def run_symbolic_miner_v70_apex():
    print("=== ACE: SOVEREIGN SYMBOLIC MINER (APEX v2) ===")
    
    file_path = os.path.join(ROOT, 'data/enriched/US/ENERGY_MasterV70.csv')
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return
        
    df = pd.read_csv(file_path)
    
    # 1. Target: Binary Crash (Tier 2/3)
    df['Forward_Min'] = df['Close'].shift(-45).rolling(window=45, min_periods=1).min()
    df['Future_DD'] = (df['Forward_Min'] - df['Close']) / df['Close']
    df['Is_Crash'] = (df['Future_DD'] <= -0.12).astype(int)
    
    # 2. Optimized Feature Selection
    # Dropping timestamps and price. Keeping only Astro + Dasha Categoricals
    exclude = ['Date', 'Close', 'Forward_Min', 'Future_DD', 'Is_Crash']
    df_encoded = pd.get_dummies(df, columns=['Mahadasha', 'Antardasha'])
    X = df_encoded.drop(columns=exclude).fillna(0)
    y = df_encoded['Is_Crash']
    
    # Scaling Astro Degrees to 0-1 for faster Convergence
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 3. Fit Symbolic Classifier (The "Search for the Absolute")
    est = SymbolicClassifier(population_size=2000,
                              generations=50,
                              stopping_criteria=0.01,
                              p_crossover=0.7, p_subtree_mutation=0.1,
                              p_hoist_mutation=0.05, p_point_mutation=0.1,
                              max_samples=0.9, verbose=1,
                              function_set=('add', 'sub', 'mul', 'div', 'sin', 'cos', 'log', 'abs'),
                              parsimony_coefficient=0.001,
                              random_state=42)
    
    print("\nBreeding Galactic Equations (Generations: 50 | Pop: 2000)...")
    est.fit(X_scaled, y)
    
    # 4. Extract the Sovereign Formula
    print("\n" + "="*70)
    print("THE LOGIC EQUATION OF THE ENERGY CRASH")
    print("="*70)
    print(est._program)
    print("="*70)
    
    # Export Formula as Code
    print("\nFormula Precision: ", est.score(X_scaled, y))

if __name__ == "__main__":
    run_symbolic_miner_v70_apex()
