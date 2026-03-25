import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pandas as pd
import numpy as np
from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.medini.yogas import YogaScanner
from src.engine.medini.temporal import TemporalScanner
import swisseph as swe
# Logic Imports
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
from src.engine.nakshatra.mapper import NakshatraMapper
from src.engine.eclipses.manager import EclipseManager
from src.engine.astro.core.declination import DeclinationLogic
from src.engine.planets.uranus.logic import UranusLogic
from src.engine.planets.neptune.logic import NeptuneLogic
from src.engine.planets.pluto.logic import PlutoLogic
from src.engine.asteroids.chiron.logic import ChironLogic
from src.engine.stars.algol.logic import AlgolLogic
from src.engine.countries.usa.logic import USARiskEngine
from tqdm import tqdm

def run_weekly_backtest():
    print("=== Arion.ai Weekly Precision Audit (1928-2026) ===")
    
    # 1. Load Weekly Data
    csv_path = 'data/raw/sp500_weekly_full.csv'
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: {csv_path} not found.")
        return

    # Convert Date (Expect yfinance format with timezone)
    date_col = df.columns[0]
    # Ensure it's treated as a column, not index if read_csv did something smart
    if date_col == 'Date':
        df[date_col] = pd.to_datetime(df[date_col], utc=True).dt.tz_localize(None)
    else:
        # Fallback if structure is different
        df['Date'] = pd.to_datetime(df.iloc[:, 0], utc=True).dt.tz_localize(None)
        date_col = 'Date'
        
    df.set_index(date_col, inplace=True)
    df.sort_index(inplace=True)
    
    print(f"Loaded {len(df)} weeks of data ({df.index.min().date()} to {df.index.max().date()})")
    
    # Calculate Next Week Return
    df['Next_Week_Close'] = df['Close'].shift(-1)
    df['Next_Week_Return'] = (df['Next_Week_Close'] - df['Close']) / df['Close']
    df.dropna(subset=['Next_Week_Return'], inplace=True)
    
    # 2. Setup Engines
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    
    scanner = YogaScanner()
    nak_manager = NakshatraManager()
    nak_mapper = NakshatraMapper()
    eclipse_manager = EclipseManager()
    decl_logic = DeclinationLogic()
    
    uranus_engine = UranusLogic()
    neptune_engine = NeptuneLogic()
    pluto_engine = PlutoLogic()
    chiron_engine = ChironLogic()
    algol_engine = AlgolLogic()
    usa_engine = USARiskEngine()
    
    results = []
    
    print("Scanning Weekly Transits...")
    
    for date, row in tqdm(df.iterrows(), total=len(df)):
        # --- Risk Calculation Logic (Same as Monthly but on Weekly Dates) ---
        
        # A. Positions
        positions = ep.get_all_positions(date)
        
        # B. Yogas & Aspects
        yogas = scanner.scan_yogas(planet_positions=positions)
        aspects = scanner.check_special_aspects(positions)
        
        yoga_score = 0
        for y in yogas:
             y_s = 0
             if y['Type'] == 'War': y_s = 10
             elif y['Type'] == 'Special Conjunction': y_s = 5
             if 'Intensity' in y: y_s += (y['Intensity'] / 20.0)
             y['score'] = y_s
             yoga_score += y_s
             
        aspect_score = len(aspects) # Simplified for speed
        
        # C. Nakshatra
        nak_stress, _ = nak_manager.get_aggregated_stress(positions)
        
        # D. Eclipse (Check if eclipse happens THIS week)
        ecl_score, ecl_signals = eclipse_manager.check_eclipses(date)
        
        # E. Outer Planets
        u_s, u_sig = uranus_engine.check_volatility(ep.get_planet_data(date, 'Uranus')[1])
        n_s, n_sig = neptune_engine.check_bubble_risk(ep.get_planet_data(date, 'Neptune')[1], [])
        p_s, p_sig = pluto_engine.check_systemic_risk(ep.get_planet_data(date, 'Pluto')[1])
        c_s, c_sig = chiron_engine.check_turnaround(ep.get_planet_data(date, 'Chiron')[1])
        
        # F. Koorma
        koorma_score = 0
        koorma_signals = []
        for p in ['Saturn', 'Mars', 'Rahu', 'Ketu']:
            lon = positions.get(p)
            if lon:
                nd = nak_mapper.get_nakshatra(lon)
                if nd and nd['direction'] == 'Center':
                    koorma_score += 5 if p == 'Saturn' else 3
                    koorma_signals.append(f"Koorma: {p} in Center")
                    
        # G. Algol
        alg_score = 0
        algols = ep.get_fixed_star("Algol", date)
        if algols[0]:
            for p in ['Mars', 'Saturn']:
                s, sig = algol_engine.check_conjunction(positions.get(p), p, algols[0])
                if s > 0:
                    alg_score += s
                    
        # H. USA Risk
        usa_score, usa_sig = usa_engine.check_risk(positions)
        
        # Total Base Risk
        base_risk = yoga_score + aspect_score + nak_stress + ecl_score + koorma_score + u_s + n_s + p_s + alg_score + usa_score
        
        if c_s > 0: base_risk -= 2 # Turnaround reduces risk
        
        # I. Mars OOB Multiplier
        m_decl = ep.get_declination(date, 'Mars')
        m_oob_mult = decl_logic.get_oob_score('Mars', m_decl)
        
        final_risk = base_risk * m_oob_mult
        
        # Collect Signals string
        sigs = []
        if usa_score > 0: sigs.extend(usa_sig)
        if u_s > 0: sigs.extend(u_sig)
        if p_s > 0: sigs.extend(p_sig)
        if koorma_score > 0: sigs.extend(koorma_signals)
        if ecl_score > 0: sigs.extend(ecl_signals)
        if m_oob_mult > 1: sigs.append("Mars OOB")
        
        results.append({
            'Date': date,
            'Risk_Score': final_risk,
            'Return': df.loc[date, 'Next_Week_Return'],
            'Signals': ", ".join(sigs)
        })
        
    res_df = pd.DataFrame(results)
    res_df['Is_Crash'] = (res_df['Return'] < -0.04).astype(int) # -4% in a week is huge
    
    # Report Generation
    with open("weekly_precision_report.md", "w", encoding="utf-8") as f:
        f.write("# Arion.ai Weekly Precision Report (1928-2026)\n")
        f.write("**Data Source:** S&P 500 Daily (Aggregated to Weekly)\n\n")
        
        # 1. 1929 Crash Analysis
        f.write("## 1. The 1929 Crash: Weekly Breakdown\n")
        f.write("Did we catch the specific week of Oct 24, 1929?\n\n")
        f.write("| Week Starting | Market Return | Score | Signals |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        
        crash_1929 = res_df[(res_df['Date'] >= '1929-10-01') & (res_df['Date'] <= '1929-11-30')]
        for _, row in crash_1929.iterrows():
            f.write(f"| {row['Date'].strftime('%Y-%m-%d')} | {row['Return']:.2%} | {row['Risk_Score']:.1f} | {row['Signals']} |\n")
            
        f.write("\n")
        
        # 2. 1987 Black Monday
        f.write("## 2. 1987 Black Monday (Oct 19)\n")
        crash_1987 = res_df[(res_df['Date'] >= '1987-10-01') & (res_df['Date'] <= '1987-10-31')]
        f.write("| Week Starting | Market Return | Score | Signals |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        for _, row in crash_1987.iterrows():
             f.write(f"| {row['Date'].strftime('%Y-%m-%d')} | {row['Return']:.2%} | {row['Risk_Score']:.1f} | {row['Signals']} |\n")
             
        f.write("\n")
        
        # 3. Overall Stats
        f.write("## 3. Weekly Accuracy Stats\n")
        total_crashes = len(res_df[res_df['Is_Crash'] == 1])
        caught = len(res_df[(res_df['Is_Crash'] == 1) & (res_df['Risk_Score'] >= 12)])
        recall = caught / total_crashes if total_crashes > 0 else 0
        
        f.write(f"- Total Weekly Crashes (Drop > 4%): {total_crashes}\n")
        f.write(f"- Caught with High Risk Score (Tier 4): {caught}\n")
        f.write(f"- **Weekly Recall:** {recall:.1%}\n")
        
    print("Weekly report generated: weekly_precision_report.md")

if __name__ == "__main__":
    run_weekly_backtest()
