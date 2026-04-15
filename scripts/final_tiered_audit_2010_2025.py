import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import swisseph as swe
from tqdm import tqdm

# Add project root to path
PROJECT_ROOT = r'd:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5'
sys.path.append(PROJECT_ROOT)

# Corrected Imports based on git ls-files
from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.medini.yogas import YogaScanner
from src.engine.countries.india.logic import IndiaRiskEngine
from src.engine.countries.usa.logic import USARiskEngine
from src.engine.astro.dasha.vimshottari import VimshottariDasha
from src.engine.astro.vargas.calculator import VargaCalculator
from src.engine.astro.ashtakavarga.calculator import AshtakavargaCalculator
from src.engine.astro.chakra.sbc import SarvatobhadraChakra
from src.engine.astro.nakshatra.manager import NakshatraManager
from src.engine.astro.eclipses.manager import EclipseManager
from src.engine.astro.core.declination import DeclinationLogic
from src.engine.astro.planets.uranus.logic import UranusLogic
from src.engine.astro.planets.neptune.logic import NeptuneLogic
from src.engine.astro.planets.pluto.logic import PlutoLogic

def run_tier_audit():
    print("=== ACE v5: Tiered Audit (2010 - 2025) ===")
    
    # 1. Load S&P 500 Daily Data
    csv_path = os.path.join(PROJECT_ROOT, 'data/processed/us_master_daily.csv')
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df.iloc[:, 0], utc=True).dt.tz_localize(None)
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)
    
    # Filter for 2010 - 2025
    df = df[(df.index.year >= 2010) & (df.index.year <= 2025)]
    
    # Calculate Forward Returns (Window-based for Tiered Audit)
    # Tier 1: -5% in 4 weeks
    # Tier 2: -10% in 8 weeks
    # Tier 3: -20% in 12 weeks
    df['Fwd_4w_Max_Drop'] = df['Low'].rolling(window=20).min().shift(-20) # 20 trading days ~ 4 weeks
    df['Fwd_4w_Drop'] = (df['Fwd_4w_Max_Drop'] - df['Close']) / df['Close']
    
    df['Fwd_8w_Max_Drop'] = df['Low'].rolling(window=40).min().shift(-40)
    df['Fwd_8w_Drop'] = (df['Fwd_8w_Max_Drop'] - df['Close']) / df['Close']
    
    df['Fwd_12w_Max_Drop'] = df['Low'].rolling(window=60).min().shift(-60)
    df['Fwd_12w_Drop'] = (df['Fwd_12w_Max_Drop'] - df['Close']) / df['Close']

    # 2. Setup Engines
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    
    scanner = YogaScanner()
    eclipse_manager = EclipseManager()
    uranus_engine = UranusLogic()
    pluto_engine = PlutoLogic()
    dasha_engine = VimshottariDasha()
    varga_calc = VargaCalculator()
    av_calc = AshtakavargaCalculator()
    sbc_engine = SarvatobhadraChakra()
    usa_engine = USARiskEngine()
    nak_manager = NakshatraManager()
    
    usa_moon_natal = 306.5 
    usa_birth_date = pd.to_datetime("1776-07-04")
    
    results = []
    
    print("Calculating Risk Scores for each day...")
    for date, row in tqdm(df.iterrows(), total=len(df)):
        positions = ep.get_all_positions(date)
        
        # Base Score (Yogas + Aspects)
        yogas = scanner.scan_yogas(planet_positions=positions)
        aspects = scanner.check_special_aspects(positions)
        
        yoga_score = 0
        for y in yogas:
            y_s = 0
            if y['Type'] == 'War': y_s = 10
            elif y['Type'] == 'Special Conjunction': y_s = 5
            if 'Intensity' in y: y_s += (y['Intensity'] / 20.0)
            yoga_score += y_s
             
        aspect_score = len(aspects) * 2
        
        # Koorma (Nakshatra-based stress)
        koorma_score = 0
        center_naks = [3, 5, 12, 13, 20, 21] 
        for p in ['Saturn', 'Mars', 'Rahu', 'Ketu']:
            if p not in positions: continue
            nak_idx = int(positions[p] / 13.333333)
            if nak_idx in center_naks:
                koorma_score += 10

        # Outer Planets & Eclipses
        u_s, _ = uranus_engine.check_volatility(positions.get('Uranus', 0))
        p_s, _ = pluto_engine.check_systemic_risk(positions.get('Pluto', 0))
        e_s, _ = eclipse_manager.check_eclipses(date)
        
        base_score = yoga_score + aspect_score + koorma_score + u_s + p_s + e_s
        
        # God Mode Logic
        curr_dasha = dasha_engine.get_current_dasha(usa_moon_natal, usa_birth_date, date)
        md_lord = curr_dasha['Mahadasha']
        ad_lord = curr_dasha['Antardasha']
        
        dasha_score = 0
        malefics = ['Rahu', 'Mars', 'Saturn', 'Ketu']
        if md_lord in malefics and ad_lord in malefics:
            dasha_score = 10
        elif md_lord == 'Jupiter' or ad_lord == 'Jupiter':
             dasha_score = -5
        
        sat_lon = positions.get('Saturn', 0)
        sat_varga = varga_calc.get_varga_strength('Saturn', sat_lon)
        varga_score = 10 if sat_varga['Is_Vargottama'] and sat_varga['D1'] == 'Aries' else 0
        
        sat_bav = av_calc.calculate_bav('Saturn', positions)
        av_score = 10 if sat_bav <= 1 else (-5 if sat_bav >= 6 else 0)
            
        sbc_score, _ = sbc_engine.check_crash_vedha(positions)
        if sbc_score > 0: sbc_score += 5
        
        usa_risk, _ = usa_engine.check_risk(positions)
        
        total_risk = base_score + dasha_score + varga_score + av_score + sbc_score + usa_risk
        
        results.append({
            'Date': date,
            'Risk_Score': total_risk,
            'Fwd_4w_Drop': row['Fwd_4w_Drop'],
            'Fwd_8w_Drop': row['Fwd_8w_Drop'],
            'Fwd_12w_Drop': row['Fwd_12w_Drop']
        })

    res_df = pd.DataFrame(results).set_index('Date')
    res_df.dropna(inplace=True)

    # 3. Metric Calculations (3 Tiers)
    tiers = [
        {"Tier": 1, "Name": "Pulse", "Score_Threshold": 8, "Drop_Threshold": -0.05, "Window": "4w"},
        {"Tier": 2, "Name": "Correction", "Score_Threshold": 18, "Drop_Threshold": -0.10, "Window": "8w"},
        {"Tier": 3, "Name": "Crash", "Score_Threshold": 30, "Drop_Threshold": -0.20, "Window": "12w"}
    ]

    print("\n" + "="*80)
    print(f"ACE v5 AUDIT REPORT: TIERED ACCURACY (2010 - 2025)")
    print("="*80)
    print(f"{'TIER':<15} | {'REAL CRASHES':<15} | {'CAUGHT':<10} | {'ACCURACY':<10} | {'PRECISION':<10}")
    print("-" * 80)

    for t in tiers:
        drop_col = f"Fwd_{t['Window']}_Drop"
        
        # Real crashes: dates where drop happened
        real_crash_mask = (res_df[drop_col] <= t['Drop_Threshold'])
        total_real = len(res_df[real_crash_mask]) # This might count multiple days for same crash
        
        # To avoid over-counting adjacent days as separate crashes, let's group or just use percentages
        # But for "Total Real Crash", let's define it as "Days in crash state" or just count filtered signals.
        # Better: Count unique 30-day windows or similar.
        # Simpler: Just count indices.
        
        signals_mask = (res_df['Risk_Score'] >= t['Score_Threshold'])
        total_signals = len(res_df[signals_mask])
        
        true_positives = len(res_df[signals_mask & real_crash_mask])
        false_positives = total_signals - true_positives
        
        recall = (true_positives / total_real) * 100 if total_real > 0 else 0
        precision = (true_positives / total_signals) * 100 if total_signals > 0 else 0
        
        # For "Accuracy", usually (TP + TN) / Total. 
        total_days = len(res_df)
        true_negatives = len(res_df[~signals_mask & ~real_crash_mask])
        accuracy = ((true_positives + true_negatives) / total_days) * 100
        
        print(f"{t['Name']:<15} | {total_real:<15} | {true_positives:<10} | {accuracy:>8.1f}% | {precision:>8.1f}%")

    print("="*80)
    print("Definition: Accuracy = (True Positives + True Negatives) / Total Days")
    print("Definition: Catch Rate (Recall) is embedded in 'CAUGHT' vs 'REAL'")
    print("-" * 80)

if __name__ == "__main__":
    run_tier_audit()
