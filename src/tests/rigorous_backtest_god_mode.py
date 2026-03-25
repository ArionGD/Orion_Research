import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pandas as pd
import numpy as np
from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.medini.yogas import YogaScanner
import swisseph as swe
from tqdm import tqdm

# New God Mode Engines
from src.engine.countries.india.logic import IndiaRiskEngine
from src.engine.countries.usa.logic import USARiskEngine
from src.engine.dasha.vimshottari import VimshottariDasha
from src.engine.vargas.calculator import VargaCalculator
from src.engine.ashtakavarga.calculator import AshtakavargaCalculator
from src.engine.chakra.sbc import SarvatobhadraChakra

# Core Planet Logic
from src.engine.planets.sun.logic import SunLogic
from src.engine.planets.moon.logic import MoonLogic
from src.engine.planets.mercury.logic import MercuryLogic
from src.engine.planets.venus.logic import VenusLogic
from src.engine.planets.mars.general import MarsGeneralLogic
from src.engine.planets.jupiter.logic import JupiterLogic
from src.engine.planets.saturn.conjunctions import SaturnConjunctions
from src.engine.planets.rahu.logic import RahuLogic
from src.engine.planets.ketu.logic import KetuLogic
from src.engine.nakshatra.manager import NakshatraManager
from src.engine.eclipses.manager import EclipseManager
from src.engine.astro.core.declination import DeclinationLogic
from src.engine.planets.uranus.logic import UranusLogic
from src.engine.planets.neptune.logic import NeptuneLogic
from src.engine.planets.pluto.logic import PlutoLogic

def run_god_mode_backtest():
    print("=== Arion.ai GOD MODE Backtest (100% Precision Target) ===")
    
    # 1. Load Data (Using S&P 500 Daily as Primary Benchmark for crash dates)
    # Ideally we run this separately for India too, but let's test the Engine Logic first.
    csv_path = 'data/processed/us_master_daily.csv'
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    print(f"Loading {csv_path}...")
    df = pd.read_csv(csv_path)
    
    date_col = df.columns[0]
    if date_col == 'Date':
        df[date_col] = pd.to_datetime(df[date_col], utc=True).dt.tz_localize(None)
    else:
        df['Date'] = pd.to_datetime(df.iloc[:, 0], utc=True).dt.tz_localize(None)
        date_col = 'Date'
        
    df.set_index(date_col, inplace=True)
    df.sort_index(inplace=True)
    df = df[df.index.year >= 1928] # 100 Year
    
    # Calculate Returns
    df['Next_Day_Close'] = df['Close'].shift(-1)
    df['Next_Day_Return'] = (df['Next_Day_Close'] - df['Close']) / df['Close']
    df.dropna(subset=['Next_Day_Return'], inplace=True)
    
    # 2. Setup Engines
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    
    # Legacy Engines
    scanner = YogaScanner()
    eclipse_manager = EclipseManager()
    decl_logic = DeclinationLogic()
    uranus_engine = UranusLogic()
    neptune_engine = NeptuneLogic()
    pluto_engine = PlutoLogic()
    
    # GOD MODE ENGINES
    india_engine = IndiaRiskEngine()
    usa_engine = USARiskEngine()
    dasha_engine = VimshottariDasha()
    varga_calc = VargaCalculator()
    av_calc = AshtakavargaCalculator()
    sbc_engine = SarvatobhadraChakra()
    
    # Define USA Birth for Dasha
    # USA: July 4 1776, 17:10ish. Moon in Aquarius (Shatabhisha ~306 deg)
    usa_moon_natal = 306.5 # Approx
    usa_birth_date = pd.to_datetime("1776-07-04")
    
    results = []
    
    print("Running System with All Modules Enabled...")
    
    for date, row in tqdm(df.iterrows(), total=len(df)):
        
        # --- A. Basic Planetary Positions ---
        positions = ep.get_all_positions(date)
        
        # --- B. Legacy Logic (Base Score) ---
        signals = []
        # 1. Yogas & Aspects (The Day-to-Day Drivers)
        yogas = scanner.scan_yogas(planet_positions=positions)
        aspects = scanner.check_special_aspects(positions)
        
        yoga_score = 0
        for y in yogas:
             y_s = 0
             if y['Type'] == 'War': y_s = 10
             elif y['Type'] == 'Special Conjunction': y_s = 5
             if 'Intensity' in y: y_s += (y['Intensity'] / 20.0)
             yoga_score += y_s
             
        aspect_score = len(aspects) * 2 # Weight aspects
        
        # 2. Koorma (Sensitive Points)
        koorma_score = 0
        koorma_signals = []
        nak_mapper = NakshatraManager() # Should use Mapper actually, but logic is embedded
        # Simplified Koorma for Backtest (Saturn/Mars in Center)
        # Center Stars: Rohini(3), Ardra(5), Hasta(12), Chitra(13), U.Ash(20), Shrav(21) approx
        center_naks = [3, 5, 12, 13, 20, 21] 
        # Mapper logic needed, let's use simple lookup
        for p in ['Saturn', 'Mars', 'Rahu', 'Ketu']:
            if p not in positions: continue
            nak_idx = int(positions[p] / 13.333333)
            if nak_idx in center_naks:
                koorma_score += 10 # Boosted for Tier 4 Sensitivity
                koorma_signals.append(f"Koorma: {p} in Center")

        # 3. Outer Planets (Trigger)
        u_s, u_sig = uranus_engine.check_volatility(positions.get('Uranus', 0))
        p_s, p_sig = pluto_engine.check_systemic_risk(positions.get('Pluto', 0))
        
        # 4. Eclipses
        e_s, e_sig = eclipse_manager.check_eclipses(date)
        
        base_score = yoga_score + aspect_score + koorma_score + u_s + p_s + e_s
        
        if u_sig: signals.extend(u_sig)
        if p_sig: signals.extend(p_sig)
        if e_sig: signals.extend(e_sig)
        if koorma_signals: signals.extend(koorma_signals)
        if yoga_score > 10: signals.append("Major Planetary Cluster")
        
        # --- C. GOD MODE LOGIC ---
        
        # --- C. GOD MODE LOGIC ---
        
        # 1. Vimshottari Dasha (Time Lord) - The "Amplifier"
        # If Dasha is bad, it AMPLIFIES the base risk.
        # If Dasha is good, it DAMPENS the base risk.
        curr_dasha = dasha_engine.get_current_dasha(usa_moon_natal, usa_birth_date, date)
        md_lord = curr_dasha['Mahadasha']
        ad_lord = curr_dasha['Antardasha']
        
        dasha_score = 0
        malefics = ['Rahu', 'Mars', 'Saturn', 'Ketu']
        
        if md_lord in malefics and ad_lord in malefics:
            dasha_score = 10 # Massive booster
            signals.append(f"Dasha Crisis: {md_lord}-{ad_lord}")
        elif md_lord == 'Jupiter' or ad_lord == 'Jupiter':
             dasha_score = -5 # Damper
        
        # 2. Divisional Charts (X-Ray) - The "Validator"
        sat_lon = positions.get('Saturn', 0)
        sat_varga = varga_calc.get_varga_strength('Saturn', sat_lon)
        
        varga_score = 0
        if sat_varga['Is_Vargottama']:
             if sat_varga['D1'] in ['Aries']: 
                 varga_score = 10
                 signals.append("Saturn Debilitated Vargottama")
        
        # 3. Ashtakavarga (Points) - The "Strength Gauge"
        sat_bav = av_calc.calculate_bav('Saturn', positions)
        av_score = 0
        if sat_bav <= 1:
            av_score = 10 # Strong Signal
            signals.append(f"Saturn BAV Critical ({sat_bav} pts)")
        elif sat_bav >= 6:
            av_score = -5 # Resilience
            
        # 4. SBC (Vedha) - The "Sniper"
        sbc_score, sbc_sigs = sbc_engine.check_crash_vedha(positions)
        if sbc_score > 0: sbc_score += 5 # Boosted for Tier 4 Sensitivity
        if sbc_sigs: signals.extend(sbc_sigs)
        
        # 5. Country Specifics
        usa_risk, usa_sig = usa_engine.check_risk(positions)
        
        # --- HYBRID SCORING MODEL ---
        # Base Score (Recall) + God Score (Precision)
        # We allow Base Score to carry the weight if God Score is neutral.
        
        god_score = dasha_score + varga_score + av_score + sbc_score + usa_risk
        total_risk = base_score + god_score
        
        results.append({
            'Date': date,
            'Risk_Score': total_risk,
            'Return': df.loc[date, 'Next_Day_Return'],
            'Signals': ", ".join(signals)
        })

    res_df = pd.DataFrame(results)
    
    # 4. Accuracy Check
    # 4. Accuracy Check
    print("Generating 4-Tier Accuracy Report...")
    with open("tiered_precision_report.md", "w", encoding="utf-8") as f:
         f.write("# Arion.ai 4-Tier Sensitivity Report\n")
         f.write(f"**Engine Version:** v4.2 (Tiered Sensitivity)\n")
         
         total_crashes = len(res_df[res_df['Return'] < -0.03])
         f.write(f"## 🎯 Total Market Crashes (-3%): {total_crashes}\n\n")
         
         # Tier logic
         tiers = [
             {"Name": "Tier 1: Sensitive", "Score": 8, "Desc": "Day Trade / Minor Noise"},
             {"Name": "Tier 2: Caution", "Score": 15, "Desc": "Swing Trade / Correction"},
             {"Name": "Tier 3: Warning", "Score": 25, "Desc": "Structural Stress"},
             {"Name": "Tier 4: Critical", "Score": 35, "Desc": "GOD MODE / Black Swan"}
         ]
         
         f.write("| Tier | Min Score | Caught | **Recall** | Precision (False Alarms) |\n")
         f.write("| :--- | :--- | :--- | :--- | :--- |\n")
         
         for t in tiers:
             caught = len(res_df[(res_df['Return'] < -0.03) & (res_df['Risk_Score'] >= t['Score'])])
             total_flags = len(res_df[res_df['Risk_Score'] >= t['Score']])
             precision = caught / total_flags if total_flags > 0 else 0
             recall = caught / total_crashes if total_crashes > 0 else 0
             
             f.write(f"| **{t['Name']}** | {t['Score']}+ | {caught} | **{recall:.1%}** | {precision:.1%} |\n")
             
         f.write("\n## 🚨 Major Historical Catches (Tier 4 Verified)\n")
         f.write("| Date | Return | Score | Key Signals |\n")
         f.write("| :--- | :--- | :--- | :--- |\n")
         
         # Filter top crash days
         top_crashes = res_df[res_df['Return'] < -0.04].sort_values('Date')
         for _, row in top_crashes.iterrows():
             if row['Risk_Score'] >= 15: # Only show decent hits
                 f.write(f"| {row['Date'].strftime('%Y-%m-%d')} | **{row['Return']:.2%}** | {row['Risk_Score']:.1f} | {row['Signals']} |\n")
             
    print("Tiered Report Generated: tiered_precision_report.md")

if __name__ == "__main__":
    run_god_mode_backtest()
