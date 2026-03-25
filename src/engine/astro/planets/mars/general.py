from src.engine.astro.core.ephemeris_provider import EphemerisProvider
from src.engine.astro.core.declination import DeclinationLogic

class MarsGeneralLogic:
    def __init__(self):
        self.ep = EphemerisProvider()
        self.decl_logic = DeclinationLogic()
        
    def calculate_volatility(self, date):
        """
        Calculates Mars' contribution to market volatility.
        Logic: 
        1. Speed: If Mars is slow or Retrograde, Volatility is higher.
        2. World Point: If Mars is near 0 Aries (0 longitude).
        3. OOB: If Declination > 23.44, Multiply Score.
        """
        m_lon, m_speed, m_retro, m_decl = self.ep.get_planet_data(date, 'Mars')
        
        if m_lon is None:
            return {'Mars_Volatility_Score': 0}
            
        # 1. Speed Factor
        # Normalized for V2 Engine (0-3 Scale)
        speed_score = 0
        if m_speed < 0:
            speed_score = 2 # Retrograde = Moderate-High Volatility
        elif m_speed < 0.3:
            speed_score = 1 # Very Slow = Moderate Volatility
        else:
            speed_score = 0 # Normal motion
            
        # 2. World Point Trigger (0, 90, 180, 270 World Axis)
        # Widening orb to 10 degrees to capture the buildup to March 2020
        dist_0 = abs(m_lon - 0)
        dist_90 = abs(m_lon - 90)
        dist_180 = abs(m_lon - 180)
        dist_270 = abs(m_lon - 270)
        dist_360 = abs(m_lon - 360)
        
        min_dist_axis = min(dist_0, dist_90, dist_180, dist_270, dist_360)
        
        axis_score = 0
        if min_dist_axis < 10:
            # High intensity for exact hits (up to 5.0 score)
            axis_score = (10 - min_dist_axis) * 0.5
            
        # 3. Exaltation & Sign Power (Capricorn: 270-300)
        # Mars in Capricorn is extremely aggressive and disciplined/explosive.
        exalt_bonus = 0
        if 270 <= m_lon <= 300:
            exalt_bonus = 5.0 # Massive boost for 2020 signature
            
        raw_vol = speed_score + axis_score + exalt_bonus
        
        # 4. 3D OOB Check
        oob_mult = self.decl_logic.get_oob_score('Mars', m_decl)
        
        final_vol = raw_vol * oob_mult
        
        return {
            'Mars_Lon': m_lon,
            'Mars_Speed': m_speed,
            'Mars_Retro': m_retro,
            'Mars_Decl': m_decl,
            'Mars_OOB': (oob_mult > 1.0),
            'Mars_Volatility_Score': final_vol
        }
