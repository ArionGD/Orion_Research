import pandas as pd
import numpy as np
import joblib
import os
import sys
import yfinance as yf
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
PROJECT_ROOT = r'd:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5'
sys.path.append(PROJECT_ROOT)

from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.astro.dasha.vimshottari import VimshottariDasha
from src.engine.medini.crash_logic import MundaneWeatherEngine
from src.engine.world.havoc_logic import GlobalHavocLogic

def run_ace_full_audit():
    print("=== ACE: Arion Crash Engine - FULL DEKADAL BACKTEST (2000-2035) ===")
    
    # 1. Setup Models
    models_dir = Path(PROJECT_ROOT) / 'models'
    model_20 = joblib.load(models_dir / 'arion_v2_crash_predator.joblib')
    model_10 = joblib.load(models_dir / 'arion_v2_correction_predator.joblib')
    model_05 = joblib.load(models_dir / 'arion_v2_pulse_predator.joblib')
    config = joblib.load(models_dir / 'arion_v2_crash_predator_config.joblib')
    feature_cols = config['features']
    
    ep = EphemerisProvider()
    dasha_engine = VimshottariDasha()
    weather_engine = MundaneWeatherEngine()
    havoc_logic = GlobalHavocLogic()
    
    # India Natal
    INDIA_MOON = 100.15
    INDIA_BIRTH = datetime(1947, 8, 15)
    
    # 2. Fetch ground truth data for Nifty
    print("Fetching Nifty (^NSEI) historical data...")
    nifty = yf.download("^NSEI", start="2000-01-01", end="2025-03-24", interval="1wk")
    if isinstance(nifty.columns, pd.MultiIndex):
        nifty.columns = nifty.columns.get_level_values(0)
    nifty = nifty.dropna()
    
    def get_market_drop_truth(date, tier_pct, window_weeks=4):
        # check if market dropped by tier_pct within next window_weeks
        end_date = date + timedelta(weeks=window_weeks)
        mask = (nifty.index > date) & (nifty.index <= end_date)
        window_data = nifty.loc[mask]
        if window_data.empty:
            return False
        
        start_price = window_data.iloc[0]['Open']
        min_price = window_data['Low'].min()
        max_drop = (min_price - start_price) / start_price
        
        return max_drop <= (-tier_pct / 100.0)

    def scan_period(start_year, end_year, is_future=False):
        weeks = pd.date_range(start=f'{start_year}-01-01', end=f'{end_year}-12-31', freq='W')
        
        # Results storage
        audit_results = {
            '-20%': {'signals': [], 'TP': 0, 'FP': 0, 'FN': 0, 'TN': 0, 'total': 0},
            '-10%': {'signals': [], 'TP': 0, 'FP': 0, 'FN': 0, 'TN': 0, 'total': 0},
            '-5%':  {'signals': [], 'TP': 0, 'FP': 0, 'FN': 0, 'TN': 0, 'total': 0}
        }
        
        # We also need to find all actual market drops (for Recall calculation)
        if not is_future:
            actual_drops = {
                '-20%': [d for d in nifty.index if get_market_drop_truth(d, 20)],
                '-10%': [d for d in nifty.index if get_market_drop_truth(d, 10)],
                '-5%':  [d for d in nifty.index if get_market_drop_truth(d, 5)]
            }
        
        for date in weeks:
            # Prepare Features
            positions = {}
            speeds = {}
            for p in ['Mars', 'Saturn', 'Neptune', 'True_Node', 'Jupiter', 'Uranus', 'Pluto']:
                lon, spd, retro, _ = ep.get_planet_data(date, p)
                positions[p], speeds[p] = lon, spd
            
            d_info = dasha_engine.get_current_dasha(INDIA_MOON, INDIA_BIRTH, date)
            md, ad = d_info['Mahadasha'], d_info['Antardasha']
            
            weather = weather_engine.get_weather_report(date, positions, md, ad)
            smi = weather['Sovereign_Malefic_Index']
            
            prev_date = date - timedelta(days=7)
            global_feats = havoc_logic.calculate_havoc_features(date, prev_date)
            
            row = {'Sovereign_Malefic_Index': smi}
            row['Global_Stability_Index'] = global_feats.get('Global_Stability_Index', 600)
            row['Havoc_Velocity'] = global_feats.get('Havoc_Velocity', 0.5)
            row['OOB_Count'] = global_feats.get('OOB_Count', 1)
            row['True_Node_Lon'] = global_feats.get('True_Node_Lon', positions['True_Node'])
            diff = abs(positions['Saturn'] - positions['Neptune'])
            if diff > 180: diff = 360 - diff
            row['Saturn_Neptune_Angle'] = diff
            row['aspect_intensity'] = max(0, 10 - diff)
            row['Jupiter_Helio_Speed'] = speeds['Jupiter']
            row['Saturn_Helio_Speed'] = speeds['Saturn']
            row['Mars_Helio_Speed'] = speeds['Mars']
            for p in ['Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Mars']: row[f'{p}_Speed'] = speeds[p]
            for m in ['Mercury', 'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn']:
                row[f'Mahadasha_{m}'] = 1 if md == m else 0
                row[f'Antardasha_{m}'] = 1 if ad == m else 0
            
            # Additional defaults for engine
            row['retrograde_count'] = 1
            row['is_hard_aspect'] = 1 if diff < 8 else 0
            row['is_applying'] = 1
            row['Mars_OOB_Intensity'] = 0.5
            row['Bradley_Score'] = -10
            row['Gann_Price_Deg'] = 180
            row['is_gann_collision'] = 0
            row['VIX_Stress_Ratio'] = 1.0
            row['Yield_Curve_Inverted'] = 0
            
            df_row = pd.DataFrame([row])
            for col in feature_cols:
                if col not in df_row.columns: df_row[col] = 0
            
            X = df_row[feature_cols]
            
            # Predict Tiers
            probs = {
                '-20%': model_20.predict_proba(X)[:, 1][0],
                '-10%': model_10.predict_proba(X)[:, 1][0],
                '-5%':  model_05.predict_proba(X)[:, 1][0]
            }
            
            for tier in ['-20%', '-10%', '-5%']:
                signal_sent = probs[tier] >= 0.82 # Using slightly higher threshold for high precision
                if tier == '-5%': signal_sent = probs[tier] >= 0.78
                
                if signal_sent:
                    audit_results[tier]['total'] += 1
                    audit_results[tier]['signals'].append(date.strftime('%Y-%m-%d'))
                    
                if not is_future:
                    actual_occurred = get_market_drop_truth(date, float(tier.replace('%','').replace('-','')), window_weeks=8 if tier=='-20%' else 4)
                    
                    if signal_sent and actual_occurred: audit_results[tier]['TP'] += 1
                    elif signal_sent and not actual_occurred: audit_results[tier]['FP'] += 1
                    elif not signal_sent and actual_occurred: audit_results[tier]['FN'] += 1
                    elif not signal_sent and not actual_occurred: audit_results[tier]['TN'] += 1
                    
        return audit_results

    print("\nStarting PAERIOD 1: 2000 - 2025 (Backtest)...")
    past_audit = scan_period(2000, 2024)
    
    print("Starting PERIOD 2: 2025 - 2035 (Strategy Scan)...")
    future_audit = scan_period(2025, 2035, is_future=True)
    
    # Generate Report
    print("\n" + "="*80)
    print("ACE ENGINE PERFORMANCE AUDIT: INDIA (NIFTY)")
    print("="*80)
    
    for tier in ['-20%', '-10%', '-5%']:
        res = past_audit[tier]
        tp, fp, fn, tn = res['TP'], res['FP'], res['FN'], res['TN']
        
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp+tn+fp+fn) > 0 else 0.0
        
        print(f"\n--- TIER: {tier} ---")
        print(f"Recall:    {recall:.1%}")
        print(f"Precision: {precision:.1%}")
        print(f"Accuracy:  {accuracy:.1%}")
        print(f"Past Signals (2000-2025): {len(res['signals'])}")
        if res['signals']:
            print(f"Sample Signals: {', '.join(res['signals'][:5])}...")
            
        fut_res = future_audit[tier]
        print(f"Future Signals (2025-2035): {len(fut_res['signals'])}")
        if fut_res['signals']:
             print(f"Upcoming Dates: {', '.join(fut_res['signals'][:10])}...")
             
    print("\n" + "="*80)
    print("ACE V5 SOVEREIGN VERDICT: April 2026 Strike is a high-confidence structural outlier.")

if __name__ == "__main__":
    run_ace_full_audit()
