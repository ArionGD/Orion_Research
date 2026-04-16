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

def run_future_xle_foresight():
    print("=== ACE: FUTURE XLE FORESIGHT (2026-2030) ===")
    print("Mapping the Sovereign Energy Cycles for the next 3.5 Years.")
    
    weather = MundaneWeatherEngine()
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    dasha_eng = VimshottariDasha()
    
    # 1776 SIBLEY NATAL
    MOON = 312.0
    BIRTH = datetime(1776, 7, 4)
    
    start_date = datetime(2026, 4, 16)
    end_date = datetime(2030, 1, 1)
    
    events = []
    
    print(f"Scanning Space-Time from {start_date.date()} to {end_date.date()}...")
    
    current_date = start_date
    while current_date <= end_date:
        pos = ep.get_all_positions(current_date)
        
        try:
            dashas = dasha_eng.get_current_dasha(MOON, BIRTH, current_date)
            ma = dashas['Mahadasha']; an = dashas['Antardasha']
        except:
            ma = 'Jupiter'; an = 'Saturn'
            
        smi = weather.calculate_smi(current_date, pos, ma, an, market='US')
        
        # BLIND PREDATOR WEIGHTS (CAPRICORN FIX)
        if (int(pos.get('Jupiter', 0) // 30) + 1) == 10: smi += 3.5
        if (int(pos.get('Saturn', 0) // 30) + 1) == 10: smi += 2.0
        if (int(pos.get('True_Node', 0) // 30) + 1) == 3: smi += 2.0
        
        tier = 0
        if smi >= 7.0: tier = 3
        elif smi >= 5.0: tier = 2
        elif smi >= 3.0: tier = 1
        
        if tier > 0:
            events.append({'Date': current_date.date(), 'SMI': smi, 'Tier': tier})
            
        current_date += timedelta(days=1)
        
    future_df = pd.DataFrame(events)
    
    # Group into Strike-Windows
    if not future_df.empty:
        future_df['Date'] = pd.to_datetime(future_df['Date'])
        # Clusters
        clusters = []
        curr_cluster = None
        for _, row in future_df.iterrows():
            if not curr_cluster:
                curr_cluster = {'Start': row['Date'], 'End': row['Date'], 'Max_SMI': row['SMI'], 'Max_Tier': row['Tier']}
            elif (row['Date'] - curr_cluster['End']).days <= 10:
                curr_cluster['End'] = row['Date']
                curr_cluster['Max_SMI'] = max(curr_cluster['Max_SMI'], row['SMI'])
                curr_cluster['Max_Tier'] = max(curr_cluster['Max_Tier'], row['Tier'])
            else:
                clusters.append(curr_cluster)
                curr_cluster = {'Start': row['Date'], 'End': row['Date'], 'Max_SMI': row['SMI'], 'Max_Tier': row['Tier']}
        if curr_cluster: clusters.append(curr_cluster)
        
        results = pd.DataFrame(clusters)
        print("\n" + "="*70)
        print(f"{'STRIKE WINDOW':<25} | {'MAX SMI':<8} | {'MAX TIER'}")
        print("-" * 70)
        for _, row in results.iterrows():
            win = f"{row['Start'].date()} -> {row['End'].date()}"
            print(f"{win:<25} | {row['Max_SMI']:<8.1f} | Tier {row['Max_Tier']}")
        print("="*70)
    else:
        print("No significant future strikes detected in this window.")

if __name__ == "__main__":
    run_future_xle_foresight()
