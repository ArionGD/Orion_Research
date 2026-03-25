from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.astro.core.zodiac import ZodiacUtility

class SunLogic:
    def __init__(self):
        self.ep = EphemerisProvider()
        
    def get_significations(self):
        return ["Government", "Authority", "Vitality", "Gold", "Wheat"]

    def calculate_risk(self, date):
        """
        Calculates Sun's risk contribution.
        1. Debilitation: Libra (180-210 deg). Peak debilitation at 190.
        2. Sun-Saturn Conflict: Opposition (180) or Conjunction (0).
        """
        s_lon, _, _, _ = self.ep.get_planet_data(date, 'Sun')
        sat_lon, _, _, _ = self.ep.get_planet_data(date, 'Saturn')
        
        if s_lon is None: return {'Sun_Risk_Score': 0}
        
        risk_score = 0
        signals = []
        
        # 1. Debilitation (Libra)
        # Libra is 180 to 210.
        if 180 <= s_lon < 210:
            risk_score += 2
            signals.append("Sun in Libra (Debilitated)")
            
        # 2. Sun-Saturn Conflict
        if sat_lon is not None:
            angle = abs(s_lon - sat_lon)
            if angle > 180: angle = 360 - angle
            
            # Conjunction or Opposition
            orb = 6.0
            if angle < orb:
                risk_score += 3
                signals.append("Sun-Saturn Conjunction")
            elif abs(angle - 180) < orb:
                risk_score += 3
                signals.append("Sun-Saturn Opposition")
                
        return {
            'Sun_Risk_Score': risk_score,
            'Sun_Signals': signals
        }
