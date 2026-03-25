from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.astro.core.zodiac import ZodiacUtility

class MercuryLogic:
    def __init__(self):
        self.ep = EphemerisProvider()
        
    def get_significations(self):
        return ["Trade", "Communication", "Volatility", "Currency"]
        
    def calculate_volatility(self, date):
        """
        Calculates Mercury's volatility contribution.
        1. Retrograde: High Volatility (Fake-outs).
        2. Combustion: Close to Sun (< 5 degrees) -> Erratic trading.
        3. Debilitation: Pisces (330-360) -> Confusion.
        """
        mer_lon, mer_speed, mer_retro, _ = self.ep.get_planet_data(date, 'Mercury')
        sun_lon, _, _, _ = self.ep.get_planet_data(date, 'Sun')
        
        if mer_lon is None: return {'Mercury_Volatility_Score': 0}
        
        risk_score = 0
        signals = []
        
        # 1. Retrograde
        if mer_retro:
            risk_score += 2
            signals.append("Mercury Retrograde")
            
        # 2. Debilitation (Pisces)
        # Pisces is 330 to 360. Deepest at 345.
        if 330 <= mer_lon < 360:
            risk_score += 2
            signals.append("Mercury Debilitated (Pisces)")
            
        # 3. Combustion
        if sun_lon is not None:
            angle = abs(mer_lon - sun_lon)
            if angle > 180: angle = 360 - angle
            if angle < 5.0:
                risk_score += 2
                signals.append("Mercury Combust")
            elif angle < 14.0: # Wide orb
                pass
                
        return {
            'Mercury_Volatility_Score': risk_score,
            'Mercury_Signals': signals
        }
