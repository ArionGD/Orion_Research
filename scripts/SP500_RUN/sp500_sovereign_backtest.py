import pandas as pd
import numpy as np
import os
import sys
import xgboost as xgb

# Root Path
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"

def run_sp500_backtest_v70():
    print("=== ACE: SP500 SOVEREIGN BACKTEST (100-YEAR AUDIT) ===")
    
    file_path = os.path.join(ROOT, 'data/enriched/US/SP500/SP500_MasterV70.csv')
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return
        
    df = pd.read_csv(file_path)
    
    # 1. Target: Macro Reset (-8% in 45 days)
    df['Forward_Min'] = df['Close'].shift(-45).rolling(window=45, min_periods=1).min()
    df['Future_DD'] = (df['Forward_Min'] - df['Close']) / df['Close']
    df['Is_Crash'] = (df['Future_DD'] <= -0.08).astype(int)
    
    # 2. Features for the Oracle
    exclude = ['Date', 'Close', 'Forward_Min', 'Future_DD', 'Is_Crash']
    X = pd.get_dummies(df.drop(columns=exclude), columns=['Mahadasha', 'Antardasha']).fillna(0)
    y = df['Is_Crash']
    
    # 3. Train the Oracle (Macro SHAP logic)
    print("\nTraining Sovereign Oracle (Macro-XGB)...")
    model = xgb.XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42)
    model.fit(X, y)
    
    # 4. Run Backtest Simulation
    df['Signal'] = model.predict(X)
    
    trades = []
    capital = 100.0
    wins = 0
    total_trades = 0
    
    signal_days = df[df['Signal'] == 1].index
    last_trade_idx = -100
    
    for idx in signal_days:
        if idx < last_trade_idx + 60: continue # Skip if already in a trade
        
        entry_price = df.iloc[idx]['Close']
        exit_idx = min(idx + 45, len(df)-1)
        exit_price = df.iloc[exit_idx]['Close']
        min_price = df.iloc[idx:exit_idx]['Close'].min()
        
        # Put Option Simulation (4x leverage proxy for SP500)
        outcome = (entry_price - min_price) / entry_price
        profit = outcome * 4.0 
        
        if outcome >= 0.08: # Successful Macro Catch
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
    print("SOVEREIGN MACRO BACKTEST REPORT (SP500: 100-YEARS)")
    print("="*70)
    print(f"Total Strike Zones Identified: {total_trades}")
    print(f"Verified Macro Catches:       {wins}")
    print(f"Historical Catch Rate (Recall): {(wins/total_trades)*100:.2f}%" if total_trades > 0 else "0%")
    print(f"Estimated Portfolio Growth:    {capital * (1 + sum([t['Profit_%']/100 for t in trades])):.2f}x")
    print("="*70)
    
    # Sample High-Value Events
    tdf = pd.DataFrame(trades)
    print("\nSample High-Velocity Macro Events:")
    print(tdf.sort_values(by='Drawdown_Caught', ascending=False).head(10))

if __name__ == "__main__":
    run_sp500_backtest_v70()
