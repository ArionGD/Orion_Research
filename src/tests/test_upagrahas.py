from src.engine.upagrahas.calculator import UpagrahaCalculator
from datetime import datetime
import swisseph as swe

def test_upagrahas():
    uc = UpagrahaCalculator()
    uc.ep.set_sidereal_mode(swe.SIDM_LAHIRI)
    
    # Test Case: NYSE
    lat = 40.7128
    lon = -74.0060
    date = datetime(2026, 2, 2, 14, 30) # 9:30 AM EST
    
    print(f"Testing Upagrahas for {date} at NYSE...")
    
    # Debug: Check Providers
    sun_lon, _, _, _ = uc.ep.get_planet_data(date, 'Sun')
    print(f"Debug: Sun Lon: {sun_lon}")
    rise, set_t = uc.ep.get_sunrise_sunset(date, lat, lon)
    print(f"Debug: Rise: {rise}, Set: {set_t}")
    
    res = uc.calculate_upagrahas(date, lat, lon)
    
    print("-" * 40)
    for k, v in res.items():
        print(f"{k:<15}: {v:.2f}")
    print("-" * 40)
    
if __name__ == "__main__":
    test_upagrahas()
