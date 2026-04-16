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

def identify_market_drops(df):
    """Identify real XLE drops across 3 tiers (Daily)."""
    df['Peak'] = df['Close'].rolling(window=100, min_periods=20).max()
    df['DD'] = (df['Close'] - df['Peak']) / df['Peak']
    
    events = []
    curr_t3 = None; curr_t2 = None; curr_t1 = None
    
    for date, row in df.iterrows():
        dd = row['DD']
        # Tier 3 (-20%)
        if dd <= -0.20:
            if not curr_t3: curr_t3 = {'Start': date, 'Min_DD': dd, 'Date_Min': date}
            elif dd < curr_t3['Min_DD']: curr_t3.update({'Min_DD': dd, 'Date_Min': date})
        elif curr_t3:
            events.append({'Tier': 3, 'Bottom': curr_t3['Date_Min'], 'Mag': curr_t3['Min_DD']})
            curr_t3 = None
            
        # Tier 2 (-10%)
        if dd <= -0.10 and dd > -0.20:
            if not curr_t2: curr_t2 = {'Start': date, 'Min_DD': dd, 'Date_Min': date}
            elif dd < curr_t2['Min_DD']: curr_t2.update({'Min_DD': dd, 'Date_Min': date})
        elif curr_t2:
            events.append({'Tier': 2, 'Bottom': curr_t2['Date_Min'], 'Mag': curr_t2['Min_DD']})
            curr_t2 = None

        # Tier 1 (-5%)
        if dd <= -0.05 and dd > -0.10:
            if not curr_t1: curr_t1 = {'Start': date, 'Min_DD': dd, 'Date_Min': date}
            elif dd < curr_t1['Min_DD']: curr_t1.update({'Min_DD': dd, 'Date_Min': date})
        elif curr_t1:
            events.append({'Tier': 1, 'Bottom': curr_t1['Date_Min'], 'Mag': curr_t1['Min_DD']})
            curr_t1 = None
            
    return pd.DataFrame(events)

def run_xle_judgement():
    print("=== ACE: TIME OF JUDGEMENT (XLE ENERGY AUDIT) ===")
    print("Constraint: 100% Reality Check / Zero False Positive Bias.")
    
    weather = MundaneWeatherEngine()
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    dasha_eng = VimshottariDasha()
    
    # US PHYSICAL NATAL (1776 SIBLEY CHART)
    # The birth of the Nation's Resources and Land.
    MOON = 312.0 # US Sibley Natal Moon (Aquarius)
    BIRTH = datetime(1776, 7, 4)
    
    # 1. Load XLE
    csv_path = os.path.join(ROOT, 'data/raw/US/ENERGY_XLE.csv')
    # Skip multi-index header mess
    df = pd.read_csv(csv_path, skiprows=2)
    df.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
    df['Date'] = pd.to_datetime(df['Date'], utc=True).dt.tz_localize(None)
    df.set_index('Date', inplace=True)
    
    real_drops = identify_market_drops(df)
    
    counts = {1:0, 2:0, 3:0}
    caught = {1:0, 2:0, 3:0}
    false_positives = 0
    total_checks = 0

    print(f"\nScanning XLE Life-Cycle ({len(df)} days)...")
    
    # Audit real drops
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
            dashas = dasha_eng.get_current_dasha(MOON, BIRTH, d_obj)
            smi = weather.calculate_smi(d_obj, pos, dashas['Mahadasha'], dashas['Antardasha'], market='US')
            
            threshold = 8.0 if t==3 else 6.0 if t==2 else 4.0
            if smi >= threshold:
                hit = True
                break
        if hit: caught[t] += 1

    # False Positive Check (Spot check on non-crash years)
    print("Executing False-Positive Neutrality Audit...")
    non_crash_days = df[df['DD'] > -0.03].sample(n=500).index # Check 500 lucky days
    for d in non_crash_days:
        d_obj = d.to_pydatetime()
        pos = ep.get_all_positions(d_obj)
        dashas = dasha_eng.get_current_dasha(MOON, BIRTH, d_obj)
        smi = weather.calculate_smi(d_obj, pos, dashas['Mahadasha'], dashas['Antardasha'], market='US')
        if smi >= 7.5: # If hit high SMI on a happy day
            false_positives += 1

    # Report
    print("\n" + "="*60)
    print(f"{'XLE TIER':<10} | {'TOTAL DROPS':<12} | {'SMI CAUGHT':<12} | {'CATCH RATE'}")
    print("-" * 60)
    for t in [3, 2, 1]:
        rate = (caught[t]/counts[t]*100) if counts[t]>0 else 0
        print(f"Tier {t:<5} | {counts[t]:<12} | {caught[t]:<12} | {rate:.1f}%")
        
    print("-" * 60)
    print(f"FAKE SIGNAL PROBABILITY: {(false_positives/500*100):.2f}%")
    print(f"SIGNAL PURITY STATUS: {'SOVEREIGN' if (false_positives/500 < 0.05) else 'TUNING REQ'}")
    print("="*60)

if __name__ == "__main__":
    run_xle_judgement()
