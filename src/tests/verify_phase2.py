from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.astro.core.zodiac import ZodiacUtility
from src.engine.medini.yogas import YogaScanner
from datetime import datetime
import pandas as pd
import swisseph as swe

def verify_medini_phase2():
    print("=== Arion.ai Phase 2 Verification: Yoga Scanner ===")
    
    # 1. Setup Provider (Sidereal)
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    scanner = YogaScanner()
    
    # 2. Test Date
    test_date = datetime.now()
    print(f"📅 Test Date: {test_date.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 3. Get Positions
    # We need a dict of {Name: Lon}
    planets = list(ep.planet_ids.keys()) + ['Ketu']
    positions = {}
    
    print("\n🌍 Planetary Positions (Sidereal):")
    for p in planets:
        lon, _, _, _ = ep.get_planet_data(test_date, p)
        if lon is not None:
            positions[p] = lon
            rasi, _, _ = ZodiacUtility.get_rasi(lon)
            print(f"  - {p:<10}: {lon:>6.2f}° ({rasi})")
            
    # 4. Scan for Yogas
    print("\n🔍 Scanning for Yogas (Combinations)...")
    yogas = scanner.scan_yogas(positions)
    
    if yogas:
        df = pd.DataFrame(yogas)
        # Reorder columns for readability
        cols = ['Name', 'Type', 'Intensity', 'Description']
        print(df[cols].to_string(index=False))
    else:
        print("✅ No major destructive Yogas detected at this moment (Orb < 5-8°).")
        
    # 5. Synthetic Test: Force a known Yoga (e.g. Shani-Mangal)
    print("\n🧪 Synthetic Test: Forcing Shani-Mangal (Saturn=300, Mars=302)...")
    synthetic_pos = {'Saturn': 300.0, 'Mars': 302.0, 'Jupiter': 10.0}
    test_yogas = scanner.scan_yogas(synthetic_pos)
    for y in test_yogas:
        print(f"  ✅ Detected: {y['Name']} (Intensity: {y['Intensity']}%)")

if __name__ == "__main__":
    verify_medini_phase2()
