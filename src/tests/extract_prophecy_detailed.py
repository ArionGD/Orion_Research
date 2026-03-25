import pandas as pd
from datetime import datetime
import sys
import os

# Set paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.countries.manager import CountryManager
from src.engine.world.translator import ArionTranslator

def extract_quarterly_data():
    ep = EphemerisProvider()
    cm = CountryManager()
    at = ArionTranslator()
    
    # Target dates
    dates = [
        datetime(2026, 2, 1),
        datetime(2026, 3, 1),
        datetime(2026, 4, 1)
    ]
    
    print("# ARION AI: QUARTERLY PROPHECY EXTRACTION (FEB-APR 2026)")
    print("="*60)
    
    for d in dates:
        date_str = d.strftime('%Y-%m-%d')
        print(f"\n### TARGET DATE: {d.strftime('%B %Y')} ({date_str})")
        
        # 1. Get All Positions for this date
        positions = ep.get_all_positions(d)
        
        # 2. Get Global Risk Score (from ArionTranslator/Prophecy CSV)
        global_feats = at.load_features(d)
        global_risk = global_feats.get('Havoc_Score', 0) if global_feats is not None else 0
        gsi = global_feats.get('Global_Stability_Index', 0) if global_feats is not None else 0
        
        print(f"**GLOBAL CONTEXT:**")
        print(f"- Global Stability Index (GSI): {gsi:.1f}")
        print(f"- Universal Havoc Score: {global_risk:.2%}")
        
        # 3. Get USA Risk
        usa_score, usa_signals = cm.check_risk('USA', positions)
        print(f"\n**USA SPECIFIC ANALYSIS:**")
        print(f"- Local Risk Score: {usa_score:.1f}")
        if usa_signals:
            print("- Signals Detected:")
            for s in usa_signals:
                print(f"  * {s}")
        else:
            print("- No significant local natal hits.")
            
        # 4. Get India Risk
        india_score, india_signals = cm.check_risk('India', positions)
        print(f"\n**INDIA SPECIFIC ANALYSIS:**")
        print(f"- Local Risk Score: {india_score:.1f}")
        if india_signals:
            print("- Signals Detected:")
            for s in india_signals:
                print(f"  * {s}")
        else:
            print("- No significant local natal hits.")
        
        print("-" * 30)

if __name__ == "__main__":
    extract_quarterly_data()
