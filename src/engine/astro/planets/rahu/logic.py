from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.astro.core.zodiac import ZodiacUtility

class RahuLogic:
    def __init__(self):
        self.ep = EphemerisProvider()
        
    def get_significations(self):
        return ["Innovation", "Disruption", "Foreign", "Tech"]
        
    def calculate_disruption(self, date):
        """
        Calculates Rahu's disruption.
        1. Stationary/Direct: Karmic heavy.
        2. Sandhi: Edge of sign (0-1 deg or 29-30 deg).
        """
        r_lon, r_speed, r_retro, _ = self.ep.get_planet_data(date, 'True_Node') # Rahu
        
        if r_lon is None: return {'Rahu_Risk_Score': 0}
        
        risk_score = 0
        signals = []
        
        # 1. Stationary / Direct
        # Rahu is usually Retro (Negative speed).
        # If Speed is Positive -> Direct (Rare).
        # If Speed is near 0 -> Stationary.
        if r_speed > 0:
            risk_score += 3
            signals.append("Rahu Direct (Rare Karma)")
        elif abs(r_speed) < 0.002: # Extremely slow
            risk_score += 3
            signals.append("Rahu Stationary")
            
        # 2. Sandhi (Edge of Sign)
        deg_in_sign = r_lon % 30
        if deg_in_sign < 1 or deg_in_sign > 29:
            risk_score += 2
            signals.append("Rahu Sandhi (Edge)")
            
        return {
            'Rahu_Risk_Score': risk_score,
            'Rahu_Signals': signals
        }
