import pandas as pd
import numpy as np
import os
import swisseph as swe
from datetime import datetime, timedelta
import sys

# Root Path
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"
sys.path.append(ROOT)

from src.engine.medini.crash_logic import MundaneWeatherEngine
from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.astro.dasha.vimshottari import VimshottariDasha

def get_aspect(d1, d2, orb=10):
    diff = abs(d1 - d2) % 360
    if diff > 180: diff = 360 - diff
    if diff <= orb: return 1 # Conj
    if abs(diff - 180) <= orb: return 2 # Opp
    if abs(diff - 90) <= orb: return 3 # Square
    return 0

def enrich_sp500_v70():
    print("=== ACE: SP500 ENRICHMENT V70 (70% DEPTH) ===")
    
    # 1. Path Management
    raw_path = os.path.join(ROOT, 'data/raw/US/MASTER/SP500_STANDARD.csv')
    enriched_dir = os.path.join(ROOT, 'data/enriched/US/SP500')
    if not os.path.exists(enriched_dir):
        os.makedirs(enriched_dir)
        
    if not os.path.exists(raw_path):
        print(f"Error: {raw_path} not found.")
        return
        
    # 2. Parsing Multi-Header Legacy Data
    # Yahoo style: Price/Ticker/Date headers. We skip 3 and map Date + Close
    df = pd.read_csv(raw_path, skiprows=3, names=['Date', 'Close', 'High', 'Low', 'Open', 'Volume'])
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 3. Engine Initialization
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    dasha_eng = VimshottariDasha()
    weather = MundaneWeatherEngine()
    
    # Sibley Chart Anchors
    BIRTH = datetime(1776, 7, 4)
    MOON = 312.0
    
    results = []
    print(f"Processing {len(df)} days of SP500 legacy data...")
    
    for idx, row in df.iterrows():
        d_obj = row['Date']
        pos = ep.get_all_positions(d_obj)
        
        # Dasha Logic
        try:
            dasha = dasha_eng.get_current_dasha(MOON, BIRTH, d_obj)
            ma = dasha['Mahadasha']; an = dasha['Antardasha']
        except: ma='Mars'; an='Saturn'
        
        # Cosmic Dimensions
        sun = pos.get('Sun', 0); moon = pos.get('Moon', 0)
        tithi = int(((moon - sun) % 360) // 12) + 1
        nakshatra = int(moon // (360/27)) + 1
        yoga = int(((sun + moon) % 360) // (360/27)) + 1
        
        # Vedha & SMI
        vedha = 0
        for p in ['Mars', 'Saturn', 'True_Node']:
            p_deg = pos.get(p, 0)
            if p_deg % 30 < 2 or p_deg % 30 > 28: vedha += 1
            
        entry = {
            'Date': d_obj.strftime('%Y-%m-%d'),
            'Close': round(row['Close'], 3),
            'Mahadasha': ma,
            'Antardasha': an,
            'SMI_Base': round(weather.calculate_smi(d_obj, pos, ma, an, market='US'), 2),
            'Tithi': tithi,
            'Nakshatra': nakshatra,
            'Nithya_Yoga': yoga,
            'Aspect_Mars_Saturn': get_aspect(pos.get('Mars', 0), pos.get('Saturn', 0)),
            'Aspect_Jup_Sun': get_aspect(pos.get('Jupiter', 0), pos.get('Sun', 0)),
            'Aspect_Rahu_Mars': get_aspect(pos.get('True_Node', 0), pos.get('Mars', 0)),
            'Vedha_Score': vedha
        }
        
        # High-Res Precision (3 decimals)
        for p, deg in pos.items():
            entry[f"{p}_Deg"] = round(deg, 3)
            entry[f"{p}_Speed"] = round(ep.get_planet_data(d_obj, p)[1], 4)
            
        results.append(entry)
        
    enriched_df = pd.DataFrame(results)
    output_file = os.path.join(enriched_dir, 'SP500_MasterV70.csv')
    enriched_df.to_csv(output_file, index=False)
    print(f"Successfully generated: {output_file}")

if __name__ == "__main__":
    enrich_sp500_v70()
