import pandas as pd
import numpy as np
import swisseph as swe
import joblib
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.astro.dasha.vimshottari import VimshottariDasha
from src.engine.medini.crash_logic import MundaneWeatherEngine

def run_ace_2030_pulse_scan():
    print("=== ACE: Arion Crash Engine - 2025-2030 PRECISION PULSE SCAN ===")
    
    # Load Models
    model_20 = joblib.load('models/arion_v2_crash_predator.joblib')
    model_10 = joblib.load('models/arion_v2_correction_predator.joblib')
    config = joblib.load('models/arion_v2_crash_predator_config.joblib')
    features = config['features']
    
    ep = EphemerisProvider()
    dasha_engine = VimshottariDasha()
    weather_engine = MundaneWeatherEngine()
    
    # S&P 500 Natal Chart
    SP_MOON = 348.0
    SP_BIRTH = datetime(1957, 3, 4)
    
    # Timeline (Extended to 2035)
    weeks = pd.date_range(start='2025-01-01', end='2035-12-31', freq='W')
    
    signals_20 = []
    signals_10 = []
    
    for date in weeks:
        # 1. Astro Positions
        positions = {}
        speeds = {}
        for p in ['Mars', 'Saturn', 'Neptune', 'True_Node', 'Jupiter', 'Uranus', 'Pluto']:
            lon, spd, retro, _ = ep.get_planet_data(date, p)
            positions[p] = lon
            speeds[p] = spd
            
        # 2. Dasha
        d_info = dasha_engine.get_current_dasha(SP_MOON, SP_BIRTH, date)
        md, ad = d_info['Mahadasha'], d_info['Antardasha']
        
        # 3. Features
        weather = weather_engine.get_weather_report(date, positions, md, ad)
        smi = weather['Sovereign_Malefic_Index']
        
        row = {'Sovereign_Malefic_Index': smi}
        diff = abs(positions['Saturn'] - positions['Neptune'])
        if diff > 180: diff = 360 - diff
        row['Saturn_Neptune_Angle'] = diff
        row['aspect_intensity'] = max(0, 10 - diff)
        
        # Speeds & Nodes
        row['Jupiter_Helio_Speed'] = speeds['Jupiter']
        row['Saturn_Helio_Speed'] = speeds['Saturn']
        row['Mars_Helio_Speed'] = speeds['Mars']
        for p in ['Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Mars']:
            row[f'{p}_Speed'] = speeds[p]
        row['True_Node_Lon'] = positions['True_Node']
        
        # Dasha One-Hot
        for m in ['Mercury', 'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn']:
            row[f'Mahadasha_{m}'] = 1 if md == m else 0
            row[f'Antardasha_{m}'] = 1 if ad == m else 0
            
        # Placeholder Defaults
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
        
        # Predictions
        prob_20 = model_20.predict_proba(X)[:, 1][0]
        prob_10 = model_10.predict_proba(X)[:, 1][0]
        
        if prob_20 >= 0.80: signals_20.append(date)
        if prob_10 >= 0.80: signals_10.append(date)

    print("\n" + "="*60)
    print("ACE: 2025-2030 TOTAL MINTING POOL (SIGNAL CENSUS)")
    print("="*60)
    print(f"Total Structural Failure Signals (-20% Scale): {len(signals_20)} Weeks")
    print(f"Total Market Correction Signals (-10% Scale): {len(signals_10)} Weeks")
    
    if signals_20:
        print("\nPEAK RISK WINDOWS (-20%):")
        for s in signals_20: print(f"-> {s.strftime('%Y-%m-%d')}")
        
    if signals_10:
        print("\nMAJOR CORRECTION PULSES (-10%):")
        df_10 = pd.DataFrame(signals_10, columns=['Date'])
        for year in range(2025, 2036):
            y_signals = df_10[df_10['Date'].dt.year == year]
            if not y_signals.empty:
                print(f"-> {year}: {len(y_signals)} Signal-Weeks")

if __name__ == "__main__":
    run_ace_2030_pulse_scan()
