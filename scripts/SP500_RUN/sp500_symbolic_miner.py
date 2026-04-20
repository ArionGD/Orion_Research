import pandas as pd
import numpy as np
import os
import sys
from gplearn.genetic import SymbolicClassifier

# Root Path
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"

def run_sp500_symbolic_miner():
    print("=== ACE: SP500 SYMBOLIC MINER (MACRO EQUATION) ===")
    
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
    
    # 3. Evolution: Solving for the Macro Equation
    print("Evolving the Macro Reset Formula (Genetic Programming)...")
    est = SymbolicClassifier(population_size=5000,
                             generations=20, stopping_criteria=0.01,
                             p_crossover=0.7, p_subtree_mutation=0.1,
                             p_hoist_mutation=0.05, p_point_mutation=0.1,
                             max_samples=0.9, verbose=1,
                             parsimony_coefficient=0.01, random_state=0)
    
    est.fit(X, y)
    
    print("\n" + "="*70)
    print("THE SP500 MACRO EQUATION (SRM)")
    print("="*70)
    print(f"Formula: {est._program}")
    print("="*70)

if __name__ == "__main__":
    run_sp500_symbolic_miner()
