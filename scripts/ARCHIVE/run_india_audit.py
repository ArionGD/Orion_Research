import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.astro.dasha.vimshottari import VimshottariDasha
from src.engine.medini.crash_logic import MundaneWeatherEngine

def run_india_multi_tier_audit():
    print("=== ACE: Arion Crash Engine - INDIA (NIFTY) MULTI-TIER AUDIT ===")
    
    # Load Models
    model_20 = joblib.load('models/arion_v2_crash_predator.joblib')
    model_10 = joblib.load('models/arion_v2_correction_predator.joblib')
    model_05 = joblib.load('models/arion_v2_pulse_predator.joblib')
    config = joblib.load('models/arion_v2_crash_predator_config.joblib')
    features = config['features']
    
    ep = EphemerisProvider()
    dasha_engine = VimshottariDasha()
    weather_engine = MundaneWeatherEngine()
    
    # INDIA NATAL (Nifty / Independent India: Aug 15, 1947)
    # Moon in Cancer ~117.0 deg
    INDIA_MOON = 117.0
    INDIA_BIRTH = datetime(1947, 8, 15)
    
    def scan_period(start_year, end_year):
        weeks = pd.date_range(start=f'{start_year}-01-01', end=f'{end_year}-12-31', freq='W')
        results = {'-20%': 0, '-10%': 0, '-5%': 0}
        
        for date in weeks:
            # Astro Features
            positions = {}
            speeds = {}
            for p in ['Mars', 'Saturn', 'Neptune', 'True_Node', 'Jupiter', 'Uranus', 'Pluto']:
                lon, spd, retro, _ = ep.get_planet_data(date, p)
                positions[p], speeds[p] = lon, spd
            
            d_info = dasha_engine.get_current_dasha(INDIA_MOON, INDIA_BIRTH, date)
            md, ad = d_info['Mahadasha'], d_info['Antardasha']
            
            weather = weather_engine.get_weather_report(date, positions, md, ad)
            smi = weather['Sovereign_Malefic_Index']
            
            row = {'Sovereign_Malefic_Index': smi}
            diff = abs(positions['Saturn'] - positions['Neptune'])
            if diff > 180: diff = 360 - diff
            row['Saturn_Neptune_Angle'] = diff
            row['aspect_intensity'] = max(0, 10 - diff)
            row['True_Node_Lon'] = positions['True_Node']
            row['Jupiter_Helio_Speed'] = speeds['Jupiter']
            row['Saturn_Helio_Speed'] = speeds['Saturn']
            row['Mars_Helio_Speed'] = speeds['Mars']
            for p in ['Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Mars']:
                row[f'{p}_Speed'] = speeds[p]
            for m in ['Mercury', 'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn']:
                row[f'Mahadasha_{m}'] = 1 if md == m else 0
                row[f'Antardasha_{m}'] = 1 if ad == m else 0
            
            # Defaults
            row['Global_Stability_Index'] = 600
            row['retrograde_count'] = 1
            row['is_hard_aspect'] = 1 if diff < 8 else 0
            row['is_applying'] = 1
            row['Havoc_Velocity'] = 0.5
            row['OOB_Count'] = 1
            row['Mars_OOB_Intensity'] = 0.5
            row['Bradley_Score'] = -10
            row['Gann_Price_Deg'] = 180
            row['is_gann_collision'] = 0
            row['VIX_Stress_Ratio'] = 1.0
            row['Yield_Curve_Inverted'] = 0
            
            df_row = pd.DataFrame([row])
            for col in features:
                if col not in df_row.columns: df_row[col] = 0
            
            X = df_row[features]
            if model_20.predict_proba(X)[:, 1][0] >= 0.80: results['-20%'] += 1
            if model_10.predict_proba(X)[:, 1][0] >= 0.80: results['-10%'] += 1
            if model_05.predict_proba(X)[:, 1][0] >= 0.80: results['-5%'] += 1
            
        return results

    print("\nScanning INDIA Period A: 2010 - 2025 (The Volatile Past)...")
    past = scan_period(2010, 2025)
    
    print("Scanning INDIA Period B: 2026 - 2035 (The Stable Future)...")
    future = scan_period(2026, 2035)
    
    print("\n" + "="*60)
    print("ACE: INDIA (NIFTY) MULTI-TIER PULSE AUDIT")
    print("="*60)
    print(f"TIER             | 2010-2025 (PAST) | 2026-2035 (FUTURE)")
    print(f"----------------------------------------------------------")
    print(f"Structural (-20%)| {past['-20%']} Signals         | {future['-20%']} Signals")
    print(f"Correction (-10%)| {past['-10%']} Signals         | {future['-10%']} Signals")
    print(f"Micro-Pulse (-5%)| {past['-5%']} Signals        | {future['-5%']} Signals")
    print("="*60)
    print("VERDICT: INDIA WEALTH PHYSICS")
    if future['-20%'] == 0:
        print("-> INDIA confirms NO 2008-scale structural failure in the next 10 years.")
        print("-> The Nifty 'Spring' is primed for compounding.")

if __name__ == "__main__":
    run_india_multi_tier_audit()
