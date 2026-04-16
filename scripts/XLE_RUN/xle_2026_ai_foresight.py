import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime, timedelta
import swisseph as swe
from sklearn.tree import DecisionTreeClassifier

# Root Path
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"
sys.path.append(ROOT)

from src.engine.medini.crash_logic import MundaneWeatherEngine
from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.astro.dasha.vimshottari import VimshottariDasha

def get_aspect(d1, d2, orb=10):
    diff = abs(d1 - d2) % 360
    if diff > 180: diff = 360 - diff
    if diff <= orb: return 1 
    if abs(diff - 180) <= orb: return 2 
    if abs(diff - 90) <= orb: return 3 
    return 0

def run_2026_fast_foresight():
    print("=== ACE: 2026 SOVEREIGN AI FORESIGHT (HIGH-SPEED DTE) ===")
    
    master_path = os.path.join(ROOT, 'data/enriched/US/ENERGY_MasterV70.csv')
    df = pd.read_csv(master_path)
    
    # 1. Future Dates Enrichment (Simplified)
    ep = EphemerisProvider(); d_eng = VimshottariDasha(); weather = MundaneWeatherEngine()
    future_data = []
    print("Enriching 2026 Future Scan...")
    for i in range(365):
        d = datetime(2026, 1, 1) + timedelta(days=i)
        pos = ep.get_all_positions(d)
        try: dasha = d_eng.get_current_dasha(312.0, datetime(1776, 7, 4), d)
        except: dasha={'Mahadasha':'Mars', 'Antardasha':'Saturn'}
        sun=pos.get('Sun',0); moon=pos.get('Moon',0)
        entry = {
            'Date': d, 'Mahadasha': dasha['Mahadasha'], 'Antardasha': dasha['Antardasha'],
            'SMI_Base': weather.calculate_smi(d, pos, dasha['Mahadasha'], dasha['Antardasha'], market='US'),
            'Tithi': int(((moon - sun) % 360) // 12) + 1,
            'Nakshatra': int(moon // (360/27)) + 1,
            'Nithya_Yoga': int(((sun + moon) % 360) // (360/27)) + 1,
            'Aspect_Mars_Saturn': get_aspect(pos.get('Mars', 0), pos.get('Saturn', 0)),
            'Aspect_Jup_Sun': get_aspect(pos.get('Jupiter', 0), pos.get('Sun', 0)),
            'Aspect_Rahu_Mars': get_aspect(pos.get('True_Node', 0), pos.get('Mars', 0)),
            'Vedha_Score': (1 if pos.get('Mars',0)%30 < 2 else 0) + (1 if pos.get('Saturn',0)%30 < 2 else 0)
        }
        for p, deg in pos.items():
            entry[f"{p}_Deg"] = deg
            entry[f"{p}_Speed"] = ep.get_planet_data(d, p)[1]
        future_data.append(entry)
        
    f_df = pd.DataFrame(future_data)
    
    # 2. Training for Tiers
    def predict_tier(threshold):
        df['Is_Drop'] = (df['Close'].shift(-30).rolling(30).min() / df['Close'] - 1 <= threshold).astype(int)
        X_train_full = pd.get_dummies(df, columns=['Mahadasha', 'Antardasha'])
        exclude = ['Date', 'Close', 'Is_Drop', 'Forward_Min', 'Future_DD', 'Is_Crash', 'Signal', 'Prob', 'Mahadasha', 'Antardasha']
        X_t = X_train_full.drop(columns=[c for c in exclude if c in X_train_full.columns]).fillna(0)
        
        X_f = pd.get_dummies(f_df, columns=['Mahadasha', 'Antardasha'])
        for c in X_t.columns: 
            if c not in X_f.columns: X_f[c] = 0
        X_f = X_f[X_t.columns]

        dt = DecisionTreeClassifier(max_depth=6, class_weight='balanced')
        dt.fit(X_t, df['Is_Drop'])
        return dt.predict_proba(X_f.fillna(0))[:, 1]

    print("Analyzing Tier 1 (-5%) & Tier 2 (-10%) Pulses...")
    f_df['Prob_T1'] = predict_tier(-0.05)
    f_df['Prob_T2'] = predict_tier(-0.10)
    
    print("\n" + "="*70)
    print("2026 SOVEREIGN AI ROADMAP (ALL TIERS)")
    print("="*70)
    
    res = f_df[(f_df['Prob_T1'] > 0.75) | (f_df['Prob_T2'] > 0.75)]
    if res.empty:
        print("The AI detects no high-confidence historical matches in 2026.")
    else:
        # Group by week to avoid spam
        res['Week'] = res['Date'].dt.to_period('W')
        summary = res.groupby('Week').first()
        for d, row in summary.iterrows():
            status = "RESISTANCE BREAK" if row['Prob_T2'] > 0.75 else "VIBRATION"
            print(f"WEEK: {row['Date'].strftime('%Y-%W')} | PROB: {max(row['Prob_T1'], row['Prob_T2']):.0%} | [{status}]")
    print("="*70)

if __name__ == "__main__":
    run_2026_fast_foresight()
