from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.countries.india.logic import IndiaRiskEngine

def forecast_india_it():
    ep = EphemerisProvider()
    engine = IndiaRiskEngine()
    
    dates = [
        datetime(2026, 2, 1), # Feb
        datetime(2026, 2, 15),
        datetime(2026, 3, 1), # March
        datetime(2026, 3, 15),
        datetime(2026, 4, 1), # April
        datetime(2026, 4, 15)
    ]
    
    print("\n# ARION AI: INDIAN IT SECTOR FORECAST (Q1 2026)")
    print("="*60)
    
    for d in dates:
        positions = ep.get_all_positions(d)
        score, signals = engine.check_it_sector_risk(positions)
        
        if positions.get('True_Node'):
             rahu = positions['True_Node']
             print(f"\nRahu Pos: {rahu:.2f}")
             
        if positions.get('Mercury'):
             merc = positions['Mercury']
             print(f"Mercury Pos: {merc:.2f}")

        print(f"\n### {d.strftime('%B %d, %Y')}")
        print(f"IT Opportunity Score: {score} {'(Bullish)' if score > 0 else '(Bearish)'}")
        if signals:
            for s in signals:
                print(f"- {s}")
        else:
            print("- No major specific signals.")
            
if __name__ == "__main__":
    forecast_india_it()
