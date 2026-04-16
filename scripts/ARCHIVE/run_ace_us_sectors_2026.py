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

def generate_us_sector_ace_prophecy():
    print("=== ACE: Arion Crash Engine - US SECTOR ANALYSIS (2026) ===")
    
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
    
    # SECTOR NATAL DATA (Birth Moons)
    # Nasdaq (Feb 8, 1971): Moon in Cancer/Leo boundary ~120.0 deg (Proxy)
    # XLF Banks (Dec 22, 1998): Moon in Aquarius ~315.0 deg
    # XLRE Real Estate (Oct 8, 2015): Moon in Leo ~135.0 deg
    
    sectors = {
        'NASDAQ (Tech)': {'moon': 120.0, 'birth': datetime(1971, 2, 8)},
        'SMH (Semis/AI)': {'moon': 45.0, 'birth': datetime(2011, 12, 20)}, # AI Proxy
        'XLF (Banks)': {'moon': 315.0, 'birth': datetime(1998, 12, 22)},
        'XLRE (Real Estate)': {'moon': 135.0, 'birth': datetime(2015, 10, 8)},
        'XLE (Energy)': {'moon': 240.0, 'birth': datetime(1998, 12, 22)},
        'GLD (Gold Proxy)': {'moon': 180.0, 'birth': datetime(2004, 11, 18)},
        'S&P 500 (Base)': {'moon': 348.0, 'birth': datetime(1957, 3, 4)}
    }
    
    # 2. Timeline (Monthly steps for 2026)
    months = pd.date_range(start='2026-01-01', end='2026-12-01', freq='MS')
    
    sector_results = {}
    
    for sector_name, info in sectors.items():
        print(f"Analyzing {sector_name} Structural Integrity...")
        monthly_probs = []
        
        for date in months:
            # A. Astro Weather
            positions = {}
            speeds = {}
            for p in ['Mars', 'Saturn', 'Neptune', 'True_Node', 'Jupiter', 'Uranus', 'Pluto']:
                lon, spd, retro, _ = ep.get_planet_data(date, p)
                positions[p] = lon
                speeds[p] = spd
            
            # B. Dasha
            d_info = dasha_engine.get_current_dasha(info['moon'], info['birth'], date)
            md = d_info['Mahadasha']
            ad = d_info['Antardasha']
            
            # C. SMI Weather
            weather = weather_engine.get_weather_report(date, positions, md, ad)
            smi = weather['Sovereign_Malefic_Index']
            
            # D. Feature Row (Simplified for prophecy scan)
            row = {}
            diff = abs(positions['Saturn'] - positions['Neptune'])
            if diff > 180: diff = 360 - diff
            
            row['Sovereign_Malefic_Index'] = smi
            row['Saturn_Neptune_Angle'] = diff
            row['aspect_intensity'] = max(0, 10 - diff)
            row['Global_Stability_Index'] = 600
            row['True_Node_Lon'] = positions['True_Node']
            row['retrograde_count'] = 1
            row['is_hard_aspect'] = 1 if diff < 8 else 0
            row['is_applying'] = 1
            row['Havoc_Velocity'] = 0.5
            row['OOB_Count'] = 1
            row['Mars_OOB_Intensity'] = 0.5
            row['Bradley_Score'] = -10
            row['Gann_Price_Deg'] = 180
            row['is_gann_collision'] = 0
            row['Jupiter_Helio_Speed'] = speeds['Jupiter']
            row['Saturn_Helio_Speed'] = speeds['Saturn']
            row['Mars_Helio_Speed'] = speeds['Mars']
            row['VIX_Stress_Ratio'] = 1.0
            row['Yield_Curve_Inverted'] = 0
            
            # Speeds
            for p in ['Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Mars']:
                row[f'{p}_Speed'] = speeds[p]
                
            # Dasha Encoding
            for m in ['Mercury', 'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn']:
                row[f'Mahadasha_{m}'] = 1 if md == m else 0
                row[f'Antardasha_{m}'] = 1 if ad == m else 0
            
            # Predict
            df_row = pd.DataFrame([row])
            # Align with feature_cols
            for col in feature_cols:
                if col not in df_row.columns:
                    df_row[col] = 0
            
            X = df_row[feature_cols]
            prob = model.predict_proba(X)[:, 1][0]
            monthly_probs.append(prob)
            
        sector_results[sector_name] = monthly_probs

    # 3. Output Report
    print("\n" + "="*60)
    print("ACE: US SECTOR ASSAULT - 2026 RISK PROBABILITY (%)")
    print("="*60)
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    results_df = pd.DataFrame(sector_results, index=month_names)
    print(results_df.applymap(lambda x: f"{x:.2%}"))
    
    print("\n" + "="*60)
    print("ACE TARGET VERDICT: THE MOST FRAGILE SECTOR FOR 2026")
    print("="*60)
    for sector in sector_results:
        peak = max(sector_results[sector])
        peak_m = month_names[sector_results[sector].index(peak)]
        print(f"-> {sector}: Peak Risk {peak:.2%} in {peak_m}")

if __name__ == "__main__":
    generate_us_sector_ace_prophecy()
