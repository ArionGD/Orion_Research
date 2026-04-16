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
from src.engine.countries.india.logic import IndiaRiskEngine

def generate_india_ace_prophecy():
    print("=== ACE: Arion Crash Engine - INDIA PROPHECY (2026) ===")
    
    # 1. Setup Models & Engines
    model_path = 'models/arion_v2_crash_predator.joblib'
    config_path = 'models/arion_v2_crash_predator_config.joblib'
    
    if not os.path.exists(model_path):
        print(f"Error: ACE Model not found.")
        return
        
    model = joblib.load(model_path)
    config = joblib.load(config_path)
    feature_cols = config['features']
    
    ep = EphemerisProvider()
    dasha_engine = VimshottariDasha()
    weather_engine = MundaneWeatherEngine()
    india_engine = IndiaRiskEngine()
    
    # INDIA NATAL DATA (Independence Chart: Aug 15, 1947, 00:00 IST)
    # Moon in Cancer (Pushya) ~100.15 deg
    india_moon = 100.15
    india_birth = datetime(1947, 8, 15, 0, 0)
    
    # 2. Project Timeline (Weekly steps for 2026)
    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 12, 31)
    
    dates = []
    curr = start_date
    while curr <= end_date:
        dates.append(curr)
        curr += relativedelta(weeks=1)
        
    print(f"Scanning 52 weeks for India Structural Risk...")
    
    prophecy_data = []
    for date in dates:
        row = {}
        # A. Basic Planet Data
        positions = {}
        speeds = {}
        for p in ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'True_Node']:
            lon, spd, retro, decl = ep.get_planet_data(date, p)
            positions[p] = lon
            speeds[p] = spd
            row[f'{p}_Lon'] = lon
            row[f'{p}_Speed'] = spd
            row[f'{p}_Retro'] = 1 if retro else 0
            if p in ['Mars', 'Moon']:
                row[f'{p}_Decl'] = decl
                
        # B. India Dasha
        d_info = dasha_engine.get_current_dasha(india_moon, india_birth, date)
        row['Mahadasha'] = d_info['Mahadasha']
        row['Antardasha'] = d_info['Antardasha']
        
        # C. Specialized Logic
        # SMI
        pos_smi = {p: positions[p] for p in ['Mars', 'Saturn', 'Neptune']}
        weather = weather_engine.get_weather_report(date, pos_smi, row['Mahadasha'], row['Antardasha'])
        row['Sovereign_Malefic_Index'] = weather['Sovereign_Malefic_Index']
        row['Astro_Weather_Status'] = weather['Astro_Weather_Status']
        
        # India Specific Risk (Sade Sati, etc)
        in_score, in_sig = india_engine.check_risk(positions)
        row['India_Risk_Score'] = in_score
        
        # D. Mapping to Model Features
        # Angle
        diff = abs(positions['Saturn'] - positions['Neptune'])
        if diff > 180: diff = 360 - diff
        row['Saturn_Neptune_Angle'] = diff
        row['is_hard_aspect'] = 1 if (diff < 8 or abs(diff-90) < 8 or abs(diff-180) < 8) else 0
        row['aspect_intensity'] = max(0, 10 - diff)
        row['Global_Stability_Index'] = 600
        row['Havoc_Velocity'] = 0
        row['OOB_Count'] = 1
        row['True_Node_Lon'] = positions['True_Node']
        row['Mars_OOB_Intensity'] = max(0, abs(row.get('Mars_Decl', 0)) - 23.44)
        row['Bradley_Score'] = 0 # Placeholder
        row['Gann_Price_Deg'] = 0
        row['is_gann_collision'] = 0
        row['Jupiter_Helio_Speed'] = speeds['Jupiter']
        row['Saturn_Helio_Speed'] = speeds['Saturn']
        row['Mars_Helio_Speed'] = speeds['Mars']
        row['VIX_Stress_Ratio'] = 1.0
        row['Yield_Curve_Inverted'] = 0
        row['is_applying'] = 1
        row['retrograde_count'] = row['Jupiter_Retro'] + row['Saturn_Retro'] + row['Uranus_Retro']

        prophecy_data.append(row)
        
    df = pd.DataFrame(prophecy_data, index=dates)
    
    # Encode and Align
    df_encoded = pd.get_dummies(df, columns=['Mahadasha', 'Antardasha'])
    for col in feature_cols:
        if col not in df_encoded.columns:
            df_encoded[col] = 0
    X_prophecy = df_encoded[feature_cols]
    
    # Predict
    probs = model.predict_proba(X_prophecy)[:, 1]
    df['Crash_Probability'] = probs
    
    # Output
    print("\n" + "="*60)
    print("ACE: ARION CRASH ENGINE - INDIA 2026 MODEM")
    print("="*60)
    
    # Group by month
    monthly = df.groupby(df.index.month)['Crash_Probability'].max()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    print("| Month | Crash Prob | India Risk | Status |")
    print("| :--- | :--- | :--- | :--- |")
    for i, p in enumerate(monthly):
        m_name = months[i]
        # Get peak row for that month
        m_data = df[df.index.month == (i+1)]
        smi = m_data['Sovereign_Malefic_Index'].max()
        risk = m_data['India_Risk_Score'].max()
        
        status = "STABLE"
        if p > 0.40: status = "DANGER"
        elif p > 0.20: status = "VOLATILE"
        
        print(f"| {m_name} | {p:.2%} | {risk} | {status} |")

if __name__ == "__main__":
    generate_india_ace_prophecy()
