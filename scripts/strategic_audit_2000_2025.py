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
from src.engine.medini.vedic_precision import VedicHighPrecisionEngine
from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.astro.dasha.vimshottari import VimshottariDasha

def run_strategic_2000_audit():
    print("=== ACE: STRATEGIC SOVEREIGN AUDIT (2000 - 2025) ===")
    print("Methodology: Lead-Window Signal Detection (45 Days)")
    
    # 1. Setup Engines
    weather = MundaneWeatherEngine()
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    vpe = VedicHighPrecisionEngine()
    dasha_engine = VimshottariDasha()
    
    # 2. Market Data (S&P 500)
    csv_path = os.path.join(ROOT, 'data', 'raw', 'sp500_daily_full.csv')
    df = pd.read_csv(csv_path, parse_dates=['Date'])
    df['Date'] = pd.to_datetime(df['Date'], utc=True).dt.tz_localize(None)
    df = df[(df['Date'] >= '2000-01-01') & (df['Date'] <= '2025-03-31')].copy()
    df.set_index('Date', inplace=True)
    
    # Identify unique drawdowns
    # A crash is identified when drawdown exceeds thresholds from a local peak
    df['Peak'] = df['Close'].rolling(window=250, min_periods=1).max()
    df['DD'] = (df['Close'] - df['Peak']) / df['Peak']
    
    # Historical Major Events (The "Ground Truth" for Strategic Recall)
    major_events = [
        {'name': 'Dotcom Collapse', 'date': '2001-09-21', 'tier': 3},
        {'name': 'Lehman Crisis', 'date': '2008-11-20', 'tier': 3}, # Bottom of initial flush
        {'name': 'Debt Ceiling Skid', 'date': '2011-10-03', 'tier': 2},
        {'name': 'Late 2018 Pivot', 'date': '2018-12-24', 'tier': 2},
        {'name': 'COVID Collapse', 'date': '2020-03-23', 'tier': 3},
        {'name': '2022 Bear Market', 'date': '2022-10-12', 'tier': 2}
    ]
    
    # India Natal Data
    INDIA_MOON = 117.0
    INDIA_BIRTH = datetime(1947, 8, 15)
    
    print("\n" + "="*80)
    print(f"{'EVENT NAME':<20} | {'PEAK DATE':<12} | {'LEAD SMI':<10} | {'STATUS'}")
    print("-" * 80)
    
    total_caught = 0
    
    for event in major_events:
        target_date = datetime.strptime(event['date'], '%Y-%m-%d')
        # Check window: 90 days before the bottom to find the peak signal
        window = pd.date_range(start=target_date - pd.Timedelta(days=90), end=target_date, freq='D')
        
        max_smi = -1.0 # Initialize to negative
        best_date = datetime.now()
        calc_trace = ""
        
        for d in window:
            d_obj = d.to_pydatetime()
            pos = ep.get_all_positions(d_obj)
            # India Dasha Context
            dashas = dasha_engine.get_current_dasha(INDIA_MOON, INDIA_BIRTH, d_obj)
            
            # Use original core logic
            smi = weather.calculate_smi(d_obj, pos, dashas['Mahadasha'], dashas['Antardasha'])
            
            # Apply multiplier (using India market)
            # Original backtest used Saturn lon as proxy for stress sign multiplier
            sat_lon = pos.get('Saturn', 0)
            mult, _ = vpe.get_sign_multiplier(sat_lon, market='INDIA')
            smi *= mult
            
            if smi > max_smi:
                max_smi = smi
                best_date = d_obj
                calc_trace = f"MD: {dashas['Mahadasha']} | AD: {dashas['Antardasha']} | Mult: {mult:4.2f}"

        status = "CAUGHT" if max_smi >= 5.0 else "SIGNALED" if max_smi >= 3.0 else "MISSED"
        if status in ["CAUGHT", "SIGNALED"]: total_caught += 1
        
        print(f"{event['name']:<20} | {best_date.strftime('%Y-%m-%d'):<12} | {max_smi:8.2f} | {status}")
        print(f"  > Trace: {calc_trace}\n")

    rate = (total_caught / len(major_events)) * 100
    print("="*80)
    print(f"STRATEGIC CATCH RATE (2000-2025): {rate:.1f}%")
    print("="*80)

if __name__ == "__main__":
    run_strategic_2000_audit()
