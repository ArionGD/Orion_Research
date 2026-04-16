import pandas as pd
import numpy as np
import os
import sys
from mlxtend.frequent_patterns import apriori, association_rules

# Root Path
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"

def run_arm_miner_v70():
    print("=== ACE: SOVEREIGN ARM MINER (DNA SEQUENCER) ===")
    
    file_path = os.path.join(ROOT, 'data/enriched/US/ENERGY_MasterV70.csv')
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return
        
    df = pd.read_csv(file_path)
    
    # 1. Discretization (Convert Continuous to Categories)
    # We create a "Basket" of boolean flags for each day
    basket = pd.DataFrame()
    
    # Signs (1-12)
    planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Saturn', 'True_Node']
    for p in planets:
        deg_col = f"{p}_Deg"
        if deg_col in df.columns:
            sign = (df[deg_col] // 30).astype(int) + 1
            # Add specific critical signs as flags
            basket[f"{p}_Sign_{10}"] = (sign == 10).astype(bool) # Capricorn focus
            basket[f"{p}_Sign_{1}"] = (sign == 1).astype(bool)  # Aries focus
            basket[f"{p}_Sign_{12}"] = (sign == 12).astype(bool) # Pisces focus
            
    # Speed Flags (Is Retrograde?)
    for p in planets:
        speed_col = f"{p}_Speed"
        if speed_col in df.columns:
            basket[f"{p}_Retro"] = (df[speed_col] < 0).astype(bool)
            
    # Aspect Flags
    basket['Mars_Saturn_Conflict'] = (df['Aspect_Mars_Saturn'] > 0).astype(bool)
    basket['Rahu_Mars_Panic'] = (df['Aspect_Rahu_Mars'] > 0).astype(bool)
    
    # Target: The Crash (Logic: -12% drop in next 45 days)
    df['Forward_Min'] = df['Close'].shift(-45).rolling(window=45, min_periods=1).min()
    df['Future_DD'] = (df['Forward_Min'] - df['Close']) / df['Close']
    basket['Is_Crash'] = (df['Future_DD'] <= -0.12).astype(bool)
    
    # 2. Run Apriori (Find Frequent Itemsets)
    print("\nExtracting Sovereign Combinations...")
    frequent_itemsets = apriori(basket, min_support=0.01, use_colnames=True)
    
    # 3. Generate Association Rules
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.5)
    
    # 4. Filter for rules that lead to CRASH
    crash_rules = rules[rules['consequents'].apply(lambda x: 'Is_Crash' in x)].sort_values(by='lift', ascending=False)
    
    print("\n" + "="*70)
    print("THE CRASH CODE (ASSOCIATION RULES)")
    print("="*70)
    if not crash_rules.empty:
        # Show Top 15 Rules
        for idx, row in crash_rules.head(15).iterrows():
            antecedents = list(row['antecedents'])
            print(f"RULE: IF {antecedents}")
            print(f"  Confidence: {row['confidence']:.2%} | Lift: {row['lift']:.2f}x")
            print("-" * 30)
    else:
        print("No high-confidence combinations found in this pass.")
    print("="*70)

if __name__ == "__main__":
    run_arm_miner_v70()
