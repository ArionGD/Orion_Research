import pandas as pd
import numpy as np
import os
import sys
from prefixspan import PrefixSpan

# Root Path
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"

def run_spm_miner_v70():
    print("=== ACE: SOVEREIGN SPM MINER (TIME-DELAY) ===")
    
    file_path = os.path.join(ROOT, 'data/enriched/US/ENERGY_MasterV70.csv')
    if not os.path.exists(file_path):
        print("Error: Dataset not found.")
        return
        
    df = pd.read_csv(file_path)
    
    # Target: Drops > 12%
    df['Forward_Min'] = df['Close'].shift(-45).rolling(window=45, min_periods=1).min()
    df['Future_DD'] = (df['Forward_Min'] - df['Close']) / df['Close']
    df['Is_Crash'] = (df['Future_DD'] <= -0.12).astype(int)
    
    # 1. Identify "Crash Clusters"
    # We take 30 days BEFORE each crash event
    crash_indices = df[df['Is_Crash'] == 1].index
    
    # 2. Convert raw days into Event Sequences
    # Event = Planet_Sign_Change, Planet_Retro, etc.
    sequences = []
    
    for ci in crash_indices:
        if ci < 60: continue
        window = df.iloc[ci-60 : ci] # 60 days of lead up
        
        day_events = []
        # Track sign changes
        for idx in range(1, len(window)):
            row = window.iloc[idx]
            prev = window.iloc[idx-1]
            
            # Simplified Events
            if int(row['Jupiter_Deg']//30) != int(prev['Jupiter_Deg']//30): day_events.append("JUP_SIGN_CHG")
            if row['Jupiter_Speed'] < 0 and prev['Jupiter_Speed'] >= 0: day_events.append("JUP_RETRO")
            if row['SMI_Base'] > 6.0 and prev['SMI_Base'] <= 6.0: day_events.append("SMI_PEAK")
            if int(row['Sun_Deg']//30) != int(prev['Sun_Deg']//30): day_events.append("SUN_SIGN_CHG") # Transition
            
        if day_events:
            sequences.append(day_events)
            
    # 3. Run PrefixSpan (Find Frequent Temporal Patterns)
    print(f"\nAnalyzing sequences from {len(sequences)} historical lead-up windows...")
    ps = PrefixSpan(sequences)
    
    # Look for top 10 most common sequences
    top_sequences = ps.topk(10)
    
    print("\n" + "="*70)
    print("THE CRASH DOMINO SEQUENCE (SPM)")
    print("="*70)
    for count, seq in top_sequences:
        print(f"COUNT {count:<4} | SEQUENCE: {' -> '.join(seq)}")
    print("="*70)

if __name__ == "__main__":
    run_spm_miner_v70()
