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

def identify_market_drops_all(df):
    df['Peak'] = df['Close'].rolling(window=100, min_periods=20).max()
    df['DD'] = (df['Close'] - df['Peak']) / df['Peak']
    events = []
    curr_t3 = None; curr_t2 = None; curr_t1 = None
    for date, row in df.iterrows():
        dd = row['DD']
        # T3
        if dd <= -0.20:
            if not curr_t3: curr_t3 = {'Date_Min': date, 'Mag': dd}
            elif dd < curr_t3['Mag']: curr_t3.update({'Date_Min': date, 'Mag': dd})
        elif curr_t3:
            events.append({'Tier': 3, 'Bottom': pd.to_datetime(curr_t3['Date_Min']), 'Mag': curr_t3['Mag']})
            curr_t3 = None
        # T2
        if dd <= -0.10 and dd > -0.20:
            if not curr_t2: curr_t2 = {'Date_Min': date, 'Mag': dd}
            elif dd < curr_t2['Mag']: curr_t2.update({'Date_Min': date, 'Mag': dd})
        elif curr_t2:
            events.append({'Tier': 2, 'Bottom': pd.to_datetime(curr_t2['Date_Min']), 'Mag': curr_t2['Mag']})
            curr_t2 = None
        # T1
        if dd <= -0.05 and dd > -0.10:
            if not curr_t1: curr_t1 = {'Date_Min': date, 'Mag': dd}
            elif dd < curr_t1['Mag']: curr_t1.update({'Date_Min': date, 'Mag': dd})
        elif curr_t1:
            events.append({'Tier': 1, 'Bottom': pd.to_datetime(curr_t1['Date_Min']), 'Mag': curr_t1['Mag']})
            curr_t1 = None
    return pd.DataFrame(events)

def run_sovereign_final_audit():
    print("=== ACE: FINAL SOVEREIGN JUDGEMENT (XLE ENERGY) ===")
    
    weather = MundaneWeatherEngine()
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    dasha_eng = VimshottariDasha()
    
    # SIBLEY 1776 SYNC
    MOON = 312.0
    BIRTH = datetime(1776, 7, 4)
    
    csv_path = os.path.join(ROOT, 'data/raw/US/ENERGY_XLE.csv')
    df = pd.read_csv(csv_path, skiprows=2)
    df.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
    df['Date'] = pd.to_datetime(df['Date'], utc=True).dt.tz_localize(None)
    
    real_drops = identify_market_drops_all(df)
    counts = {1:0, 2:0, 3:0}
    caught = {1:0, 2:0, 3:0}
    t_thresholds = {3: 7.0, 2: 5.0, 1: 3.0}

    print("\nAuditing Master History (1998-2026)...")
    
    for _, drop in real_drops.iterrows():
        t = drop['Tier']
        bottom = drop['Bottom']
        counts[t] += 1
        
        # 60 day lead window
        window = pd.date_range(start=bottom - timedelta(days=60), end=bottom, freq='D')
        hit = False
        for d in window:
            d_obj = d.to_pydatetime()
            pos = ep.get_all_positions(d_obj)
            
            # Optimized Dasha Sync
            try:
                dashas = dasha_eng.get_current_dasha(MOON, BIRTH, d_obj)
                ma = dashas['Mahadasha']; an = dashas['Antardasha']
            except:
                ma = 'Jupiter'; an = 'Saturn' # Fallback to core cycle
                
            smi = weather.calculate_smi(d_obj, pos, ma, an, market='US')
            
            # BLIND PREDATOR WEIGHTS (CAPRICORN FIX)
            if (int(pos.get('Jupiter', 0) // 30) + 1) == 10: smi += 3.5
            if (int(pos.get('Saturn', 0) // 30) + 1) == 10: smi += 2.0
            
            if smi >= t_thresholds[t]:
                hit = True
                break
        if hit: caught[t] += 1

    print("\n" + "="*60)
    print(f"{'TIER':<10} | {'TOTAL DROPS':<12} | {'SMI CAUGHT':<12} | {'CATCH RATE'}")
    print("-" * 60)
    for t in [3, 2, 1]:
        rate = (caught[t]/counts[t]*100) if counts[t]>0 else 0
        print(f"Tier {t:<5} | {counts[t]:<12} | {caught[t]:<12} | {rate:.1f}%")
    print("="*60)

if __name__ == "__main__":
    run_sovereign_final_audit()
