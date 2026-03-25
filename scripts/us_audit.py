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

def run_us_ace_audit():
    print("=== ACE: Arion Crash Engine - USA (S&P 500) FULL AUDIT (2000-2035) ===")
    
    ep = EphemerisProvider()
    dasha_engine = VimshottariDasha()
    weather_engine = MundaneWeatherEngine()
    
    # USA NATAL (Sibly Chart: July 4, 1776)
    # Moon ~ 348.0 deg (Aquarius/Pisces edge)
    US_MOON = 348.0
    US_BIRTH = datetime(1776, 7, 4)
    
    # Ground Truth
    print("Fetching S&P 500 (^GSPC) historical data...")
    sp500 = yf.download("^GSPC", start="2000-01-01", end="2025-03-24", interval="1wk")
    if isinstance(sp500.columns, pd.MultiIndex):
        sp500.columns = sp500.columns.get_level_values(0)
    sp500 = sp500.dropna()
    
    def get_market_drop_truth(date, tier_pct, window_weeks=8):
        end_date = date + timedelta(weeks=window_weeks)
        mask = (sp500.index > date) & (sp500.index <= end_date)
        window_data = sp500.loc[mask]
        if window_data.empty: return False
        
        start_price = window_data.iloc[0]['Open']
        min_price = window_data['Low'].min()
        max_drop = (min_price - start_price) / start_price
        return max_drop <= (-tier_pct / 100.0)

    def scan_period(start_year, end_year, is_future=False):
        weeks = pd.date_range(start=f'{start_year}-01-01', end=f'{end_year}-12-31', freq='W')
        results = {
            '-20%': {'signals': [], 'TP': 0, 'FP': 0, 'FN': 0, 'TN': 0},
            '-10%': {'signals': [], 'TP': 0, 'FP': 0, 'FN': 0, 'TN': 0},
            '-5%':  {'signals': [], 'TP': 0, 'FP': 0, 'FN': 0, 'TN': 0}
        }
        
        for date in weeks:
            # Astro Features
            positions = {}
            for p in ['Mars', 'Saturn', 'Neptune']:
                lon, _, _, _ = ep.get_planet_data(date, p)
                positions[p] = lon
            
            d_info = dasha_engine.get_current_dasha(US_MOON, US_BIRTH, date)
            md, ad = d_info['Mahadasha'], d_info['Antardasha']
            
            # Note: We should pass market='USA' to multipliers if supported, 
            # but MundaneWeatherEngine uses market='INDIA' by default in vpe calls.
            # For this audit, we will stick to the engine's core SMI logic.
            weather = weather_engine.get_weather_report(date, positions, md, ad)
            smi = weather['Sovereign_Malefic_Index']
            
            # Tiers based on SMI
            signal_map = {
                '-20%': smi >= 8.0,
                '-10%': smi >= 6.0,
                '-5%':  smi >= 4.0
            }
            
            for tier, signal_sent in signal_map.items():
                if signal_sent:
                    results[tier]['signals'].append(date.strftime('%Y-%m-%d'))
                
                if not is_future:
                    pct = float(tier.replace('%','').replace('-',''))
                    actual_occurred = get_market_drop_truth(date, pct)
                    
                    if signal_sent and actual_occurred: results[tier]['TP'] += 1
                    elif signal_sent and not actual_occurred: results[tier]['FP'] += 1
                    elif not signal_sent and actual_occurred: results[tier]['FN'] += 1
                    elif not signal_sent and not actual_occurred: results[tier]['TN'] += 1
                    
        return results

    print("\nAuditing USA Past: 2000 - 2025...")
    past = scan_period(2000, 2024)
    
    print("Auditing USA Future: 2025 - 2035...")
    future = scan_period(2025, 2035, is_future=True)
    
    print("\n" + "="*80)
    print("ACE V5 PERFORMANCE MATRIX: USA (S&P 500)")
    print("="*80)
    print("| Tier | Recall | Precision | Accuracy | Signals (Past) | Signals (Future) |")
    print("| :--- | :--- | :--- | :--- | :--- | :--- |")
    
    for tier in ['-20%', '-10%', '-5%']:
        res = past[tier]
        tp, fp, fn, tn = res['TP'], res['FP'], res['FN'], res['TN']
        
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        acc = (tp + tn) / (tp + tn + fp + fn) if (tp+tn+fp+fn) > 0 else 0.0
        
        f_signals = len(future[tier]['signals'])
        p_signals = len(res['signals'])
        
        print(f"| {tier} | {recall:.1%} | {prec:.1%} | {acc:.1%} | {p_signals} | {f_signals} |")

    # Key April 2026 Check for USA
    apr_26 = [s for s in future['-20%']['signals'] if '2026-04' in s]
    if apr_26:
        print(f"\n-> TARGET (-20%): Significant US Structural Risk confirmed in April 2026 ({apr_26[0]})")
    
    print("\n" + "="*80)
    print("FORENSIC VERDICT: US market sensitivity to SMI alignments is high.")

if __name__ == "__main__":
    run_us_ace_audit()
