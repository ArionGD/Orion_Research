import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime, timedelta
import swisseph as swe

# Root Path
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"
sys.path.append(ROOT)

from src.engine.medini.crash_logic import MundaneWeatherEngine
from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.astro.dasha.vimshottari import VimshottariDasha

def identify_3_week_strike_zone():
    print("=== ACE: PRECISION STRIKE-ZONE ANALYSIS (APRIL 2026) ===")
    print("Target: The 'Golden 21 Days' of Maximum Volatility Velocity.")
    
    weather = MundaneWeatherEngine()
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    dasha_engine = VimshottariDasha()
    
    # Dual Market Testing
    markets = [
        {'name': 'USA (Nasdaq/S&P)', 'moon': 348.0, 'birth': datetime(1957, 3, 4), 'id': 'US'},
        {'name': 'INDIA (Bank Nifty)', 'moon': 117.0, 'birth': datetime(1947, 8, 15), 'id': 'INDIA'}
    ]
    
    # 60-Day High Res Scan
    start_date = datetime(2026, 4, 1)
    results = []
    
    for i in range(60):
        d = start_date + timedelta(days=i)
        pos = ep.get_all_positions(d)
        
        row = {'Date': d}
        for m in markets:
            dashas = dasha_engine.get_current_dasha(m['moon'], m['birth'], d)
            smi = weather.calculate_smi(d, pos, dashas['Mahadasha'], dashas['Antardasha'], market=m['id'])
            row[f"{m['id']}_SMI"] = smi
            
        results.append(row)
        
    df = pd.DataFrame(results)
    df['Composite_SMI'] = df['US_SMI'] + df['INDIA_SMI']
    
    # Find the 21-day rolling window with highest Composite SMI
    df['Rolling_21d'] = df['Composite_SMI'].rolling(window=21).sum()
    peak_idx = df['Rolling_21d'].idxmax()
    
    strike_end = df.loc[peak_idx, 'Date']
    strike_start = strike_end - timedelta(days=20)
    
    print("\n" + "="*80)
    print(f"THE PRECISION 21-DAY STRIKE WINDOW:")
    print(f"START DATE : {strike_start.strftime('%Y-%m-%d')}")
    print(f"APEX DATE  : {df.loc[df['Composite_SMI'].idxmax(), 'Date'].strftime('%Y-%m-%d')}")
    print(f"EXIT DATE  : {strike_end.strftime('%Y-%m-%d')}")
    print("="*80)
    
    print("\nWEEKLY STRESS PROGRESSION:")
    # Group by week for readability
    df['Week'] = df['Date'].dt.isocalendar().week
    weekly = df.groupby('Week').agg({
        'Date': 'first',
        'US_SMI': 'max',
        'INDIA_SMI': 'max'
    })
    
    print(f"{'WEEK START':<12} | {'US MAX SMI':<12} | {'INDIA MAX SMI':<12} | {'VERDICT'}")
    print("-" * 80)
    for idx, w in weekly.iterrows():
        status = "CRITICAL FRACTURE" if w['US_SMI'] >= 8.5 else "HIGH VOLATILITY" if w['US_SMI'] >= 6.5 else "MONITOR"
        print(f"{w['Date'].strftime('%Y-%m-%d'):<12} | {w['US_SMI']:12.2f} | {w['INDIA_SMI']:13.2f} | {status}")

if __name__ == "__main__":
    identify_3_week_strike_zone()
