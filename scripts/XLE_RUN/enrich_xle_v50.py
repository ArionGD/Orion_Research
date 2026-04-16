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

def run_enrichment_v50():
    print("=== ACE: 50% SOVEREIGN ENRICHMENT (LEVEL 2) ===")
    
    weather = MundaneWeatherEngine()
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    dasha_eng = VimshottariDasha()
    
    # 1776 SIBLEY NATAL (For Dasha Context)
    MOON = 312.0
    BIRTH = datetime(1776, 7, 4)
    
    csv_path = os.path.join(ROOT, 'data/raw/US/ENERGY_XLE.csv')
    df = pd.read_csv(csv_path, skiprows=2)
    df.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
    df['Date'] = pd.to_datetime(df['Date'], utc=True).dt.tz_localize(None)
    
    # Result list
    enriched_data = []
    
    print(f"Enriching {len(df)} days with Level 2 Dimensions...")
    
    for idx, row in df.iterrows():
        d_obj = row['Date'].to_pydatetime()
        
        # 1. Astro Positions & Speeds
        pos = ep.get_all_positions(d_obj)
        speeds = {f"{p}_Speed": ep.get_planet_data(d_obj, p)[1] for p in pos.keys()}
        
        # 2. Dasha State (Timeline)
        try:
            dasha = dasha_eng.get_current_dasha(MOON, BIRTH, d_obj)
            ma = dasha['Mahadasha']; an = dasha['Antardasha']
        except:
            ma = 'Unknown'; an = 'Unknown'
            
        # 3. SMI Pressure (Raw Tension)
        smi = weather.calculate_smi(d_obj, pos, ma, an, market='US')
        
        # 4. Tithi & Nakshatra (Sentiment)
        moon_deg = pos.get('Moon', 0)
        sun_deg = pos.get('Sun', 0)
        diff = (moon_deg - sun_deg) % 360
        tithi = int(diff // 12) + 1 # 1-30
        nakshatra = int(moon_deg // (360/27)) + 1 # 1-27
        
        # Assemble Row
        entry = {
            'Date': row['Date'],
            'Close': round(row['Close'], 2),
            'Mahadasha': ma,
            'Antardasha': an,
            'SMI_Base': round(smi, 2),
            'Tithi': tithi,
            'Nakshatra': nakshatra
        }
        
        # Add positions
        for p, deg in pos.items():
            entry[f"{p}_Deg"] = round(deg, 3)
            # Is Debilitated (Capricorn check for Jup)
            if p == 'Jupiter': entry['Jup_Debilitated'] = 1 if (int(deg // 30) + 1 == 10) else 0
            if p == 'Saturn': entry['Sat_Debilitated'] = 1 if (int(deg // 30) + 1 == 1) else 0 # Sat in Aries
            
        # Add speeds (rounded)
        for p, speed in speeds.items():
            entry[p] = round(speed, 4) # Speeds need 4 for slow planets
            
        enriched_data.append(entry)
        
        if idx % 1000 == 0: print(f"Processed {idx} days...")

    master_df = pd.DataFrame(enriched_data)
    save_path = os.path.join(ROOT, 'data/enriched/US/ENERGY_XLE_v50.csv')
    master_df.to_csv(save_path, index=False)
    print(f"\nFinalized: {save_path}")

if __name__ == "__main__":
    run_enrichment_v50()
