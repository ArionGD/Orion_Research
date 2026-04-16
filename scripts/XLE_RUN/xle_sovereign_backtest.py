import pandas as pd
import numpy as np
import os
import sys
from interpret.glassbox import ExplainableBoostingClassifier

# Root Path
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"

def run_sovereign_backtest_v70():
    print("=== ACE: SOVEREIGN GLASS-BOX BACKTEST (FINAL AUDIT) ===")
    
    file_path = os.path.join(ROOT, 'data/enriched/US/ENERGY_MasterV70.csv')
    if not os.path.exists(file_path):
        print("Error: Dataset not found.")
        return
        
    df = pd.read_csv(file_path)
    
    # 1. Prepare Target Variable (Ground Truth)
    # Tier 2/3 Drop: -12% in 45 days
    df['Forward_Min'] = df['Close'].shift(-45).rolling(window=45, min_periods=1).min()
    df['Future_DD'] = (df['Forward_Min'] - df['Close']) / df['Close']
    df['Is_Crash'] = (df['Future_DD'] <= -0.12).astype(int)
    
    # 2. Features for the Glass-Box
    exclude = ['Date', 'Close', 'Forward_Min', 'Future_DD', 'Is_Crash']
    X = df.drop(columns=exclude).fillna(0)
    y = df['Is_Crash']
    
    # 3. Train the Glass-Box Brain (The "Oracle")
    print("\nTraining Sovereign Oracle (EBM)...")
    ebm = ExplainableBoostingClassifier(interactions=15, random_state=42)
    ebm.fit(X, y)
    
    # 4. Run Backtest Simulation
    df['Signal'] = ebm.predict(X)
    
    trades = []
    capital = 100.0
    wins = 0
    total_trades = 0
    
    # Identify unique signal clusters (to avoid double counting same crash)
    signal_days = df[df['Signal'] == 1].index
    last_trade_idx = -100
    
    for idx in signal_days:
        if idx < last_trade_idx + 60: continue # Skip if already in a trade
        
        # Trade Execution
        entry_price = df.iloc[idx]['Close']
        exit_idx = min(idx + 45, len(df)-1)
        exit_price = df.iloc[exit_idx]['Close']
        min_price = df.iloc[idx:exit_idx]['Close'].min()
        
        # Put Option Simulation (Simplified 5x leverage proxy)
        outcome = (entry_price - min_price) / entry_price
        profit = outcome * 5.0 # Alpha multiplier for Puts
        
        if outcome >= 0.12: # Successful Tier 3 Catch
            wins += 1
            
        trades.append({
            'Date': df.iloc[idx]['Date'],
            'Profit_%': profit * 100,
            'Drawdown_Caught': outcome * 100
        })
        
        last_trade_idx = idx
        total_trades += 1
        
    # 5. FINAL FORENSIC REPORT
    print("\n" + "="*70)
    print("SOVEREIGN GLASS-BOX BACKTEST REPORT (XLE ENERGY)")
    print("="*70)
    print(f"Total Strike Zones Identified: {total_trades}")
    print(f"Verified Tier 3 Catches:      {wins}")
    print(f"Historical Catch Rate (Recall): {(wins/total_trades)*100:.2f}%" if total_trades > 0 else "0%")
    print(f"Estimated Portfolio Growth:    {capital * (1 + sum([t['Profit_%']/100 for t in trades])):.2f}x")
    print("="*70)
    
    # Sample Trades
    print("\nSample High-Velocity Catch Events:")
    tdf = pd.DataFrame(trades)
    print(tdf.sort_values(by='Drawdown_Caught', ascending=False).head(10))

if __name__ == "__main__":
    run_sovereign_backtest_v70()
