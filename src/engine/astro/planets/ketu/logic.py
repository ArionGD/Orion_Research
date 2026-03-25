from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.astro.core.zodiac import ZodiacUtility

class KetuLogic:
    def __init__(self):
        self.ep = EphemerisProvider()
        
    def get_significations(self):
        return ["Isolation", "Spirituality", "Loss", "Hidden"]
        
    def calculate_disruption(self, date):
        """
        Calculates Ketu Disruption.
        Often mirrors Rahu but can be checked independently.
        """
        # Ketu is opposite Rahu.
        # We can fetch Rahu and add 180.
        r_lon, r_speed, r_retro, _ = self.ep.get_planet_data(date, 'True_Node')
        
        if r_lon is None: return {'Ketu_Risk_Score': 0}
        
        k_lon = (r_lon + 180) % 360
        # Speed is same as Rahu usually
        
        risk_score = 0
        signals = []
        
        # 1. Stationary (Using Rahu speed as proxy since they are axis)
        if abs(r_speed) < 0.002:
            risk_score += 3
            signals.append("Ketu Stationary")
            
        # 2. Sandhi
        deg_in_sign = k_lon % 30
        if deg_in_sign < 1 or deg_in_sign > 29:
            risk_score += 2
            signals.append("Ketu Sandhi")
            
        return {
            'Ketu_Risk_Score': risk_score,
            'Ketu_Signals': signals
        }
