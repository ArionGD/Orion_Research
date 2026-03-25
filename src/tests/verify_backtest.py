from src.engine.medini.synthesizer import MediniSynthesizer
from datetime import datetime

def run_backtest():
    print("=== Arion.ai Phase 4: Historical Backtest & Verification ===\n")
    synth = MediniSynthesizer()
    
    # 1. COVID Crash (March 20, 2020)
    # Expectation: Mars conjunct Saturn/Pluto/Jupiter in Capricorn
    date_covid = datetime(2020, 3, 20)
    print(f"📅 TEST CASE 1: COVID CRASH PEAK ({date_covid.date()})")
    print("-" * 50)
    print(synth.generate_medini_report(date_covid))
    print("\n")
    
    # 2. 2008 Financial Crisis (Lehman - Sept 15, 2008)
    date_lehman = datetime(2008, 9, 15)
    print(f"📅 TEST CASE 2: LEHMAN BROTHERS COLLAPSE ({date_lehman.date()})")
    print("-" * 50)
    print(synth.generate_medini_report(date_lehman))
    print("\n")

    # 3. Known Eclipse (April 8, 2024)
    # Expectation: Solar Eclipse
    date_eclipse = datetime(2024, 4, 8, 19, 0)
    print(f"📅 TEST CASE 3: TOTAL SOLAR ECLIPSE ({date_eclipse.date()})")
    print("-" * 50)
    print(synth.generate_medini_report(date_eclipse))
    print("\n")

if __name__ == "__main__":
    run_backtest()
