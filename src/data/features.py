import pandas as pd
import os
from datetime import timedelta
import sys

# Ensure src is in pythonpath
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# -- New Modular Imports --
from src.engine.astro.planets.saturn.conjunctions import SaturnConjunctions
from src.engine.astro.planets.mars.general import MarsGeneralLogic
from src.engine.world.havoc_logic import GlobalHavocLogic
from src.engine.world.speculation_logic import SpeculationLogic
from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.medini.gann_geometry import GannPriceTranslator
from src.engine.medini.vix_gex_plumbing import VolatilityPlumbingScanner
from src.engine.astro.bradley import BradleyOscillator
from src.engine.medini.crash_logic import MundaneWeatherEngine

def process_features_modular():
    print("Initializing Modular Feature Engine...")
    
    input_path = 'data/raw/century_master.csv'
    if not os.path.exists(input_path):
        print("Raw data not found.")
        return

    df = pd.read_csv(input_path, parse_dates=['Date'], index_col='Date')
    
    # Initialize Engines
    sn_engine = SaturnConjunctions()
    mars_engine = MarsGeneralLogic()
    gh_engine = GlobalHavocLogic()
    spec_engine = SpeculationLogic()
    gann_engine = GannPriceTranslator()
    vix_engine = VolatilityPlumbingScanner()
    bradley_engine = BradleyOscillator()
    weather_engine = MundaneWeatherEngine()
    ep = EphemerisProvider()
    
    # We also need planetary speeds for the other outer planets (Jup, Ura, Plu) 
    # as they were in the original model.
    other_outers = ['Jupiter', 'Uranus', 'Pluto']

    refined_data = []
    
    print(f"Processing {len(df)} rows with Global Havoc Logic...")
    
    for date in df.index:
        row_feat = {}
        
        # 1. Saturn-Neptune Module
        prev_date = date - timedelta(days=1)
        sn_feats = sn_engine.analyze_neptune_relation(date, prev_date)
        row_feat.update(sn_feats)
        
        # 2. Mars Volatility Module
        mars_feats = mars_engine.calculate_volatility(date)
        row_feat.update(mars_feats)

        # 3. Global Havoc Module
        havoc_feats = gh_engine.calculate_havoc_features(date, prev_date)
        row_feat.update(havoc_feats)

        # 4. Mundane Weather & Sovereign Malefic Index (SMI)
        # Fetch current positions for SMI
        positions_smi = {p: df.loc[date, f'{p}_Lon'] for p in ['Mars', 'Saturn', 'Neptune'] if f'{p}_Lon' in df.columns}
        md = df.loc[date, 'Mahadasha'] if 'Mahadasha' in df.columns else 'Unknown'
        ad = df.loc[date, 'Antardasha'] if 'Antardasha' in df.columns else 'Unknown'
        weather_feats = weather_engine.get_weather_report(date, positions_smi, md, ad)
        row_feat.update(weather_feats)

        # 5. Speculation/Flash Crash Module
        spec_feats = spec_engine.calculate_speculation_features(date)
        row_feat.update(spec_feats)
        
        # 6. Gann Price-Planet Geometry (PURE ASTRO - No VIX Interference)
        if 'Close' in df.columns:
            p_lon = gann_engine.calculate_price_longitude(pd.Series([df.loc[date, 'Close']]))[0]
            row_feat['Gann_Price_Deg'] = p_lon
            # Collision Logic: Price vs Saturn (Hard Angle)
            sat_lon, _, _, _ = ep.get_planet_data(date, 'Saturn')
            row_feat['is_gann_collision'] = 1 if gann_engine.detect_price_time_collision(p_lon, sat_lon) else 0
        
        # 6. VIX Plumbing Module
        if 'VIX_Close' in df.columns:
            # We pass the full VIX series to calculate SMA/Backwardation
            vix_ratio = vix_engine.calculate_synthetic_backwardation(df['VIX_Close']).loc[date]
            row_feat['VIX_Backwardation_Ratio'] = vix_ratio
            row_feat['Structural_Failure_Trigger'] = 1 if (df.loc[date, 'VIX_Close'] > 40 and vix_ratio > 1.30) else 0
        
        # 7. Lunar Sentiment Sniper Features
        if 'Moon_Phase_Deg' in df.columns:
            # Distance to New Moon (0) or Full Moon (180) - normalized to danger
            phase = df.loc[date, 'Moon_Phase_Deg']
            # New moon (Panic/Euphoria) or Full Moon (Emotional/Drain)
            synodic_dist = min(abs(phase - 0), abs(phase - 180), abs(phase - 360))
            row_feat['Lunar_Synodic_Danger'] = 1.0 - (synodic_dist / 90.0) # 1.0 = High synodic stress
            
        # 8. Synthetic Chaos Proxy (The Structural Pulse)
        # Replacing VIX-noise with pure Astro-Mechanical Momentum
        price_mom = df['Log_Return'].rolling(window=3, min_periods=1).mean().loc[date]
        row_feat['Astro_Momentum_Pulse'] = row_feat['Sovereign_Malefic_Index'] - price_mom
            
        # 9. Yield Curve & Momentum Pass-through (from ingestor)
        pass_cols = [
            'Yield_Curve_Spread', 'Yield_Curve_Inverted', 'Momentum_4W', 
            'Momentum_12W', 'Volatility_20W',
            'Mars_Helio_Lon', 'Mars_Helio_Speed', 'Jupiter_Helio_Lon', 
            'Jupiter_Helio_Speed', 'Saturn_Helio_Lon', 'Saturn_Helio_Speed',
            'Moon_Decl', 'Mars_Decl'
        ]
        for col in pass_cols:
            if col in df.columns:
                val = df.loc[date, col]
                if pd.notna(val):
                    row_feat[col] = val

        # 10. Bradley Siderograph Feature
        # Pass all planetary longitudes to the Bradley Engine
        lons = {c.replace('_Lon', ''): df.loc[date, c] for c in df.columns if '_Lon' in c}
        row_feat['Bradley_Score'] = bradley_engine.calculate_bradley_score(lons)

        # 11. Weighted OOB Physics (Exact intensity of declination)
        if 'Mars_Decl' in row_feat:
            # Over 23.5 degrees is OOB. We track the 'Distance' into chaos.
            row_feat['Mars_OOB_Intensity'] = max(0, abs(row_feat['Mars_Decl']) - 23.44)
        if 'Moon_Decl' in row_feat:
            row_feat['Moon_OOB_Intensity'] = max(0, abs(row_feat['Moon_Decl']) - 23.44)

        # 12. Lunar Velocity Acceleration
        if 'Moon_Speed' in df.columns:
            # High speed Moon = High retail emotion
            row_feat['Moon_Velocity'] = df.loc[date, 'Moon_Speed']
            # Change in speed (Acceleration)
            prev_row_idx = df.index.get_loc(date) - 1
            if prev_row_idx >= 0:
                accel = df.loc[date, 'Moon_Speed'] - df.iloc[prev_row_idx]['Moon_Speed']
                row_feat['Moon_Acceleration'] = accel
            
        # 9. Other Outers (Jupiter, Uranus, Pluto) - Direct from Provider
        for p in other_outers:
            lon, speed, retro, _ = ep.get_planet_data(date, p)
            if lon is not None:
                row_feat[f'{p}_Speed'] = speed
                row_feat[f'{p}_Retro'] = retro
                row_feat[f'{p}_Lon'] = lon
        
        # 5. Retrograde Count (Sum of Jup, Sat, Ura, Nep, Plu)
        count = 0
        for p in ['Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']:
            k = f'{p}_Retro'
            if k in row_feat:
                count += row_feat[k]
        row_feat['retrograde_count'] = count
        
        refined_data.append(row_feat)
        
    # Convert to DF
    feat_df = pd.DataFrame(refined_data, index=df.index)
    
    # Combine with original data
    # Drop existing feature columns from original info to avoid overlap
    new_cols = feat_df.columns
    existing_cols = [c for c in df.columns if c not in new_cols]
    final_df = pd.concat([df[existing_cols], feat_df], axis=1)

    # Save
    output_path = 'data/processed/refined_features.csv' 
    final_df.to_csv(output_path)
    print(f"Modular features saved to: {output_path}")
    print(final_df[['Saturn_Neptune_Angle', 'Global_Stability_Index', 'Flash_Crash_Probability']].head())

if __name__ == "__main__":
    process_features_modular()

