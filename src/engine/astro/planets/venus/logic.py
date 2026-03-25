from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.astro.core.zodiac import ZodiacUtility

class VenusLogic:
    def __init__(self):
        self.ep = EphemerisProvider()
        
    def get_significations(self):
        return ["Luxury", "Automobiles", "Currency", "Sugar"]
        
    def calculate_value_risk(self, date):
        """
        Calculates Venus risk (Currency/Value).
        1. Retrograde: Pricing Anomalies / Re-valuation.
        2. Debilitation: Virgo (150-180).
        """
        v_lon, v_speed, v_retro, _ = self.ep.get_planet_data(date, 'Venus')
        
        if v_lon is None: return {'Venus_Risk_Score': 0}
        
        risk_score = 0
        signals = []
        
        # 1. Retrograde
        if v_retro:
            risk_score += 2
            signals.append("Venus Retrograde")
            
        # 2. Debilitation (Virgo)
        # Virgo is 150 to 180. Deepest at 177.
        if 150 <= v_lon < 180:
            risk_score += 2
            signals.append("Venus Debilitated (Virgo)")
            
        return {
            'Venus_Risk_Score': risk_score,
            'Venus_Signals': signals
        }
