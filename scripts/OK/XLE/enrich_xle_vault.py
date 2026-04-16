import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
import swisseph as swe

# Root Path
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"
sys.path.append(ROOT)

from src.engine.astro.core.ephemeris_provider import EphemerisProvider

def enrich_dataset():
    print("=== ACE: ENRICHING SOVEREIGN VAULT (XLE ENERGY) ===")
    
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    
    input_path = os.path.join(ROOT, 'data/raw/US/ENERGY_XLE.csv')
    output_dir = os.path.join(ROOT, 'data/enriched/US')
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    output_path = os.path.join(output_dir, 'ENERGY_XLE_ENRICHED.csv')
    
    # Load correctly
    df = pd.read_csv(input_path, skiprows=2)
    df.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
    df['Date'] = pd.to_datetime(df['Date'], utc=True).dt.tz_localize(None)
    
    print(f"Processing {len(df)} days of Space-Time mapping...")
    
    planets = {
        'Sun': swe.SUN, 'Moon': swe.MOON, 'Mars': swe.MARS, 
        'Mercury': swe.MERCURY, 'Jupiter': swe.JUPITER, 
        'Venus': swe.VENUS, 'Saturn': swe.SATURN, 
        'Rahu': swe.MEAN_NODE
    }
    
    enriched_rows = []
    
    for _, row in df.iterrows():
        d = row['Date'].to_pydatetime()
        pos_data = {'Date': row['Date'], 'Close': row['Close']}
        
        for p_name, p_const in planets.items():
            res, _ = swe.calc_ut(swe.julday(d.year, d.month, d.day, d.hour), p_const)
            pos_data[f'{p_name}_Deg'] = res[0]
            pos_data[f'{p_name}_Speed'] = res[3]
            
        # Add Ketu (Rahu + 180)
        pos_data['Ketu_Deg'] = (pos_data['Rahu_Deg'] + 180) % 360
        enriched_rows.append(pos_data)
        
    enriched_df = pd.DataFrame(enriched_rows)
    enriched_df.to_csv(output_path, index=False)
    print(f"\n[SUCCESS] Enriched Vault Created: {output_path}")

if __name__ == "__main__":
    enrich_dataset()
