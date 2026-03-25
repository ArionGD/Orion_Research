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

def run_daily_backtest():
    print("=== Arion.ai Daily Precision Audit (100-Year) ===")
    
    # 1. Load Daily Data (Investable Grade US Master)
    csv_path = 'data/processed/us_master_daily.csv'
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found. Run data_builder.py first.")
        return

    print(f"Loading {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Handle Date Parsing Robustly
    date_col = df.columns[0]
    if date_col == 'Date':
        df[date_col] = pd.to_datetime(df[date_col], utc=True).dt.tz_localize(None)
    else:
        df['Date'] = pd.to_datetime(df.iloc[:, 0], utc=True).dt.tz_localize(None)
        date_col = 'Date'
        
    df.set_index(date_col, inplace=True)
    df.sort_index(inplace=True)
    
    # Filter for valid dates (1928+)
    df = df[df.index.year >= 1928]
    
    print(f"Loaded {len(df)} trading days ({df.index.min().date()} to {df.index.max().date()})")
    
    # Calculate Next Day Return
    df['Next_Day_Close'] = df['Close'].shift(-1)
    df['Next_Day_Return'] = (df['Next_Day_Close'] - df['Close']) / df['Close']
    df.dropna(subset=['Next_Day_Return'], inplace=True)
    
    # 2. Setup Engines
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    
    scanner = YogaScanner()
    nak_manager = NakshatraManager()
    nak_mapper = NakshatraMapper()
    eclipse_manager = EclipseManager()
    decl_logic = DeclinationLogic()
    
    # Planet Engines
    uranus_engine = UranusLogic()
    neptune_engine = NeptuneLogic()
    pluto_engine = PlutoLogic()
    chiron_engine = ChironLogic()
    algol_engine = AlgolLogic()
    usa_engine = USARiskEngine()
    
    results = []
    
    print("Scanning Daily Transits (This may take 2-3 mins)...")
    
    for date, row in tqdm(df.iterrows(), total=len(df)):
        # --- Optimized Daily Risk Calculation ---
        
        # A. Positions (Daily)
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
             yoga_score += y_s
             
        aspect_score = len(aspects) 
        
        # C. Eclipse (Check if eclipse happens TODAY or very close)
        ecl_score, ecl_signals = eclipse_manager.check_eclipses(date)
        
        # D. Outer Planets (Slow moving, but check exact hits)
        u_s, u_sig = uranus_engine.check_volatility(ep.get_planet_data(date, 'Uranus')[1])
        n_s, n_sig = neptune_engine.check_bubble_risk(ep.get_planet_data(date, 'Neptune')[1], [])
        p_s, p_sig = pluto_engine.check_systemic_risk(ep.get_planet_data(date, 'Pluto')[1])
        
        # E. Koorma (Sensitive Points)
        koorma_score = 0
        koorma_signals = []
        for p in ['Saturn', 'Mars', 'Rahu', 'Ketu']:
            lon = positions.get(p)
            if lon:
                nd = nak_mapper.get_nakshatra(lon)
                if nd and nd['direction'] == 'Center':
                    koorma_score += 5 if p == 'Saturn' else 3
                    koorma_signals.append(f"Koorma: {p} in Center")
                    
        # F. USA Risk (Specific to US Market)
        usa_score, usa_sig = usa_engine.check_risk(positions)
        
        # Total Base Risk
        base_risk = yoga_score + aspect_score + ecl_score + koorma_score + u_s + n_s + p_s + usa_score
        
        # G. Multipliers
        # Mars OOB
        m_decl = ep.get_declination(date, 'Mars')
        m_oob_mult = decl_logic.get_oob_score('Mars', m_decl)
        
        final_risk = base_risk * m_oob_mult
        
        # Signal Strings for Report
        sigs = []
        if usa_score > 0: sigs.extend(usa_sig)
        if u_s > 0: sigs.extend(u_sig)
        if p_s > 0: sigs.extend(p_sig)
        if koorma_score > 0: sigs.extend(koorma_signals)
        if ecl_score > 0: sigs.extend(ecl_signals)
        if m_oob_mult > 1: sigs.append("Mars OOB")
        if yoga_score > 15: sigs.append("Major Planetary War/Cluster")
        
        results.append({
            'Date': date,
            'Risk_Score': final_risk,
            'Return': df.loc[date, 'Next_Day_Return'],
            'Signals': ", ".join(sigs)
        })
        
    res_df = pd.DataFrame(results)
    res_df['Is_Crash'] = (res_df['Return'] < -0.03).astype(int) # -3% in a single day is a crash
    
    # 3. Report Generation
    print("Generating Daily Report...")
    with open("daily_precision_report.md", "w", encoding="utf-8") as f:
        f.write("# Arion.ai Daily Precision Report (100-Year Audit)\n")
        f.write("**Data Source:** S&P 500 Daily (Investable Grade)\n\n")
        
        # A. 1929 Great Crash (Oct 24 - Black Thursday)
        f.write("## 1. The 1929 Crash (The Daily Test)\n")
        f.write("| Date | Market Return | Score | Signals |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        
        crash_1929 = res_df[(res_df['Date'] >= '1929-10-20') & (res_df['Date'] <= '1929-10-31')]
        for _, row in crash_1929.iterrows():
            day_name = row['Date'].strftime('%A')
            f.write(f"| {row['Date'].strftime('%Y-%m-%d')} ({day_name}) | **{row['Return']:.2%}** | {row['Risk_Score']:.1f} | {row['Signals']} |\n")
            
        f.write("\n")
        
        # B. 1987 Black Monday (Oct 19)
        f.write("## 2. 1987 Black Monday (Oct 19)\n")
        f.write("| Date | Return | Score | Signals |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        crash_1987 = res_df[(res_df['Date'] >= '1987-10-14') & (res_df['Date'] <= '1987-10-23')]
        for _, row in crash_1987.iterrows():
             f.write(f"| {row['Date'].strftime('%Y-%m-%d')} | **{row['Return']:.2%}** | {row['Risk_Score']:.1f} | {row['Signals']} |\n")
             
        f.write("\n")
        
        # C. 2008 Financial Crisis (Lehman Moment - Sept)
        f.write("## 3. 2008 Financial Crisis (Sept 29 Drop)\n")
        f.write("| Date | Return | Score | Signals |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        crash_2008 = res_df[(res_df['Date'] >= '2008-09-25') & (res_df['Date'] <= '2008-10-05')]
        for _, row in crash_2008.iterrows():
             f.write(f"| {row['Date'].strftime('%Y-%m-%d')} | **{row['Return']:.2%}** | {row['Risk_Score']:.1f} | {row['Signals']} |\n")
             
        f.write("\n")
        
        # D. 2020 Covid Crash (March)
        f.write("## 4. 2020 Covid Crash (March 12/16)\n")
        f.write("| Date | Return | Score | Signals |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        crash_2020 = res_df[(res_df['Date'] >= '2020-03-09') & (res_df['Date'] <= '2020-03-20')]
        for _, row in crash_2020.iterrows():
             f.write(f"| {row['Date'].strftime('%Y-%m-%d')} | **{row['Return']:.2%}** | {row['Risk_Score']:.1f} | {row['Signals']} |\n")

        # Stats
        f.write("\n## 5. Daily Accuracy Stats\n")
        total_crashes = len(res_df[res_df['Return'] < -0.03]) # Days with -3% or worse
        caught = len(res_df[(res_df['Return'] < -0.03) & (res_df['Risk_Score'] >= 10)])
        
        f.write(f"- Total 'Crash Days' (-3%+): {total_crashes}\n")
        f.write(f"- Accurately Flagged (Score >= 10): {caught}\n")
        if total_crashes > 0:
            f.write(f"- **Daily Crash Recall:** {caught/total_crashes:.1%}\n")
            
    print("Daily Report Generated: daily_precision_report.md")

if __name__ == "__main__":
    run_daily_backtest()
