from src.engine.lagna.calculator import LagnaCalculator
from datetime import datetime
import swisseph as swe

def test_lagnas():
    lc = LagnaCalculator()
    lc.ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    
    # Test Case: NYSE (New York)
    # Lat: 40.7128 N, Lon: -74.0060 W
    lat = 40.7128
    lon = -74.0060
    
    # Date: Market Open approx
    date = datetime(2026, 2, 2, 9, 30) # 9:30 AM EST
    # Need to convert local to UTC for accurate SwissEph? 
    # SwissEph takes UTC usually? My EphemerisProvider expects datetime object.
    # If I pass 9:30, it treats as 9:30.
    # Let's assume input matches the ephemeris expectation (UTC usually best practice).
    # NY is UTC-5. So 9:30 AM = 14:30 UTC.
    date_utc = datetime(2026, 2, 2, 14, 30)
    
    print(f"Testing Lagnas for {date_utc} UTC at NYSE coordinates...")
    
    res = lc.calculate_special_lagnas(date_utc, lat, lon)
    
    print("-" * 40)
    print(f"Ascendant (Lagna): {res['Ascendant']:.2f}")
    print(f"MC (10th Cusp):    {res['MC']:.2f}")
    print(f"Hora Lagna (HL):   {res['Hora_Lagna']:.2f}")
    print(f"Ghatika Lagna (GL):{res['Ghatika_Lagna']:.2f}")
    print(f"Arudha Lagna (AL): Sign {res['Arudha_Lagna_Sign']} (~{res['Arudha_Lagna_Deg']} deg)")
    print(f"Lagna Lord:        {res['Lagna_Lord']}")
    print("-" * 40)
    
if __name__ == "__main__":
    test_lagnas()
