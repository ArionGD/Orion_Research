"""
Foundation Indices Manager
==========================
Stores and prepares Natal Charts for major global market indices.
This allows transits to be checked against the 'Birth' of the market itself.

Birth Data Source:
- NIFTY 50: November 1, 1994, 09:15 AM IST, Mumbai (NSE Launch)
- S&P 500: March 4, 1957, 10:00 AM EST, New York (Modern inception)
- SENSEX: January 2, 1986, 12:00 PM IST, Mumbai
"""

from datetime import datetime
import swisseph as swe
from src.engine.astro.core.ephemeris_provider import EphemerisProvider

class FoundationIndices:
    """
    Manages the Natal Charts of major stock indices.
    """
    
    INDEX_CHARTS = {
        'NIFTY_50': {
            'name': 'NSE Nifty 50',
            'birth_date': datetime(1994, 11, 1, 9, 15),
            'lat': 18.97, # Mumbai
            'lon': 72.82,
            'tz': 5.5,
            # Pre-calculated Sidereal (Lahiri) for speed
            'natal_moon': 171.25, # Virgo (Hasta)
            'natal_sun': 194.85, # Libra (Swati)
            'lagna': 225.40, # Scorpio (Anuradha/Jyeshtha)
            'natal_saturn': 312.45, # Aquarius (Shatabhisha)
        },
        'SP_500': {
            'name': 'S&P 500',
            'birth_date': datetime(1957, 3, 4, 10, 0),
            'lat': 40.71, # New York
            'lon': -74.00,
            'tz': -5.0,
            'natal_moon': 9.45, # Aries (Ashwini)
            'natal_sun': 319.80, # Aquarius (Shatabhisha)
            'lagna': 52.15, # Taurus (Rohini)
            'natal_saturn': 228.30, # Scorpio (Anuradha)
        }
    }

    def __init__(self):
        self.ep = EphemerisProvider()
        self.ep.set_sidereal_mode()

    def get_index_chart(self, index_name):
        """Returns chart data for a named index."""
        return self.INDEX_CHARTS.get(index_name)

    def calculate_full_natal(self, index_name):
        """
        Dynamically calculates all planetary positions for an index birth.
        """
        chart = self.INDEX_CHARTS.get(index_name)
        if not chart: return None
        
        # Adjust for UTC
        birth_utc = chart['birth_date'] - timedelta(hours=chart['tz'])
        jd = swe.julday(birth_utc.year, birth_utc.month, birth_utc.day, 
                        birth_utc.hour + birth_utc.minute/60.0)
        
        positions = {}
        for p_name, pid in self.ep.planet_ids.items():
            try:
                res, _ = swe.calc_ut(jd, pid, swe.FLG_SIDEREAL | swe.FLG_SPEED)
                positions[p_name] = res[0]
            except:
                continue
        return positions
