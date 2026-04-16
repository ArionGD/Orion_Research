import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime, timedelta
import swisseph as swe

# Root Path
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"
sys.path.append(ROOT)

from src.engine.medini.crash_logic import MundaneWeatherEngine
from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.astro.dasha.vimshottari import VimshottariDasha

def run_live_audit_2026():
    print("=== ACE: LIVE SOVEREIGN AUDIT (FEB 2026 - JUNE 2026) ===")
    
    weather = MundaneWeatherEngine()
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    dasha_eng = VimshottariDasha()
    
    # 1776 SIBLEY NATAL
    MOON = 312.0
    BIRTH = datetime(1776, 7, 4)
    
    csv_path = os.path.join(ROOT, 'data/raw/US/ENERGY_XLE.csv')
    df = pd.read_csv(csv_path, skiprows=2)
    df.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
    df['Date'] = pd.to_datetime(df['Date'], utc=True).dt.tz_localize(None)
    df.set_index('Date', inplace=True)
    
    # Slice the window
    target_start = datetime(2026, 2, 1)
    target_end = datetime(2026, 6, 1)
    
    print(f"Auditing Strike Window: Feb 1 -> June 1, 2026")
    print("-" * 60)
    
    current_date = target_start
    signals = []
    
    while current_date <= target_end:
        d_obj = current_date
        
        # Market Price (if exists)
        price = df.loc[d_obj, 'Close'] if d_obj in df.index else None
        
        # Engine Signal
        pos = ep.get_all_positions(d_obj)
        try:
            dashas = dasha_eng.get_current_dasha(MOON, BIRTH, d_obj)
            ma = dashas['Mahadasha']; an = dashas['Antardasha']
        except:
            ma = 'Jupiter'; an = 'Saturn'
            
        smi = weather.calculate_smi(d_obj, pos, ma, an, market='US')
        # Capricorn Penalty
        if (int(pos.get('Jupiter', 0) // 30) + 1) == 10: smi += 3.5
        
        signals.append({
            'Date': d_obj.date(),
            'SMI': smi,
            'Price': price
        })
        current_date += timedelta(days=1)
        
    report = pd.DataFrame(signals)
    
    # Identify Peaks/Drops in the report
    start_price = report['Price'].dropna().iloc[0] if not report['Price'].dropna().empty else 1
    report['Gain_Loss'] = (report['Price'] - start_price) / start_price * 100
    
    print(f"{'DATE':<12} | {'SMI':<6} | {'PRICE':<8} | {'DROP %':<10} | {'SIGNAL'}")
    print("-" * 60)
    
    for _, row in report.iterrows():
        sig = "STRIKE (T3)" if row['SMI'] >= 7.0 else "WARNING (T2)" if row['SMI'] >= 5.0 else ""
        drop_str = f"{row['Gain_Loss']:.2f}%" if not pd.isna(row['Gain_Loss']) else "FUTURE"
        price_str = f"{row['Price']:.2f}" if not pd.isna(row['Price']) else "---"
        
        # Only show significant dates or signal dates
        if row['SMI'] >= 5.0 or row['Gain_Loss'] < -5.0:
            print(f"{str(row['Date']):<12} | {row['SMI']:<6.1f} | {price_str:<8} | {drop_str:<10} | {sig}")

if __name__ == "__main__":
    run_live_audit_2026()
