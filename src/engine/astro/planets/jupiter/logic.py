from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.astro.core.zodiac import ZodiacUtility

class JupiterLogic:
    def __init__(self):
        self.ep = EphemerisProvider()
        
    def get_significations(self):
        return ["Expansion", "Banking", "Optimism", "Law"]
        
    def calculate_optimism(self, date):
        """
        Calculates Jupiter's optimism/stress.
        1. Debilitation: Capricorn (270-300).
        2. Retrograde: Re-thinking growth.
        """
        j_lon, j_speed, j_retro, _ = self.ep.get_planet_data(date, 'Jupiter')
        
        if j_lon is None: return {'Jupiter_Stress_Score': 0}
        
        risk_score = 0
        signals = []
        
        # 1. Debilitation (Capricorn)
        # Capricorn is 270 to 300. Deepest at 275.
        if 270 <= j_lon < 300:
            risk_score += 2
            signals.append("Jupiter Debilitated (Capricorn)")
            
        # 2. Retrograde
        if j_retro:
            risk_score += 1 # Mild negative
            signals.append("Jupiter Retrograde")
            
        return {
            'Jupiter_Stress_Score': risk_score,
            'Jupiter_Signals': signals
        }
