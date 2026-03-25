from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.astro.core.zodiac import ZodiacUtility

class MoonLogic:
    def __init__(self):
        self.ep = EphemerisProvider()
        
    def get_significations(self):
        return ["Sentiment", "Liquids", "Silver", "Public Mood"]
        
    def calculate_mood(self, date):
        """
        Calculates Moon's sentiment/risk contribution.
        1. Gandanta: Edge of Water/Fire signs (Pisces-Aries, Cancer-Leo, Scorpio-Sag).
        2. Kemadruma Yoga: (Simplified) Moon isolated.
        """
        m_lon, _, _, _ = self.ep.get_planet_data(date, 'Moon')
        
        if m_lon is None: return {'Moon_Risk_Score': 0}
        
        risk_score = 0
        signals = []
        
        # 1. Gandanta (Transition Points)
        # Cancer-Leo (approx 120), Scorpio-Sag (approx 240), Pisces-Aries (0/360)
        # Danger zone is +/- 1 degree from these points
        gandanta_points = [0, 120, 240]
        is_gandanta = False
        for p in gandanta_points:
            dist = abs(m_lon - p)
            if dist > 350: dist = 360 - dist # Wrap for 0/360
            if dist < 2.0: # 2 degrees orb
                is_gandanta = True
                break
                
        if is_gandanta:
            risk_score += 2
            signals.append("Moon in Gandanta (Drowning/Volatility)")
            
        return {
            'Moon_Risk_Score': risk_score,
            'Moon_Signals': signals
        }
