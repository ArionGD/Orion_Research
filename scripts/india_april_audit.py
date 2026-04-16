import pandas as pd
from datetime import datetime, timedelta
import sys
import os
import swisseph as swe

# Root Path
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"
sys.path.append(ROOT)

from src.engine.medini.crash_logic import MundaneWeatherEngine
from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.astro.dasha.vimshottari import VimshottariDasha

def run_india_audit():
    print("=== ACE: INDIA HAVOC STATUS (APRIL 2026) ===")
    
    weather = MundaneWeatherEngine()
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    dasha_eng = VimshottariDasha()
    
    # India Natal (1947 Moon: 117.0)
    INDIA_MOON = 117.0
    INDIA_BIRTH = datetime(1947, 8, 15)
    
    start = datetime(2026, 4, 1)
    results = []
    
    for i in range(30):
        d = start + timedelta(days=i)
        pos = ep.get_all_positions(d)
        dashas = dasha_eng.get_current_dasha(INDIA_MOON, INDIA_BIRTH, d)
        smi = weather.calculate_smi(d, pos, dashas['Mahadasha'], dashas['Antardasha'], market='INDIA')
        
        results.append({'Date': d, 'SMI': smi, 'Mahadasha': dashas['Mahadasha'], 'Antardasha': dashas['Antardasha']})
        
    df = pd.DataFrame(results)
    
    # Highlight the "Strike"
    print(f"\n{'DATE':<12} | {'SMI':<8} | {'DASHA':<15} | {'VERDICT'}")
    print("-" * 60)
    
    for idx, row in df.iterrows():
        status = "FRACTURE" if row['SMI'] >= 8.5 else "STRESS" if row['SMI'] >= 7.0 else "STEALTH"
        print(f"{row['Date'].strftime('%Y-%m-%d'):<12} | {row['SMI']:<8.2f} | {row['Mahadasha']}-{row['Antardasha']:<10} | {status}")

if __name__ == "__main__":
    run_india_audit()
