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

def identify_century_crashes(df):
    """Identifies major Tier 3 events (>20% DD) across 100 years."""
    df['Peak'] = df['Close'].rolling(window=252*2, min_periods=100).max() # 2-year rolling peak
    df['Drawdown'] = (df['Close'] - df['Peak']) / df['Peak']
    
    events = []
    current_event = None
    
    for date, row in df.iterrows():
        dd = row['Drawdown']
        if dd <= -0.20: # STRICT TIER 3
            if current_event is None:
                current_event = {'Start': date, 'Max_DD': dd, 'Date_Max': date}
            else:
                if dd < current_event['Max_DD']:
                    current_event['Max_DD'] = dd
                    current_event['Date_Max'] = date
        else:
            if current_event:
                events.append({'Bottom': current_event['Date_Max'], 'Mag': abs(current_event['Max_DD'])})
                current_event = None
    return pd.DataFrame(events)

def run_century_audit():
    print("=== ACE: CENTURY TIER 3 FORENSIC AUDIT (1927 - 2025) ===")
    print("Objective: Verify the big structural crash recall across 10 decades.")
    
    weather = MundaneWeatherEngine()
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    dasha_engine = VimshottariDasha()
    
    US_MOON = 348.0
    US_BIRTH = datetime(1957, 3, 4)
    
    csv_path = os.path.join(ROOT, 'data', 'raw', 'US/MASTER/SP500_STANDARD.csv')
    df = pd.read_csv(csv_path, parse_dates=['Date'])
    df['Date'] = pd.to_datetime(df['Date'], utc=True).dt.tz_localize(None)
    df.set_index('Date', inplace=True)
    
    crashes = identify_century_crashes(df)
    
    total = len(crashes)
    caught = 0
    
    print(f"\nScanning {total} Major Historic Crashes (>20% Collapse)...")
    print("-" * 60)
    print(f"{'CRASH BOTTOM':<15} | {'MAGNITUDE':<10} | {'STATUS'}")
    
    for idx, crash in crashes.iterrows():
        bottom = crash['Bottom']
        # 90-day lead-up
        window = pd.date_range(start=bottom - pd.Timedelta(days=90), end=bottom, freq='D')
        was_caught = False
        
        for d in window:
            d_obj = d.to_pydatetime()
            pos = ep.get_all_positions(d_obj)
            dashas = dasha_engine.get_current_dasha(US_MOON, US_BIRTH, d_obj)
            smi = weather.calculate_smi(d_obj, pos, dashas['Mahadasha'], dashas['Antardasha'], market='US')
            
            if smi >= 6.0: # Strike Level
                was_caught = True
                break
        
        if was_caught: 
            caught += 1
            status = "CAUGHT"
        else: 
            status = "MISS"
            
        print(f"{bottom.strftime('%Y-%m-%d'):<15} | {crash['Mag']*100:8.1f}% | {status}")
        
    print("-" * 60)
    print(f"TOTAL TIER 3 EVENTS: {total}")
    print(f"TOTAL CAUGHT       : {caught}")
    print(f"CENTURY ACCURACY    : {(caught / total * 100):.1f}%")
    print("="*60)

if __name__ == "__main__":
    run_century_audit()
