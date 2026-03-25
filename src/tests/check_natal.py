import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.engine.countries.india.profile import IndiaCountryProfile
from src.engine.countries.usa.profile import USACountryProfile

def print_natal_positions():
    india = IndiaCountryProfile()
    usa = USACountryProfile()
    
    print("NATAL POSITIONS (Sidereal Lahiri)")
    print("="*40)
    print("\nINDIA:")
    for k, v in india.get_natal_positions().items():
        if v is not None:
            print(f"{k}: {v:.2f}")
            
    print("\nUSA:")
    for k, v in usa.get_natal_positions().items():
        if v is not None:
            print(f"{k}: {v:.2f}")

if __name__ == "__main__":
    print_natal_positions()
