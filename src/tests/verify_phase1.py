from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.astro.core.zodiac import ZodiacUtility
from datetime import datetime
import pandas as pd
import swisseph as swe

def verify_medini_foundation():
    print("=== Arion.ai Phase 1 Verification: Medini Foundation ===")
    
    # 1. Initialize Provider & Set Sidereal
    ep = EphemerisProvider()
    ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    print("✅ Ephemeris Mode set to Sidereal (Lahiri)")
    
    # 2. Test Date: Current
    test_date = datetime.now()
    print(f"📅 Test Date: {test_date.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 3. Fetch All Planets (inc. Ketu)
    planets = list(ep.planet_ids.keys()) + ['Ketu']
    
    data = []
    
    for p in planets:
        lon, speed, _, _ = ep.get_planet_data(test_date, p)
        
        if lon is not None:
            # Rasi
            rasi, _, deg_in_rasi = ZodiacUtility.get_rasi(lon)
            
            # Nakshatra
            nak, _, pada = ZodiacUtility.get_nakshatra(lon)
            
            data.append({
                'Planet': p,
                'Longitude': f"{lon:.2f}",
                'Rasi (Sign)': f"{rasi} ({deg_in_rasi:.2f}°)",
                'Nakshatra': f"{nak} (Pada {pada})",
                'Speed': f"{speed:.4f}" if speed else "-"
            })
            
    # 4. Display
    df = pd.DataFrame(data)
    print("\n🌌 MEDINI SKY MAP (Sidereal):")
    print(df.to_string(index=False))
    
    # Verify Ketu-Rahu Axis (180 deg)
    rahu = df[df['Planet'] == 'True_Node']['Longitude'].values[0]
    ketu = df[df['Planet'] == 'Ketu']['Longitude'].values[0]
    print(f"\n✅ Axis Check: Rahu ({rahu}) vs Ketu ({ketu}) | Diff ~180°")

if __name__ == "__main__":
    verify_medini_foundation()
