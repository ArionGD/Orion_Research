"""
Corporate Astrology Module
Analyzes risk/opportunity for companies based on Incorporation Date.
"""
import swisseph as swe
from src.engine.astro.core.ephemeris_provider import EphemerisProvider

class CorporateRiskEngine:
    def __init__(self):
        self.ep = EphemerisProvider()
        self.ep.set_sidereal_mode()
        
    def get_natal_positions(self, incorporation_date):
        """
        Calculates natal positions for a company.
        Assumes 09:00 AM local time (approx stock market open/registration time)
        """
        # Convert to Julian Day (using 09:00 AM approx)
        jd = swe.julday(incorporation_date.year, incorporation_date.month, incorporation_date.day, 3.5) # 09:00 IST - 5:30 = 03:30 UTC
        
        positions = {}
        for p_name, pid in self.ep.planet_ids.items():
            if p_name == 'Chiron': continue
            try:
                res, _ = swe.calc_ut(jd, pid, swe.FLG_SIDEREAL | swe.FLG_SPEED)
                positions[p_name] = res[0]
            except:
                positions[p_name] = None
        return positions

    def check_company_risk(self, company_name, incorporation_date, transit_positions):
        """
        Analyzes specific company risks for Q1 2026.
        Returns: (score, signals)
        """
        score = 0
        signals = []
        
        natal = self.get_natal_positions(incorporation_date)
        
        t_saturn = transit_positions.get('Saturn', 0)
        t_jupiter = transit_positions.get('Jupiter', 0)
        t_rahu = transit_positions.get('True_Node', 0)
        t_ketu = (t_rahu + 180) % 360
        
        n_sun = natal.get('Sun')
        n_moon = natal.get('Moon')
        n_saturn = natal.get('Saturn')
        n_jupiter = natal.get('Jupiter')
        n_mercury = natal.get('Mercury')
        
        # --- LEGACY STRUGGLES (Saturn/Ketu Impact) ---
        
        # 1. Saturn Sade Sati / Kantaka Shani (Saturn on Moon)
        # Old companies with Moon in Pisces/Aquarius are suffering
        if n_moon:
            diff = abs(t_saturn - n_moon)
            if diff > 180: diff = 360 - diff
            if diff < 10:
                score -= 10
                signals.append(f"{company_name}: Saturn Crushing Natal Moon (Sade Sati Peak - Organizational Stress)")

        # 2. Ketu on Natal Sun/Mercury (Identity Crisis / Obsolescence)
        # Ketu in Virgo dissolved old code. If company has planets in Virgo, they struggle.
        # Virgo is 150-180.
        if n_sun and (150 < n_sun < 180): # Sun in Virgo
             if 150 < t_ketu < 180:
                score -= 15
                signals.append(f"{company_name}: Ketu Eclipsing Natal Sun (Identity/Leadership Crisis)")
                
        if n_mercury and (150 < n_mercury < 180): # Mercury in Virgo (Exalted but hit by Ketu)
             if 150 < t_ketu < 180:
                score -= 12
                signals.append(f"{company_name}: Ketu Scrambling Natal Mercury (Legacy Code/Service Issues)")

        # --- NEW AGE GROWTH (Jupiter/Rahu Impact) ---
        
        # 3. Jupiter Return / Aspecting Sun (Expansion)
        if n_jupiter:
            diff = abs(t_jupiter - n_jupiter)
            if diff > 180: diff = 360 - diff
            if diff < 10:
                score += 10
                signals.append(f"{company_name}: Jupiter Return (New Growth Cycle)")
        
        # 4. Rahu Trine Mercury (AI/Innovation Surge)
        # Rahu in Aquarius (300-330). Trine is Libra(180-210) or Gemini(60-90).
        if n_mercury:
            diff = abs(t_rahu - n_mercury)
            if diff > 180: diff = 360 - diff
            if abs(diff - 120) < 10:
                score += 15
                signals.append(f"{company_name}: Rahu Trine Mercury (Massive AI Adoption)")

        return score, signals
