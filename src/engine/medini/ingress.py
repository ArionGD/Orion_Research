"""
Medini Ingress (Sankranti) Analyzer
===================================
Calculates the 'Lord of the Year' based on the Sun's entry into 0° Aries.
This is the single most important annual cycle in Vedic Mundane Astrology.

Logic:
1. Calculate the exact UTC moment Sun reaches 0.0 longitude (Sidereal Lahiri).
2. Determine the Day (Vara) of that moment.
3. The Vara Lord becomes the 'Raja' (King) of the Year.
   - Sun: Government strife, high gold prices
   - Moon: Public prosperity, rainfall, food
   - Mars: War, fires, military escalation
   - Mercury: Digital/IT boom, trade expansion
   - Jupiter: Economic growth, wealth creation
   - Venus: Luxury/Vehicle boom, arts, peace
   - Saturn: Hardship, famine, restructuring
"""

import swisseph as swe
from datetime import datetime, timedelta

class IngressAnalyzer:
    """
    Analyzes the annual Aries Ingress (Mesh Sankranti).
    """
    
    VARA_LORDS = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']

    def __init__(self):
        # Using tropical search then converting or direct sidereal search
        pass

    def get_aries_ingress_utc(self, year):
        """
        Calculates the exact UTC time when Sun enters 0 Sidereal Aries (Lahiri).
        ~Mid-April each year.
        """
        # Approx start search: April 10
        start_jd = swe.julday(year, 4, 10, 0.0)
        
        # We need to find when sun_long = 0 in sidereal mode
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        
        # Simple iterative search for 0.0
        jd = start_jd
        step = 0.5 # 12 hours
        for _ in range(20):
            res, _ = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL)
            lon = res[0]
            
            # If cross 360/0
            if lon > 300: lon -= 360 
            
            if abs(lon) < 0.0001:
                break
                
            # Newton-like step (Sun moves ~0.041 deg/hr or ~1 deg/day)
            # Diff / 1 deg/day
            jd -= (lon / 1.0)
            
        return jd

    def analyze_year(self, year):
        """
        Returns the King (Raja) and Minister (Mantri) of the year.
        Minister is the Vara Lord of Sun entering Gemini (Mithuna Sankranti).
        """
        ingress_jd = self.get_aries_ingress_utc(year)
        
        # Vara Lord: Julian day modulo 7
        # 0 = Monday, 1 = Tuesday... but Vedic starts from Sun.
        # swe.day_of_week(jd) returns 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday, 5=Saturday, 6=Sunday
        dow = swe.day_of_week(ingress_jd)
        
        # Convert to Vedic Order (0=Sun, 1=Moon...)
        mapping = {6:0, 0:1, 1:2, 2:3, 3:4, 4:5, 5:6}
        vedic_dow = mapping[dow]
        
        king = self.VARA_LORDS[vedic_dow]
        
        # Simple Logic for Big Event Bias
        bias = 0
        desc = ""
        if king in ['Sun', 'Mars', 'Saturn']:
            bias = -3 # Malefic Kings = more risk/stability issues
            desc = f"{king} is King: A year of tension, structural pressure, and governance/border issues."
        elif king in ['Jupiter', 'Venus', 'Mercury']:
            bias = +3 # Benefic Kings = expansion/trade/peace
            desc = f"{king} is King: A year of economic growth, trade expansion, and prosperity."
        else:
            bias = 0
            desc = f"{king} is King: A balanced year focusing on public sentiment and internal stability."

        return {
            'Year': year,
            'King': king,
            'Medini_Bias': bias,
            'Description': desc,
            'Ingress_JD': ingress_jd
        }
