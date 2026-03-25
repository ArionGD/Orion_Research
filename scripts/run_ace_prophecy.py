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
from src.engine.world.havoc_logic import GlobalHavocLogic
from src.engine.medini.gann_geometry import GannPriceTranslator
from src.engine.astro.bradley import BradleyOscillator

def generate_ace_prophecy():
    print("=== ACE: Arion Crash Engine - Prophecy Mode (2026-2030) ===")
    
    # 1. Setup Models & Engines
    model_path = 'models/arion_v2_crash_predator.joblib'
    config_path = 'models/arion_v2_crash_predator_config.joblib'
    
    if not os.path.exists(model_path):
        print(f"Error: ACE Model not found at {model_path}")
        return
        
    model = joblib.load(model_path)
    config = joblib.load(config_path)
    feature_cols = config['features']
    
    ep = EphemerisProvider()
    dasha_engine = VimshottariDasha()
    weather_engine = MundaneWeatherEngine()
    gh_engine = GlobalHavocLogic()
    gann_engine = GannPriceTranslator()
    bradley_engine = BradleyOscillator()
    
    # S&P 500 Natal Data
    natal_moon = 348.0
    birth_dt = datetime(1957, 3, 4)
    
    # 2. Project Timeline (Weekly steps)
    start_date = datetime(2026, 1, 1)
    end_date = datetime(2050, 1, 1)
    
    dates = []
    curr = start_date
    while curr <= end_date:
        dates.append(curr)
        curr += relativedelta(weeks=1)
        
    print(f"Scanning {len(dates)} weeks for Crash Signatures...")
    
    prophecy_data = []
    for date in dates:
        row = {}
        prev_date = date - relativedelta(days=7)
        
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
                
        # B. Dasha
        d_info = dasha_engine.get_current_dasha(natal_moon, birth_dt, date)
        row['Mahadasha'] = d_info['Mahadasha']
        row['Antardasha'] = d_info['Antardasha']
        
        # C. Specialized Logic
        # SMI
        pos_smi = {p: positions[p] for p in ['Mars', 'Saturn', 'Neptune']}
        weather = weather_engine.get_weather_report(date, pos_smi, row['Mahadasha'], row['Antardasha'])
        row.update(weather)
        
        # Havoc
        havoc = gh_engine.calculate_havoc_features(date, prev_date)
        row.update(havoc)
        
        # Bradley
        lons_bradley = {p: positions[p] for p in positions}
        row['Bradley_Score'] = bradley_engine.calculate_bradley_score(lons_bradley)
        
        # Gann (Assuming hypothetical price stable at 5000 for Lon calculation)
        p_lon = gann_engine.calculate_price_longitude(pd.Series([5000]))[0]
        row['Gann_Price_Deg'] = p_lon
        row['is_gann_collision'] = 1 if gann_engine.detect_price_time_collision(p_lon, positions['Saturn']) else 0
        
        # SN Angle
        diff = abs(positions['Saturn'] - positions['Neptune'])
        if diff > 180: diff = 360 - diff
        row['Saturn_Neptune_Angle'] = diff
        
        # Helio (Approximated or fixed for simple scan)
        # For full accuracy, ep.get_planet_data needs helio flag handled.
        # Here we'll use geo speeds as proxies or set to 0 to avoid crash if missing
        row['Jupiter_Helio_Speed'] = speeds['Jupiter'] * 0.9 # Approximation
        row['Saturn_Helio_Speed'] = speeds['Saturn'] * 0.9
        row['Mars_Helio_Speed'] = speeds['Mars'] * 1.1
        
        # OOB Intensity
        row['Mars_OOB_Intensity'] = max(0, abs(row.get('Mars_Decl', 0)) - 23.44)
        
        # Technical Proxies (Neutral defaults for prophecy)
        row['VIX_Stress_Ratio'] = 1.0 
        row['Yield_Curve_Inverted'] = 0
        
        # Aspect logic
        row['is_hard_aspect'] = 1 if (diff < 8 or abs(diff-90) < 8 or abs(diff-180) < 8) else 0
        row['is_applying'] = 1 # Neutral
        row['aspect_intensity'] = max(0, 10 - diff)
        
        # Retro count
        row['retrograde_count'] = row['Jupiter_Retro'] + row['Saturn_Retro'] + row['Uranus_Retro'] + row['Neptune_Retro'] + row['Pluto_Retro']

        prophecy_data.append(row)
        
    df = pd.DataFrame(prophecy_data, index=dates)
    
    # One-Hot Encode Dasha to match model features
    df_encoded = pd.get_dummies(df, columns=['Mahadasha', 'Antardasha'])
    
    # Ensure all model columns exist
    for col in feature_cols:
        if col not in df_encoded.columns:
            df_encoded[col] = 0
            
    # Reorder
    X_prophecy = df_encoded[feature_cols]
    
    # Predict
    probs = model.predict_proba(X_prophecy)[:, 1]
    df['Crash_Probability'] = probs
    
    # 3. Report
    print("\n" + "="*60)
    print("ACE: ARION CRASH ENGINE - 2026/2030 PROPHECY REPORT")
    print("="*60)
    
    high_risk = df[df['Crash_Probability'] > 0.70].sort_values('Crash_Probability', ascending=False)
    
    if high_risk.empty:
        print("No critical structural failures detected in the 2026-2030 window.")
    else:
        print(f"Detected {len(high_risk)} High-Risk Weekly Windows.")
        print("\nTop Critical Windows:")
        print(high_risk[['Crash_Probability', 'Sovereign_Malefic_Index', 'Astro_Weather_Status']].head(10))
        
    df.to_csv('data/processed/ace_prophecy_2026_2050.csv')
    
    with open("ACE_PROPHECY_REPORT_2050.md", "w", encoding="utf-8") as f:
        f.write("# ACE: Arion Crash Engine - Sovereign Prophecy (2026-2050)\n")
        f.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write("**Engine Version:** V5.0 (Crash Predator Mode)\n\n")
        
        f.write("## 1. Executive Summary\n")
        f.write(f"The ACE model has scanned **{len(dates)} weeks** of future astronomical data. ")
        f.write(f"It identified **{len(high_risk)} critical windows** where the probability of a structural failure (-20% drawdown) exceeds 70%.\n\n")
        
        f.write("## 2. Top Critical Risk Windows (2026-2030)\n")
        f.write("| Date | Crash Prob | SMI | Weather Status | Dasha Period |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        
        for date, row in high_risk.head(15).iterrows():
            f.write(f"| {date.strftime('%Y-%W')} | **{row['Crash_Probability']:.1%}** | {row['Sovereign_Malefic_Index']:.1f} | {row['Astro_Weather_Status']} | {row['Mahadasha']}-{row['Antardasha']} |\n")
            
        f.write("\n\n## 3. Year-by-Year Breakdown\n")
        years_to_scan = list(range(2026, 2050))
        for year in years_to_scan:
            y_df = df[df.index.year == year]
            if y_df.empty: continue
            peak = y_df['Crash_Probability'].max()
            f.write(f"- **{year}**: Peak Risk level at **{peak:.1%}**. ")
            if peak > 0.70:
                f.write("🔴 **CRITICAL WARNING**\n")
            elif peak > 0.40:
                f.write("🟡 **ELEVATED RISK**\n")
            else:
                f.write("🟢 **STABLE**\n")

        f.write("\n\n*This report is generated using Pure Astrological AI Physics. Trade at your own risk.*")

    print("\nACE Prophecy Report generated: ACE_PROPHECY_REPORT.md")

if __name__ == "__main__":
    generate_ace_prophecy()
