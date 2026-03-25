from datetime import datetime
import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.corporate.risk_engine import CorporateRiskEngine

def analyze_legacy_vs_newage():
    ep = EphemerisProvider()
    cre = CorporateRiskEngine()
    
    # Target Date: March 1, 2026 (Mid Q1)
    target_date = datetime(2026, 3, 1)
    transit_pos = ep.get_all_positions(target_date)
    
    companies = [
        # Legacy Giants
        {"name": "TCS", "date": datetime(1968, 4, 1), "type": "Legacy"},
        {"name": "Infosys", "date": datetime(1981, 7, 2), "type": "Legacy"},
        {"name": "Wipro", "date": datetime(1945, 12, 29), "type": "Legacy"},
        {"name": "HCL Tech", "date": datetime(1991, 11, 12), "type": "Legacy"},
        
        # New Age / Mid-Cap / AI Focus
        {"name": "Affle India", "date": datetime(1994, 8, 18), "type": "New Age"},
        {"name": "Happiest Minds", "date": datetime(2011, 3, 30), "type": "New Age"},
        {"name": "Saksoft", "date": datetime(1999, 11, 24), "type": "New Age"},
        {"name": "Persistent Sys", "date": datetime(1990, 5, 30), "type": "New Age"}
    ]
    
    print(f"# ARION AI: CORPORATE TRANSIT SCAN (target: {target_date.strftime('%Y-%m-%d')})")
    print("="*70)
    print(f"{'COMPANY':<20} | {'TYPE':<10} | {'SCORE':<5} | {'SIGNALS'}")
    print("-" * 70)
    
    for c in companies:
        score, signals = cre.check_company_risk(c['name'], c['date'], transit_pos)
        
        # Formatting output
        sig_str = ", ".join(signals) if signals else "Neutral"
        print(f"{c['name']:<20} | {c['type']:<10} | {score:<5} | {sig_str}")
        print("-" * 70)

if __name__ == "__main__":
    analyze_legacy_vs_newage()
