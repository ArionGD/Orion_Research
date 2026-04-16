import pandas as pd
import numpy as np
import os
import sys

# Root Path
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"

def run_blind_miner():
    print("=== ACE: THE BLIND ROOM (ENERGY PATTERN MINER) ===")
    
    path = os.path.join(ROOT, 'data/enriched/US/ENERGY_XLE_ENRICHED.csv')
    df = pd.read_csv(path)
    
    # Calculate Drawdown
    df['Peak'] = df['Close'].rolling(window=100, min_periods=20).max()
    df['DD'] = (df['Close'] - df['Peak']) / df['Peak']
    
    # Identify Big Drop Days (<-10% )
    crash_days = df[df['DD'] <= -0.10].copy()
    happy_days = df[df['DD'] >= -0.02].copy()
    
    print(f"Total Crash Days Found: {len(crash_days)}")
    print(f"Total Healthy Days Found: {len(happy_days)}")
    print("-" * 60)
    
    planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
    
    sig_report = []
    
    for p in planets:
        # Check Sign Concentration (Each 30deg)
        crash_days[f'{p}_Sign'] = (crash_days[f'{p}_Deg'] // 30).astype(int)
        happy_days[f'{p}_Sign'] = (happy_days[f'{p}_Deg'] // 30).astype(int)
        
        crash_dist = crash_days[f'{p}_Sign'].value_counts(normalize=True).sort_index()
        happy_dist = happy_days[f'{p}_Sign'].value_counts(normalize=True).sort_index()
        
        # Find where concentration in crashes is > 2X concentration in healthy days
        for sign in range(12):
            c_val = crash_dist.get(sign, 0)
            h_val = happy_dist.get(sign, 0)
            if c_val > (h_val * 2) and c_val > 0.15: # Significant bias
                sig_report.append({
                    'Planet': p,
                    'Sign': sign + 1,
                    'Crash_Freq': f"{c_val*100:.1f}%",
                    'Healthy_Freq': f"{h_val*100:.1f}%",
                    'Intensity': f"{c_val/h_val:.2f}X" if h_val >0 else 'INF'
                })
                
    results = pd.DataFrame(sig_report)
    if not results.empty:
        print(f"{'PLANET':<10} | {'SIGN (RASHI)':<12} | {'CRASH FREQ':<10} | {'BIAS'}")
        print("-" * 60)
        for _, row in results.iterrows():
            print(f"{row['Planet']:<10} | {row['Sign']:<12} | {row['Crash_Freq']:<10} | {row['Intensity']}")
    else:
        print("No extreme single-planet bias found. Pattern is likely multi-planetary (Cluster).")

if __name__ == "__main__":
    run_blind_miner()
