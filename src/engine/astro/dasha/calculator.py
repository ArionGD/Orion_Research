class DashaCalculator:
    """
    Calculates Vimshottari Dasha periods based on Moon's longitude.
    Cycle: 120 Years.
    Sequence: Ketu(7), Venus(20), Sun(6), Moon(10), Mars(7), Rahu(18), Jupiter(16), Saturn(19), Mercury(17).
    """
    def __init__(self):
        self.lords = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
        self.years = [7, 20, 6, 10, 7, 18, 16, 19, 17]
        self.total_cycle = 120
        # Nakshatra Ruler Mapping (0=Ashwini->Ketu)
        # Sequence repeats 3 times (1-9, 10-18, 19-27)
        
    def get_current_mahadasha(self, moon_lon, birth_moon_lon=None, current_date=None, birth_date=None):
        """
        If we are doing Mundane Astrology (Country), we need the Country's Birth Moon (Independence Chart).
        For now, this calculator just returns the Ruler for a given Moon position (Transcript Dasha? No, Dasha is from Birth).
        
        If 'moon_lon' is passed as the CURRENT transit moon, that's just Nakshatra Lord.
        
        To calculate Dasha properly, we need:
        1. Birth Moon Longitude (e.g., India's Independence Moon).
        2. Birth Date.
        3. Current Date.
        """
        if birth_moon_lon is None:
             # Just return the ruler of the longitude passed
             return self.get_nakshatra_lord(moon_lon)
             
        # Full Dasha Calculation Logic (Todo)
        return "Unknown"

    def get_nakshatra_lord(self, lon):
        nak_len = 13.3333333333
        nak_idx = int(lon / nak_len)
        cycle_idx = nak_idx % 9
        return self.lords[cycle_idx]
