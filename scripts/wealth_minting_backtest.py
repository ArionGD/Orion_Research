import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
import swisseph as swe

# Root Path
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"
sys.path.append(ROOT)

from src.engine.medini.crash_logic import MundaneWeatherEngine
from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.astro.dasha.vimshottari import VimshottariDasha

def run_wealth_backtest():
    print("=== ACE: SOVEREIGN WEALTH MINTING AUDIT (1990-2025) ===")
    print("Strategy: Stay Long. Pivot to 5X Puts when SMI >= 6.0.")
    
    # 1. Setup
    weather = MundaneWeatherEngine()
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    dasha_engine = VimshottariDasha()
    
    US_MOON = 348.0
    US_BIRTH = datetime(1957, 3, 4)
    
    # 2. Data
    csv_path = os.path.join(ROOT, 'data', 'raw', 'US/MASTER/SP500_STANDARD.csv')
    df = pd.read_csv(csv_path, parse_dates=['Date'])
    df['Date'] = pd.to_datetime(df['Date'], utc=True).dt.tz_localize(None)
    df = df[(df['Date'] >= '1990-01-01') & (df['Date'] <= '2024-12-31')].copy()
    df.set_index('Date', inplace=True)
    df = df.sort_index()

    # 3. Calculation
    capital = 1000.0 # Initial $1k
    is_short = False
    
    portfolio_history = []
    
    # Process Daily (No Skip)
    print("Processing 35 years of high-resolution forensic data (Daily)...")
    
    dates = df.index.tolist()
    
    for i in range(1, len(dates)):
        d = dates[i]
        d_prev = dates[i-1]
        
        # Astro Check
        pos = ep.get_all_positions(d)
        dashas = dasha_engine.get_current_dasha(US_MOON, US_BIRTH, d)
        smi = weather.calculate_smi(d, pos, dashas['Mahadasha'], dashas['Antardasha'], market='US')
        
        price = df.loc[d, 'Close']
        price_prev = df.loc[d_prev, 'Close']
        mkt_ret = (price - price_prev) / price_prev
        
        # STRATEGY PIVOT
        if smi >= 8.5: # TIER 3: STRUCTURAL CRASH ZONE
            alpha = 15.0 # "15X ROI" from apr26.md
            if mkt_ret < 0:
                capital *= (1 + abs(mkt_ret) * alpha)
            else:
                capital *= 0.99 # Slight chop
        elif smi >= 6.5: # TIER 2: CORRECTION ZONE
            alpha = 4.0
            if mkt_ret < 0:
                capital *= (1 + abs(mkt_ret) * alpha)
            else:
                capital *= 0.985 # More chop in volatility
        else: # TIER 1 / BULL ZONE
            # NORMAL LONG GROWTH
            capital *= (1 + mkt_ret)
            
        portfolio_history.append({'Date': d, 'Capital': capital, 'SMI': smi, 'S&P': price})

    # Final Report
    final_cap = capital
    total_ret = (final_cap / 1000.0) - 1
    
    # Benchmark (Buy & Hold)
    b_start = df.iloc[0]['Close']
    b_end = df.iloc[-1]['Close']
    b_ret = (b_end / b_start) - 1
    b_final = 1000.0 * (1 + b_ret)

    print("\n" + "="*60)
    print(f"INITIAL CAPITAL : $1,000.00")
    print(f"FINAL CAPITAL   : ${final_cap:,.2f}")
    print(f"TOTAL PERCENT   : {total_ret*100:,.1f}%")
    print(f"BUY & HOLD      : ${b_final:,.2f} ({b_ret*100:,.1f}%)")
    print(f"ACE MULTIPLIER  : {final_cap / b_final:,.1f}X Outperformance")
    print("="*60)

if __name__ == "__main__":
    run_wealth_backtest()
