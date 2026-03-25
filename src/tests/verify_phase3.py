from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.medini.temporal import TemporalScanner
from src.engine.astro.core.zodiac import ZodiacUtility
from datetime import datetime, timedelta
import swisseph as swe

def verify_medini_phase3():
    print("=== Arion.ai Phase 3 Verification: Temporal Scanner ===")
    
    # 1. Setup Provider (Sidereal)
    ep = EphemerisProvider()
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    scanner = TemporalScanner()
    scanner.set_sidereal_mode(swe.SIDM_LAHIRI)
    
    # 2. Test Case: Known Total Solar Eclipse (April 8, 2024)
    eclipse_date = datetime(2024, 4, 8, 18, 0, 0) # UTC approx
    print(f"\n🌑 Testing Known Eclipse Date: {eclipse_date.strftime('%Y-%m-%d')}")
    
    events = scanner.scan_temporal_events(eclipse_date)
    found = False
    for e in events:
        print(f"  ✅ Detected: {e['Type']} (Node Dist: {e['Node_Distance']}°) Axis: {e['Axis']}")
        found = True
        
    if not found:
        print("  ❌ Failed to detect April 8 2024 Eclipse!")

    # 3. Test Case: Sun Ingress (Sankranti) - Mid Jan to Mid Feb
    # Sun enters Capricorn ~Jan 14 (Sidereal/Makar Sankranti)
    d1 = datetime(2024, 1, 10)
    d2 = datetime(2024, 1, 20)
    print(f"\n☀️ Testing Sun Ingress (Makar Sankranti): {d1.date()} -> {d2.date()}")
    
    # Debug
    s1, _, _, _ = ep.get_planet_data(d1, 'Sun')
    s2, _, _, _ = ep.get_planet_data(d2, 'Sun')
    if s1: print(f"  Jan 10 Lon: {s1:.2f} ({ZodiacUtility.get_rasi(s1)[0]})") 
    # Actual check
    ingress = scanner.check_ingress('Sun', d1, d2)
    if ingress:
        print(f"  ✅ Detected: {ingress['Event']} | {ingress['From']} -> {ingress['To']}")
    else:
        print(f"  ❌ Failed. positions: {s1:.2f} -> {s2:.2f}")

if __name__ == "__main__":
    verify_medini_phase3()
