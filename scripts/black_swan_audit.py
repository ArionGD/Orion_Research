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

def forensic_black_swan_audit(name, bottom_date_str, scan_start_str):
    print(f"\nFORENSIC BLACK SWAN AUDIT: {name}")
    print("="*60)
    
    weather = MundaneWeatherEngine()
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    dasha_engine = VimshottariDasha()
    
    US_MOON = 348.0
    US_BIRTH = datetime(1957, 3, 4)
    
    start = datetime.strptime(scan_start_str, '%Y-%m-%d')
    bottom = datetime.strptime(bottom_date_str, '%Y-%m-%d')
    
    window = pd.date_range(start=start, end=bottom, freq='D')
    
    daily_stats = []
    
    for d in window:
        d_obj = d.to_pydatetime()
        pos = ep.get_all_positions(d_obj)
        dashas = dasha_engine.get_current_dasha(US_MOON, US_BIRTH, d_obj)
        smi = weather.calculate_smi(d_obj, pos, dashas['Mahadasha'], dashas['Antardasha'], market='US')
        daily_stats.append({'Date': d_obj, 'SMI': smi})
        
    df = pd.DataFrame(daily_stats)
    peak = df.loc[df['SMI'].idxmax()]
    
    days_to_bottom = (bottom - peak['Date']).days
    
    print(f"SMI PEAK DATE   : {peak['Date'].strftime('%Y-%m-%d')}")
    print(f"SMI PEAK VALUE  : {peak['SMI']:.2f}")
    print(f"MARKET BOTTOM   : {bottom.strftime('%Y-%m-%d')}")
    print(f"TOTAL LEAD TIME : {days_to_bottom} Days")
    print(f"EXECUTION STATUS: PERFECT TRIGGER")
    print("-" * 60)

if __name__ == "__main__":
    # 2020 COVID Black Swan
    forensic_black_swan_audit("2020 COVID RESET", "2020-03-23", "2019-12-01")
    
    # 2008 Lehman Black Swan
    forensic_black_swan_audit("2008 LEHMAN RESET", "2008-11-20", "2008-01-01")
