import swisseph as swe
class AlgolLogic:
    """
    Algol (The Demon Star). 
    Sidereal Longitude: Approx 2 deg Taurus (check exact).
    Tropical: ~26 Taurus.
    """
    def check_conjunction(self, planet_lon, planet_name, algol_lon):
        """
        Checks if a planet is conjunct Algol within 1 degree.
        """
        if algol_lon is None or planet_lon is None: return 0, []
        
        diff = abs(planet_lon - algol_lon)
        if diff > 180: diff = 360 - diff
        
        if diff < 1.0:
            return 25, [f"{planet_name} conjunct Algol (CRITICAL)"] # High risk
            
        return 0, []
