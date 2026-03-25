import sys
from datetime import datetime
from pathlib import Path
import pandas as pd

PROJECT_ROOT = r'd:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5'
sys.path.append(PROJECT_ROOT)

from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.astro.dasha.vimshottari import VimshottariDasha
from src.engine.medini.crash_logic import MundaneWeatherEngine
from src.engine.medini.conflict_modifier import ConflictModifier

def check_april_19_2026():
    ep = EphemerisProvider()
    dasha_engine = VimshottariDasha()
    weather_engine = MundaneWeatherEngine()
    conflict_engine = ConflictModifier()
    
    # India Natal as per run_ace_india_2026.py
    INDIA_MOON = 100.15
    INDIA_BIRTH = datetime(1947, 8, 15)
    
    target_date = datetime(2026, 4, 19)
    print(f"--- ANALYSING DATE: {target_date.strftime('%Y-%m-%d')} ---")
    
    # 1. Dasha
    d_info = dasha_engine.get_current_dasha(INDIA_MOON, INDIA_BIRTH, target_date)
    md, ad = d_info['Mahadasha'], d_info['Antardasha']
    print(f"Dasha: {md} - {ad}")
    
    # 2. Positions
    positions = {}
    for p in ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'True_Node']:
        lon, _, _, _ = ep.get_planet_data(target_date, p)
        positions[p] = lon
        
    # 3. Basic SMI
    weather = weather_engine.get_weather_report(target_date, positions, md, ad)
    print(f"Basic SMI: {weather['Sovereign_Malefic_Index']}")
    
    # 4. Conflict Analysis
    conflict = conflict_engine.analyze_conflict(positions, date=target_date)
    print(f"Conflict Type: {conflict['conflict_type']}")
    print(f"Conflict Intensity: {conflict['intensity']}%")
    print(f"Sector Modifiers: {conflict['sector_modifiers']}")
    
    # 5. Total Risk (Summing SMI + specific sector pressure for Tech/Banks)
    tech_hit = abs(conflict['sector_modifiers'].get('Tech & AI', 0))
    bank_hit = abs(conflict['sector_modifiers'].get('Banking & Finance', 0))
    
    composite_risk = weather['Sovereign_Malefic_Index'] + (tech_hit * 0.5) + (bank_hit * 0.5)
    print(f"Composite Risk Score (Experimental): {composite_risk}")

if __name__ == "__main__":
    check_april_19_2026()
