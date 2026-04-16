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

def get_aspect(d1, d2, orb=10):
    diff = abs(d1 - d2) % 360
    if diff > 180: diff = 360 - diff
    if diff <= orb: return 1 # Conjunction
    if abs(diff - 180) <= orb: return 2 # Opposition
    if abs(diff - 90) <= orb: return 3 # Square
    return 0

def run_enrichment_v70():
    print("=== ACE: 70% SOVEREIGN ENRICHMENT (LEVEL 3) ===")
    
    weather = MundaneWeatherEngine()
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    dasha_eng = VimshottariDasha()
    
    # SIBLEY NATAL
    MOON = 312.0
    BIRTH = datetime(1776, 7, 4)
    
    csv_path = os.path.join(ROOT, 'data/raw/US/ENERGY_XLE.csv')
    df = pd.read_csv(csv_path, skiprows=2)
    df.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
    df['Date'] = pd.to_datetime(df['Date'], utc=True).dt.tz_localize(None)
    
    enriched_data = []
    
    print(f"Enriching 27 years with Level 3 Sovereign Dimensions...")
    
    for idx, row in df.iterrows():
        d_obj = row['Date'].to_pydatetime()
        pos = ep.get_all_positions(d_obj)
        
        # 1. Dasha & Panchang
        try:
            dasha = dasha_eng.get_current_dasha(MOON, BIRTH, d_obj)
            ma = dasha['Mahadasha']; an = dasha['Antardasha']
        except:
            ma = 'Unknown'; an = 'Unknown'
            
        sun = pos.get('Sun', 0); moon = pos.get('Moon', 0)
        tithi = int(((moon - sun) % 360) // 12) + 1
        nakshatra = int(moon // (360/27)) + 1
        nithya_yoga = int(((sun + moon) % 360) // (360/27)) + 1
        
        # 2. Key Malefic Aspects (Tension)
        m_s_aspect = get_aspect(pos.get('Mars', 0), pos.get('Saturn', 0))
        j_s_aspect = get_aspect(pos.get('Jupiter', 0), pos.get('Sun', 0))
        r_m_aspect = get_aspect(pos.get('True_Node', 0), pos.get('Mars', 0))
        
        # 3. SBC Simple Vedha Proxy (Malefics hitting sensitive degrees)
        # We count conjunctions of any malefic with key sign boundaries (0, 90, 180, 270)
        vedha_score = 0
        for p in ['Mars', 'Saturn', 'True_Node']:
            p_deg = pos.get(p, 0)
            if p_deg % 30 < 2 or p_deg % 30 > 28: vedha_score += 1 # Border tension
            
        # 4. SMI Base
        smi = weather.calculate_smi(d_obj, pos, ma, an, market='US')
        
        # Assemble Level 3 Row
        entry = {
            'Date': row['Date'],
            'Close': round(row['Close'], 2),
            'Mahadasha': ma,
            'Antardasha': an,
            'SMI_Base': round(smi, 2),
            'Tithi': tithi,
            'Nakshatra': nakshatra,
            'Nithya_Yoga': nithya_yoga,
            'Aspect_Mars_Saturn': m_s_aspect,
            'Aspect_Jup_Sun': j_s_aspect,
            'Aspect_Rahu_Mars': r_m_aspect,
            'Vedha_Score': vedha_score
        }
        
        # Add positions & speeds
        for p, deg in pos.items():
            entry[f"{p}_Deg"] = round(deg, 3)
            entry[f"{p}_Speed"] = round(ep.get_planet_data(d_obj, p)[1], 4)
            
        enriched_data.append(entry)
        if idx % 1000 == 0: print(f"70% Progress: {idx} days...")

    master_df = pd.DataFrame(enriched_data)
    save_path = os.path.join(ROOT, 'data/enriched/US/ENERGY_MasterV70.csv')
    master_df.to_csv(save_path, index=False)
    print(f"\nLocked & Archived: {save_path}")

if __name__ == "__main__":
    run_enrichment_v70()
